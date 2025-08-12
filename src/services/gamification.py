"""
Gamification Service for SG Money Buddy
Tracks achievements, streaks, and provides dopamine hits for consistent behavior!
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class Achievement:
    """Achievement data structure"""
    id: str
    name: str
    description: str
    emoji: str
    unlocked: bool
    unlocked_date: Optional[datetime]
    progress: float  # 0.0 to 1.0
    target: int
    current: int

@dataclass
class Streak:
    """Streak tracking data structure"""
    type: str
    current: int
    best: int
    last_date: datetime
    is_active: bool

class GamificationService:
    """Core gamification service for user engagement"""
    
    # =============================================================================
    # ACHIEVEMENT DEFINITIONS - Singapore context achievements
    # =============================================================================
    
    ACHIEVEMENTS = {
        'first_expense': {
            'name': 'First Steps',
            'description': 'Log your first expense',
            'emoji': '👶',
            'target': 1
        },
        'daily_logger_3': {
            'name': 'Habit Builder',
            'description': 'Log expenses for 3 consecutive days',
            'emoji': '🏗️',
            'target': 3
        },
        'daily_logger_7': {
            'name': 'Week Warrior',
            'description': 'Log expenses for 7 consecutive days',
            'emoji': '🏆',
            'target': 7
        },
        'daily_logger_30': {
            'name': 'Month Master',
            'description': 'Log expenses for 30 consecutive days',
            'emoji': '👑',
            'target': 30
        },
        'hawker_master': {
            'name': 'Hawker Champion',
            'description': 'Choose hawker over restaurant 10 times',
            'emoji': '🍜',
            'target': 10
        },
        'transport_saver': {
            'name': 'Transport Ninja',
            'description': 'Use public transport 20 times',
            'emoji': '🚌',
            'target': 20
        },
        'budget_keeper': {
            'name': 'Budget Master',
            'emoji': '💰',
            'description': 'Stay under daily budget 5 times',
            'target': 5
        },
        'early_bird': {
            'name': 'Early Bird',
            'description': 'Log first expense before 9 AM for 5 days',
            'emoji': '🌅',
            'target': 5
        },
        'night_owl': {
            'name': 'Night Owl',
            'description': 'Log expenses after 10 PM for 3 days',
            'emoji': '🦉',
            'target': 3
        },
        'value_hunter': {
            'name': 'Value Hunter',
            'description': 'Log 20 expenses under $5',
            'emoji': '🔍',
            'target': 20
        },
        'weekend_warrior': {
            'name': 'Weekend Warrior',
            'description': 'Log expenses every weekend for 4 weeks',
            'emoji': '🎉',
            'target': 4
        },
        'singapore_explorer': {
            'name': 'Singapore Explorer',
            'description': 'Log expenses in 5 different areas',
            'emoji': '🗺️',
            'target': 5
        }
    }
    
    # =============================================================================
    # STREAK TYPES - Different types of streaks to track
    # =============================================================================
    
    STREAK_TYPES = {
        'daily_logging': 'Daily expense logging',
        'budget_adherence': 'Staying under budget',
        'hawker_choices': 'Choosing hawker over restaurant',
        'public_transport': 'Using public transport',
        'early_logging': 'Logging first expense early',
        'weekend_logging': 'Weekend expense logging'
    }
    
    # =============================================================================
    # CORE GAMIFICATION METHODS
    # =============================================================================
    
    def __init__(self, user_id: int):
        """Initialize gamification service for a user"""
        self.user_id = user_id
        self.achievements: Dict[str, Achievement] = {}
        self.streaks: Dict[str, Streak] = {}
        self._load_user_data()
    
    def _load_user_data(self):
        """Load user's achievement and streak data"""
        # TODO: Load from database
        # For now, initialize with default values
        for achievement_id, achievement_data in self.ACHIEVEMENTS.items():
            self.achievements[achievement_id] = Achievement(
                id=achievement_id,
                name=achievement_data['name'],
                description=achievement_data['description'],
                emoji=achievement_data['emoji'],
                unlocked=False,
                unlocked_date=None,
                progress=0.0,
                target=achievement_data['target'],
                current=0
            )
        
        # Initialize streaks
        for streak_type in self.STREAK_TYPES:
            self.streaks[streak_type] = Streak(
                type=streak_type,
                current=0,
                best=0,
                last_date=datetime.now(),
                is_active=False
            )
    
    async def process_expense(self, amount: float, category: str, 
                            timestamp: datetime = None) -> List[str]:
        """Process a new expense and return any achievements unlocked"""
        if timestamp is None:
            timestamp = datetime.now()
        
        unlocked_achievements = []
        
        # Update basic achievements
        unlocked = await self._update_basic_achievements(amount, category, timestamp)
        unlocked_achievements.extend(unlocked)
        
        # Update streaks
        await self._update_streaks(amount, category, timestamp)
        
        # Check for streak-based achievements
        streak_achievements = await self._check_streak_achievements()
        unlocked_achievements.extend(streak_achievements)
        
        return unlocked_achievements
    
    async def _update_basic_achievements(self, amount: float, category: str, 
                                       timestamp: datetime) -> List[str]:
        """Update basic achievements based on expense"""
        unlocked = []
        
        # First expense achievement
        if not self.achievements['first_expense'].unlocked:
            self.achievements['first_expense'].unlocked = True
            self.achievements['first_expense'].unlocked_date = timestamp
            unlocked.append('first_expense')
        
        # Value hunter achievement
        if amount <= 5:
            value_hunter = self.achievements['value_hunter']
            value_hunter.current += 1
            value_hunter.progress = min(1.0, value_hunter.current / value_hunter.target)
            
            if value_hunter.current >= value_hunter.target and not value_hunter.unlocked:
                value_hunter.unlocked = True
                value_hunter.unlocked_date = timestamp
                unlocked.append('value_hunter')
        
        # Hawker master achievement
        if category.lower() == 'food' and amount <= 8:
            hawker_master = self.achievements['hawker_master']
            hawker_master.current += 1
            hawker_master.progress = min(1.0, hawker_master.current / hawker_master.target)
            
            if hawker_master.current >= hawker_master.target and not hawker_master.unlocked:
                hawker_master.unlocked = True
                hawker_master.unlocked_date = timestamp
                unlocked.append('hawker_master')
        
        # Transport saver achievement
        if category.lower() == 'transport' and amount <= 3:
            transport_saver = self.achievements['transport_saver']
            transport_saver.current += 1
            transport_saver.progress = min(1.0, transport_saver.current / transport_saver.target)
            
            if transport_saver.current >= transport_saver.target and not transport_saver.unlocked:
                transport_saver.unlocked = True
                transport_saver.unlocked_date = timestamp
                unlocked.append('transport_saver')
        
        # Early bird achievement
        if timestamp.hour < 9:
            early_bird = self.achievements['early_bird']
            early_bird.current += 1
            early_bird.progress = min(1.0, early_bird.current / early_bird.target)
            
            if early_bird.current >= early_bird.target and not early_bird.unlocked:
                early_bird.unlocked = True
                early_bird.unlocked_date = timestamp
                unlocked.append('early_bird')
        
        # Night owl achievement
        if timestamp.hour >= 22:
            night_owl = self.achievements['night_owl']
            night_owl.current += 1
            night_owl.progress = min(1.0, night_owl.current / night_owl.target)
            
            if night_owl.current >= night_owl.target and not night_owl.unlocked:
                night_owl.unlocked = True
                night_owl.unlocked_date = timestamp
                unlocked.append('night_owl')
        
        return unlocked
    
    async def _update_streaks(self, amount: float, category: str, timestamp: datetime):
        """Update various streaks based on expense"""
        today = timestamp.date()
        
        # Daily logging streak
        await self._update_daily_logging_streak(today)
        
        # Hawker choices streak
        if category.lower() == 'food' and amount <= 8:
            await self._update_hawker_streak(today)
        
        # Public transport streak
        if category.lower() == 'transport' and amount <= 3:
            await self._update_public_transport_streak(today)
        
        # Early logging streak
        if timestamp.hour < 9:
            await self._update_early_logging_streak(today)
        
        # Weekend logging streak
        if timestamp.weekday() >= 5:  # Saturday = 5, Sunday = 6
            await self._update_weekend_streak(today)
    
    async def _update_daily_logging_streak(self, today: datetime.date):
        """Update daily logging streak"""
        streak = self.streaks['daily_logging']
        
        if not streak.is_active:
            streak.current = 1
            streak.is_active = True
        else:
            days_diff = (today - streak.last_date.date()).days
            
            if days_diff == 1:  # Consecutive day
                streak.current += 1
            elif days_diff == 0:  # Same day, multiple expenses
                pass  # Keep current streak
            else:  # Streak broken
                streak.current = 1
        
        streak.last_date = datetime.combine(today, datetime.min.time())
        streak.best = max(streak.best, streak.current)
    
    async def _update_hawker_streak(self, today: datetime.date):
        """Update hawker choices streak"""
        streak = self.streaks['hawker_choices']
        
        if not streak.is_active:
            streak.current = 1
            streak.is_active = True
        else:
            days_diff = (today - streak.last_date.date()).days
            
            if days_diff == 1:  # Consecutive day
                streak.current += 1
            elif days_diff == 0:  # Same day, multiple hawker choices
                pass  # Keep current streak
            else:  # Streak broken
                streak.current = 1
        
        streak.last_date = datetime.combine(today, datetime.min.time())
        streak.best = max(streak.best, streak.current)
    
    async def _update_public_transport_streak(self, today: datetime.date):
        """Update public transport streak"""
        streak = self.streaks['public_transport']
        
        if not streak.is_active:
            streak.current = 1
            streak.is_active = True
        else:
            days_diff = (today - streak.last_date.date()).days
            
            if days_diff == 1:  # Consecutive day
                streak.current += 1
            elif days_diff == 0:  # Same day, multiple transport uses
                pass  # Keep current streak
            else:  # Streak broken
                streak.current = 1
        
        streak.last_date = datetime.combine(today, datetime.min.time())
        streak.best = max(streak.best, streak.current)
    
    async def _update_early_logging_streak(self, today: datetime.date):
        """Update early logging streak"""
        streak = self.streaks['early_logging']
        
        if not streak.is_active:
            streak.current = 1
            streak.is_active = True
        else:
            days_diff = (today - streak.last_date.date()).days
            
            if days_diff == 1:  # Consecutive day
                streak.current += 1
            elif days_diff == 0:  # Same day, multiple early logs
                pass  # Keep current streak
            else:  # Streak broken
                streak.current = 1
        
        streak.last_date = datetime.combine(today, datetime.min.time())
        streak.best = max(streak.best, streak.current)
    
    async def _update_weekend_streak(self, today: datetime.date):
        """Update weekend logging streak"""
        streak = self.streaks['weekend_logging']
        
        if not streak.is_active:
            streak.current = 1
            streak.is_active = True
        else:
            # Check if this is the next weekend
            days_diff = (today - streak.last_date.date()).days
            
            if days_diff >= 7:  # Next weekend
                streak.current += 1
            elif days_diff < 7 and today.weekday() >= 5:  # Same weekend
                pass  # Keep current streak
            else:  # Streak broken
                streak.current = 1
        
        streak.last_date = datetime.combine(today, datetime.min.time())
        streak.best = max(streak.best, streak.current)
    
    async def _check_streak_achievements(self) -> List[str]:
        """Check if any streak-based achievements should be unlocked"""
        unlocked = []
        
        # Daily logging achievements
        daily_streak = self.streaks['daily_logging']
        
        if daily_streak.current >= 3 and not self.achievements['daily_logger_3'].unlocked:
            self.achievements['daily_logger_3'].unlocked = True
            self.achievements['daily_logger_3'].unlocked_date = datetime.now()
            unlocked.append('daily_logger_3')
        
        if daily_streak.current >= 7 and not self.achievements['daily_logger_7'].unlocked:
            self.achievements['daily_logger_7'].unlocked = True
            self.achievements['daily_logger_7'].unlocked_date = datetime.now()
            unlocked.append('daily_logger_7')
        
        if daily_streak.current >= 30 and not self.achievements['daily_logger_30'].unlocked:
            self.achievements['daily_logger_30'].unlocked = True
            self.achievements['daily_logger_30'].unlocked_date = datetime.now()
            unlocked.append('daily_logger_30')
        
        return unlocked
    
    # =============================================================================
    # ACHIEVEMENT QUERY METHODS
    # =============================================================================
    
    def get_unlocked_achievements(self) -> List[Achievement]:
        """Get list of unlocked achievements"""
        return [achievement for achievement in self.achievements.values() 
                if achievement.unlocked]
    
    def get_locked_achievements(self) -> List[Achievement]:
        """Get list of locked achievements"""
        return [achievement for achievement in self.achievements.values() 
                if not achievement.unlocked]
    
    def get_achievement_progress(self) -> Dict[str, float]:
        """Get progress for all achievements"""
        return {achievement.id: achievement.progress 
                for achievement in self.achievements.values()}
    
    def get_streak_summary(self) -> Dict[str, Streak]:
        """Get summary of all streaks"""
        return self.streaks.copy()
    
    def get_total_achievements(self) -> int:
        """Get total number of achievements"""
        return len(self.ACHIEVEMENTS)
    
    def get_unlocked_count(self) -> int:
        """Get count of unlocked achievements"""
        return len(self.get_unlocked_achievements())
    
    def get_completion_percentage(self) -> float:
        """Get percentage of achievements completed"""
        if self.get_total_achievements() == 0:
            return 0.0
        return (self.get_unlocked_count() / self.get_total_achievements()) * 100
    
    # =============================================================================
    # ENGAGEMENT METHODS - For daily touchpoints
    # =============================================================================
    
    def get_daily_motivation(self) -> str:
        """Get daily motivation message based on user's progress"""
        unlocked_count = self.get_unlocked_count()
        total_count = self.get_total_achievements()
        
        if unlocked_count == 0:
            return "🌱 Ready to start your money tracking journey? Let's log your first expense!"
        elif unlocked_count <= total_count * 0.25:
            return f"🚀 Great start! You've unlocked {unlocked_count} achievements. Keep going!"
        elif unlocked_count <= total_count * 0.5:
            return f"🔥 You're on fire! {unlocked_count} achievements unlocked. Halfway there!"
        elif unlocked_count <= total_count * 0.75:
            return f"💪 Almost there! {unlocked_count} achievements. You're a money master!"
        else:
            return f"👑 Legendary! {unlocked_count}/{total_count} achievements. You're unstoppable!"
    
    def get_streak_encouragement(self) -> str:
        """Get encouragement based on current streaks"""
        active_streaks = [streak for streak in self.streaks.values() if streak.is_active]
        
        if not active_streaks:
            return "💡 Start a new streak today! Log an expense to begin!"
        
        best_streak = max(active_streaks, key=lambda s: s.current)
        
        if best_streak.current >= 7:
            return f"🔥 {best_streak.current} day streak! You're unstoppable! 💪"
        elif best_streak.current >= 3:
            return f"🏆 {best_streak.current} day streak! Keep the momentum going! 🚀"
        else:
            return f"🌱 {best_streak.current} day streak! Every day counts! 💪"
    
    def get_next_achievement_hint(self) -> Optional[str]:
        """Get hint about next achievable achievement"""
        locked_achievements = self.get_locked_achievements()
        
        if not locked_achievements:
            return "🎉 All achievements unlocked! You're a legend!"
        
        # Find closest to completion
        closest = min(locked_achievements, key=lambda a: a.target - a.current)
        
        if closest.current > 0:
            remaining = closest.target - closest.current
            return f"🎯 Next up: {closest.name} ({remaining} more to go!)"
        else:
            return f"🎯 Try: {closest.name} - {closest.description}"
