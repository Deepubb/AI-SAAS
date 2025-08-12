#!/usr/bin/env python3
"""
FastAPI webhook server for SG Money Buddy
Production deployment with webhook support
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import Application

from src.bot.handlers import setup_handlers
from src.utils.config import Config
from src.data.database import init_database

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO'))
)
logger = logging.getLogger(__name__)

# Global application instance
ptb_application: Application = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    global ptb_application
    
    # Initialize configuration
    config = Config()
    
    if not config.telegram_token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    # Initialize database
    await init_database()
    logger.info("Database initialized successfully")
    
    # Create and setup Telegram application
    ptb_application = Application.builder().token(config.telegram_token).build()
    setup_handlers(ptb_application)
    
    # Initialize the application
    await ptb_application.initialize()
    await ptb_application.start()
    
    # Set webhook
    if config.webhook_url:
        webhook_url = f"{config.webhook_url}/webhook"
        await ptb_application.bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    
    logger.info("SG Money Buddy Bot started successfully! 🇸🇬💰")
    
    yield
    
    # Cleanup
    await ptb_application.stop()
    await ptb_application.shutdown()
    logger.info("SG Money Buddy Bot stopped")


# Create FastAPI app
app = FastAPI(
    title="SG Money Buddy Bot",
    description="Singapore Personal Finance Telegram Bot",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "SG Money Buddy Bot is running! 🇸🇬💰",
        "version": "1.0.0"
    }


@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming Telegram updates"""
    try:
        # Get the raw body
        body = await request.body()
        
        # Parse update
        update = Update.de_json(data=await request.json(), bot=ptb_application.bot)
        
        if update:
            # Process update
            await ptb_application.process_update(update)
            return {"status": "ok"}
        else:
            logger.warning("Received invalid update")
            raise HTTPException(status_code=400, detail="Invalid update")
            
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/webhook/info")
async def webhook_info():
    """Get webhook information"""
    if ptb_application and ptb_application.bot:
        try:
            webhook_info = await ptb_application.bot.get_webhook_info()
            return {
                "url": webhook_info.url,
                "has_custom_certificate": webhook_info.has_custom_certificate,
                "pending_update_count": webhook_info.pending_update_count,
                "last_error_date": webhook_info.last_error_date,
                "last_error_message": webhook_info.last_error_message,
                "max_connections": webhook_info.max_connections,
                "allowed_updates": webhook_info.allowed_updates
            }
        except Exception as e:
            logger.error(f"Error getting webhook info: {e}")
            raise HTTPException(status_code=500, detail="Could not get webhook info")
    else:
        raise HTTPException(status_code=503, detail="Bot not initialized")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("webhook:app", host="0.0.0.0", port=port, reload=False)
