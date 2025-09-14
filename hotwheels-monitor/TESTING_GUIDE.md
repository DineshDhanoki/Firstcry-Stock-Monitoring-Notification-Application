# 🧪 HotWheels Monitor - Testing Guide

This guide will help you test all notification channels locally before deploying to GitHub Actions.

## 📋 Prerequisites

1. **Python 3.11+** installed
2. **Git** installed
3. **GitHub account** (for repository setup)

## 🚀 Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` file with your actual credentials (see configuration sections below)

### 3. Test Individual Notification Channels

#### A. Test Telegram Notifications

1. **Create a Telegram Bot:**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot`
   - Follow instructions to create your bot
   - Copy the bot token

2. **Get Your Chat ID:**
   - Message [@userinfobot](https://t.me/userinfobot) on Telegram
   - Copy your chat ID

3. **Update .env file:**
   ```env
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   TELEGRAM_CHAT_ID=your_actual_chat_id_here
   ```

4. **Test Telegram:**
   ```bash
   python test_telegram.py
   ```

#### B. Test Email Notifications

1. **For Gmail:**
   - Enable 2-Factor Authentication on your Google account
   - Generate an App Password:
     - Go to Google Account settings
     - Security → 2-Step Verification → App passwords
     - Generate password for "Mail"
   - Use your Gmail address and the app password

2. **For Outlook:**
   - Use your regular Outlook credentials
   - Make sure "Less secure app access" is enabled (if using personal account)

3. **Update .env file:**
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password_here
   SMTP_FROM_EMAIL=your_email@gmail.com
   SMTP_TO_EMAILS=recipient@example.com
   SMTP_USE_TLS=true
   ```

#### C. Test WhatsApp Notifications (Optional)

1. **Sign up for Twilio:**
   - Go to [Twilio Console](https://console.twilio.com/)
   - Sign up for a free account
   - Get your Account SID and Auth Token

2. **Set up WhatsApp Sandbox:**
   - Go to Messaging → Try it out → Send a WhatsApp message
   - Follow instructions to join the sandbox
   - Note the sandbox number (usually `whatsapp:+14155238886`)

3. **Update .env file:**
   ```env
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   TWILIO_WHATSAPP_TO=whatsapp:+your_phone_number
   ```

### 4. Test All Notifications Together

Run the test mode to verify all configured channels:

```bash
python monitor.py --test
```

This will:
- Send test messages to all configured notification channels
- Show success/failure status for each channel
- Not perform any actual product monitoring

### 5. Test Product Monitoring (Optional)

1. **Add a test product:**
   ```bash
   python monitor.py
   ```
   - Choose option 1 (Add product)
   - Add any HotWheels product URL and pincode

2. **Run monitoring:**
   - Choose option 4 (Start monitoring)
   - This will check products every 60 seconds
   - Press Ctrl+C to stop

### 6. GitHub Actions Setup

1. **Create a private GitHub repository**

2. **Add GitHub Secrets:**
   Go to your repo → Settings → Secrets and variables → Actions
   
   Add these secrets (only add the ones you want to use):
   ```
   TELEGRAM_BOT_TOKEN
   TELEGRAM_CHAT_ID
   SMTP_HOST
   SMTP_PORT
   SMTP_USERNAME
   SMTP_PASSWORD
   SMTP_FROM_EMAIL
   SMTP_TO_EMAILS
   SMTP_USE_TLS
   TWILIO_ACCOUNT_SID
   TWILIO_AUTH_TOKEN
   TWILIO_WHATSAPP_FROM
   TWILIO_WHATSAPP_TO
   ```

3. **Push your code:**
   ```bash
   git add .
   git commit -m "Add notification channels and testing support"
   git push origin main
   ```

4. **Test GitHub Actions:**
   - Go to Actions tab in your repository
   - Run the "HotWheels Monitor" workflow manually
   - Check the logs to see if notifications are sent

## 🔧 Troubleshooting

### Common Issues

1. **Telegram "Unauthorized" error:**
   - Check if bot token is correct
   - Make sure you've started a conversation with your bot

2. **Email authentication failed:**
   - For Gmail: Use App Password, not regular password
   - For Outlook: Check if 2FA is enabled and use app password

3. **WhatsApp "Invalid phone number" error:**
   - Make sure phone numbers include country code
   - Format: `whatsapp:+1234567890`

4. **Environment variables not loading:**
   - Make sure `.env` file is in the same directory as `monitor.py`
   - Check for typos in variable names
   - Restart your terminal/IDE after creating `.env`

### Debug Mode

To see detailed logs, run:
```bash
python -c "import logging; logging.basicConfig(level=logging.DEBUG); exec(open('monitor.py').read())" --test
```

## ✅ Verification Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with correct credentials
- [ ] Telegram test successful (`python test_telegram.py`)
- [ ] Email test successful (check your inbox)
- [ ] WhatsApp test successful (check your WhatsApp)
- [ ] All channels test successful (`python monitor.py --test`)
- [ ] GitHub repository created and configured
- [ ] GitHub Secrets added
- [ ] Code pushed to GitHub
- [ ] GitHub Actions workflow runs successfully

## 🎯 Next Steps

Once testing is complete:
1. Add your actual HotWheels products to monitor
2. The system will run automatically every 15 minutes via GitHub Actions
3. You'll receive notifications when products come back in stock
4. Use GitHub Issues to manage your product list remotely

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs in GitHub Actions
3. Verify all credentials are correct
4. Test each notification channel individually
