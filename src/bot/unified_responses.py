"""
Unified BaoJiak Response System - Combining technical responses with companion personality
"""

import random
from datetime import datetime
from typing import List, Dict, Any, Optional

class BaoJiakResponses:
    """Unified response system with companion personality + technical accuracy"""
    
    # =============================================================================
    # WELCOME & ONBOARDING - Warm and inviting
    # =============================================================================
    
    WELCOME_MESSAGES = [
        "Wah! Welcome to BaoJiak lah! I'm your money tracking kakis! 🇸🇬💰\nReady to save money together?",
        "Eh hello there! I'm BaoJiak, your personal finance buddy! 🤗\nLet's make your money stretch further leh!",
        "Welcome welcome! I'm here to help you track spending and save money! 😊\nWhat you want to tell me today?",
        "Yo! BaoJiak here! Your friendly neighborhood money tracker! 💪\nReady to become money-smart together?"
    ]
    
    # =============================================================================
    # EXPENSE RESPONSES - Based on amount with personality
    # =============================================================================
    
    @staticmethod
    def get_expense_response(amount: float, category: str = "others") -> str:
        """Get personalized expense response based on amount"""
        
        if amount <= 2:
            responses = [
                f"Wah only ${amount}? You damn thrifty leh! Teach me! 😄💪",
                f"${amount} only?! You sure you ate enough? So cheap! 🤔",
                f"Eh ${amount} very reasonable! You know how to save! 👍"
            ]
        elif amount <= 5:
            responses = [
                f"${amount} not bad lah! Normal normal! 😊",
                f"Okay ${amount} quite reasonable for {category}! 👌",
                f"${amount} sounds about right! You doing good! ✅"
            ]
        elif amount <= 10:
            responses = [
                f"${amount} ah... okay lah, not too bad! 😐",
                f"${amount} for {category}... can accept lah! 💸",
                f"${amount}... hmm quite standard price nowadays! 📈"
            ]
        elif amount <= 20:
            responses = [
                f"Wah ${amount}! Quite ex leh! But okay if you happy! 😅💸",
                f"${amount}?! Your wallet feeling it! Hope worth it ah! 💔",
                f"Alamak ${amount}! Must be very nice {category}! 😬"
            ]
        else:
            responses = [
                f"ALAMAK ${amount}?! Bro/sis you okay?! So expensive! 😱💸💸",
                f"${amount}... wah... I speechless... your wallet RIP... 💀💰",
                f"Eh ${amount} very the ex leh! You sure you never kena con? 🤯"
            ]
        
        return random.choice(responses)
    
    # =============================================================================
    # ENCOURAGEMENT & EMOTIONAL RESPONSES
    # =============================================================================
    
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
    
    # =============================================================================
    # PATIENCE & UNDERSTANDING - For confused users
    # =============================================================================
    
    PATIENCE_RESPONSES = [
        "Eh don't worry lah! I very patient one! Try again slowly! 😊",
        "No problem! Even my ah ma also blur sometimes! Tell me again? 🤗",
        "It's okay! Take your time! I wait for you! ⏰",
        "Alamak! I also blur sometimes! Can repeat? No rush! 😅",
        "Don't stress! We learn together! Try once more? 💪"
    ]
    
    # =============================================================================
    # BUDGET RESPONSES - Caring but not naggy
    # =============================================================================
    
    BUDGET_WARNINGS = [
        "Eh! You spent ${amount} already. Maybe cut down a bit? 😅",
        "Alamak! {percentage}% of budget used for {category}. Careful leh! ⚠️",
        "Wah quite a lot spent on {category} already. Take it easy! 🙈",
        "Bro/sis, I worry about your {category} spending... maybe slow down? 💔"
    ]
    
    BUDGET_SUCCESS = [
        "Wah! Still within budget! You very disciplined! 🌟",
        "Good job staying within {category} budget! Keep it up! 👍",
        "Your budget control very steady! I'm impressed! 😄"
    ]
    
    # =============================================================================
    # DEAL ALERTS - Excited sharing
    # =============================================================================
    
    DEAL_ALERTS = [
        "Wah shiok! Found this deal for you! 🔥",
        "Eh got lobang! Check out this promotion! 💰",
        "Steady lah! This deal confirm plus chop good! ⭐",
        "Eh psst! I found good deal for you! Don't tell others! 🤫"
    ]
    
    # =============================================================================
    # ERROR HANDLING - Friendly and forgiving
    # =============================================================================
    
    ERROR_MESSAGES = [
        "Alamak! Something went wrong lah. Try again? 😅",
        "Eh sorry ah, got some problem. Can try once more? 🙏",
        "Aiyo! System a bit lag. Please wait and try again!",
        "Eh blur blur now! Give me a moment to think! 🤔"
    ]
    
    # =============================================================================
    # HELP & GUIDANCE - Patient teacher
    # =============================================================================
    
    HELP_MESSAGES = [
        "No worries! Just tell me simple simple:\n• 'lunch 5' (what + how much)\n• '3.50' (just amount)\n• 'spent 10' (also can!)",
        "Very easy one! Just type what you spend:\n• 'coffee 3'\n• 'bus 2'\n• 'makan 5'\nI understand everything!",
        "Don't stress! I very flexible:\n• 'lunch $5' ✅\n• 'eat 5 dollar' ✅\n• 'spend 5' ✅\nAll also can!"
    ]
    
    # =============================================================================
    # MOOD DETECTION & RESPONSES
    # =============================================================================
    
    @staticmethod
    def react_to_user_mood(text: str) -> Optional[str]:
        """React to user's mood based on their message"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['sad', 'sian', 'tired', 'stress', 'headache']):
            return random.choice([
                "Eh you okay? Don't sad sad... money not everything! 🤗💕",
                "Aiyo why you sian? Come I cheer you up! You're doing great! 😊✨",
                "Stress ah? Don't worry, we handle money together! I help you! 🤝",
                "Tired ah? Rest first, money tracking can wait! Health important! 💤❤️"
            ])
        
        elif any(word in text_lower for word in ['happy', 'good', 'great', 'shiok', 'nice']):
            return random.choice([
                "Wah you sound happy! I also happy! Good mood save more money! 😄💰",
                "Shiok! When you happy, I also happy! Let's celebrate! 🎉",
                "Good mood very important! Happy people make better money decisions! 😊✨",
                "Your happiness is contagious! I feel so energetic now! ⚡😄"
            ])
        
        elif any(word in text_lower for word in ['angry', 'mad', 'pissed', 'cb', 'wtf']):
            return random.choice([
                "Eh eh calm down! Don't angry! Deep breath... I'm here for you! 😮‍💨🤗",
                "Wah you very angry ah? What happened? Tell me lah! 😟",
                "Don't be mad! Whatever happen, we solve together! 💪🤝",
                "Angry spending very dangerous! Let's cool down first okay? 🧊😌"
            ])
        
        return None
    
    # =============================================================================
    # UTILITY FUNCTIONS
    # =============================================================================
    
    @staticmethod
    def get_random_response(category: str, **kwargs) -> str:
        """Get a random response from a category"""
        category_upper = category.upper()
        responses = getattr(BaoJiakResponses, category_upper, [])
        
        if not responses:
            return "Sorry, no response available lah! 😅"
        
        message = random.choice(responses)
        try:
            return message.format(**kwargs)
        except:
            return message
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format amount in Singapore dollars"""
        return f"${amount:.2f}"
    
    @staticmethod
    def add_singlish_emphasis(message: str, intensity: str = "mild") -> str:
        """Add Singlish particles for emphasis"""
        particles = {
            "mild": ["lah", "leh", "lor"],
            "medium": ["lah", "leh", "lor", "mah", "what"],
            "strong": ["lah", "leh", "lor", "mah", "what", "sia", "hor"]
        }
        
        particle = random.choice(particles.get(intensity, particles["mild"]))
        return f"{message} {particle}!"
    
    @staticmethod
    def get_daily_mood() -> str:
        """Get BaoJiak's mood for the day"""
        day = datetime.now().day
        moods = [
            "I feeling very energetic today! Ready to help you save money! ⚡",
            "Today I quite relaxed... let's take it easy with spending! 😌",
            "Wah I excited today! Got feeling you will save a lot! 🎉",
            "Today I feeling wise... let me give you good advice! 🧙‍♂️",
            "I bit sleepy today but still here for you! Coffee first! ☕😴"
        ]
        return moods[day % len(moods)]
    
    @staticmethod
    def get_time_based_greeting() -> str:
        """Get greeting based on time of day"""
        hour = datetime.now().hour
        
        if hour < 12:
            return random.choice([
                "Eh good morning! Had breakfast already? 🌅",
                "Morning lah! Ready to jiak and track spending today? ☕",
                "Wah early bird! What you eating for breakfast? 🥐"
            ])
        elif hour < 18:
            return random.choice([
                "Afternoon! Lunch time already? What you having? 🍜",
                "Eh bro/sis! How's your day going? Spent a lot today? 😄",
                "Yo! Feeling hungry? Tell me what you eating! 🍛"
            ])
        else:
            return random.choice([
                "Evening! Dinner plans? Don't forget to tell me! 🌆",
                "Eh good evening! How much you spent today ah? 🌙",
                "Night time liao! What you having for dinner? 🍲"
            ])
    
    # =============================================================================
    # SMART RESPONSE BUILDER
    # =============================================================================
    
    @staticmethod
    def build_smart_response(expense_amount: float, category: str, daily_total: float = 0, user_mood: str = "") -> str:
        """Build a smart response combining multiple elements"""
        
        # Start with expense response
        response = BaoJiakResponses.get_expense_response(expense_amount, category)
        
        # Add daily spending context
        if daily_total > 50:
            response += "\n\nEh bro/sis, you spent quite a lot today already leh! Maybe take it easy? 😟"
        elif daily_total > 30:
            response += "\n\nToday's spending getting up there! Watch out ah! 👀"
        elif daily_total < 10:
            response += "\n\nWah you very disciplined today! Keep it up! 🌟"
        
        # React to mood if detected
        mood_response = BaoJiakResponses.react_to_user_mood(user_mood)
        if mood_response:
            response += f"\n\n{mood_response}"
        
        # Add encouragement randomly (30% chance)
        if random.random() < 0.3:
            response += f"\n\n{random.choice(BaoJiakResponses.ENCOURAGEMENT)}"
        
        return response

# =============================================================================
# BACKWARD COMPATIBILITY - For existing code
# =============================================================================

class SingaporeResponses:
    """Backward compatibility wrapper"""
    
    @staticmethod
    def get_random_response(category: str, **kwargs) -> str:
        return BaoJiakResponses.get_random_response(category, **kwargs)
    
    @staticmethod
    def format_currency(amount: float) -> str:
        return BaoJiakResponses.format_currency(amount)
    
    @staticmethod
    def add_singlish_emphasis(message: str, intensity: str = "mild") -> str:
        return BaoJiakResponses.add_singlish_emphasis(message, intensity)

# Test the unified system
if __name__ == "__main__":
    print("=== BaoJiak Unified Response System Test ===")
    print(f"Welcome: {BaoJiakResponses.get_random_response('welcome_messages')}")
    print(f"Expense $5: {BaoJiakResponses.get_expense_response(5, 'food')}")
    print(f"Expense $25: {BaoJiakResponses.get_expense_response(25, 'transport')}")
    print(f"Daily mood: {BaoJiakResponses.get_daily_mood()}")
    print(f"Time greeting: {BaoJiakResponses.get_time_based_greeting()}")
    print(f"Smart response: {BaoJiakResponses.build_smart_response(8, 'food', 23, 'happy')}")

