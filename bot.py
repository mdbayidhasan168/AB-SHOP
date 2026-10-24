import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# আপনার বটের টোকেন এবং ইউজার আইডি
BOT_TOKEN = "8811802511:AAEj_hDw9Vga-r1J2lYqbXZrAuDAn6GhR8g"
ADMIN_USER_ID = 7108803747

# নমুনাস্বরূপ কিছু পণ্যের তালিকা
PRODUCTS = {
    "1": {"name": "প্রিমিয়াম সার্ভিস A", "price": "৳ ৫০০"},
    "2": {"name": "প্রিমিয়াম সার্ভিস B", "price": "৳ ১০০০"},
    "3": {"name": "ডিজিটাল অ্যাকাউন্ট C", "price": "৳ ৩০০"}
}

# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🛍️ প্রডাক্ট ক্যাটালগ", callback_data="catalog")],
        [InlineKeyboardButton("📞 সাপোর্ট / যোগাযোগ", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_msg = (
        f"হ্যালো {user.first_name}! 👋\n\n"
        f"আমাদের শপ বটে আপনাকে স্বাগতম। নিচে দেওয়া বাটন চাপুন এবং সেবা সিলেক্ট করুন:"
    )
    
    if update.message:
        await update.message.reply_text(welcome_msg, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_msg, reply_markup=reply_markup)

# বাটন ক্লিকে কাজ করার হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "catalog":
        keyboard = []
        for p_id, p_info in PRODUCTS.items():
            keyboard.append([InlineKeyboardButton(f"{p_info['name']} - {p_info['price']}", callback_data=f"buy_{p_id}")])
        keyboard.append([InlineKeyboardButton("🔙 প্রধান মেনু", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("🛒 আমাদের পাওয়া যায় এমন সকল প্রোডাক্টের তালিকা:", reply_markup=reply_markup)
        
    elif query.data.startswith("buy_"):
        product_id = query.data.split("_")[1]
        product = PRODUCTS.get(product_id)
        
        if product:
            msg = (
                f"✅ **আপনি সিলেক্ট করেছেন:** {product['name']}\n"
                f"💰 **মূল্য:** {product['price']}\n\n"
                f"অর্ডার কনফার্ম করতে এবং পেমেন্ট ডিটেইলস পেতে অ্যাডমিনের সাথে যোগাযোগ করুন।"
            )
            keyboard = [
                [InlineKeyboardButton("💬 অ্যাডমিন মেসেজ দিন", url="https://t.me/mdbayidhasan168")],
                [InlineKeyboardButton("🔙 ক্যাটালগে ফিরে যান", callback_data="catalog")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.edit_text(msg, reply_markup=reply_markup, parse_mode="Markdown")
            
    elif query.data == "support":
        keyboard = [[InlineKeyboardButton("🔙 প্রধান মেনু", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("📩 যেকোনো প্রয়োজনে আমাদের অ্যাডমিন অ্যাকাউন্টে নক দিন.", reply_markup=reply_markup)
        
    elif query.data == "main_menu":
        await start(update, context)

# Render-এর পোর্ট ঠিক রাখার জন্য সিম্পল ওয়েব সার্ভার
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")
    def log_message(self, format, *args):
        return  # অতিরিক্ত লগ স্প্যাম হওয়া রোধ করতে

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# মূল রানার ফাংশন
def main():
    # ব্যাকগ্রাউন্ডে ওয়েব সার্ভার চালু করা
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    # টেলিগ্রাম বট চালু করা
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
