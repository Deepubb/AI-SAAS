#!/usr/bin/env python3
"""
BaoJiak - Ultra Simple Singapore Companion Bot
For uncles, aunties, and anyone who finds tech confusing!
"""

import os
import logging
import random
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

# Load environment
load_dotenv()

# Simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our database functions
import asyncio
from src.data.database import init_database, get_or_create_user, save_expense, get_user_expenses

# =============================================================================
# COMPANION PERSONALITY - Like talking to your best friend!
# =============================================================================

class BaoJiakCompanion:
    """BaoJiak's personality - your friendly neighborhood kakis"""
    
    # Different personalities based on time/mood
    GREETINGS = {
        "morning": [
            "Eh good morning! Had breakfast already? 🌅",
            "Morning lah! Ready to jiak and track spending today? ☕",
            "Wah early bird! What you eating for breakfast? 🥐"
        ],
        "afternoon": [
            "Afternoon! Lunch time already? What you having? 🍜",
            "Eh bro/sis! How's your day going? Spent a lot today? 😄",
            "Yo! Feeling hungry? Tell me what you eating! 🍛"
        ],
        "evening": [
            "Evening! Dinner plans? Don't forget to tell me! 🌆",
            "Eh good evening! How much you spent today ah? 🌙",
            "Night time liao! What you having for dinner? 🍲"
        ]
    }
    
    ENCOURAGEMENT = [
        "Wah you very good at tracking! Keep it up! 💪",
        "Steady lah! You're becoming money-smart! 🧠💰",
        "I'm proud of you for tracking expenses! 👏",
        "You're my best student! So disciplined! 📚",
        "Eh you're doing great! Your wallet will thank you! 👛"
    ]
    
    CONCERN = [
        "Eh... spending quite a lot today leh. You okay? 😟",
        "Bro/sis, maybe slow down a bit? Your money running away! 💸",
        "Alamak! Your wallet crying already! Take care ah! 😅",
        "Eh careful lah! Money not easy to earn nowadays! 💔"
    ]
    
    CELEBRATION = [
        "Wah! You saved money today! So proud! 🎉",
        "Good job! Your piggy bank getting fatter! 🐷💰",
        "Shiok! You're becoming a savings expert! 🏆",
        "Steady! Your future self will thank you! 🙏"
    ]

companion = BaoJiakCompanion()

# =============================================================================
# ULTRA SIMPLE KEYBOARDS - Big buttons, clear labels
# =============================================================================

def get_simple_keyboard():
    """Simple keyboard that even ah gong can use"""
    keyboard = [
        [KeyboardButton("💰 How much I spent?"), KeyboardButton("📊 Show my money")],
        [KeyboardButton("❓ Help me lah"), KeyboardButton("🎯 Set budget")],
        [KeyboardButton("🔥 Got discount?"), KeyboardButton("💡 Give me advice")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_quick_amounts():
    """Quick amount buttons for common expenses"""
    keyboard = [
        [KeyboardButton("$2"), KeyboardButton("$3"), KeyboardButton("$5")],
        [KeyboardButton("$8"), KeyboardButton("$10"), KeyboardButton("$15")],
        [KeyboardButton("$20"), KeyboardButton("$25"), KeyboardButton("Other amount")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

# =============================================================================
# SIMPLE EXPENSE PARSING - Understand broken English + Singlish
# =============================================================================

def parse_simple_expense(text):
    """Parse expense even if user types like ah gong"""
    text = text.lower().strip()
    
    # Common patterns that uncles/aunties use
    patterns = [
        r'(\d+\.?\d*)',  # Just numbers: "5", "3.50"
        r'\$(\d+\.?\d*)',  # With dollar: "$5"
        r'spent?\s*(\d+\.?\d*)',  # "spent 5"
        r'pay\s*(\d+\.?\d*)',  # "pay 5"
        r'buy\s*(\d+\.?\d*)',  # "buy 5"
        r'cost\s*(\d+\.?\d*)',  # "cost 5"
    ]
    
    amount = None
    for pattern in patterns:
        import re
        match = re.search(pattern, text)
        if match:
            try:
                amount = float(match.group(1))
                break
            except:
                continue
    
    if not amount:
        return None
    
    # Simple category detection
    category = "others"
    if any(word in text for word in ['eat', 'food', 'makan', 'lunch', 'dinner', 'breakfast', 'drink', 'coffee', 'tea']):
        category = "food"
    elif any(word in text for word in ['bus', 'mrt', 'taxi', 'grab', 'transport', 'go']):
        category = "transport"
    elif any(word in text for word in ['movie', 'shop', 'buy', 'game']):
        category = "entertainment"
    
    return {
        'amount': amount,
        'category': category,
        'description': text[:50],  # Keep it simple
        'currency': 'SGD'
    }

# =============================================================================
# COMPANION RESPONSES - Like talking to your best friend
# =============================================================================

def get_companion_response(expense_amount, category, daily_total=0):
    """Get a companion-like response based on spending"""
    
    responses = []
    
    # Basic acknowledgment with personality
    if expense_amount <= 5:
        responses.extend([
            f"Okay noted! ${expense_amount} for {category}. Not bad lah! 👍",
            f"Got it! ${expense_amount} only. You quite thrifty eh! 😊",
            f"Wah only ${expense_amount}? You very good at saving! 💪"
        ])
    elif expense_amount <= 15:
        responses.extend([
            f"Okay! ${expense_amount} for {category}. Reasonable lah! 😄",
            f"${expense_amount} noted! Normal spending lor! 📝",
            f"Alright! ${expense_amount} for {category}. Still okay! 👌"
        ])
    else:
        responses.extend([
            f"Wah ${expense_amount}! Quite expensive leh! But okay lah! 😅",
            f"${expense_amount}?! Your wallet feeling it! But I understand! 💸",
            f"Alamak ${expense_amount}! Hope it's worth it ah! 😬"
        ])
    
    # Add daily spending context
    if daily_total > 50:
        responses.append("\n\nEh bro/sis, you spent quite a lot today already leh! Maybe take it easy? 😟")
    elif daily_total > 30:
        responses.append("\n\nToday's spending getting up there! Watch out ah! 👀")
    elif daily_total < 10:
        responses.append("\n\nWah you very disciplined today! Keep it up! 🌟")
    
    return random.choice(responses)

# =============================================================================
# ULTRA SIMPLE HANDLERS - No complex commands
# =============================================================================

async def start(update, context):
    """Super simple welcome"""
    user = update.effective_user
    name = user.first_name or "friend"
    
    # Register user
    try:
        await get_or_create_user(user.id, {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        })
    except:
        pass  # Don't confuse user with errors
    
    # Time-based greeting
    from datetime import datetime
    hour = datetime.now().hour
    if hour < 12:
        greeting = random.choice(companion.GREETINGS["morning"])
    elif hour < 18:
        greeting = random.choice(companion.GREETINGS["afternoon"])  
    else:
        greeting = random.choice(companion.GREETINGS["evening"])
    
    welcome = f"Eh {name}! {greeting}\n\n" \
              "I'm BaoJiak, your money tracking kakis! 🇸🇬\n\n" \
              "Very simple one:\n" \
              "• Just tell me what you spend: '5' or 'lunch 5'\n" \
              "• I help you track everything!\n" \
              "• No need remember commands!\n\n" \
              "Try telling me: 'coffee 3' or just '5' can already! 😊"
    
    await update.message.reply_text(welcome, reply_markup=get_simple_keyboard())

async def handle_anything(update, context):
    """Handle ANY message - be super forgiving"""
    text = update.message.text
    user_id = update.effective_user.id
    
    # Handle button presses
    if text == "💰 How much I spent?":
        await show_simple_summary(update, context)
        return
    elif text == "📊 Show my money":
        await show_simple_summary(update, context)
        return
    elif text == "❓ Help me lah":
        await show_simple_help(update, context)
        return
    elif text == "💡 Give me advice":
        await give_simple_advice(update, context)
        return
    elif text == "🔥 Got discount?":
        await show_simple_deals(update, context)
        return
    
    # Try to parse as expense
    expense = parse_simple_expense(text)
    
    if expense:
        # Save expense
        try:
            success = await save_expense(user_id, expense)
            if success:
                # Get today's total for context
                from datetime import datetime
                today_expenses = await get_user_expenses(user_id, days=1)
                daily_total = sum(exp['amount'] for exp in today_expenses)
                
                response = get_companion_response(expense['amount'], expense['category'], daily_total)
                
                # Add encouragement randomly
                if random.random() < 0.3:  # 30% chance
                    response += f"\n\n{random.choice(companion.ENCOURAGEMENT)}"
                
                await update.message.reply_text(response, reply_markup=get_simple_keyboard())
            else:
                await update.message.reply_text(
                    "Alamak! I cannot save this time! Try again can? 😅",
                    reply_markup=get_simple_keyboard()
                )
        except Exception as e:
            logger.error(f"Error saving expense: {e}")
            await update.message.reply_text(
                "Eh sorry lah! I blur blur now! Can try again? 😵",
                reply_markup=get_simple_keyboard()
            )
    else:
        # Be super helpful and forgiving
        await update.message.reply_text(
            "Eh I don't understand leh! 😅\n\n"
            "Just tell me simple simple:\n"
            "• 'lunch 5' (what + how much)\n"
            "• '3.50' (just the amount)\n"
            "• 'spent 10' (also can!)\n\n"
            "Don't worry, I very patient one! Try again! 😊",
            reply_markup=get_simple_keyboard()
        )

async def show_simple_summary(update, context):
    """Super simple summary that anyone can understand"""
    user_id = update.effective_user.id
    
    try:
        # Get last 7 days (easier to understand than 30)
        expenses = await get_user_expenses(user_id, days=7)
        
        if not expenses:
            await update.message.reply_text(
                "Eh you never tell me any spending yet! 😄\n\n"
                "Start by telling me: 'lunch 5' or just '5' can already!\n\n"
                "I will help you track everything! 💪",
                reply_markup=get_simple_keyboard()
            )
            return
        
        total = sum(exp['amount'] for exp in expenses)
        count = len(expenses)
        daily_avg = total / 7
        
        # Super simple message
        message = f"📊 *Your Money This Week* 💰\n\n"
        message += f"🏦 Total spent: ${total:.2f}\n"
        message += f"📝 Times you spent: {count}\n"
        message += f"📈 Average per day: ${daily_avg:.2f}\n\n"
        
        # Simple category breakdown (only top 2)
        categories = {}
        for exp in expenses:
            cat = exp['category']
            categories[cat] = categories.get(cat, 0) + exp['amount']
        
        if categories:
            message += "*Where your money went:*\n"
            sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            for cat, amount in sorted_cats[:2]:  # Only show top 2
                emoji = {"food": "🍜", "transport": "🚌", "entertainment": "🎬"}.get(cat, "💼")
                message += f"{emoji} {cat.title()}: ${amount:.2f}\n"
        
        # Simple advice
        if daily_avg > 20:
            message += f"\n💡 You spending ${daily_avg:.2f} per day. Maybe can save a bit? 😊"
        elif daily_avg < 10:
            message += f"\n🌟 Wah! Only ${daily_avg:.2f} per day! You very good at saving! 👏"
        else:
            message += f"\n👍 ${daily_avg:.2f} per day quite reasonable lah!"
        
        await update.message.reply_text(message, parse_mode='Markdown', reply_markup=get_simple_keyboard())
        
    except Exception as e:
        logger.error(f"Error in summary: {e}")
        await update.message.reply_text(
            "Eh sorry! I cannot calculate now! Try again later can? 😅",
            reply_markup=get_simple_keyboard()
        )

async def show_simple_help(update, context):
    """Super simple help"""
    help_msg = "❓ *How to use BaoJiak?* 🤔\n\n" \
               "Very simple one! Just tell me what you spend:\n\n" \
               "✅ 'lunch 5' - I know you spent $5 on food\n" \
               "✅ 'bus 2' - I know you spent $2 on transport\n" \
               "✅ '10' - I also can understand!\n" \
               "✅ 'coffee 3.50' - Decimal also okay!\n\n" \
               "🔘 Use the buttons below for quick access!\n\n" \
               "Don't worry if you make mistake! I very understanding one! 😊"
    
    await update.message.reply_text(help_msg, parse_mode='Markdown', reply_markup=get_simple_keyboard())

async def give_simple_advice(update, context):
    """Give simple, practical advice"""
    user_id = update.effective_user.id
    
    try:
        expenses = await get_user_expenses(user_id, days=7)
        
        if not expenses:
            advice = "💡 *My Advice* 🧠\n\n" \
                    "Start tracking your spending first!\n\n" \
                    "Just tell me: 'lunch 5' or 'coffee 3'\n\n" \
                    "Once I know your spending pattern, I can give you better advice! 😊"
        else:
            total = sum(exp['amount'] for exp in expenses)
            daily_avg = total / 7
            
            advice = f"💡 *My Advice for You* 🧠\n\n"
            
            if daily_avg > 25:
                advice += "You spending quite a lot leh! Try these:\n\n" \
                         "🍜 Eat at hawker center more\n" \
                         "🚌 Take MRT instead of Grab\n" \
                         "☕ Make coffee at home\n" \
                         "🛍️ Think twice before buying\n\n"
            elif daily_avg > 15:
                advice += "Your spending quite normal lah! But can still save:\n\n" \
                         "💰 Set aside $5 daily for savings\n" \
                         "🍜 Cook at home sometimes\n" \
                         "🎬 Look for promotions\n\n"
            else:
                advice += "Wah! You very good at saving! Keep it up!\n\n" \
                         "🌟 You're doing great!\n" \
                         "💪 Maybe can save even more?\n" \
                         "🎯 Set a savings goal?\n\n"
            
            advice += "Remember: Small savings add up to big money! 💰"
        
        await update.message.reply_text(advice, parse_mode='Markdown', reply_markup=get_simple_keyboard())
        
    except Exception as e:
        logger.error(f"Error giving advice: {e}")
        await update.message.reply_text(
            "Eh I blur blur now! Cannot give advice! Try again later? 😅",
            reply_markup=get_simple_keyboard()
        )

async def show_simple_deals(update, context):
    """Show simple deals"""
    deals_msg = "🔥 *Today's Good Deals!* 💰\n\n" \
               "🧋 Gong Cha: Buy 1 Get 1 Free!\n" \
               "📍 All outlets (except airport)\n" \
               "⏰ Until tomorrow only!\n\n" \
               "🎬 Golden Village: 50% off tickets!\n" \
               "📍 All cinemas\n" \
               "⏰ Monday to Thursday\n\n" \
               "🚗 Grab: Free delivery!\n" \
               "📍 Minimum $15 order\n" \
               "⏰ New users only\n\n" \
               "More deals coming soon! I will tell you! 😊"
    
    await update.message.reply_text(deals_msg, parse_mode='Markdown', reply_markup=get_simple_keyboard())

# =============================================================================
# MAIN FUNCTION - Keep it super simple
# =============================================================================

def main():
    """Main function - ultra simple setup"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ No token found!")
        return
    
    print("🇸🇬 Starting BaoJiak - Your Simple Money Companion...")
    
    # Setup database (hide complexity from user)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(init_database())
        print("✅ Ready to help you track money!")
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return
    
    # Create simple app
    app = Application.builder().token(token).build()
    
    # Only 2 handlers - keep it simple!
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_anything))  # Handle EVERYTHING
    
    print("🚀 BaoJiak is ready!")
    print("💬 Features:")
    print("   🗣️  Understands broken English + Singlish")
    print("   🔘  Big buttons for easy navigation")  
    print("   💰  Super simple expense tracking")
    print("   📊  Easy-to-understand summaries")
    print("   💡  Practical money advice")
    print("   🤗  Friendly companion personality")
    print("")
    print("👴👵 Perfect for uncles, aunties, and everyone!")
    
    # Run bot
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
