import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# আপনার বটের টোকেন এখানে বসানো হয়েছে
BOT_TOKEN = "8811802511:AAEj_hDw9Vga-r1J2lYqbXZrAuDAn6GhR8g"

# আপনার টেলিগ্রাম ইউজার আইডি এখানে সেট করা হলো (অ্যাডমিন কাজের জন্য)
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
        await query.message.edit_text("📩 যেকোনো প্রয়োজনে আমাদের অ্যাডমিন অ্যাকাউন্টে নক দিন।", reply_markup=reply_markup)
        
    elif query.data == "main_menu":
        await start(update, context)

# মূল রানার ফাংশন
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
