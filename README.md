
# SG Money Buddy 🇸🇬💰

A Telegram bot designed specifically for Singaporeans to manage daily expenses and combat the cost of living crisis.

## Features

### Phase 1 (MVP) - Currently Building
- ✅ Basic expense tracking via natural language
- ✅ Singapore-specific categories and pricing validation
- ✅ Simple budget alerts with Singlish responses
- ✅ Local context awareness (hawker centers, MRT, etc.)
- ✅ Interactive keyboards for easy navigation

### Planned Features
- 🔄 Automated deal aggregation from Singapore channels
- 🔄 AI-powered personalized savings advice
- 🔄 Weekly/monthly spending summaries with local insights
- 🔄 Goal setting and tracking
- 🔄 Integration with local services (GrabPay, PayLah!, etc.)

## Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd sg-finance-bot
```

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your tokens
nano .env
```

Required environment variables:
- `TELEGRAM_BOT_TOKEN`: Get from [@BotFather](https://t.me/botfather)
- `OPENAI_API_KEY`: Optional, for AI features
- `DATABASE_URL`: SQLite by default

### 4. Run the Bot
```bash
# Development mode (polling)
python main.py

# Production mode (webhook)
python webhook.py
```

## Singapore-Specific Features

### 🍜 Local Pricing Intelligence
- Understands hawker food ($3-15), coffee shop prices ($2-8)
- Validates transport costs (MRT $1-3, bus $1-2, Grab $8-50)
- Recognizes HDB, condo, and landed property contexts

### 🗣️ Singlish Support
Natural conversation with local expressions:
- "Wah! Welcome to SG Money Buddy lah!"
- "Alamak! You spent quite a lot on transport leh!"
- "Steady lah! Good job saving money!"

### 🏪 Category Mapping
Singapore-specific expense categories:
- **Food**: Hawker, zi char, cai png, coffee shops
- **Transport**: MRT, bus, Grab, car park, petrol
- **Housing**: HDB rent, utilities, conservancy charges
- **Entertainment**: Movies, KTV, shopping malls

### 📍 Location Context
Recognizes Singapore locations:
- Central: Orchard, Marina Bay, Bugis, Clarke Quay
- Heartlands: Tampines, Jurong, Woodlands, Toa Payoh
- Shopping: Vivo City, ION, Plaza Singapura

## Usage Examples

### Basic Expense Tracking
```
User: "lunch hawker $4.50"
Bot: "Got it! $4.50 for Food. You've spent $23 on food this week - still within your $40 budget! Well done lah 👍"

User: "transport $25"
Bot: "Wah! $25 for transport quite expensive leh. You sure need grab? Maybe try MRT next time? 😅"

User: "coffee $8"
Bot: "Alamak! $8 for coffee quite pricey sia! Maybe try kopitiam next time?"
```

### Budget Monitoring
```
User: "/budget"
Bot: "💰 Your Budget Status 📊

✅ Food
Budget: $600.00
Spent: $450.00 (75%)
Remaining: $150.00
Good job! On track! 👍

⚠️ Transport
Budget: $120.00
Spent: $95.00 (79%)
Remaining: $25.00
Careful leh! Close to budget limit! ⚠️"
```

### Deal Notifications (Coming Soon)
```
Bot: "Wah shiok! Found this deal for you! 🔥

🔥 1-for-1 Bubble Tea at Gong Cha
📍 Location: Islandwide
💰 Was: $6.50
✅ Now: $3.25
💵 Save: $3.25 (50%)

Valid Mon-Fri, 2-6pm only
⏰ Expires: 25 Dec 2024, 6:00 PM
📢 Source: @sgfooddeals

Steady lah! This deal confirm plus chop good! 🇸🇬"
```

## Development

### Project Structure
```
sg-finance-bot/
├── .cursor/rules/          # Development rules and patterns
├── src/
│   ├── bot/               # Telegram bot handlers
│   │   ├── handlers.py    # Main message handlers
│   │   ├── commands.py    # Command handlers
│   │   ├── responses.py   # Singapore-specific responses
│   │   └── keyboards.py   # Interactive keyboards
│   ├── services/          # Business logic
│   │   ├── expense_tracker.py    # Expense parsing & tracking
│   │   ├── deals_aggregator.py   # Deal aggregation
│   │   ├── ai_advisor.py         # AI financial advice
│   │   └── budget_manager.py     # Budget management
│   ├── data/              # Database layer
│   │   ├── models.py      # SQLAlchemy models
│   │   ├── database.py    # Database operations
│   │   └── migrations/    # Database migrations
│   ├── utils/             # Utilities
│   │   ├── config.py      # Configuration management
│   │   ├── helpers.py     # Singapore-specific helpers
│   │   └── validators.py  # Input validation
│   └── tests/             # Test suite
├── main.py                # Development entry point
├── webhook.py            # Production webhook server
└── requirements.txt      # Dependencies
```

### Tech Stack
- **Framework**: python-telegram-bot v22.3 with async/await
- **Database**: SQLite (dev), PostgreSQL (prod) with SQLAlchemy
- **Web Server**: FastAPI + Uvicorn for webhooks
- **AI**: OpenAI GPT for intelligent responses
- **Testing**: pytest with async support
- **Deployment**: Railway/Render/Heroku ready

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest src/tests/test_handlers.py

# Run with coverage
pytest --cov=src

# Run integration tests
pytest -m integration
```

### Code Quality
```bash
# Format code
black src/

# Type checking (if using mypy)
mypy src/

# Linting
flake8 src/
```

## Deployment

### Environment Variables (Production)
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
WEBHOOK_URL=https://your-app.railway.app/webhook
DATABASE_URL=postgresql://user:pass@host:port/db
OPENAI_API_KEY=your_openai_key
APP_ENV=production
SECRET_KEY=your_secret_key
LOG_LEVEL=INFO
```

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy with automatic builds

### Heroku Deployment
```bash
# Create Heroku app
heroku create sg-money-buddy

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token

# Deploy
git push heroku main
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "webhook.py"]
```

## Singapore Context & Localization

### Price Validation Ranges
| Category | Min | Max | Average | Examples |
|----------|-----|-----|---------|----------|
| Food | $2 | $50 | $8 | Hawker ($3-6), Restaurant ($15-30) |
| Transport | $1 | $100 | $15 | MRT ($1-3), Bus ($1-2), Grab ($8-50) |
| Housing | $50 | $5000 | $800 | HDB room ($500-800), Condo ($1500-3000) |
| Entertainment | $10 | $200 | $40 | Movie ($13), KTV ($30/hr) |

### Local Services Integration (Planned)
- **Payment**: GrabPay, PayLah!, PayNow
- **Transport**: EZ-Link card balance, MRT disruptions
- **Deals**: Integration with major Singapore deal channels
- **Banking**: DBS, OCBC, UOB transaction categorization

### Cultural Considerations
- **Language**: Mix of English and Singlish for authenticity
- **Humor**: Light-hearted approach to money management
- **Social Context**: Understanding of Singapore lifestyle and costs
- **Privacy**: No storage of sensitive financial data (bank details, NRIC)

## Contributing

### Singapore-First Development Principles
1. **Local Context**: Always consider Singapore pricing and culture
2. **Singlish Integration**: Include local expressions in user-facing text
3. **Privacy First**: Never store sensitive financial information
4. **Testing**: Include Singapore-specific test cases

### Code Standards
- Follow PEP 8 with 88-character line length (Black formatting)
- Use type hints for all function parameters and returns
- Include docstrings for all public functions
- Write tests for Singapore-specific features

### Pull Request Process
1. Fork the repository
2. Create feature branch (`feature/singapore-feature-name`)
3. Include tests for Singapore-specific functionality
4. Update documentation if needed
5. Submit pull request with detailed description

## Roadmap

### Q1 2024
- [x] Basic expense tracking with natural language
- [x] Singapore pricing validation
- [x] Singlish responses
- [ ] Budget management with alerts
- [ ] Weekly/monthly summaries

### Q2 2024
- [ ] Deal aggregation from Telegram channels
- [ ] AI-powered savings advice
- [ ] Goal setting and tracking
- [ ] Export data functionality

### Q3 2024
- [ ] Integration with Singapore payment apps
- [ ] Group expense tracking for families
- [ ] Merchant category insights
- [ ] Advanced analytics dashboard

### Q4 2024
- [ ] Voice message support (Singlish recognition)
- [ ] Photo receipt parsing
- [ ] Integration with local banks (read-only)
- [ ] Community features (anonymous spending insights)

## Support

### Getting Help
- 📧 Email: support@sgmoneybuddy.com
- 💬 Telegram: [@sgmoneybuddy_support](https://t.me/sgmoneybuddy_support)
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/sg-finance-bot/issues)

### Community
- 👥 Singapore Personal Finance: [Join our group](https://t.me/sgpersonalfinance)
- 📱 Updates Channel: [@sgmoneybuddy_updates](https://t.me/sgmoneybuddy_updates)

## License

MIT License - Built with ❤️ for Singapore

## Acknowledgments

- Singapore fintech community for inspiration
- Local deal channels for data insights
- Beta testers from Singapore universities and workplaces
- Open source contributors to python-telegram-bot

---

*"Making every dollar count in Singapore, one expense at a time lah!"* 🇸🇬💪
