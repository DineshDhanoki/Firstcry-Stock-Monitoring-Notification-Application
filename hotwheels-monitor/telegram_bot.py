#!/usr/bin/env python3
"""
Telegram Bot Interface for HotWheels Monitor
Interactive bot with menus and product browsing
"""

import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from firstcry_scraper import FirstCryScraper
import yaml

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Configuration
CONFIG_FILE = "config.yaml"
STATE_FILE = "bot_state.json"

class HotWheelsBot:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.scraper = FirstCryScraper()
        self.products_cache = {}
        self.user_states = {}  # Track user interaction states
        
    def load_config(self):
        """Load configuration from YAML file"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {"products": [], "delay_between_requests": 3}
    
    def save_config(self, config):
        """Save configuration to YAML file"""
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            yaml.safe_dump(config, f, sort_keys=False)
    
    def get_main_menu(self):
        """Get main menu keyboard"""
        keyboard = [
            [InlineKeyboardButton("🔍 Browse HotWheels", callback_data="browse")],
            [InlineKeyboardButton("📋 My Watchlist", callback_data="watchlist")],
            [InlineKeyboardButton("➕ Add Product", callback_data="add_product")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
            [InlineKeyboardButton("🧪 Test Notifications", callback_data="test")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_pincode_menu(self):
        """Get pincode selection menu"""
        keyboard = [
            [InlineKeyboardButton("400001 (Mumbai)", callback_data="pincode_400001")],
            [InlineKeyboardButton("110001 (Delhi)", callback_data="pincode_110001")],
            [InlineKeyboardButton("560001 (Bangalore)", callback_data="pincode_560001")],
            [InlineKeyboardButton("700001 (Kolkata)", callback_data="pincode_700001")],
            [InlineKeyboardButton("600001 (Chennai)", callback_data="pincode_600001")],
            [InlineKeyboardButton("Custom Pincode", callback_data="custom_pincode")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_product_list_keyboard(self, products, page=0, pincode="400001"):
        """Get product list keyboard with pagination"""
        keyboard = []
        items_per_page = 5
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        
        for i, product in enumerate(products[start_idx:end_idx], start_idx):
            stock_emoji = "✅" if product['in_stock'] else "❌"
            button_text = f"{stock_emoji} {product['title'][:30]}..."
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"product_{i}")])
        
        # Pagination buttons
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{page-1}"))
        if end_idx < len(products):
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_{page+1}"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        # Back button
        keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_text = """
🤖 **Welcome to HotWheels Monitor Bot!**

I can help you:
• 🔍 Browse all HotWheels on FirstCry
• 📋 Manage your watchlist
• 🔔 Get notified when products are back in stock
• 🧪 Test notifications

Choose an option below:
        """
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=self.get_main_menu(),
            parse_mode='Markdown'
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
        if data == "main_menu":
            await query.edit_message_text(
                "🤖 **HotWheels Monitor Bot**\n\nChoose an option:",
                reply_markup=self.get_main_menu(),
                parse_mode='Markdown'
            )
        
        elif data == "browse":
            await query.edit_message_text(
                "📍 **Select your pincode to browse HotWheels:**",
                reply_markup=self.get_pincode_menu(),
                parse_mode='Markdown'
            )
        
        elif data.startswith("pincode_"):
            pincode = data.split("_")[1]
            await self.show_hotwheels_list(query, pincode)
        
        elif data == "custom_pincode":
            self.user_states[user_id] = "waiting_pincode"
            await query.edit_message_text(
                "📍 **Enter your pincode:**\n\nSend me a message with your 6-digit pincode.",
                parse_mode='Markdown'
            )
        
        elif data.startswith("page_"):
            page = int(data.split("_")[1])
            pincode = self.user_states.get(f"{user_id}_pincode", "400001")
            await self.show_hotwheels_list(query, pincode, page)
        
        elif data.startswith("product_"):
            product_idx = int(data.split("_")[1])
            pincode = self.user_states.get(f"{user_id}_pincode", "400001")
            await self.show_product_details(query, product_idx, pincode)
        
        elif data == "watchlist":
            await self.show_watchlist(query)
        
        elif data == "add_product":
            await query.edit_message_text(
                "➕ **Add Product to Watchlist**\n\nUse the Browse option to find products, then add them to your watchlist!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔍 Browse HotWheels", callback_data="browse")
                ]]),
                parse_mode='Markdown'
            )
        
        elif data == "test":
            await self.test_notifications(query)
        
        elif data.startswith("add_to_watchlist_"):
            product_idx = int(data.split("_")[3])
            await self.add_to_watchlist(query, product_idx)
    
    async def show_hotwheels_list(self, query, pincode, page=0):
        """Show list of HotWheels products"""
        user_id = query.from_user.id
        self.user_states[f"{user_id}_pincode"] = pincode
        
        # Check cache first
        cache_key = f"products_{pincode}"
        if cache_key not in self.products_cache:
            await query.edit_message_text("🔍 **Searching for HotWheels products...**\n\nThis may take a moment...", parse_mode='Markdown')
            
            products = self.scraper.search_hotwheels(pincode=pincode, max_pages=3)
            self.products_cache[cache_key] = products
        else:
            products = self.products_cache[cache_key]
        
        if not products:
            await query.edit_message_text(
                "❌ **No HotWheels products found!**\n\nTry a different pincode or check back later.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")
                ]]),
                parse_mode='Markdown'
            )
            return
        
        text = f"🚗 **HotWheels Products (Pincode: {pincode})**\n\n"
        text += f"Found {len(products)} products. Page {page + 1}:\n\n"
        
        await query.edit_message_text(
            text,
            reply_markup=self.get_product_list_keyboard(products, page, pincode),
            parse_mode='Markdown'
        )
    
    async def show_product_details(self, query, product_idx, pincode):
        """Show detailed product information"""
        cache_key = f"products_{pincode}"
        products = self.products_cache.get(cache_key, [])
        
        if product_idx >= len(products):
            await query.answer("Product not found!")
            return
        
        product = products[product_idx]
        
        # Get detailed stock status
        details = self.scraper.get_product_details(product['url'], pincode)
        
        text = f"🚗 **{product['title']}**\n\n"
        text += f"💰 **Price:** {product['price']}\n"
        text += f"📦 **Stock:** {'✅ In Stock' if details['in_stock'] else '❌ Out of Stock'}\n"
        text += f"📍 **Pincode:** {pincode}\n\n"
        text += f"🔗 **URL:** {product['url']}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("➕ Add to Watchlist", callback_data=f"add_to_watchlist_{product_idx}")],
            [InlineKeyboardButton("🔙 Back to List", callback_data="browse")]
        ]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def add_to_watchlist(self, query, product_idx):
        """Add product to watchlist"""
        user_id = query.from_user.id
        pincode = self.user_states.get(f"{user_id}_pincode", "400001")
        cache_key = f"products_{pincode}"
        products = self.products_cache.get(cache_key, [])
        
        if product_idx >= len(products):
            await query.answer("Product not found!")
            return
        
        product = products[product_idx]
        
        # Load current config
        config = self.load_config()
        
        # Check if product already exists
        existing = any(p['url'] == product['url'] and p.get('pincode') == pincode for p in config['products'])
        
        if existing:
            await query.answer("❌ Product already in watchlist!")
            return
        
        # Add to watchlist
        new_product = {
            'id': f"prod{len(config['products']) + 1}",
            'title': product['title'],
            'url': product['url'],
            'pincode': pincode
        }
        
        config['products'].append(new_product)
        self.save_config(config)
        
        await query.answer("✅ Added to watchlist!")
        
        # Show updated product details
        await self.show_product_details(query, product_idx, pincode)
    
    async def show_watchlist(self, query):
        """Show user's watchlist"""
        config = self.load_config()
        products = config.get('products', [])
        
        if not products:
            text = "📭 **Your watchlist is empty!**\n\nUse the Browse option to find and add HotWheels products."
            keyboard = [[InlineKeyboardButton("🔍 Browse HotWheels", callback_data="browse")]]
        else:
            text = f"📋 **Your Watchlist ({len(products)} products)**\n\n"
            for i, product in enumerate(products, 1):
                text += f"{i}. {product['title']}\n"
                text += f"   📍 Pincode: {product.get('pincode', 'N/A')}\n"
                text += f"   🔗 {product['url']}\n\n"
            
            keyboard = [
                [InlineKeyboardButton("🔍 Browse More", callback_data="browse")],
                [InlineKeyboardButton("🧪 Test Monitor", callback_data="test")]
            ]
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")])
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def test_notifications(self, query):
        """Test notification system"""
        from monitor import send_telegram
        
        test_message = "🧪 **Test notification from HotWheels Monitor!**\n\nYour Telegram notifications are working correctly! 🎉"
        
        success = send_telegram(self.bot_token, str(query.from_user.id), test_message)
        
        if success:
            await query.answer("✅ Test notification sent!")
        else:
            await query.answer("❌ Failed to send test notification!")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        if not update.message or not update.message.from_user:
            return
            
        user_id = update.message.from_user.id
        text = update.message.text.strip()
        
        if self.user_states.get(user_id) == "waiting_pincode":
            if text.isdigit() and len(text) == 6:
                # Create a mock query object for show_hotwheels_list
                class MockQuery:
                    def __init__(self, message):
                        self.message = message
                        self.from_user = message.from_user
                    
                    async def edit_message_text(self, text, reply_markup=None, parse_mode=None):
                        await self.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
                
                mock_query = MockQuery(update.message)
                await self.show_hotwheels_list(mock_query, text)
                self.user_states[user_id] = None
            else:
                await update.message.reply_text(
                    "❌ **Invalid pincode!**\n\nPlease enter a valid 6-digit pincode.",
                    parse_mode='Markdown'
                )
        else:
            await update.message.reply_text(
                "🤖 **HotWheels Monitor Bot**\n\nUse the menu below to get started!",
                reply_markup=self.get_main_menu(),
                parse_mode='Markdown'
            )
    
    def run(self):
        """Start the bot"""
        if not self.bot_token:
            logging.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
            return
        
        application = Application.builder().token(self.bot_token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CallbackQueryHandler(self.handle_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logging.info("🤖 Starting HotWheels Monitor Bot...")
        application.run_polling()

if __name__ == "__main__":
    bot = HotWheelsBot()
    bot.run()
