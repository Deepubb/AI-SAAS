"""Database connection and operations for SG Money Buddy"""

import logging
import asyncio
import aiosqlite
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from src.utils.config import Config

logger = logging.getLogger(__name__)

# Global variables
db_path = None
config = Config()


async def init_database():
    """Initialize SQLite database and create tables"""
    global db_path
    
    try:
        # Use simple SQLite path
        db_path = "sg_finance_bot.db"
        
        # Create tables
        async with aiosqlite.connect(db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT,
                    language_code TEXT DEFAULT 'en',
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    currency TEXT DEFAULT 'SGD',
                    location TEXT,
                    validation_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    period TEXT DEFAULT 'monthly',
                    currency TEXT DEFAULT 'SGD',
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    currency TEXT DEFAULT 'SGD',
                    timezone TEXT DEFAULT 'Asia/Singapore',
                    language TEXT DEFAULT 'singlish',
                    notification_enabled BOOLEAN DEFAULT 1,
                    budget_alerts BOOLEAN DEFAULT 1,
                    deal_notifications BOOLEAN DEFAULT 1,
                    weekly_summary BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            await db.commit()
        
        # Initialize default data
        await _initialize_default_data()
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def _initialize_default_data():
    """Initialize default expense categories and other reference data"""
    try:
        async with aiosqlite.connect(db_path) as db:
            # Check if we need to initialize data
            cursor = await db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='expense_categories'")
            table_exists = await cursor.fetchone()
            
            if not table_exists[0]:
                # Create expense categories table
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS expense_categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        display_name TEXT NOT NULL,
                        emoji TEXT,
                        description TEXT,
                        keywords TEXT,
                        average_price_sg REAL,
                        min_price_sg REAL,
                        max_price_sg REAL,
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Insert default Singapore expense categories
                categories = [
                    ("food", "Food & Drinks", "🍜", "Meals, snacks, beverages, hawker food, restaurants", 
                     '["makan", "food", "eat", "lunch", "dinner", "breakfast", "coffee", "tea", "hawker", "restaurant"]', 8.0, 2.0, 50.0),
                    ("transport", "Transport", "🚌", "MRT, bus, taxi, grab, petrol, car park",
                     '["transport", "bus", "mrt", "grab", "taxi", "petrol", "car park", "ezlink"]', 15.0, 1.0, 100.0),
                    ("housing", "Housing & Utilities", "🏠", "Rent, utilities, internet, phone bills",
                     '["rent", "utilities", "water", "electricity", "internet", "phone", "wifi"]', 800.0, 50.0, 5000.0),
                    ("entertainment", "Entertainment", "🎬", "Movies, games, outings, subscriptions",
                     '["movie", "cinema", "game", "netflix", "spotify", "entertainment", "fun"]', 40.0, 10.0, 200.0),
                    ("shopping", "Shopping", "🛍️", "Clothes, electronics, personal items",
                     '["shopping", "clothes", "shoes", "electronics", "gadget", "lazada", "shopee"]', 100.0, 10.0, 1000.0),
                    ("healthcare", "Healthcare", "🏥", "Doctor, medicine, supplements, insurance",
                     '["doctor", "clinic", "medicine", "pharmacy", "hospital", "dental"]', 80.0, 20.0, 500.0),
                    ("education", "Education", "📚", "Courses, books, tuition, training",
                     '["course", "book", "tuition", "school", "education", "training"]', 150.0, 20.0, 1000.0),
                    ("others", "Others", "💼", "Miscellaneous expenses",
                     '["others", "misc", "miscellaneous"]', 50.0, 1.0, 500.0)
                ]
                
                await db.executemany('''
                    INSERT INTO expense_categories 
                    (name, display_name, emoji, description, keywords, average_price_sg, min_price_sg, max_price_sg)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', categories)
                
                await db.commit()
                logger.info("Default expense categories created")
        
    except Exception as e:
        logger.error(f"Error initializing default data: {e}")


async def get_or_create_user(telegram_id: int, user_data: Dict) -> Dict:
    """Get existing user or create new one"""
    try:
        async with aiosqlite.connect(db_path) as db:
            # Try to get existing user
            cursor = await db.execute(
                "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
            )
            user_row = await cursor.fetchone()
            
            if user_row:
                # Update user info if needed
                await db.execute('''
                    UPDATE users 
                    SET first_name = ?, last_name = ?, username = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE telegram_id = ?
                ''', (
                    user_data.get("first_name", user_row[2]),
                    user_data.get("last_name", user_row[3]), 
                    user_data.get("username", user_row[4]),
                    telegram_id
                ))
                user_id = user_row[0]
            else:
                # Create new user
                cursor = await db.execute('''
                    INSERT INTO users (telegram_id, first_name, last_name, username, language_code)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    telegram_id,
                    user_data.get("first_name"),
                    user_data.get("last_name"),
                    user_data.get("username"),
                    user_data.get("language_code", "en")
                ))
                user_id = cursor.lastrowid
                
                # Create default preferences
                await db.execute('''
                    INSERT INTO user_preferences (user_id)
                    VALUES (?)
                ''', (user_id,))
            
            await db.commit()
            
            # Return user data
            cursor = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_row = await cursor.fetchone()
            
            return {
                "id": user_row[0],
                "telegram_id": user_row[1],
                "first_name": user_row[2],
                "last_name": user_row[3],
                "username": user_row[4]
            }
            
    except Exception as e:
        logger.error(f"Error getting/creating user: {e}")
        raise


async def save_expense(telegram_user_id: int, expense_data: Dict) -> bool:
    """Save expense to database"""
    try:
        async with aiosqlite.connect(db_path) as db:
            # Get user
            cursor = await db.execute(
                "SELECT id FROM users WHERE telegram_id = ?", (telegram_user_id,)
            )
            user_row = await cursor.fetchone()
            
            if not user_row:
                logger.error(f"User not found: {telegram_user_id}")
                return False
            
            user_id = user_row[0]
            
            # Save expense
            await db.execute('''
                INSERT INTO expenses (user_id, amount, category, description, currency, location, validation_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                expense_data["amount"],
                expense_data["category"],
                expense_data["description"],
                expense_data.get("currency", "SGD"),
                expense_data.get("location"),
                json.dumps(expense_data.get("validation", {}))
            ))
            
            await db.commit()
            logger.info(f"Expense saved: {expense_data}")
            return True
            
    except Exception as e:
        logger.error(f"Error saving expense: {e}")
        return False


async def get_user_expenses(telegram_user_id: int, days: int = 30) -> List[Dict]:
    """Get user expenses for the last N days"""
    try:
        async with aiosqlite.connect(db_path) as db:
            # Get user
            cursor = await db.execute(
                "SELECT id FROM users WHERE telegram_id = ?", (telegram_user_id,)
            )
            user_row = await cursor.fetchone()
            
            if not user_row:
                return []
            
            user_id = user_row[0]
            
            # Get expenses
            cursor = await db.execute('''
                SELECT id, amount, category, description, currency, location, created_at
                FROM expenses 
                WHERE user_id = ? AND created_at >= datetime('now', '-{} days')
                ORDER BY created_at DESC
            '''.format(days), (user_id,))
            
            expenses = await cursor.fetchall()
            
            return [
                {
                    "id": exp[0],
                    "amount": exp[1],
                    "category": exp[2],
                    "description": exp[3],
                    "currency": exp[4],
                    "location": exp[5],
                    "created_at": exp[6]
                }
                for exp in expenses
            ]
            
    except Exception as e:
        logger.error(f"Error getting user expenses: {e}")
        return []


async def get_expense_categories() -> List[Dict]:
    """Get all active expense categories"""
    try:
        async with aiosqlite.connect(db_path) as db:
            cursor = await db.execute('''
                SELECT name, display_name, emoji, description, average_price_sg
                FROM expense_categories
                WHERE is_active = 1
            ''')
            categories = await cursor.fetchall()
            
            return [
                {
                    "name": cat[0],
                    "display_name": cat[1],
                    "emoji": cat[2],
                    "description": cat[3],
                    "average_price": cat[4]
                }
                for cat in categories
            ]
            
    except Exception as e:
        logger.error(f"Error getting expense categories: {e}")
        return []


async def save_budget(telegram_user_id: int, category: str, amount: float, period: str = "monthly") -> bool:
    """Save user budget"""
    try:
        async with aiosqlite.connect(db_path) as db:
            # Get user
            cursor = await db.execute(
                "SELECT id FROM users WHERE telegram_id = ?", (telegram_user_id,)
            )
            user_row = await cursor.fetchone()
            
            if not user_row:
                return False
            
            user_id = user_row[0]
            
            # Check if budget exists
            cursor = await db.execute('''
                SELECT id FROM budgets WHERE user_id = ? AND category = ? AND is_active = 1
            ''', (user_id, category))
            existing_budget = await cursor.fetchone()
            
            if existing_budget:
                # Update existing budget
                await db.execute('''
                    UPDATE budgets 
                    SET amount = ?, period = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (amount, period, existing_budget[0]))
            else:
                # Create new budget
                await db.execute('''
                    INSERT INTO budgets (user_id, category, amount, period)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, category, amount, period))
            
            await db.commit()
            logger.info(f"Budget saved: {category} ${amount} {period}")
            return True
            
    except Exception as e:
        logger.error(f"Error saving budget: {e}")
        return False


async def get_user_budgets(telegram_user_id: int) -> List[Dict]:
    """Get user budgets"""
    try:
        async with aiosqlite.connect(db_path) as db:
            # Get user
            cursor = await db.execute(
                "SELECT id FROM users WHERE telegram_id = ?", (telegram_user_id,)
            )
            user_row = await cursor.fetchone()
            
            if not user_row:
                return []
            
            user_id = user_row[0]
            
            # Get budgets
            cursor = await db.execute('''
                SELECT category, amount, period, created_at
                FROM budgets
                WHERE user_id = ? AND is_active = 1
                ORDER BY created_at DESC
            ''', (user_id,))
            
            budgets = await cursor.fetchall()
            
            return [
                {
                    "category": budget[0],
                    "amount": budget[1],
                    "period": budget[2],
                    "created_at": budget[3]
                }
                for budget in budgets
            ]
            
    except Exception as e:
        logger.error(f"Error getting user budgets: {e}")
        return []


async def close_database():
    """Close database connections"""
    # No persistent connections to close with aiosqlite
    logger.info("Database connections closed")
