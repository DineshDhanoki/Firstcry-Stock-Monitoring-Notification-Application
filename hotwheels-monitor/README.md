# 🔔 HotWheels Stock Monitor

This project monitors **Hot Wheels products on FirstCry** and sends notifications to you via **Telegram and/or Email** when selected items are back in stock for your chosen pincode.  
It runs automatically every 15 minutes using **GitHub Actions**, so it works even when your computer is off.  

---

## 🚀 Features
- Add products (by URL + pincode) to monitor
- Notifications via **Telegram** and/or **Email**
- GitHub Actions automation → no local machine needed
- Update product list directly from **GitHub Issues**
- Always checks stock at **MRP price** (FirstCry always sells MRP)

---

## 📂 Project Structure
```
hotwheels-monitor/
│
├── monitor.py                # Main script (menu + monitor logic)
├── requirements.txt           # Python dependencies
├── config.yaml                # Product + pincode list (auto-created)
├── state.json                 # Cache (do not edit manually)
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

### 3. First Time Setup (Local)
Run this locally once to add products:
```bash
pip install -r requirements.txt
python monitor.py
```
This will create `config.yaml` with your product list and pincode.  
Commit + push it to GitHub.

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
