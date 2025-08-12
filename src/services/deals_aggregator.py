"""Deal aggregation service for Singapore channels"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DealsAggregator:
    """Aggregate deals from Singapore Telegram channels and websites"""
    
    SINGAPORE_DEAL_SOURCES = {
        "telegram_channels": [
            "@sgbudgetbabes",
            "@sgfooddeals", 
            "@sgtravelpromos",
            "@sgshoppingdeals",
            "@sghawkerdeals"
        ],
        "keywords": [
            "1-for-1", "discount", "promo", "sale", "cheap", "lobang",
            "free delivery", "student discount", "senior discount",
            "flash sale", "limited time", "exclusive"
        ],
        "locations": [
            "orchard", "bugis", "tampines", "jurong", "woodlands",
            "toa payoh", "bishan", "ang mo kio", "clementi", "bedok",
            "punggol", "sengkang", "hougang", "pasir ris"
        ]
    }
    
    def __init__(self):
        self.cached_deals = []
        self.last_update = None
    
    async def get_latest_deals(self, category: Optional[str] = None, location: Optional[str] = None) -> List[Dict]:
        """Get latest deals, optionally filtered by category and location"""
        try:
            # For now, return placeholder deals
            # In production, this would connect to actual Telegram channels
            placeholder_deals = [
                {
                    "title": "1-for-1 Bubble Tea at Gong Cha",
                    "description": "Any size, any flavor! Valid at all outlets except airport.",
                    "category": "food",
                    "location": "islandwide",
                    "original_price": 6.50,
                    "discounted_price": 3.25,
                    "savings": 3.25,
                    "source": "@sgfooddeals",
                    "expires": datetime.now() + timedelta(days=3),
                    "terms": "Valid Mon-Fri, 2-6pm only"
                },
                {
                    "title": "Free Grab Delivery (Min $15)",
                    "description": "Use code FREEDELIVERY. Valid for new users only.",
                    "category": "transport",
                    "location": "singapore",
                    "original_price": 3.99,
                    "discounted_price": 0.00,
                    "savings": 3.99,
                    "source": "@sgbudgetbabes",
                    "expires": datetime.now() + timedelta(days=7),
                    "terms": "New users only, min spend $15"
                },
                {
                    "title": "50% Off Movie Tickets at Golden Village",
                    "description": "All movies, all showtimes! Book through their app.",
                    "category": "entertainment",
                    "location": "islandwide",
                    "original_price": 13.50,
                    "discounted_price": 6.75,
                    "savings": 6.75,
                    "source": "@sgshoppingdeals",
                    "expires": datetime.now() + timedelta(days=5),
                    "terms": "Valid Mon-Thu only, book via GV app"
                }
            ]
            
            # Filter by category if specified
            if category:
                placeholder_deals = [deal for deal in placeholder_deals if deal["category"] == category]
            
            # Filter by location if specified
            if location:
                location_lower = location.lower()
                placeholder_deals = [
                    deal for deal in placeholder_deals 
                    if location_lower in deal["location"].lower() or deal["location"] == "islandwide"
                ]
            
            return placeholder_deals
            
        except Exception as e:
            logger.error(f"Error getting deals: {e}")
            return []
    
    async def search_deals(self, query: str) -> List[Dict]:
        """Search for deals matching a query"""
        try:
            all_deals = await self.get_latest_deals()
            query_lower = query.lower()
            
            matching_deals = []
            for deal in all_deals:
                if (query_lower in deal["title"].lower() or 
                    query_lower in deal["description"].lower() or
                    query_lower in deal["category"].lower()):
                    matching_deals.append(deal)
            
            return matching_deals
            
        except Exception as e:
            logger.error(f"Error searching deals: {e}")
            return []
    
    def format_deal_message(self, deal: Dict) -> str:
        """Format a deal into a nice Telegram message"""
        try:
            savings_percent = (deal["savings"] / deal["original_price"]) * 100
            
            message = f"🔥 *{deal['title']}*\n\n"
            message += f"📍 Location: {deal['location'].title()}\n"
            message += f"💰 Was: ${deal['original_price']:.2f}\n"
            message += f"✅ Now: ${deal['discounted_price']:.2f}\n"
            message += f"💵 Save: ${deal['savings']:.2f} ({savings_percent:.0f}%)\n\n"
            message += f"📝 {deal['description']}\n\n"
            
            if deal.get("terms"):
                message += f"⚠️ Terms: {deal['terms']}\n"
            
            expires_str = deal["expires"].strftime("%d %b %Y, %I:%M %p")
            message += f"⏰ Expires: {expires_str}\n"
            message += f"📢 Source: {deal['source']}\n\n"
            message += "Wah shiok deal! Don't miss out lah! 🇸🇬"
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting deal message: {e}")
            return "Error displaying deal information."
    
    async def get_deals_by_category(self, category: str) -> List[Dict]:
        """Get deals filtered by category"""
        return await self.get_latest_deals(category=category)
    
    async def get_deals_near_location(self, location: str) -> List[Dict]:
        """Get deals near a specific location"""
        return await self.get_latest_deals(location=location)
