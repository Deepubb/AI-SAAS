#!/usr/bin/env python3
"""
BaoJiak - Ultra Simple Singapore Companion Bot
Your friendly neighborhood money tracking kakis! 🇸🇬💰
"""

import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

# Load environment
load_dotenv()

# Simple logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import our systems
from src.data.database import init_database, get_or_create_user, save_expense, get_user_expenses
from src.services.expense_tracker import ExpenseTracker
from src.bot.unified_responses import BaoJiakResponses

# =============================================================================
# REPLY KEYBOARDS - Persistent and accessible interface
# =============================================================================

def get_main_menu():
    """Main menu with reply keyboard - persistent and accessible"""
    keyboard = [
        [KeyboardButton("📊 My Spending"), KeyboardButton("💰 Quick Add")],
        [KeyboardButton("🎯 Budgets"), KeyboardButton("📈 Analytics")],
        [KeyboardButton("🔥 Deals"), KeyboardButton("💡 Advice")],
        [KeyboardButton("⚙️ Settings"), KeyboardButton("❓ Help")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def get_quick_add_keyboard():
    """Quick expense amounts"""
    keyboard = [
        [KeyboardButton("$2"), KeyboardButton("$3"), KeyboardButton("$5")],
        [KeyboardButton("$8"), KeyboardButton("$10"), KeyboardButton("$15")],
        [KeyboardButton("$20"), KeyboardButton("$25"), KeyboardButton("💬 Custom")],
        [KeyboardButton("🔙 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_category_keyboard():
    """Category selection for expenses"""
    keyboard = [
        [KeyboardButton("🍜 Food"), KeyboardButton("🚌 Transport")],
        [KeyboardButton("🎬 Entertainment"), KeyboardButton("🛍️ Shopping")],
        [KeyboardButton("🏥 Healthcare"), KeyboardButton("💼 Others")],
        [KeyboardButton("🔙 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_budget_keyboard():
    """Budget management options"""
    keyboard = [
        [KeyboardButton("📊 View Budgets"), KeyboardButton("➕ Set Budget")],
        [KeyboardButton("⚠️ Alerts"), KeyboardButton("📈 Progress")],
        [KeyboardButton("🔙 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_analytics_keyboard():
    """Analytics and reports options"""
    keyboard = [
        [KeyboardButton("📊 Weekly Report"), KeyboardButton("📅 Monthly Report")],
        [KeyboardButton("📈 Spending Trends"), KeyboardButton("🏆 Top Categories")],
        [KeyboardButton("💰 Savings Goal"), KeyboardButton("📱 Export Data")],
        [KeyboardButton("🔙 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_settings_keyboard():
    """Settings and preferences"""
    keyboard = [
        [KeyboardButton("💱 Currency"), KeyboardButton("🌍 Language")],
        [KeyboardButton("🔔 Notifications"), KeyboardButton("🗑️ Clear Data")],
        [KeyboardButton("📤 Export"), KeyboardButton("📥 Import")],
        [KeyboardButton("🔙 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

# =============================================================================
# BOT HANDLERS - Super simple and forgiving
# =============================================================================

async def start(update, context):
    """Enhanced welcome with persistent keyboard"""
    user = update.effective_user
    name = user.first_name or "friend"
    
    # Register user quietly
    try:
        await get_or_create_user(user.id, {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        })
    except:
        pass  # Don't confuse user with errors
    
    # Get time-based greeting
    greeting = BaoJiakResponses.get_time_based_greeting()
    
    welcome = f"Eh {name}! {greeting}\n\n" \
              "🤖 I'm *BaoJiak*, your AI money tracking companion! 🇸🇬💰\n\n" \
              "✨ *What I can do:*\n" \
              "💬 Track expenses: Just say 'lunch 5' or 'coffee 3'\n" \
              "📊 Smart analytics & budgeting\n" \
              "🔥 Find deals & save money\n" \
              "💡 Personalized financial advice\n" \
              "🗣️ Understand Singlish & broken English\n\n" \
              "Use the buttons below for quick actions, or just tell me your expenses! 😊"
    
    # Show welcome with persistent main menu
    await update.message.reply_text(
        welcome, 
        parse_mode='Markdown',
        reply_markup=get_main_menu()
    )

async def handle_message(update, context):
    """Handle ANY message - buttons and expense tracking"""
    text = update.message.text
    user_id = update.effective_user.id
    
    # Handle main menu button presses
    if text == "📊 My Spending":
        await show_spending_summary(update, context)
        return
    elif text == "💰 Quick Add":
        await show_quick_add_menu(update, context)
        return
    elif text == "🎯 Budgets":
        await show_budget_menu(update, context)
        return
    elif text == "📈 Analytics":
        await show_analytics_menu(update, context)
        return
    elif text == "🔥 Deals":
        await show_deals(update, context)
        return
    elif text == "💡 Advice":
        await show_advice(update, context)
        return
    elif text == "⚙️ Settings":
        await show_settings_menu(update, context)
        return
    elif text == "❓ Help":
        await show_help(update, context)
        return
    elif text == "🔙 Main Menu":
        await show_main_menu(update, context)
        return
    
    # Handle quick add amounts
    elif text in ["$2", "$3", "$5", "$8", "$10", "$15", "$20", "$25"]:
        amount = float(text.replace("$", ""))
        context.user_data['pending_amount'] = amount
        await show_category_menu(update, context, amount)
        return
    elif text == "💬 Custom":
        await update.message.reply_text(
            "💰 *Custom Amount*\n\nJust tell me the amount and what it's for!\n\nExample: 'lunch 7.50' or 'transport 3'",
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )
        return
    
    # Handle category selection
    elif text in ["🍜 Food", "🚌 Transport", "🎬 Entertainment", "🛍️ Shopping", "🏥 Healthcare", "💼 Others"]:
        category = text.split()[1].lower()  # Extract category from button text
        amount = context.user_data.get('pending_amount', 0)
        
        if amount > 0:
            await save_quick_expense(update, context, amount, category)
            context.user_data.pop('pending_amount', None)
        else:
            await update.message.reply_text(
                "❌ No amount found! Please start over.",
                reply_markup=get_main_menu()
            )
        return
    
    # Handle analytics buttons
    elif text in ["📊 Weekly Report", "📅 Monthly Report", "📈 Spending Trends", "🏆 Top Categories", "💰 Savings Goal", "📱 Export Data"]:
        await update.message.reply_text(
            f"🚧 *{text}*\n\nThis feature is coming soon! Stay tuned for updates! 😊",
            parse_mode='Markdown',
            reply_markup=get_analytics_keyboard()
        )
        return
    
    # Handle budget buttons
    elif text in ["📊 View Budgets", "➕ Set Budget", "⚠️ Alerts", "📈 Progress"]:
        if text == "➕ Set Budget":
            await update.message.reply_text(
                "🎯 *Set Budget*\n\nTo set a budget, send me a message like:\n`/setbudget food 500`\n\nOr go back to main menu:",
                parse_mode='Markdown',
                reply_markup=get_main_menu()
            )
        else:
            await update.message.reply_text(
                f"🚧 *{text}*\n\nThis feature is coming soon! Stay tuned for updates! 😊",
                parse_mode='Markdown',
                reply_markup=get_budget_keyboard()
            )
        return
    
    # Handle settings buttons
    elif text in ["💱 Currency", "🌍 Language", "🔔 Notifications", "🗑️ Clear Data", "📤 Export", "📥 Import"]:
        await update.message.reply_text(
            f"🚧 *{text}*\n\nThis feature is coming soon! Stay tuned for updates! 😊",
            parse_mode='Markdown',
            reply_markup=get_settings_keyboard()
        )
        return
    
    # Try to parse as expense
    tracker = ExpenseTracker()
    expense = tracker.parse_expense_message(text)
    
    if expense:
        # Save expense
        try:
            success = await save_expense(user_id, expense)
            if success:
                # Get today's total for context
                today_expenses = await get_user_expenses(user_id, days=1)
                daily_total = sum(exp['amount'] for exp in today_expenses)
                
                # Build smart response
                response = BaoJiakResponses.build_smart_response(
                    expense['amount'], 
                    expense['category'], 
                    daily_total, 
                    text
                )
                
                await update.message.reply_text(response, reply_markup=get_main_menu())
            else:
                await update.message.reply_text(
                    BaoJiakResponses.get_random_response("error_messages"),
                    reply_markup=get_main_menu()
                )
        except Exception as e:
            logger.error(f"Error saving expense: {e}")
            await update.message.reply_text(
                "Eh sorry lah! I blur blur now! Can try again? 😵",
                reply_markup=get_main_menu()
            )
    else:
        # Be super helpful and patient
        help_response = BaoJiakResponses.get_random_response("help_messages")
        await update.message.reply_text(help_response, reply_markup=get_main_menu())

# =============================================================================
# REPLY KEYBOARD HANDLERS - Handle button presses
# =============================================================================

async def show_main_menu(update, context):
    """Show main menu"""
    await update.message.reply_text(
        "🎯 *Main Menu*\n\nWhat would you like to do?",
        parse_mode='Markdown',
        reply_markup=get_main_menu()
    )

async def show_quick_add_menu(update, context):
    """Show quick add expense menu"""
    await update.message.reply_text(
        "💰 *Quick Add Expense*\n\nChoose a common amount:",
        parse_mode='Markdown',
        reply_markup=get_quick_add_keyboard()
    )

async def show_category_menu(update, context, amount):
    """Show category selection menu"""
    await update.message.reply_text(
        f"💰 Adding ${amount} expense\n\nWhat category?",
        parse_mode='Markdown',
        reply_markup=get_category_keyboard()
    )

async def save_quick_expense(update, context, amount, category):
    """Save quick expense from buttons"""
    user_id = update.effective_user.id
    
    expense_data = {
        'amount': amount,
        'category': category,
        'description': f'{category} expense',
        'currency': 'SGD'
    }
    
    try:
        success = await save_expense(user_id, expense_data)
        if success:
            response = BaoJiakResponses.get_expense_response(amount, category)
            await update.message.reply_text(
                f"✅ *Expense Added!*\n\n{response}",
                parse_mode='Markdown',
                reply_markup=get_main_menu()
            )
        else:
            await update.message.reply_text(
                "❌ *Error*\n\nCannot save expense right now lah! Try again!",
                parse_mode='Markdown',
                reply_markup=get_main_menu()
            )
    except Exception as e:
        logger.error(f"Error saving quick expense: {e}")
        await update.message.reply_text(
            "❌ Something went wrong! Try again lah! 😅",
            reply_markup=get_main_menu()
        )

async def show_budget_menu(update, context):
    """Show budget management menu"""
    await update.message.reply_text(
        "🎯 *Budget Management*\n\nManage your spending limits:",
        parse_mode='Markdown',
        reply_markup=get_budget_keyboard()
    )

async def show_analytics_menu(update, context):
    """Show analytics menu"""
    await update.message.reply_text(
        "📈 *Analytics & Reports*\n\nDetailed insights into your spending:",
        parse_mode='Markdown',
        reply_markup=get_analytics_keyboard()
    )

async def show_settings_menu(update, context):
    """Show settings menu"""
    await update.message.reply_text(
        "⚙️ *Settings*\n\nCustomize your BaoJiak experience:",
        parse_mode='Markdown',
        reply_markup=get_settings_keyboard()
    )

# =============================================================================
# MAIN FEATURE FUNCTIONS
# =============================================================================

async def show_spending_summary(update, context):
    """Show spending summary"""
    user_id = update.effective_user.id
    
    try:
        expenses = await get_user_expenses(user_id, days=7)
        
        if not expenses:
            await update.message.reply_text(
                "📊 *Your Spending Summary*\n\nNo expenses tracked yet! Start by telling me what you spend:\n• 'lunch 5'\n• 'coffee 3'\n• 'transport 2'",
                parse_mode='Markdown',
                reply_markup=get_main_menu()
            )
            return
        
        total = sum(exp['amount'] for exp in expenses)
        count = len(expenses)
        daily_avg = total / 7
        
        # Category breakdown
        categories = {}
        for exp in expenses:
            cat = exp['category']
            categories[cat] = categories.get(cat, 0) + exp['amount']
        
        message = f"📊 *Your Weekly Summary*\n\n"
        message += f"💰 Total: ${total:.2f}\n"
        message += f"📝 Transactions: {count}\n"
        message += f"📈 Daily Average: ${daily_avg:.2f}\n\n"
        
        if categories:
            message += "*Top Categories:*\n"
            sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
            for cat, amount in sorted_cats:
                emoji = {"food": "🍜", "transport": "🚌", "entertainment": "🎬", "shopping": "🛍️"}.get(cat, "💼")
                message += f"{emoji} {cat.title()}: ${amount:.2f}\n"
        
        # Simple advice
        if daily_avg > 20:
            message += f"\n💡 Spending ${daily_avg:.2f}/day - maybe can save a bit? 😊"
        elif daily_avg < 10:
            message += f"\n🌟 Only ${daily_avg:.2f}/day - excellent saving! 👏"
        else:
            message += f"\n👍 ${daily_avg:.2f}/day is quite reasonable!"
        
        await update.message.reply_text(
            message,
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )
        
    except Exception as e:
        logger.error(f"Error in summary: {e}")
        await update.message.reply_text(
            "❌ Cannot get summary right now lah! Try again! 😅",
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )

async def show_deals(update, context):
    """Show deals"""
    deals_msg = "🔥 *Today's Hot Deals!*\n\n" \
               "🧋 *Gong Cha*: Buy 1 Get 1 Free!\n" \
               "📍 All outlets (except airport)\n" \
               "⏰ Until tomorrow only!\n\n" \
               "🎬 *Golden Village*: 50% off tickets!\n" \
               "📍 All cinemas\n" \
               "⏰ Monday to Thursday\n\n" \
               "🚗 *Grab*: Free delivery!\n" \
               "📍 Min $15 order, new users only\n\n" \
               "💰 More deals coming soon!"
    
    await update.message.reply_text(
        deals_msg,
        parse_mode='Markdown',
        reply_markup=get_main_menu()
    )

async def show_advice(update, context):
    """Show personalized advice"""
    user_id = update.effective_user.id
    
    try:
        expenses = await get_user_expenses(user_id, days=7)
        
        if not expenses:
            advice = "💡 *My Advice*\n\nStart tracking your spending first!\n\nJust tell me: 'lunch 5' or 'coffee 3'\n\nOnce I know your pattern, I can give better advice! 😊"
        else:
            total = sum(exp['amount'] for exp in expenses)
            daily_avg = total / 7
            
            advice = f"💡 *Personal Advice*\n\n"
            
            if daily_avg > 25:
                advice += "You spending quite high leh! Try:\n\n🍜 Hawker centers vs restaurants\n🚌 MRT vs Grab\n☕ Home coffee vs café\n💭 Think before buying\n\n"
            elif daily_avg > 15:
                advice += "Spending is normal! Can still save:\n\n💰 Save $5 daily\n🏠 Cook at home sometimes\n🎬 Look for promotions\n\n"
            else:
                advice += "Excellent saving habits! 👏\n\n🌟 You're doing great!\n💪 Maybe save even more?\n🎯 Set savings goals?\n\n"
            
            advice += f"📊 Weekly average: ${daily_avg:.2f}/day\n💰 Small savings = Big money!"
        
        await update.message.reply_text(
            advice,
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )
        
    except Exception as e:
        logger.error(f"Error in advice: {e}")
        await update.message.reply_text(
            "❌ Cannot get advice right now! Try again lah! 😅",
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )

async def show_help(update, context):
    """Show help"""
    help_msg = "❓ *How to use BaoJiak?*\n\n" \
               "Very simple! Just tell me your expenses:\n\n" \
               "✅ `lunch 5` - Food expense\n" \
               "✅ `bus 2` - Transport\n" \
               "✅ `coffee 3.50` - Decimals work!\n" \
               "✅ `makan 4` - Singlish OK!\n" \
               "✅ `i spend 10` - Broken English OK!\n\n" \
               "🔘 Use buttons for quick actions\n" \
               "📊 Check summaries anytime\n" \
               "💡 Get personalized advice\n\n" \
               "Don't worry about mistakes - I understand everything! 😊"
    
    await update.message.reply_text(
        help_msg,
        parse_mode='Markdown',
        reply_markup=get_main_menu()
    )

# =============================================================================
# MAIN FUNCTION - Ultra simple setup
# =============================================================================

def main():
    """Main function - ultra simple setup"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ No TELEGRAM_BOT_TOKEN found!")
        return
    
    print("🇸🇬 Starting BaoJiak - Your Money Companion...")
    
    # Setup database
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(init_database())
        print("✅ Database ready!")
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return
    
    # Create simple app
    app = Application.builder().token(token).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))  # Handle text messages and buttons
    
    print("🚀 BaoJiak is ready!")
    print("💬 Enhanced Features:")
    print("   🗣️  Understands broken English + Singlish")
    print("   🔘  Persistent reply keyboard interface")  
    print("   💰  Quick expense tracking + custom amounts")
    print("   📊  Smart analytics & summaries")
    print("   🎯  Budget management")
    print("   🔥  Deal notifications")
    print("   💡  Personalized financial advice")
    print("   ⚙️  Settings & preferences")
    print("   🤗  Friendly companion personality")
    print("")
    print("👴👵 Perfect for everyone in Singapore!")
    print("")
    print("💬 Try sending to your bot:")
    print("   /start - Get started with main menu")
    print("   'lunch 5' - Track expense naturally")
    print("   'makan 4.50' - Singlish works!")
    print("   'i spend 10' - Broken English OK!")
    print("   Use persistent buttons for quick actions! 🔘")
    
    # Run bot
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

