"""Expense tracking service for SG Money Buddy"""

import re
import logging
from typing import Dict, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ExpenseTracker:
    """Handle expense parsing and tracking"""
    
    # Singapore-specific category keywords
    CATEGORY_KEYWORDS = {
        "food": [
            "makan", "food", "eat", "lunch", "dinner", "breakfast", "dabao",
            "hawker", "coffee", "tea", "drink", "restaurant", "cafe", "zi char",
            "cai png", "chicken rice", "laksa", "roti", "nasi", "mee"
        ],
        "transport": [
            "transport", "bus", "mrt", "grab", "taxi", "car park", "petrol",
            "gojek", "comfort", "citycab", "ezlink", "fare", "top up"
        ],
        "housing": [
            "rent", "utilities", "water", "electricity", "internet", "phone",
            "hdb", "condo", "maintenance", "conservancy", "wifi"
        ],
        "entertainment": [
            "movie", "cinema", "ktv", "club", "game", "staycation", "netflix",
            "spotify", "shopping", "mall", "orchard", "vivo", "marina"
        ],
        "healthcare": [
            "doctor", "clinic", "medicine", "pharmacy", "hospital", "dental",
            "checkup", "insurance", "supplement"
        ],
        "education": [
            "course", "book", "tuition", "school", "university", "exam",
            "certification", "training"
        ],
        "shopping": [
            "clothes", "shoes", "bag", "accessory", "electronics", "gadget",
            "gift", "online", "lazada", "shopee", "qoo10"
        ]
    }
    
    def __init__(self):
        self.singapore_prices = {
            "food": {"min": 2.0, "max": 50.0, "avg": 8.0},
            "transport": {"min": 1.0, "max": 100.0, "avg": 15.0},
            "housing": {"min": 50.0, "max": 5000.0, "avg": 800.0},
            "entertainment": {"min": 10.0, "max": 200.0, "avg": 40.0},
            "healthcare": {"min": 20.0, "max": 500.0, "avg": 80.0},
            "education": {"min": 20.0, "max": 1000.0, "avg": 150.0},
            "shopping": {"min": 10.0, "max": 1000.0, "avg": 100.0}
        }
    
    def parse_expense_message(self, text: str) -> Optional[Dict]:
        """Parse natural language expense input"""
        try:
            # Clean the text
            text = text.lower().strip()
            
            # Pattern to match: [description] [amount]
            # Examples: "lunch $5", "transport 2.50", "coffee $3 at starbucks"
            patterns = [
                r'(.+?)\s*\$(\d+\.?\d*)',  # "lunch $5"
                r'(.+?)\s*(\d+\.?\d*)\s*dollars?',  # "lunch 5 dollars"
                r'(.+?)\s*(\d+\.?\d*)',  # "lunch 5"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    description = match.group(1).strip()
                    amount = float(match.group(2))
                    
                    # Categorize the expense
                    category = self._categorize_expense(description)
                    
                    # Validate Singapore pricing
                    validation = self._validate_singapore_pricing(amount, category)
                    
                    return {
                        'description': description,
                        'amount': amount,
                        'category': category,
                        'currency': 'SGD',
                        'timestamp': datetime.now(),
                        'validation': validation
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing expense message: {e}")
            return None
    
    def _categorize_expense(self, description: str) -> str:
        """Categorize expense based on description keywords"""
        description_lower = description.lower()
        
        # Check each category for matching keywords
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category
        
        # Default category
        return "others"
    
    def _validate_singapore_pricing(self, amount: float, category: str) -> Dict:
        """Validate if expense amount is reasonable for Singapore context"""
        price_data = self.singapore_prices.get(category, {"min": 0, "max": float('inf'), "avg": 0})
        
        result = {
            "is_valid": True,
            "warning": None,
            "suggestion": None
        }
        
        if amount < price_data["min"]:
            result["warning"] = f"Wah so cheap! Only ${amount}? Sure or not? 😄"
        elif amount > price_data["max"]:
            result["warning"] = f"Alamak! ${amount} quite expensive for {category} leh!"
            result["suggestion"] = f"Maybe can find cheaper option? Average is ${price_data['avg']:.2f}."
        elif amount > (price_data["avg"] * 3):
            result["warning"] = f"Eh quite pricey! ${amount} for {category} above usual lah."
        
        return result
    
    async def log_expense(self, user_id: int, expense_data: Dict) -> bool:
        """Save expense to database"""
        try:
            # Import here to avoid circular imports
            from src.data.database import save_expense
            
            return await save_expense(user_id, expense_data)
            
        except Exception as e:
            logger.error(f"Error logging expense: {e}")
            return False
    
    async def get_user_expenses(self, user_id: int, days: int = 30) -> List[Dict]:
        """Get user expenses for the last N days"""
        try:
            from src.data.database import get_user_expenses
            
            return await get_user_expenses(user_id, days)
            
        except Exception as e:
            logger.error(f"Error getting user expenses: {e}")
            return []
