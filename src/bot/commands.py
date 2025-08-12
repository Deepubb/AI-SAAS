"""Telegram bot command handlers for SG Money Buddy"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from .responses import SingaporeResponses
from .keyboards import SGKeyboards

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    
    # Register user in database
    from src.data.database import get_or_create_user
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": user.language_code
    }
    
    try:
        await get_or_create_user(user.id, user_data)
    except Exception as e:
        logger.error(f"Error registering user: {e}")
    
    welcome_message = SingaporeResponses.get_random_response("welcome_messages")
    welcome_message = f"Hello {user.first_name}! {welcome_message}"
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=SGKeyboards.main_menu()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
🇸🇬 *SG Money Buddy - Help Guide*

*Quick Commands:*
/start - Show main menu
/budget - Check your budget status
/summary - View spending summary
/deals - Find latest deals
/settings - Bot preferences

*Track Expenses:*
Just type naturally! Examples:
• "lunch $5" or "makan $5"
• "transport $2.50"
• "coffee $3 at starbucks"
• "grab $15 to orchard"

*Categories:*
🍜 Food & Drinks
🚌 Transport (MRT, bus, grab)
🏠 Housing & Utilities
🎬 Entertainment
🛍️ Shopping
🏥 Healthcare
📚 Education
💼 Others

*Singapore Features:*
✅ Singlish responses lah!
✅ Local price validation
✅ Deal aggregation from SG channels
✅ MRT/hawker center context

Need help? Just ask! I'm here to help you save money in Singapore! 💪
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode='Markdown'
    )


async def budget_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /budget command"""
    user_id = update.effective_user.id
    
    try:
        from src.data.database import get_user_budgets
        budgets = await get_user_budgets(user_id)
        
        if budgets:
            message = "💰 *Your Current Budgets* 📊\n\n"
            for budget in budgets:
                message += f"• {budget['category'].title()}: ${budget['amount']:.2f} ({budget['period']})\n"
            
            message += "\n💡 To set a new budget, use: `/setbudget food 500`"
        else:
            message = "💰 *No budgets set yet!* \n\n" \
                     "Set your first budget with: `/setbudget food 500`\n\n" \
                     "📊 Recommended Singapore budgets:\n" \
                     "• Food: $400-800/month\n" \
                     "• Transport: $80-150/month\n" \
                     "• Entertainment: $200-400/month"
        
        await update.message.reply_text(
            message,
            parse_mode='Markdown',
            reply_markup=SGKeyboards.expense_categories()
        )
        
    except Exception as e:
        logger.error(f"Error getting budgets: {e}")
        await update.message.reply_text(
            "Alamak! Cannot get budget info right now lah! Try again later! 😅"
        )


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /summary command"""
    user_id = update.effective_user.id
    
    try:
        from src.services.expense_tracker import ExpenseTracker
        tracker = ExpenseTracker()
        
        # Get expenses for last 30 days
        expenses = await tracker.get_user_expenses(user_id, days=30)
        
        if not expenses:
            await update.message.reply_text(
                "📊 *No expenses tracked yet!*\n\n"
                "Start tracking by sending messages like:\n"
                "• 'lunch $5'\n"
                "• 'transport $2.50'\n"
                "• 'coffee $3'\n\n"
                "I'll give you detailed summaries once you start tracking! 💪"
            )
            return
        
        # Calculate summary
        total = sum(exp["amount"] for exp in expenses)
        count = len(expenses)
        
        # Group by category
        by_category = {}
        for exp in expenses:
            cat = exp["category"]
            by_category[cat] = by_category.get(cat, 0) + exp["amount"]
        
        # Create summary message
        message = f"📊 *Your 30-Day Summary* 🇸🇬\n\n"
        message += f"💰 Total Spent: ${total:.2f}\n"
        message += f"📝 Transactions: {count}\n"
        message += f"📈 Average per day: ${total/30:.2f}\n\n"
        
        message += "*By Category:*\n"
        for category, amount in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100 if total > 0 else 0
            emoji = {"food": "🍜", "transport": "🚌", "entertainment": "🎬", 
                    "shopping": "🛍️", "healthcare": "🏥"}.get(category, "💼")
            message += f"{emoji} {category.title()}: ${amount:.2f} ({percentage:.0f}%)\n"
        
        # Add Singapore insights
        message += "\n🇸🇬 *Singapore Insights:*\n"
        if "food" in by_category:
            food_daily = by_category["food"] / 30
            if food_daily > 20:
                message += "• Food spending quite high leh! Try hawker centers more! 🍜\n"
            elif food_daily < 8:
                message += "• Great job on food budget! Very economical! 👍\n"
        
        if "transport" in by_category:
            transport_daily = by_category["transport"] / 30
            if transport_daily > 8:
                message += "• Transport costs high sia! Maybe use MRT more? 🚌\n"
            elif transport_daily < 3:
                message += "• Excellent transport savings! MRT FTW! 🚇\n"
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        await update.message.reply_text(
            "Alamak! Cannot generate summary right now lah! Try again later! 😅"
        )


async def deals_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /deals command"""
    try:
        from src.services.deals_aggregator import DealsAggregator
        aggregator = DealsAggregator()
        
        # Get latest deals
        deals = await aggregator.get_latest_deals()
        
        if deals:
            deals_message = SingaporeResponses.get_random_response("deal_alerts")
            message = f"{deals_message}\n\n"
            
            # Show top 3 deals
            for i, deal in enumerate(deals[:3], 1):
                savings = deal["original_price"] - deal["discounted_price"]
                savings_percent = (savings / deal["original_price"]) * 100
                
                message += f"🔥 *{deal['title']}*\n"
                message += f"📍 {deal['location'].title()}\n"
                message += f"💰 Was: ${deal['original_price']:.2f} → Now: ${deal['discounted_price']:.2f}\n"
                message += f"💵 Save: ${savings:.2f} ({savings_percent:.0f}%)\n"
                message += f"⏰ Expires: {deal['expires'].strftime('%d %b')}\n\n"
            
            message += "More deals coming from @sgbudgetbabes, @sgfooddeals! 🇸🇬"
        else:
            message = "🔍 No deals available right now lah!\n\n" \
                     "🚧 Deal aggregation feature coming soon!\n" \
                     "Will connect to @sgbudgetbabes, @sgfooddeals and more!"
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error getting deals: {e}")
        await update.message.reply_text(
            "Alamak! Cannot get deals right now lah! Try again later! 😅"
        )


async def setbudget_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setbudget command"""
    user_id = update.effective_user.id
    
    # Parse arguments
    if len(context.args) < 2:
        await update.message.reply_text(
            "💰 *Set Budget* 📊\n\n"
            "Usage: `/setbudget <category> <amount>`\n\n"
            "Examples:\n"
            "• `/setbudget food 500` - $500/month for food\n"
            "• `/setbudget transport 120` - $120/month for transport\n\n"
            "📊 Recommended Singapore budgets:\n"
            "• Food: $400-800/month\n"
            "• Transport: $80-150/month\n"
            "• Entertainment: $200-400/month\n"
            "• Shopping: $150-300/month",
            parse_mode='Markdown'
        )
        return
    
    category = context.args[0].lower()
    try:
        amount = float(context.args[1])
    except ValueError:
        await update.message.reply_text(
            "Eh! Please enter a valid amount lah!\n"
            "Example: `/setbudget food 500`"
        )
        return
    
    # Validate category
    valid_categories = ["food", "transport", "housing", "entertainment", "shopping", "healthcare", "education", "others"]
    if category not in valid_categories:
        await update.message.reply_text(
            f"Sorry leh! '{category}' not a valid category.\n\n"
            f"Valid categories: {', '.join(valid_categories)}"
        )
        return
    
    # Validate amount
    if amount <= 0:
        await update.message.reply_text("Amount must be more than $0 lah!")
        return
    
    if amount > 10000:
        await update.message.reply_text("Wah! More than $10,000? That's quite a lot sia! Sure or not?")
        return
    
    try:
        from src.data.database import save_budget
        success = await save_budget(user_id, category, amount, "monthly")
        
        if success:
            # Add Singapore context
            validation_msg = ""
            if category == "food" and amount > 800:
                validation_msg = "\n\n💡 That's quite high for food in Singapore leh! Maybe can reduce a bit?"
            elif category == "food" and amount < 300:
                validation_msg = "\n\n⚠️ That's quite low for food budget! Make sure you eat enough!"
            elif category == "transport" and amount > 200:
                validation_msg = "\n\n💡 Transport budget quite high! Maybe use MRT more?"
            
            response = f"✅ Budget set successfully!\n\n" \
                      f"💰 {category.title()}: ${amount:.2f}/month{validation_msg}\n\n" \
                      f"Use /budget to see all your budgets!"
            
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(
                "Alamak! Cannot save budget right now lah! Try again later! 😅"
            )
            
    except Exception as e:
        logger.error(f"Error setting budget: {e}")
        await update.message.reply_text(
            "Alamak! Something went wrong setting your budget! Try again later leh! 😅"
        )


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /settings command"""
    settings_text = """
⚙️ *Settings*

Current Settings:
• Currency: SGD 🇸🇬
• Language: Singlish + English
• Timezone: Asia/Singapore
• Notifications: Enabled

🚧 More settings coming soon:
• Budget alerts
• Deal notifications
• Spending categories
• Export data
"""
    
    await update.message.reply_text(
        settings_text,
        parse_mode='Markdown'
    )
