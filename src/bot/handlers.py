"""Main bot handlers for SG Money Buddy"""

import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, filters, ContextTypes
)

from .commands import (
    start_command, help_command, budget_command, setbudget_command,
    summary_command, deals_command, settings_command
)
from .responses import SingaporeResponses
from .keyboards import SGKeyboards

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    await start_command(update, context)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    await help_command(update, context)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle general text messages (expense tracking)"""
    message_text = update.message.text.lower()
    
    # Try to parse as expense
    from src.services.expense_tracker import ExpenseTracker
    tracker = ExpenseTracker()
    
    parsed_expense = tracker.parse_expense_message(message_text)
    
    if parsed_expense:
        # Log expense to database
        user_id = update.effective_user.id
        success = await tracker.log_expense(user_id, parsed_expense)
        
        if success:
            response = SingaporeResponses.get_random_response(
                "expense_logged",
                amount=SingaporeResponses.format_currency(parsed_expense['amount']),
                category=parsed_expense['category']
            )
            
            # Add validation feedback if available
            validation = parsed_expense.get('validation', {})
            if validation.get('warning'):
                response += f"\n\n⚠️ {validation['warning']}"
            
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(
                "Alamak! Cannot save your expense. Try again later leh! 😅"
            )
    else:
        # Fallback response
        await update.message.reply_text(
            "Eh, I don't understand leh! 🤔\n"
            "Try something like: 'lunch $5' or 'transport $2.50'\n"
            "Or use /help to see what I can do!"
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Exception while handling update: {context.error}")
    
    if update and hasattr(update, 'effective_message'):
        await update.effective_message.reply_text(
            SingaporeResponses.get_random_response("error_messages")
        )


def setup_handlers(application: Application) -> None:
    """Setup all bot handlers"""
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("budget", budget_command))
    application.add_handler(CommandHandler("setbudget", setbudget_command))
    application.add_handler(CommandHandler("summary", summary_command))
    application.add_handler(CommandHandler("deals", deals_command))
    application.add_handler(CommandHandler("settings", settings_command))
    
    # Message handlers
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    )
    
    # Callback query handlers (for inline keyboards)
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    logger.info("All handlers registered successfully")


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "track_expense":
        await query.edit_message_text(
            "What did you spend on? 💰\nJust type something like: 'lunch $5' or 'transport $2.50'",
            reply_markup=SGKeyboards.expense_categories()
        )
    elif data == "check_budget":
        await budget_command(update, context)
    elif data == "find_deals":
        await deals_command(update, context)
    elif data == "help":
        await help_command(update, context)
    else:
        await query.edit_message_text(
            f"Feature '{data}' coming soon lah! 🚧\nStay tuned for updates!"
        )
