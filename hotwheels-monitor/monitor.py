import requests, yaml, json, os, time, logging, sys
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

CONFIG_FILE = "config.yaml"
STATE_FILE = "state.json"

# ---------- Helpers ----------
def load_yaml(path=CONFIG_FILE):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {"products": [], "delay_between_requests": 3}

def save_yaml(cfg, path=CONFIG_FILE):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

# ---------- Notifications ----------
def send_telegram(bot_token, chat_id, message):
    if not bot_token or not chat_id:
        logging.warning("Telegram not configured")
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": message})

def send_email(cfg, subject, body):
    if not cfg or not cfg.get("host"):
        return
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["From"] = cfg["from_email"]
    msg["To"] = ",".join(cfg["to_emails"])
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(cfg["host"], cfg["port"]) as server:
        if cfg.get("use_tls", True):
            server.starttls()
        server.login(cfg["username"], cfg["password"])
        server.send_message(msg)

# ---------- Scraper ----------
def fetch_html(url, pincode):
    try:
        cookies = {"FC_PINCODE": str(pincode)}
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, cookies=cookies, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        logging.warning("Failed to fetch %s: %s", url, e)
        return None

def check_stock(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True).lower()
    if "out of stock" in text or "notify me" in text or "sold out" in text:
        return False
    if "add to cart" in text or "buy now" in text or "add to bag" in text:
        return True
    return False

# ---------- Monitor ----------
def run_monitor():
    cfg = load_yaml()
    state = load_state()

    telegram_bot = os.getenv("TELEGRAM_BOT_TOKEN") or (cfg.get("telegram") or {}).get("bot_token")
    telegram_chat = os.getenv("TELEGRAM_CHAT_ID") or (cfg.get("telegram") or {}).get("chat_id")

    smtp_cfg = None
    if os.getenv("SMTP_HOST"):
        smtp_cfg = {
            "host": os.getenv("SMTP_HOST"),
            "port": int(os.getenv("SMTP_PORT", "587")),
            "username": os.getenv("SMTP_USERNAME"),
            "password": os.getenv("SMTP_PASSWORD"),
            "from_email": os.getenv("SMTP_FROM_EMAIL"),
            "to_emails": os.getenv("SMTP_TO_EMAILS", "").split(","),
            "use_tls": True
        }
    elif cfg.get("smtp"):
        smtp_cfg = cfg["smtp"]

    for product in cfg["products"]:
        url, title, pincode = product["url"], product["title"], product.get("pincode")
        key = f"{product['id']}_{pincode}"
        logging.info("Checking %s (pincode %s)", title, pincode)

        html = fetch_html(url, pincode)
        if not html:
            continue

        in_stock = check_stock(html)
        last_status = state.get(key, {}).get("in_stock", False)

        if in_stock and not last_status:
            message = f"✅ {title} is AVAILABLE!\nPincode: {pincode}\n{url}"
            if telegram_bot and telegram_chat:
                send_telegram(telegram_bot, telegram_chat, message)
            if smtp_cfg:
                send_email(smtp_cfg, f"[HotWheels Alert] {title} available", message)
            logging.info("Notification sent for %s [%s]", title, pincode)

        state[key] = {"in_stock": in_stock}
        time.sleep(cfg.get("delay_between_requests", 3))

    save_state(state)

# ---------- CLI ----------
def menu():
    cfg = load_yaml()
    while True:
        print("\n==== HotWheels Stock Watcher ====")
        print("1. Add product")
        print("2. Remove product")
        print("3. List products")
        print("4. Start monitoring")
        print("5. Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            title = input("Enter product title: ").strip()
            url = input("Enter product URL: ").strip()
            pincode = input("Enter pincode: ").strip()
            pid = f"prod{len(cfg['products'])+1}"
            cfg["products"].append({"id": pid, "title": title, "url": url, "pincode": pincode})
            save_yaml(cfg)
            print(f"✅ Added {title} [{pincode}]")
        elif choice == "2":
            for i, p in enumerate(cfg["products"], 1):
                print(f"{i}. {p['title']} [{p['pincode']}]")
            idx = input("Enter product number to remove: ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(cfg["products"]):
                removed = cfg["products"].pop(int(idx)-1)
                save_yaml(cfg)
                print(f"❌ Removed {removed['title']}")
            else:
                print("Invalid choice")
        elif choice == "3":
            if not cfg["products"]:
                print("No products in watchlist.")
            else:
                for i, p in enumerate(cfg["products"], 1):
                    print(f"{i}. {p['title']} [{p['pincode']}] → {p['url']}")
        elif choice == "4":
            print("🔄 Starting monitor... (Ctrl+C to stop)")
            while True:
                run_monitor()
                print("Sleeping before next check...")
                time.sleep(60)
        elif choice == "5":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    if "--ci" in sys.argv:
        run_monitor()
    else:
        menu()
