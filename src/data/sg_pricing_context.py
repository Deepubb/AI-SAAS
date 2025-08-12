"""
Singapore Pricing Intelligence System
Provides context-aware pricing insights and validation for local spending patterns
"""

from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from datetime import datetime, time
import random

@dataclass
class PriceRange:
    """Price range for Singapore context"""
    min_price: float
    max_price: float
    typical_price: float
    description: str
    area_multiplier: float = 1.0

@dataclass
class LocationContext:
    """Location-based pricing context"""
    area_name: str
    multiplier: float
    description: str
    typical_categories: List[str]

class SingaporePricingIntelligence:
    """Singapore-specific pricing intelligence and validation"""
    
    # =============================================================================
    # SINGAPORE PRICING DATABASE - Realistic local pricing
    # =============================================================================
    
    HAWKER_PRICES = {
        "chicken_rice": PriceRange(3.0, 5.5, 4.0, "Chicken rice - hawker staple"),
        "laksa": PriceRange(4.0, 6.0, 5.0, "Laksa - spicy noodle soup"),
        "char_kway_teow": PriceRange(3.5, 5.5, 4.5, "Char kway teow - wok-fried noodles"),
        "nasi_lemak": PriceRange(2.5, 4.5, 3.5, "Nasi lemak - coconut rice"),
        "roti_prata": PriceRange(1.0, 2.5, 1.8, "Roti prata - flatbread"),
        "mee_goreng": PriceRange(3.0, 5.0, 4.0, "Mee goreng - fried noodles"),
        "fishball_noodles": PriceRange(3.0, 4.5, 3.8, "Fishball noodles"),
        "bak_kut_teh": PriceRange(6.0, 9.0, 7.5, "Bak kut teh - pork rib soup"),
        "dim_sum": PriceRange(2.5, 4.0, 3.2, "Dim sum - small bites"),
        "kopi": PriceRange(1.2, 2.0, 1.6, "Kopi - local coffee"),
        "teh_tarik": PriceRange(1.2, 2.0, 1.6, "Teh tarik - pulled tea"),
        "bubble_tea": PriceRange(3.5, 6.0, 4.8, "Bubble tea - sweet drink")
    }
    
    RESTAURANT_PRICES = {
        "casual_dining": PriceRange(12.0, 25.0, 18.0, "Casual restaurant meal"),
        "mid_range": PriceRange(25.0, 45.0, 35.0, "Mid-range restaurant"),
        "fine_dining": PriceRange(45.0, 120.0, 80.0, "Fine dining experience"),
        "fast_food": PriceRange(8.0, 15.0, 12.0, "Fast food chain"),
        "cafe": PriceRange(15.0, 30.0, 22.0, "Cafe dining"),
        "food_court": PriceRange(6.0, 12.0, 9.0, "Food court meal")
    }
    
    TRANSPORT_COSTS = {
        "bus": PriceRange(1.47, 2.37, 1.92, "Bus fare"),
        "mrt_short": PriceRange(1.65, 2.15, 1.90, "Short MRT journey"),
        "mrt_medium": PriceRange(2.15, 2.85, 2.50, "Medium MRT journey"),
        "mrt_long": PriceRange(2.85, 3.45, 3.15, "Long MRT journey"),
        "grab_short": PriceRange(8.0, 15.0, 11.5, "Short Grab ride"),
        "grab_medium": PriceRange(15.0, 25.0, 20.0, "Medium Grab ride"),
        "grab_long": PriceRange(25.0, 45.0, 35.0, "Long Grab ride"),
        "taxi_meter": PriceRange(3.90, 25.0, 14.5, "Taxi meter fare"),
        "bicycle_rental": PriceRange(1.0, 3.0, 2.0, "Bicycle rental")
    }
    
    SHOPPING_PRICES = {
        "groceries": PriceRange(15.0, 80.0, 45.0, "Grocery shopping"),
        "clothing": PriceRange(25.0, 150.0, 87.5, "Clothing item"),
        "electronics": PriceRange(50.0, 500.0, 275.0, "Electronics"),
        "books": PriceRange(15.0, 45.0, 30.0, "Books"),
        "cosmetics": PriceRange(8.0, 50.0, 29.0, "Cosmetics"),
        "pharmacy": PriceRange(5.0, 30.0, 17.5, "Pharmacy items")
    }
    
    ENTERTAINMENT_PRICES = {
        "movie_ticket": PriceRange(8.0, 15.0, 11.5, "Movie ticket"),
        "concert": PriceRange(50.0, 200.0, 125.0, "Concert ticket"),
        "museum": PriceRange(5.0, 25.0, 15.0, "Museum entry"),
        "theme_park": PriceRange(60.0, 120.0, 90.0, "Theme park entry"),
        "bowling": PriceRange(15.0, 30.0, 22.5, "Bowling game"),
        "karaoke": PriceRange(20.0, 50.0, 35.0, "Karaoke session")
    }
    
    # =============================================================================
    # LOCATION-BASED PRICING MULTIPLIERS
    # =============================================================================
    
    LOCATION_MULTIPLIERS = {
        "cbd": LocationContext("CBD", 1.4, "Central Business District - premium pricing", 
                              ["restaurants", "cafes", "shopping"]),
        "orchard": LocationContext("Orchard", 1.6, "Shopping district - tourist pricing", 
                                  ["shopping", "restaurants", "entertainment"]),
        "marina_bay": LocationContext("Marina Bay", 1.8, "Tourist area - premium pricing", 
                                     ["restaurants", "entertainment", "hotels"]),
        "sentosa": LocationContext("Sentosa", 1.5, "Island resort - tourist pricing", 
                                  ["entertainment", "restaurants", "activities"]),
        "heartland": LocationContext("Heartland", 0.9, "Residential areas - local pricing", 
                                    ["hawker", "groceries", "daily_needs"]),
        "suburban": LocationContext("Suburban", 1.0, "Suburban areas - standard pricing", 
                                   ["mixed", "balanced"]),
        "airport": LocationContext("Airport", 1.3, "Airport - convenience pricing", 
                                  ["food", "shopping", "services"]),
        "university": LocationContext("University", 0.8, "University areas - student pricing", 
                                     ["food", "entertainment", "services"])
    }
    
    # =============================================================================
    # TIME-BASED PRICING FACTORS
    # =============================================================================
    
    TIME_MULTIPLIERS = {
        "peak_hours": {
            "breakfast": (time(7, 0), time(9, 0), 1.1, "Breakfast rush"),
            "lunch": (time(12, 0), time(14, 0), 1.2, "Lunch rush"),
            "dinner": (time(18, 0), time(20, 0), 1.15, "Dinner rush"),
            "late_night": (time(22, 0), time(6, 0), 1.25, "Late night premium")
        },
        "weekend_multiplier": 1.1,
        "public_holiday_multiplier": 1.2
    }
    
    # =============================================================================
    # CORE PRICING INTELLIGENCE METHODS
    # =============================================================================
    
    @staticmethod
    def validate_price(amount: float, category: str, subcategory: str = None, 
                      location: str = None, timestamp: datetime = None) -> Dict:
        """Validate if a price is reasonable for Singapore context"""
        
        # Get base price range
        base_range = SingaporePricingIntelligence._get_price_range(category, subcategory)
        if not base_range:
            return {
                "is_reasonable": True,
                "confidence": "low",
                "message": "Price validation not available for this category",
                "suggestions": []
            }
        
        # Apply location multiplier
        location_multiplier = SingaporePricingIntelligence._get_location_multiplier(location)
        adjusted_min = base_range.min_price * location_multiplier
        adjusted_max = base_range.max_price * location_multiplier
        
        # Apply time-based factors
        time_multiplier = SingaporePricingIntelligence._get_time_multiplier(timestamp)
        adjusted_min *= time_multiplier
        adjusted_max *= time_multiplier
        
        # Validate price
        is_reasonable = adjusted_min <= amount <= adjusted_max
        confidence = SingaporePricingIntelligence._calculate_confidence(amount, adjusted_min, adjusted_max)
        
        # Generate suggestions
        suggestions = SingaporePricingIntelligence._generate_suggestions(
            amount, category, subcategory, adjusted_min, adjusted_max, location
        )
        
        # Generate response message
        message = SingaporePricingIntelligence._generate_validation_message(
            amount, is_reasonable, adjusted_min, adjusted_max, category, location
        )
        
        return {
            "is_reasonable": is_reasonable,
            "confidence": confidence,
            "message": message,
            "suggestions": suggestions,
            "price_range": {
                "min": adjusted_min,
                "max": adjusted_max,
                "typical": base_range.typical_price * location_multiplier * time_multiplier
            },
            "location_context": location,
            "time_context": timestamp
        }
    
    @staticmethod
    def get_price_insights(amount: float, category: str, subcategory: str = None,
                          location: str = None) -> Dict:
        """Get intelligent insights about pricing"""
        
        base_range = SingaporePricingIntelligence._get_price_range(category, subcategory)
        if not base_range:
            return {"insights": [], "comparisons": []}
        
        insights = []
        comparisons = []
        
        # Price positioning insights
        if amount <= base_range.min_price:
            insights.append("💰 Great value! You're getting this below typical market price")
        elif amount <= base_range.typical_price:
            insights.append("👍 Good price! You're paying around the typical market rate")
        elif amount <= base_range.max_price:
            insights.append("⚠️ Higher price, but still within reasonable range")
        else:
            insights.append("🚨 Price seems high - consider alternatives or check for premium features")
        
        # Category-specific insights
        category_insights = SingaporePricingIntelligence._get_category_insights(
            amount, category, subcategory
        )
        insights.extend(category_insights)
        
        # Location insights
        if location:
            location_insight = SingaporePricingIntelligence._get_location_insight(
                amount, category, location
            )
            if location_insight:
                insights.append(location_insight)
        
        # Alternative suggestions
        alternatives = SingaporePricingIntelligence._get_alternatives(
            amount, category, subcategory, location
        )
        if alternatives:
            insights.append(f"💡 Consider: {alternatives}")
        
        # Price comparisons
        comparisons = SingaporePricingIntelligence._get_price_comparisons(
            amount, category, subcategory, location
        )
        
        return {
            "insights": insights,
            "comparisons": comparisons,
            "value_score": SingaporePricingIntelligence._calculate_value_score(
                amount, base_range.typical_price
            )
        }
    
    @staticmethod
    def suggest_alternatives(amount: float, category: str, subcategory: str = None,
                           location: str = None) -> List[Dict]:
        """Suggest alternative options for better value"""
        
        alternatives = []
        
        if category.lower() == "food":
            if amount > 8:  # Expensive food
                alternatives.append({
                    "option": "Hawker centers",
                    "savings": f"Save ${amount - 5:.2f}",
                    "description": "Authentic local food at great prices",
                    "locations": ["Any heartland area", "Food courts"]
                })
                
                alternatives.append({
                    "option": "Food courts",
                    "savings": f"Save ${amount - 7:.2f}",
                    "description": "Variety of cuisines at reasonable prices",
                    "locations": ["Shopping malls", "Office buildings"]
                })
        
        elif category.lower() == "transport":
            if amount > 15:  # Expensive transport
                alternatives.append({
                    "option": "Public transport",
                    "savings": f"Save ${amount - 2:.2f}",
                    "description": "MRT and bus network coverage",
                    "locations": ["All areas", "Peak hours"]
                })
                
                alternatives.append({
                    "option": "Walking/Cycling",
                    "savings": f"Save ${amount}",
                    "description": "Free and healthy option for short distances",
                    "locations": ["Short distances", "Good weather"]
                })
        
        elif category.lower() == "entertainment":
            if amount > 20:  # Expensive entertainment
                alternatives.append({
                    "option": "Free activities",
                    "savings": f"Save ${amount}",
                    "description": "Parks, museums, walking trails",
                    "locations": ["All over Singapore", "Good weather days"]
                })
        
        return alternatives
    
    # =============================================================================
    # HELPER METHODS - Internal pricing logic
    # =============================================================================
    
    @staticmethod
    def _get_price_range(category: str, subcategory: str = None) -> Optional[PriceRange]:
        """Get price range for a category and subcategory"""
        category_lower = category.lower()
        
        if category_lower == "food":
            if subcategory and subcategory.lower() in SingaporePricingIntelligence.HAWKER_PRICES:
                return SingaporePricingIntelligence.HAWKER_PRICES[subcategory.lower()]
            elif subcategory and subcategory.lower() in SingaporePricingIntelligence.RESTAURANT_PRICES:
                return SingaporePricingIntelligence.RESTAURANT_PRICES[subcategory.lower()]
            else:
                # Default food pricing
                return PriceRange(3.0, 25.0, 12.0, "General food pricing")
        
        elif category_lower == "transport":
            if subcategory and subcategory.lower() in SingaporePricingIntelligence.TRANSPORT_COSTS:
                return SingaporePricingIntelligence.TRANSPORT_COSTS[subcategory.lower()]
            else:
                return PriceRange(1.47, 45.0, 15.0, "General transport pricing")
        
        elif category_lower == "shopping":
            if subcategory and subcategory.lower() in SingaporePricingIntelligence.SHOPPING_PRICES:
                return SingaporePricingIntelligence.SHOPPING_PRICES[subcategory.lower()]
            else:
                return PriceRange(5.0, 500.0, 100.0, "General shopping pricing")
        
        elif category_lower == "entertainment":
            if subcategory and subcategory.lower() in SingaporePricingIntelligence.ENTERTAINMENT_PRICES:
                return SingaporePricingIntelligence.ENTERTAINMENT_PRICES[subcategory.lower()]
            else:
                return PriceRange(5.0, 200.0, 50.0, "General entertainment pricing")
        
        return None
    
    @staticmethod
    def _get_location_multiplier(location: str = None) -> float:
        """Get location-based price multiplier"""
        if not location:
            return 1.0
        
        location_lower = location.lower()
        for key, context in SingaporePricingIntelligence.LOCATION_MULTIPLIERS.items():
            if key in location_lower or context.area_name.lower() in location_lower:
                return context.multiplier
        
        return 1.0
    
    @staticmethod
    def _get_time_multiplier(timestamp: datetime = None) -> float:
        """Get time-based price multiplier"""
        if not timestamp:
            return 1.0
        
        multiplier = 1.0
        
        # Check peak hours
        current_time = timestamp.time()
        for period, (start, end, period_mult, desc) in SingaporePricingIntelligence.TIME_MULTIPLIERS["peak_hours"].items():
            if start <= current_time <= end:
                multiplier *= period_mult
                break
        
        # Check weekend
        if timestamp.weekday() >= 5:  # Saturday or Sunday
            multiplier *= SingaporePricingIntelligence.TIME_MULTIPLIERS["weekend_multiplier"]
        
        # Check public holidays (simplified)
        # TODO: Integrate with actual public holiday API
        
        return multiplier
    
    @staticmethod
    def _calculate_confidence(amount: float, min_price: float, max_price: float) -> str:
        """Calculate confidence level in price validation"""
        range_size = max_price - min_price
        if range_size == 0:
            return "high"
        
        position = (amount - min_price) / range_size
        
        if position < 0.2 or position > 0.8:
            return "high"
        elif position < 0.4 or position > 0.6:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def _generate_suggestions(amount: float, category: str, subcategory: str,
                             min_price: float, max_price: float, location: str) -> List[str]:
        """Generate helpful suggestions based on price validation"""
        suggestions = []
        
        if amount < min_price:
            suggestions.append("Double-check the price - this seems unusually low")
            suggestions.append("Verify the quality and portion size")
        
        elif amount > max_price:
            suggestions.append("Consider alternatives for better value")
            suggestions.append("Check if there are premium features included")
            suggestions.append("Look for promotions or discounts")
        
        # Category-specific suggestions
        if category.lower() == "food" and amount > 15:
            suggestions.append("Try hawker centers for authentic local food at better prices")
        
        elif category.lower() == "transport" and amount > 20:
            suggestions.append("Consider public transport for regular routes")
            suggestions.append("Check if Grab surge pricing is active")
        
        return suggestions
    
    @staticmethod
    def _generate_validation_message(amount: float, is_reasonable: bool, min_price: float,
                                   max_price: float, category: str, location: str) -> str:
        """Generate user-friendly validation message"""
        
        if is_reasonable:
            if amount <= min_price:
                return f"✅ Great value! ${amount:.2f} is below typical prices for {category}"
            elif amount <= (min_price + max_price) / 2:
                return f"👍 Good price! ${amount:.2f} is reasonable for {category}"
            else:
                return f"⚠️ Higher price but acceptable. ${amount:.2f} for {category}"
        else:
            if amount < min_price:
                return f"🤔 Unusually low price: ${amount:.2f} for {category}. Double-check!"
            else:
                return f"🚨 Price seems high: ${amount:.2f} for {category}. Consider alternatives!"
    
    @staticmethod
    def _get_category_insights(amount: float, category: str, subcategory: str) -> List[str]:
        """Get category-specific insights"""
        insights = []
        
        if category.lower() == "food":
            if amount <= 5:
                insights.append("🍜 Hawker champion! You're getting great value")
            elif amount <= 8:
                insights.append("🍽️ Good food court or casual dining price")
            elif amount <= 15:
                insights.append("🍴 Mid-range restaurant territory")
            else:
                insights.append("🌟 Premium dining experience")
        
        elif category.lower() == "transport":
            if amount <= 3:
                insights.append("🚌 Public transport - smart money move!")
            elif amount <= 15:
                insights.append("🚗 Grab or taxi - convenience has a price")
            else:
                insights.append("✈️ Long distance or premium transport")
        
        return insights
    
    @staticmethod
    def _get_location_insight(amount: float, category: str, location: str) -> Optional[str]:
        """Get location-specific insight"""
        location_lower = location.lower()
        
        if "cbd" in location_lower or "orchard" in location_lower:
            return "🏢 Premium area pricing - consider heartland alternatives for better value"
        elif "heartland" in location_lower:
            return "🏠 Local area pricing - you're getting authentic Singapore value"
        elif "airport" in location_lower:
            return "✈️ Airport convenience pricing - higher but expected"
        
        return None
    
    @staticmethod
    def _get_alternatives(amount: float, category: str, subcategory: str, location: str) -> str:
        """Get alternative suggestions"""
        if category.lower() == "food" and amount > 10:
            return "hawker centers, food courts, or home cooking"
        elif category.lower() == "transport" and amount > 15:
            return "public transport, walking, or cycling"
        elif category.lower() == "entertainment" and amount > 30:
            return "free activities, parks, or community events"
        
        return ""
    
    @staticmethod
    def _get_price_comparisons(amount: float, category: str, subcategory: str, location: str) -> List[Dict]:
        """Get price comparisons for context"""
        comparisons = []
        
        if category.lower() == "food":
            comparisons.append({
                "option": "Hawker center",
                "price": "$3-8",
                "savings": f"${amount - 5:.2f}" if amount > 5 else "Already good value"
            })
            
            comparisons.append({
                "option": "Food court",
                "price": "$6-12",
                "savings": f"${amount - 9:.2f}" if amount > 9 else "Already good value"
            })
        
        elif category.lower() == "transport":
            comparisons.append({
                "option": "Public transport",
                "price": "$1.47-3.45",
                "savings": f"${amount - 2.5:.2f}" if amount > 2.5 else "Already good value"
            })
        
        return comparisons
    
    @staticmethod
    def _calculate_value_score(amount: float, typical_price: float) -> float:
        """Calculate value score (0-100, higher is better value)"""
        if typical_price == 0:
            return 50.0
        
        ratio = typical_price / amount
        score = min(100.0, ratio * 100)
        return max(0.0, score)

