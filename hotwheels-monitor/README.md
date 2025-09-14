# 🔔 HotWheels Stock Monitor

This project monitors **Hot Wheels products on FirstCry** and sends notifications to you via **Telegram and/or Email** when selected items are back in stock for your chosen pincode.  
It runs automatically every 15 minutes using **GitHub Actions**, so it works even when your computer is off.  

---

## 🚀 Features
- **🤖 Interactive Telegram Bot** - Browse and add products directly in Telegram
- **🔍 Complete HotWheels Catalog** - View all HotWheels products from FirstCry
- **📱 Telegram Menu Interface** - No more terminal commands needed
- **🔔 Smart Notifications** - Get notified when products are back in stock
- **📍 Pincode Support** - Check availability for your location
- **📋 Watchlist Management** - Add/remove products through Telegram
- **🧪 Test Mode** - Test notifications before going live
- **🔒 Secure Setup** - Environment variables for credentials

---

## 📂 Project Structure
```
hotwheels-monitor/
│
├── monitor.py                # Main monitoring script
├── telegram_bot.py           # Interactive Telegram bot interface
├── firstcry_scraper.py       # FirstCry product scraper
├── requirements.txt           # Python dependencies
├── config.yaml                # Product + pincode list (auto-created)
├── state.json                 # Cache (do not edit manually)
├── .env                       # Environment variables (create from env.example)
├── env.example                # Sample environment configuration
├── test_telegram.py           # Test Telegram notifications
├── test_whatsapp.py           # Test WhatsApp notifications
├── test_bot.py                # Test bot functionality
├── stop_bot.py                # Stop running bot
├── TESTING_GUIDE.md           # Comprehensive testing instructions
│
├── scripts/
│   └── issue_handler.py       # Handles GitHub Issues → config updates
│
└── .github/
    └── workflows/
        ├── monitor.yml        # Runs monitor every 15 mins
        └── config-manager.yml # Sync config.yaml via Issues
```

---

## ⚙️ Setup Instructions

### 1. Fork or Create Private Repo
- Create a **private GitHub repository**.
- Upload the project files (`monitor.py`, `.github/`, etc.).

### 2. Add GitHub Secrets
Go to **Repo → Settings → Secrets and variables → Actions** and add:

#### Telegram (optional but recommended)
- `TELEGRAM_BOT_TOKEN` = your bot token  
- `TELEGRAM_CHAT_ID` = your chat ID  

#### Email (optional)
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_FROM_EMAIL`
- `SMTP_TO_EMAILS` (comma separated list)
- `SMTP_USE_TLS` = true

#### WhatsApp (optional)
- `TWILIO_ACCOUNT_SID` = your Twilio account SID
- `TWILIO_AUTH_TOKEN` = your Twilio auth token
- `TWILIO_WHATSAPP_FROM` = whatsapp:+14155238886 (sandbox number)
- `TWILIO_WHATSAPP_TO` = whatsapp:+your_phone_number

### 3. First Time Setup (Local)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Telegram bot:**
   ```bash
   cp env.example .env
   # Edit .env with your Telegram bot token and chat ID
   ```

3. **Test your setup:**
   ```bash
   python test_telegram.py    # Test basic notifications
   python test_bot.py         # Test bot functionality
   ```

4. **Start the Telegram bot:**
   ```bash
   python telegram_bot.py
   ```

5. **Use the bot in Telegram:**
   - Search for `@Hotwheels_stock_bot`
   - Send `/start` to see the menu
   - Browse HotWheels products and add to watchlist
   - Test notifications through the bot

### 4. Automated Runs
- GitHub Actions (`.github/workflows/monitor.yml`) runs every 15 minutes.
- You’ll get notifications on Telegram/Email when products are in stock.

---

## 📝 Managing Products via GitHub Issues
You don’t need your computer again!  
To add/remove products:

1. Go to your repo **Issues**.
2. Create a new Issue with one of these titles:
   - `Add product`
   - `Remove product`
3. In the Issue body, include:
   ```
   URL: <product URL>
   Pincode: <your pincode>
   ```

The Action will update `config.yaml` automatically.

---

## 🧪 Testing

### Local Testing
1. **Test individual channels:**
   ```bash
   python test_telegram.py    # Test Telegram
   python test_whatsapp.py    # Test WhatsApp
   ```

2. **Test all channels:**
   ```bash
   python monitor.py --test
   ```

3. **Full testing guide:** See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed instructions.

### GitHub Actions Testing
- Go to Actions tab → "HotWheels Monitor" → "Run workflow"
- Check logs to verify notifications are sent

---

## 🔒 Notes
- Keep repo **private** (your product list + emails are stored here).
- Only commit `config.yaml` changes, **never** secrets.
- FirstCry may rate-limit scraping if abused. Default is every 15 minutes.

---

## ✅ Example `config.yaml`
```yaml
products:
  - url: "https://www.firstcry.com/hotwheels/hot-wheels-car-123/123456"
    pincode: "400001"
  - url: "https://www.firstcry.com/hotwheels/hot-wheels-track-789/987654"
    pincode: "400002"
```

---

### 🔮 Future Ideas
- Support more e-commerce sites (Amazon, Flipkart, etc.)
- Push notifications to WhatsApp
- Web dashboard to view stock history

---

💡 Now just add products, and relax — you’ll be pinged the moment HotWheels come back in stock!
