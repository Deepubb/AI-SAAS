"""
Enhanced Response System for SG Money Buddy
Dopamine-driven, context-aware responses that make users addicted to tracking expenses!
"""

import random
from datetime import datetime, time
from typing import Dict, List, Optional

class EnhancedResponses:
    """Premium response system with Singapore context and dopamine hits"""
    
    # =============================================================================
    # DOPAMINE RESPONSE PATTERNS - Context-aware celebrations
    # =============================================================================
    
    RESPONSE_PATTERNS = {
        'hawker': [
            "Shiok! Hawker uncle treating you well! 🍜 That's like ${per_dish:.2f} per dish if got 3 items - value for money sia!",
            "Smart choice! Hawker > overpriced cafe any day! 💰 You just saved ${saved_vs_restaurant:.2f} vs restaurant!",
            "Hawker power! 🍜 Your wallet says thank you! That's ${saved_vs_restaurant:.2f} saved vs fancy places!",
            "Hawker champion! 🏆 ${amount} for authentic Singapore taste - can't beat that lah!",
            "Wah! Hawker food at ${amount}? Uncle giving you special price sia! 🍜✨"
        ],
        
        'grab': [
            "Wah Grab again? Maybe bus next time save some money? 🚌 That's ${amount} for transport today!",
            "Convenience has a price lah! 🚗 ${amount} for Grab vs ${bus_cost:.2f} for bus - but hey, comfort matters!",
            "Grab life! 🚗 ${amount} for door-to-door service. Sometimes worth it for the convenience!",
            "Transport expense logged! 🚗 ${amount} for Grab. Consider MRT next time to save ${savings:.2f}!",
            "Grab expense: ${amount} 🚗 Remember: MRT = ${mrt_cost:.2f}, Bus = ${bus_cost:.2f}. Choose wisely!"
        ],
        
        'kopi': [
            "Kopi break well-deserved! ☕ ${amount} for your daily dose of happiness!",
            "That's your daily dose of happiness! ☕✨ ${amount} well spent on kopi!",
            "Kopi time! ☕ ${amount} for liquid gold. Singapore runs on kopi!",
            "Kopi expense: ${amount} ☕ Your morning ritual is safe!",
            "Kopi break logged! ☕ ${amount} for the best drink in Singapore!"
        ],
        
        'bubble_tea': [
            "Bubble tea addiction real sia! 🧋 ${amount} for sweet happiness!",
            "Sweet treat = happy day! 🧋😊 ${amount} for bubble tea joy!",
            "Bubble tea logged! 🧋 ${amount} for your sweet tooth satisfaction!",
            "Bubble tea time! 🧋 ${amount} for the perfect afternoon pick-me-up!",
            "Sweet indulgence: ${amount} 🧋 Bubble tea is life in Singapore!"
        ],
        
        'transport': [
            "Transport expense: ${amount} 🚌 Smart choice using public transport!",
            "Moving around Singapore: ${amount} 🚇 That's the cost of being mobile!",
            "Transport logged: ${amount} 🚌 Public transport = smart money move!",
            "Getting around: ${amount} 🚇 Singapore's transport network at work!",
            "Transport expense: ${amount} 🚌 Your daily commute investment!"
        ],
        
        'food': [
            "Food expense: ${amount} 🍽️ Fueling your Singapore adventure!",
            "Makan time: ${amount} 🍜 Good food = good life!",
            "Food logged: ${amount} 🍽️ Your taste buds thank you!",
            "Dining expense: ${amount} 🍜 Singapore's culinary scene explored!",
            "Food expense: ${amount} 🍽️ Good food is always worth it!"
        ]
    }
    
    # =============================================================================
    # MICRO-CELEBRATIONS - Achievement system responses
    # =============================================================================
    
    ACHIEVEMENT_RESPONSES = {
        'first_expense_day': [
            "Early bird catches the worm! 🌅 First expense of the day logged!",
            "Day starter! 🌅 You're on track for a great financial day!",
            "Morning momentum! 🌅 First expense logged - keep it going!",
            "Early riser! 🌅 Your day is off to a smart financial start!",
            "Day opener! 🌅 First expense tracked - you're ahead of the game!"
        ],
        
        'streak_3': [
            "Habit building champion! 🏆 3 days in a row - you're on fire! 🔥",
            "Consistency king! 👑 3-day streak! You're building great money habits!",
            "Streak master! 🏆 3 days straight! Your wallet loves you!",
            "Habit hero! 🦸‍♂️ 3-day streak! You're becoming a money master!",
            "Streak superstar! ⭐ 3 days in a row! Consistency is key!"
        ],
        
        'streak_7': [
            "Week warrior! 🏆 7-day streak! You're unstoppable! 💪",
            "Weekly champion! 🏆 7 days straight! You're building wealth!",
            "Streak legend! 🏆 7 days! You're a money tracking machine!",
            "Week master! 🏆 7-day streak! Your financial future is bright!",
            "Weekly hero! 🦸‍♂️ 7 days! You're mastering money management!"
        ],
        
        'under_budget': [
            "Budget ninja! 🥷 You're under budget today! Stealth savings!",
            "Budget master! 🎯 Under budget achievement unlocked! 💰",
            "Savings champion! 🏆 Under budget today! Your wallet is happy!",
            "Budget hero! 🦸‍♂️ Under budget! You're crushing your financial goals!",
            "Budget wizard! 🧙‍♂️ Under budget today! Magic money moves!"
        ],
        
        'hawker_choice': [
            "Smart money move! 💡 Hawker over restaurant = savings unlocked!",
            "Value champion! 🏆 Hawker choice saves you money! Smart thinking!",
            "Budget hero! 💰 Hawker choice = more money for other things!",
            "Smart spender! 🧠 Hawker over restaurant = financial wisdom!",
            "Value master! 💡 Hawker choice = maximum value for money!"
        ],
        
        'public_transport': [
            "Eco warrior! 🌱 Public transport = save money + save planet!",
            "Smart commuter! 🚌 Public transport = wallet-friendly choice!",
            "Transport champion! 🏆 Public transport = smart money move!",
            "Eco hero! 🌍 Public transport = good for wallet and environment!",
            "Smart traveler! 🚇 Public transport = maximum value for money!"
        ]
    }
    
    # =============================================================================
    # TIME-BASED CONTEXTUAL RESPONSES
    # =============================================================================
    
    TIME_RESPONSES = {
        'morning': [
            "Wah early bird! 🌅 Starting your day with smart money tracking!",
            "Morning momentum! 🌅 Early expense tracking = financial success!",
            "Breakfast under ${amount}? Respect! 💪 Smart morning choices!",
            "Morning expense logged! 🌅 You're ahead of the game!",
            "Early start! 🌅 Your financial day begins with smart tracking!"
        ],
        
        'lunch': [
            "Lunch at {time}? Beat the crowd and prices! 😎",
            "Lunch time! 🍽️ Smart timing for better deals!",
            "Midday meal: ${amount} 🍜 Fueling your afternoon!",
            "Lunch logged! 🍽️ Your energy investment for the day!",
            "Lunch expense: ${amount} 🍜 Powering through the day!"
        ],
        
        'afternoon': [
            "Afternoon pick-me-up: ${amount} ☕ Midday energy boost!",
            "Afternoon expense: ${amount} 🌞 Keeping your day going!",
            "Midday spending: ${amount} 🌞 Your afternoon investment!",
            "Afternoon logged: ${amount} 🌞 Powering through the day!",
            "Afternoon expense: ${amount} 🌞 Your day's momentum!"
        ],
        
        'evening': [
            "Dinner time! 🍳 ${amount} for evening fuel!",
            "Evening meal: ${amount} 🌙 Ending your day with good food!",
            "Dinner logged: ${amount} 🍳 Your day's grand finale!",
            "Evening expense: ${amount} 🌙 Perfect ending to your day!",
            "Dinner time: ${amount} 🍳 Your day's celebration meal!"
        ],
        
        'late_night': [
            "Late night craving: ${amount} 🌙 Midnight munchies satisfied!",
            "Night owl expense: ${amount} 🌙 Late night indulgence!",
            "Late night logged: ${amount} 🌙 Your nocturnal needs met!",
            "Night expense: ${amount} 🌙 Your late night satisfaction!",
            "Late night: ${amount} 🌙 Your night's special treat!"
        ]
    }
    
    # =============================================================================
    # SMART CONTEXTUAL RESPONSES - Main response builder
    # =============================================================================
    
    @staticmethod
    def build_smart_response(amount: float, category: str, daily_total: float, 
                           original_text: str, user_id: int = None) -> str:
        """Build a smart, contextual response that celebrates and educates"""
        
        # Get time context
        current_time = datetime.now().time()
        time_context = EnhancedResponses._get_time_context(current_time)
        
        # Get category-specific response
        category_response = EnhancedResponses._get_category_response(amount, category, daily_total)
        
        # Get achievement response if applicable
        achievement_response = EnhancedResponses._get_achievement_response(amount, category, daily_total)
        
        # Get time-based response
        time_response = EnhancedResponses._get_time_based_response(amount, time_context)
        
        # Build the complete response
        response_parts = []
        
        # Main expense confirmation
        response_parts.append(f"✅ *Expense Logged!* ${amount:.2f} for {category.title()}")
        
        # Add category-specific celebration
        if category_response:
            response_parts.append(f"\n{category_response}")
        
        # Add time context
        if time_response:
            response_parts.append(f"\n{time_response}")
        
        # Add achievement celebration
        if achievement_response:
            response_parts.append(f"\n\n🎉 {achievement_response}")
        
        # Add daily context
        daily_context = EnhancedResponses._get_daily_context(daily_total, amount)
        if daily_context:
            response_parts.append(f"\n\n📊 {daily_context}")
        
        # Add smart tip
        smart_tip = EnhancedResponses._get_smart_tip(amount, category, daily_total)
        if smart_tip:
            response_parts.append(f"\n\n💡 *Smart Tip:* {smart_tip}")
        
        return "\n".join(response_parts)
    
    # =============================================================================
    # HELPER METHODS - Context detection and response generation
    # =============================================================================
    
    @staticmethod
    def _get_time_context(current_time: time) -> str:
        """Get time-based context for responses"""
        if time(5, 0) <= current_time < time(11, 0):
            return 'morning'
        elif time(11, 0) <= current_time < time(14, 0):
            return 'lunch'
        elif time(14, 0) <= current_time < time(18, 0):
            return 'afternoon'
        elif time(18, 0) <= current_time < time(22, 0):
            return 'evening'
        else:
            return 'late_night'
    
    @staticmethod
    def _get_category_response(amount: float, category: str, daily_total: float) -> str:
        """Get category-specific response with context"""
        category_lower = category.lower()
        
        # Check for specific patterns
        if 'hawker' in category_lower or amount <= 8:
            saved_vs_restaurant = amount * 2.5  # Hawker vs restaurant estimate
            per_dish = amount / 3 if amount >= 6 else amount / 2
            return random.choice(EnhancedResponses.RESPONSE_PATTERNS['hawker']).format(
                saved_vs_restaurant=saved_vs_restaurant,
                per_dish=per_dish,
                amount=amount
            )
        
        elif 'grab' in category_lower or 'transport' in category_lower:
            bus_cost = 1.47
            mrt_cost = 1.65
            savings = amount - mrt_cost
            return random.choice(EnhancedResponses.RESPONSE_PATTERNS['grab']).format(
                amount=amount,
                bus_cost=bus_cost,
                mrt_cost=mrt_cost,
                savings=savings
            )
        
        elif 'kopi' in category_lower or 'coffee' in category_lower:
            return random.choice(EnhancedResponses.RESPONSE_PATTERNS['kopi']).format(amount=amount)
        
        elif 'bubble' in category_lower or 'tea' in category_lower:
            return random.choice(EnhancedResponses.RESPONSE_PATTERNS['bubble_tea']).format(amount=amount)
        
        elif 'transport' in category_lower:
            return random.choice(EnhancedResponses.RESPONSE_PATTERNS['transport']).format(amount=amount)
        
        else:
            return random.choice(EnhancedResponses.RESPONSE_PATTERNS['food']).format(amount=amount)
    
    @staticmethod
    def _get_achievement_response(amount: float, category: str, daily_total: float) -> str:
        """Get achievement-based response"""
        # This would integrate with user achievement tracking
        # For now, return basic achievements
        if daily_total == amount:  # First expense of day
            return random.choice(EnhancedResponses.ACHIEVEMENT_RESPONSES['first_expense_day'])
        
        # Check for budget achievements (would need user budget data)
        if amount <= 5 and 'food' in category.lower():
            return random.choice(EnhancedResponses.ACHIEVEMENT_RESPONSES['hawker_choice'])
        
        return None
    
    @staticmethod
    def _get_time_based_response(amount: float, time_context: str) -> str:
        """Get time-based contextual response"""
        if time_context in EnhancedResponses.TIME_RESPONSES:
            time_str = datetime.now().strftime("%I:%M %p")
            return random.choice(EnhancedResponses.TIME_RESPONSES[time_context]).format(
                amount=amount,
                time=time_str
            )
        return None
    
    @staticmethod
    def _get_daily_context(daily_total: float, current_amount: float) -> str:
        """Get daily spending context"""
        if daily_total <= 15:
            return f"Today's total: ${daily_total:.2f} 💰 You're having a budget-friendly day!"
        elif daily_total <= 25:
            return f"Today's total: ${daily_total:.2f} 💰 Moderate spending - staying on track!"
        elif daily_total <= 40:
            return f"Today's total: ${daily_total:.2f} 💰 Active day! Consider tomorrow's budget."
        else:
            return f"Today's total: ${daily_total:.2f} 💰 High spending day - maybe slow down tomorrow?"
    
    @staticmethod
    def _get_smart_tip(amount: float, category: str, daily_total: float) -> str:
        """Get contextual smart tip"""
        category_lower = category.lower()
        
        if 'transport' in category_lower and amount > 15:
            return "Consider MRT/bus for regular routes to save money! 🚌"
        
        elif 'food' in category_lower and amount > 12:
            return "Hawker centers offer great value! Try them next time! 🍜"
        
        elif daily_total > 30:
            return "You're spending actively today. Consider setting a daily budget! 💡"
        
        elif amount <= 5:
            return "Great value choice! Small amounts add up to big savings! 💰"
        
        return None
    
    # =============================================================================
    # LEGACY SUPPORT - Keep existing response methods
    # =============================================================================
    
    @staticmethod
    def get_expense_response(amount: float, category: str, daily_total: float = 0, 
                           original_text: str = "") -> str:
        """Legacy method - now uses enhanced smart response"""
        return EnhancedResponses.build_smart_response(amount, category, daily_total, original_text)
    
    @staticmethod
    def get_random_response(category: str, **kwargs) -> str:
        """Get random response from legacy categories"""
        # Map legacy categories to new system
        if category == "expense_logged":
            return f"Got it! ${kwargs.get('amount', '0')} for {kwargs.get('category', 'expense')}. Very good lah! 👍"
        elif category == "error_messages":
            return "Alamak! Something went wrong lah. Try again? 😅"
        else:
            return "Response not found. Try again lah! 😊"

