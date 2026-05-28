from rubka.asynco import Robot, Message, filters
from rubka.keypad import ChatKeypadBuilder
import asyncio
import json
import os
import random
from time import time
from datetime import datetime, timedelta

bot = Robot("BCIDFE0AVDXMRPBRBUETITANHZAVTJIFVMEWFZIYLAHCNZQPCXERZQOKTVEAJOWE")
users_db = {}
user_states = {}
ban_list = []

# ======================= ۸۰ تا شغل جدید با حقوق حداکثر ۲۰,۰۰۰ =======================
JOBS = {
    # سطح 1 (حقوق ۵۰۰-۱۰۰۰)
    "کارگر ساده": {"salary": 500, "price": 100, "level": 1},
    "باربر": {"salary": 600, "price": 150, "level": 1},
    "نظافت‌چی": {"salary": 550, "price": 120, "level": 1},
    "باغبان": {"salary": 580, "price": 130, "level": 1},
    "انباردار": {"salary": 620, "price": 140, "level": 1},
    "خدماتي": {"salary": 500, "price": 100, "level": 1},
    "آشپز ساده": {"salary": 700, "price": 200, "level": 1},
    "راننده آژانس": {"salary": 750, "price": 250, "level": 1},
    "نگهبان": {"salary": 650, "price": 180, "level": 1},
    "صندوقدار": {"salary": 680, "price": 190, "level": 1},
    
    # سطح 2 (حقوق ۱۰۰۰-۲۰۰۰)
    "پیک موتوری": {"salary": 800, "price": 500, "level": 2},
    "فروشنده": {"salary": 900, "price": 600, "level": 2},
    "تلفن‌چی": {"salary": 850, "price": 550, "level": 2},
    "منشی": {"salary": 950, "price": 650, "level": 2},
    "بازاریاب": {"salary": 1000, "price": 700, "level": 2},
    "طراح ساده": {"salary": 1100, "price": 800, "level": 2},
    "تدوینگر": {"salary": 1050, "price": 750, "level": 2},
    "عکاس": {"salary": 1150, "price": 850, "level": 2},
    "خبرنگار": {"salary": 1080, "price": 780, "level": 2},
    "مترجم": {"salary": 1200, "price": 900, "level": 2},
    
    # سطح 3 (حقوق ۲۰۰۰-۳۵۰۰)
    "راننده تاکسی": {"salary": 1300, "price": 1000, "level": 3},
    "مکانیک": {"salary": 1400, "price": 1100, "level": 3},
    "برقکار": {"salary": 1450, "price": 1150, "level": 3},
    "لوله‌کش": {"salary": 1350, "price": 1050, "level": 3},
    "جوشکار": {"salary": 1500, "price": 1200, "level": 3},
    "نجار": {"salary": 1420, "price": 1120, "level": 3},
    "بنّا": {"salary": 1380, "price": 1080, "level": 3},
    "نقاش ساختمان": {"salary": 1480, "price": 1180, "level": 3},
    "کاشیکار": {"salary": 1460, "price": 1160, "level": 3},
    "گچکار": {"salary": 1440, "price": 1140, "level": 3},
    
    # سطح 4 (حقوق ۳۵۰۰-۵۰۰۰)
    "برنامه‌نویس ساده": {"salary": 1600, "price": 1300, "level": 4},
    "تکنسین کامپیوتر": {"salary": 1700, "price": 1400, "level": 4},
    "مدیر فروش": {"salary": 1800, "price": 1500, "level": 4},
    "حسابدار": {"salary": 1750, "price": 1450, "level": 4},
    "مدیر پروژه": {"salary": 1900, "price": 1600, "level": 4},
    "کارشناس بازاریابی": {"salary": 1650, "price": 1350, "level": 4},
    "مدیر تولید": {"salary": 1850, "price": 1550, "level": 4},
    "کارشناس فروش": {"salary": 1720, "price": 1420, "level": 4},
    "مدیر اداری": {"salary": 1880, "price": 1580, "level": 4},
    "روابط عمومی": {"salary": 1680, "price": 1380, "level": 4},
    
    # سطح 5 (حقوق ۵۰۰۰-۷۰۰۰)
    "دکتر عمومی": {"salary": 2500, "price": 2000, "level": 5},
    "پرستار": {"salary": 2200, "price": 1700, "level": 5},
    "داروساز": {"salary": 2400, "price": 1900, "level": 5},
    "دندانپزشک": {"salary": 2600, "price": 2100, "level": 5},
    "متخصص قلب": {"salary": 2800, "price": 2300, "level": 5},
    "روانشناس": {"salary": 2300, "price": 1800, "level": 5},
    "فیزیوتراپ": {"salary": 2450, "price": 1950, "level": 5},
    "تغذیه‌شناس": {"salary": 2350, "price": 1850, "level": 5},
    "ماما": {"salary": 2250, "price": 1750, "level": 5},
    "تکنولوژیست آزمایشگاه": {"salary": 2550, "price": 2050, "level": 5},
    
    # سطح 6 (حقوق ۷۰۰۰-۹۰۰۰)
    "وکیل پایه یک": {"salary": 3500, "price": 3000, "level": 6},
    "مشاور حقوقی": {"salary": 3200, "price": 2700, "level": 6},
    "قاضی": {"salary": 3800, "price": 3300, "level": 6},
    "داور": {"salary": 3400, "price": 2900, "level": 6},
    "سردفتر": {"salary": 3600, "price": 3100, "level": 6},
    "کارشناس ارشد حقوق": {"salary": 3300, "price": 2800, "level": 6},
    "مشاور خانواده": {"salary": 3100, "price": 2600, "level": 6},
    "مشاور مالیاتی": {"salary": 3700, "price": 3200, "level": 6},
    "کارشناس ثبت": {"salary": 3450, "price": 2950, "level": 6},
    
    # سطح 7 (حقوق ۹۰۰۰-۱۲۰۰۰)
    "مهندس عمران": {"salary": 4500, "price": 4000, "level": 7},
    "مهندس معماری": {"salary": 4700, "price": 4200, "level": 7},
    "مهندس مکانیک": {"salary": 4600, "price": 4100, "level": 7},
    "مهندس برق": {"salary": 4800, "price": 4300, "level": 7},
    "مهندس صنایع": {"salary": 4400, "price": 3900, "level": 7},
    "مهندس شیمی": {"salary": 4650, "price": 4150, "level": 7},
    "مهندس نرم‌افزار": {"salary": 4900, "price": 4400, "level": 7},
    "مهندس سخت‌افزار": {"salary": 4850, "price": 4350, "level": 7},
    "مهندس شبکه": {"salary": 4750, "price": 4250, "level": 7},
    "مهندس رباتیک": {"salary": 5000, "price": 4500, "level": 7},
    
    # سطح 8 (حقوق ۱۲۰۰۰-۱۶۰۰۰)
    "مدیر اجرایی": {"salary": 6500, "price": 6000, "level": 8},
    "مدیر عامل": {"salary": 7500, "price": 7000, "level": 8},
    "مشاور ارشد": {"salary": 7000, "price": 6500, "level": 8},
    "مدیر بازرگانی": {"salary": 6800, "price": 6300, "level": 8},
    "مدیر مالی": {"salary": 7200, "price": 6700, "level": 8},
    "مدیر منابع انسانی": {"salary": 6600, "price": 6100, "level": 8},
    "مدیر فناوری": {"salary": 7400, "price": 6900, "level": 8},
    "مدیر فروش منطقه": {"salary": 6900, "price": 6400, "level": 8},
    "مدیر برند": {"salary": 7100, "price": 6600, "level": 8},
    "مدیر تحقیق و توسعه": {"salary": 7300, "price": 6800, "level": 8},
    
    # سطح 9 (حقوق ۱۶۰۰۰-۲۰۰۰۰)
    "املاکی": {"salary": 9000, "price": 8500, "level": 9},
    "بورس کار": {"salary": 9500, "price": 9000, "level": 9},
    "کارآفرین": {"salary": 10000, "price": 9500, "level": 9},
    "سرمایه‌گذار": {"salary": 11000, "price": 10500, "level": 9},
    "تحلیلگر بازار": {"salary": 10500, "price": 10000, "level": 9},
    "مشاور سرمایه‌گذاری": {"salary": 11500, "price": 11000, "level": 9},
    "کارشناس ارشد مالی": {"salary": 9800, "price": 9300, "level": 9},
    "تحلیلگر ریسک": {"salary": 10200, "price": 9700, "level": 9},
    "مدیر صندوق": {"salary": 12000, "price": 11500, "level": 9},
    "تاجر": {"salary": 12500, "price": 12000, "level": 9},
    
    # سطح 10 (حقوق ۲۰۰۰۰ سقف)
    "سیاستمدار": {"salary": 15000, "price": 14500, "level": 10},
    "سفیر": {"salary": 16000, "price": 15500, "level": 10},
    "وزیر": {"salary": 17500, "price": 17000, "level": 10},
    "نماینده مجلس": {"salary": 16500, "price": 16000, "level": 10},
    "استاد دانشگاه": {"salary": 14000, "price": 13500, "level": 10},
    "پژوهشگر ارشد": {"salary": 14500, "price": 14000, "level": 10},
    "دانشمند": {"salary": 18000, "price": 17500, "level": 10},
    "مخترع": {"salary": 17000, "price": 16500, "level": 10},
    "مدیرعامل شرکت بزرگ": {"salary": 19000, "price": 18500, "level": 10},
    "بیزینس من": {"salary": 20000, "price": 19500, "level": 10},
}

SHIELDS = {
    "سپر عادی": {"count": 3, "price": 1000},
    "سپر برنزی": {"count": 5, "price": 1500},
    "سپر نقره‌ای": {"count": 10, "price": 3000},
    "سپر طلایی": {"count": 20, "price": 5000},
    "سپر الماسی": {"count": 50, "price": 10000},
}

MINING_FARMS = {
    "مزرعه معمولی": {"hourly_profit": 75, "price": 2000, "level": 1},
    "مزرعه پیشرفته": {"hourly_profit": 200, "price": 8000, "level": 2},
    "مزرعه صنعتی": {"hourly_profit": 500, "price": 25000, "level": 3},
    "مزرعه ابرقدرت": {"hourly_profit": 1500, "price": 100000, "level": 4},
}

# ======================= منوهای کامل (با تعریف همه keypadها) =======================
main_keypad = (
    ChatKeypadBuilder()
    .row(ChatKeypadBuilder().button("help", "🌟 راهنما و اطلاعات"))
    .row(
        ChatKeypadBuilder().button("profile", "👤 پروفایل من"),
        ChatKeypadBuilder().button("balance", "💰 کیف پول من")
    )
    .row(
        ChatKeypadBuilder().button("daily_luck", "🍀 شانس امروز"),
        ChatKeypadBuilder().button("referral", "🤝 شراکت و دعوت")
    )
    .row(
        ChatKeypadBuilder().button("games", "🎮 شرط‌بندی و بازی‌ها"),
        ChatKeypadBuilder().button("mining", "⛏️ مزرعه استخراج")
    )
    .row(
        ChatKeypadBuilder().button("jobs", "💼 استخدام و کار"),
        ChatKeypadBuilder().button("bank", "🏦 بانک و سرمایه‌گذاری")
    )
    .row(
        ChatKeypadBuilder().button("mafia", "🥷 عملیات مخفی (دزدی)"),
        ChatKeypadBuilder().button("top", "🏆 رتبه‌بندی هفتگی")
    )
    .row(
        ChatKeypadBuilder().button("setname", "✏️ تغییر نام"),
        ChatKeypadBuilder().button("transfer", "💸 انتقال وجه")
    )
    .build()
)

jobs_keypad = (
    ChatKeypadBuilder()
    .row(ChatKeypadBuilder().button("job_list", "📋 لیست مشاغل (۸۰ شغل)"))
    .row(ChatKeypadBuilder().button("my_job", "💼 شغل من"))
    .row(ChatKeypadBuilder().button("resign_job", "❌ استعفا و حذف شغل"))
    .row(ChatKeypadBuilder().button("back", "🔙 منوی اصلی"))
    .build()
)

games_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button("slot_help", "🎰 اسلات (Slot)"),
        ChatKeypadBuilder().button("roulette_help", "🎯 رولت روسی")
    )
    .row(
        ChatKeypadBuilder().button("casino_numbers_help", "🎲 کازینوی اعداد"),
        ChatKeypadBuilder().button("rps_help", "✂️ سنگ/کاغذ/قیچی")
    )
    .row(
        ChatKeypadBuilder().button("risk_help", "⚡ ریسک (تخم مرغ)"),
        ChatKeypadBuilder().button("wheel", "🎡 گردونه شانس")
    )
    .row(ChatKeypadBuilder().button("back", "🔙 منوی اصلی"))
    .build()
)

mafia_keypad = (
    ChatKeypadBuilder()
    .row(ChatKeypadBuilder().button("steal", "🗺️ دزدی از کاربر"))
    .row(ChatKeypadBuilder().button("buy_shield", "🛡️ خرید سپر"))
    .row(ChatKeypadBuilder().button("my_shield", "🔒 وضعیت سپر من"))
    .row(ChatKeypadBuilder().button("back", "🔙 منوی اصلی"))
    .build()
)

bank_keypad = (
    ChatKeypadBuilder()
    .row(ChatKeypadBuilder().button("bank_info", "📊 اطلاعات بانک"))
    .row(
        ChatKeypadBuilder().button("deposit", "💰 واریز به بانک"),
        ChatKeypadBuilder().button("withdraw", "🏧 برداشت از بانک")
    )
    .row(ChatKeypadBuilder().button("back", "🔙 منوی اصلی"))
    .build()
)

admin_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button("admin_add_money", "💰 افزودن پول به کاربر"),
        ChatKeypadBuilder().button("admin_remove_money", "💸 کم کردن پول کاربر")
    )
    .row(
        ChatKeypadBuilder().button("admin_take_assets", "🏦 گرفتن دارایی کاربر"),
        ChatKeypadBuilder().button("admin_set_job", "💼 تنظیم شغل")
    )
    .row(
        ChatKeypadBuilder().button("admin_remove_job", "❌ حذف شغل کاربر"),
        ChatKeypadBuilder().button("admin_set_shield", "🛡️ تنظیم سپر")
    )
    .row(
        ChatKeypadBuilder().button("admin_broadcast", "📢 ارسال پیام همگانی"),
        ChatKeypadBuilder().button("admin_weekly_reset", "🔄 ریست مسابقه هفتگی")
    )
    .row(
        ChatKeypadBuilder().button("admin_stats", "📈 آمار پیشرفته"),
        ChatKeypadBuilder().button("admin_reset_user", "🗑️ ریست کامل کاربر")
    )
    .row(ChatKeypadBuilder().button("back", "🔙 منوی اصلی"))
    .build()
)

back_keypad = ChatKeypadBuilder().row(ChatKeypadBuilder().button("back", "🔙 منوی اصلی")).build()

# ======================= توابع کمکی =======================
def save_data():
    data = {"users": users_db, "bans": ban_list}
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    global users_db, ban_list
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            users_db = data.get("users", {})
            ban_list = data.get("bans", [])

def format_number(num):
    if num is None:
        return "0"
    num = int(float(num))
    return f"{num:,}"

def init_user(uid, referrer_id=None):
    if uid not in users_db:
        now = time()
        users_db[uid] = {
            "name": f"کاربر{uid[-4:]}",
            "cash": 1000,
            "bank": 0,
            "job": None,
            "shield": 1,
            "wins": 0,
            "losses": 0,
            "steals_success": 0,
            "steals_fail": 0,
            "total_gambled": 0,
            "last_salary": 0,
            "in_jail": 0,
            "is_admin": False,
            "referrer": referrer_id,
            "referrals": [],
            "mining_farm": None,
            "mining_last_collect": 0,
            "daily_luck": 1.0,
            "last_luck_update": 0,
            "weekly_rank_bonus": 0,
            "total_stolen": 0
        }
        
        if referrer_id and referrer_id in users_db:
            bonus = 500
            users_db[referrer_id]["cash"] += bonus
            if uid not in users_db[referrer_id]["referrals"]:
                users_db[referrer_id]["referrals"].append(uid)
            save_data()
            asyncio.create_task(send(referrer_id, f"🎉 شما {users_db[uid]['name']} را دعوت کردید و {format_number(bonus)} تومان پاداش گرفتید!"))
    
    # به‌روزرسانی شانس روزانه
    if users_db[uid]["last_luck_update"] < (time() - 86400):
        luck_types = [0.5, 0.8, 1.0, 1.2, 1.5, 2.0]
        users_db[uid]["daily_luck"] = random.choice(luck_types)
        users_db[uid]["last_luck_update"] = time()
        save_data()
    
    return users_db[uid]

async def send(uid, text, keypad=None, inline=None):
    try:
        if keypad and inline:
            await bot.send_message(uid, text, chat_keypad=keypad, inline_keypad=inline)
        elif keypad:
            await bot.send_message(uid, text, chat_keypad=keypad)
        elif inline:
            await bot.send_message(uid, text, inline_keypad=inline)
        else:
            await bot.send_message(uid, text)
    except:
        pass

# ======================= هندلرهای اصلی =======================
@bot.on_message()
async def start_handler(_, message: Message):
    uid = str(message.chat_id)
    text = message.text or ""
    
    if text.startswith("/start"):
        ref_id = None
        if len(text.split()) > 1:
            ref_id = text.split()[1]
        init_user(uid, ref_id)
        await send(uid, 
            "🔥🔥 **به ابر ربات اقتصاد و ثروت خوش آمدید!** 🔥🔥\n\n"
            "⚡ اینجا فقط یه بات ساده نیست، یه **امپراتوری مالی**ه!\n"
            "💰 با دعوت از دوستان، ماینینگ، دزدی و سرمایه‌گذاری، ثروتمندترین فرد روبیکا شو!\n\n"
            "⚠️ **هشدار**: بعضی از آدم‌ها اینجا فقط منتظر یه اشتباه از طرف شما هستند...\n"
            "📞 پشتیبانی و ایده‌های جدید: @closeIntheworld\n\n"
            "🔥 **برای شروع، یکی از دکمه‌های پایین رو بزن!** 🔥",
            main_keypad
        )

@bot.on_message()
async def admin_command_handler(_, message: Message):
    uid = str(message.chat_id)
    user = init_user(uid)
    
    if message.text == "/admin" and user.get("is_admin"):
        await send(uid, "🛠️ **پنل مدیریت پیشرفته**", admin_keypad)

@bot.on_message()
async def main_handler(_, message: Message):
    uid = str(message.chat_id)
    text = message.text or ""
    user = init_user(uid)
    
    if uid in ban_list:
        return
    
    if user["in_jail"] > 0:
        await send(uid, f"🚫 **شما در زندان هستید!**\n⏳ {user['in_jail']} روز باقی مانده.\n💸 هیچ فعالیتی (دزدی، قمار، کار) ممکن نیست.", back_keypad)
        return
    
    # فعال‌سازی ادمین با کد مخفی
    if text == "ADMINBOTCODETANSARIAN" and not user.get("is_admin"):
        user["is_admin"] = True
        user["shield"] = 999
        user["job"] = "ادمین بات"
        save_data()
        await send(uid, "✅ **شما به عنوان ادمین کل سیستم تایید شدید!**\n🛡️ سپر نامحدود دریافت کردید.", admin_keypad)
        return
    
    if text == "🔙 منوی اصلی" or text == "back" or text == "🔙 بازگشت":
        user_states[uid] = None
        await send(uid, "🏠 **منوی اصلی:**", main_keypad)
        return
    
    # ========== راهنما ==========
    if text == "help" or text == "🌟 راهنما و اطلاعات":
        help_text = (
            "📚 **راهنمای سریع بات ثروت**\n"
            "⭐️ ═══════════════ ⭐️\n"
            "💸 **انتقال وجه:** از منوی اصلی، گزینه انتقال وجه رو بزن.\n"
            "💰 **شارژ کیف پول:** از بخش بانک، پولتو به حساب واریز کن.\n"
            "🥷 **دزدی:** از بخش مافیا، آدی قربانی رو بده.\n"
            "🛡️ **سپر:** از بخش مافیا می‌تونی سپر بخری.\n"
            "⛏️ **ماینینگ:** یه مزرعه بخر و هر ساعت سود بگیر.\n"
            "🎮 **بازی‌ها:** اسلات، رولت، کازینو اعداد و سنگ کاغذ قیچی\n"
            "🍀 **شانس روزانه:** هر روز شانست عوض میشه.\n"
            "🤝 **دعوت از دوستان:** از بخش شراکت لینک بده.\n"
            "⭐️ ═══════════════ ⭐️"
        )
        await send(uid, help_text, main_keypad)
        return
    
    # ========== پروفایل ==========
    if text == "👤 پروفایل من":
        job_name = user["job"] if user["job"] else "🚫 بیکار"
        shield_text = "❌ ندارد" if user["shield"] == 0 else f"🛡️ {user['shield']} عدد"
        admin_tag = " 👑" if user.get("is_admin") else ""
        farming = user["mining_farm"] if user["mining_farm"] else "❌ ندارد"
        
        text_profile = (
            f"📸 **پروفایل شما** {admin_tag}\n"
            f"⭐️ ═══════════════ ⭐️\n"
            f"📛 **نام:** {user['name']}\n"
            f"🆔 **آیدی:** `{uid}`\n"
            f"💵 **موجودی:** {format_number(user['cash'])} تومان\n"
            f"🏦 **بانک:** {format_number(user['bank'])} تومان\n"
            f"💼 **شغل:** {job_name}\n"
            f"🛡️ **سپر:** {shield_text}\n"
            f"⛏️ **مزرعه:** {farming}\n"
            f"🍀 **شانس:** {user['daily_luck']}x\n"
            f"🏆 **برد:** {user['wins']} | **باخت:** {user['losses']}\n"
            f"🥷 **دزدی موفق:** {user['steals_success']} | **ناموفق:** {user['steals_fail']}\n"
            f"⭐️ ═══════════════ ⭐️"
        )
        await send(uid, text_profile, main_keypad)
        return
    
    # ========== موجودی ==========
    if text == "💰 کیف پول من":
        text_balance = (
            f"💰 **کیف پول شما**\n"
            f"⭐️ ═══════════════ ⭐️\n"
            f"💵 **نقد:** {format_number(user['cash'])} تومان\n"
            f"🏦 **بانک:** {format_number(user['bank'])} تومان\n"
            f"💎 **مجموع:** {format_number(user['cash'] + user['bank'])} تومان\n"
            f"📊 **کل شرط:** {format_number(user['total_gambled'])} تومان\n"
            f"⭐️ ═══════════════ ⭐️"
        )
        await send(uid, text_balance, main_keypad)
        return
    
    # ========== شانس روزانه ==========
    if text == "🍀 شانس امروز":
        luck_desc = {
            0.5: "💀 بدشانس مطلق",
            0.8: "😞 نسبتاً بدشانس",
            1.0: "😐 معمولی",
            1.2: "🙂 خوش شانس",
            1.5: "😍 خیلی خوش شانس",
            2.0: "🤯 افسانه‌ای!!!"
        }
        await send(uid, f"🍀 **شانس امروز:** {luck_desc.get(user['daily_luck'], 'معمولی')}\n✨ روی برد دزدی، قمار و ماینینگ تأثیر دارد!", main_keypad)
        return
    
    # ========== شراکت ==========
    if text == "🤝 شراکت و دعوت":
        referral_link = f"https://rubika.ir/join?start={uid}"
        text_ref = (
            f"🤝 **سیستم شراکت**\n⭐️ ═══════════════ ⭐️\n"
            f"🔗 **لینک دعوت:**\n`{referral_link}`\n\n"
            f"✨ **مزایا:**\n• ۵۰۰ تومان پاداش به ازای هر دعوت\n• ۵٪ از درآمد دوستانت\n\n"
            f"👥 **دعوت شده‌ها:** {len(user['referrals'])} نفر\n"
            f"⭐️ ═══════════════ ⭐️"
        )
        await send(uid, text_ref, main_keypad)
        return
    
    # ========== رتبه‌بندی ==========
    if text == "🏆 رتبه‌بندی هفتگی":
        sorted_users = sorted(users_db.items(), key=lambda x: x[1]["cash"] + x[1]["bank"], reverse=True)[:5]
        text_top = "🏆 **برترین ثروتمندان هفته**\n⭐️ ═══════════════ ⭐️\n"
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        for i, (uid_, u) in enumerate(sorted_users):
            total = u["cash"] + u["bank"]
            text_top += f"{medals[i]} **{u['name']}** : {format_number(total)} تومان\n"
        await send(uid, text_top, main_keypad)
        return
    
    # ========== تغییر نام ==========
    if text == "✏️ تغییر نام":
        user_states[uid] = "awaiting_name"
        await send(uid, "✏️ **اسم جدیدت رو بفرست (حداقل ۲ حرف):**", back_keypad)
        return
    
    # ========== مشاغل ==========
    if text == "💼 استخدام و کار":
        await send(uid, "💼 **بازار کار و استخدام**\nاز منوی زیر انتخاب کن:", jobs_keypad)
        return
    
    if text == "📋 لیست مشاغل (۸۰ شغل)":
        text_jobs = "📋 **لیست ۸۰ شغل موجود**\n⭐️ ═══════════════ ⭐️\n"
        for job, info in sorted(JOBS.items(), key=lambda x: x[1]["level"]):
            status = " ✅ (شغل فعلی)" if user["job"] == job else ""
            cost_text = "رایگان" if info.get("price", 0) == 0 else f"{format_number(info['price'])} تومان"
            text_jobs += f"• **{job}** | حقوق: {format_number(info['salary'])} | هزینه: {cost_text}{status}\n"
        text_jobs += "\n📝 **برای استخدام:** استخدام [نام شغل]\nمثال: استخدام تاجر"
        await send(uid, text_jobs, jobs_keypad)
        return
    
    if text == "💼 شغل من":
        if user["job"] and user["job"] in JOBS:
            salary = JOBS[user["job"]]["salary"]
            last_time = user.get("last_salary", 0)
            remaining = max(0, 3600 - (time() - last_time))
            minutes = remaining // 60
            text_myjob = (
                f"💼 **شغل شما:** {user['job']}\n"
                f"💰 **حقوق روزانه:** {format_number(salary)} تومان\n"
            )
            if remaining > 0:
                text_myjob += f"⏳ تا حقوق بعدی: {minutes} دقیقه"
            else:
                text_myjob += f"✅ می‌توانید با دستور `حقوق` دریافت کنید!"
        else:
            text_myjob = "❌ شما شغلی ندارید!\nاز لیست مشاغل یکی انتخاب کنید."
        await send(uid, text_myjob, jobs_keypad)
        return
    
    if text == "❌ استعفا و حذف شغل":
        if user["job"]:
            user["job"] = None
            save_data()
            await send(uid, "✅ شما از شغل خود استعفا دادید و الان بیکار هستید!", jobs_keypad)
        else:
            await send(uid, "❌ شما شغلی ندارید که استعفا بدید!", jobs_keypad)
        return
    
    if text.startswith("استخدام "):
        job_name = text.replace("استخدام ", "")
        if user.get("is_admin"):
            await send(uid, "❌ شما ادمین هستید!", main_keypad)
            return
        if user["job"]:
            await send(uid, "❌ شما قبلاً شغل دارید! اول استعفا بدید (❌ استعفا و حذف شغل)", jobs_keypad)
            return
        if job_name not in JOBS:
            await send(uid, "❌ این شغل وجود ندارد!", jobs_keypad)
            return
        
        job_info = JOBS[job_name]
        job_price = job_info.get("price", 0)
        if job_price > 0:
            if user["cash"] < job_price:
                await send(uid, f"❌ برای استخدام نیاز به {format_number(job_price)} تومان داری!", jobs_keypad)
                return
            user["cash"] -= job_price
        user["job"] = job_name
        save_data()
        await send(uid, f"✅ **تبریک!** تو الان یک {job_name} هستی.\n💰 حقوق روزانه: {format_number(job_info['salary'])} تومان", jobs_keypad)
        return
    
    if text == "حقوق":
        if user["job"] and user["job"] in JOBS:
            salary = JOBS[user["job"]]["salary"]
            if time() - user.get("last_salary", 0) >= 3600:
                user["cash"] += salary
                user["last_salary"] = time()
                save_data()
                await send(uid, f"✅ حقوق {format_number(salary)} تومانی تو واریز شد!", main_keypad)
            else:
                remain = 3600 - (time() - user["last_salary"])
                await send(uid, f"⏳ {int(remain//60)} دقیقه دیگه بیا حقوق بگیر.", main_keypad)
        else:
            await send(uid, "❌ تو که بیکاری! اول یه شغل استخدام شو.", jobs_keypad)
        return
    
    # ========== بانک ==========
    if text == "🏦 بانک و سرمایه‌گذاری":
        await send(uid, "🏦 **سیستم بانکی**\nاز منوی زیر انتخاب کن:", bank_keypad)
        return
    
    if text == "📊 اطلاعات بانک":
        await send(uid, f"🏦 **اطلاعات بانکی شما**\n⭐️ ═══════════════ ⭐️\n💰 نقد: {format_number(user['cash'])}\n🏦 بانک: {format_number(user['bank'])}\n💎 مجموع: {format_number(user['cash'] + user['bank'])}", bank_keypad)
        return
    
    if text == "💰 واریز به بانک":
        user_states[uid] = "awaiting_deposit"
        await send(uid, "💰 **مبلغ واریز به بانک رو بفرست:**", bank_keypad)
        return
    
    if text == "🏧 برداشت از بانک":
        user_states[uid] = "awaiting_withdraw"
        await send(uid, "🏧 **مبلغ برداشت از بانک رو بفرست:**", bank_keypad)
        return
    
    # ========== بازی‌ها ==========
    if text == "🎮 شرط‌بندی و بازی‌ها":
        await send(uid, "🎮 **بازی‌های کازینویی**\nاز منوی زیر انتخاب کن:", games_keypad)
        return
    
    if text == "🎰 اسلات (Slot)":
        await send(uid, "🎰 **بازی اسلات**\n📝 فرمت: `اسلات [مبلغ]`\nمثال: اسلات 100\n\n🎁 برنده شدن با سه علامت یکسان = ۱۰x\nدو علامت یکسان = ۲x", games_keypad)
        return
    
    if text == "🎯 رولت روسی":
        await send(uid, "🎯 **رولت روسی**\n📝 فرمت: `رولت [مبلغ]`\nمثال: رولت 500\n\n💥 شانس ۱ از ۶ برای برنده شدن ۶x", games_keypad)
        return
    
    if text == "🎲 کازینوی اعداد":
        await send(uid, "🎲 **کازینوی اعداد**\n📝 فرمت: `بازی اعداد [1-10] [مبلغ]`\nمثال: بازی اعداد 5 100\n\n🎁 ضریب‌ها:\n• حدس دقیق = ۱۰x\n• اختلاف ۱ عدد = ۳x\n• اختلاف ۲ عدد = ۱.۵x", games_keypad)
        return
    
    if text == "✂️ سنگ/کاغذ/قیچی":
        await send(uid, "✂️ **سنگ/کاغذ/قیچی**\n📝 فرمت: `rps [سنگ/کاغذ/قیچی] [مبلغ]`\nمثال: rps سنگ 100", games_keypad)
        return
    
    if text == "⚡ ریسک (تخم مرغ)":
        await send(uid, "⚡ **بازی ریسک**\n📝 فرمت: `ریسک [مبلغ]`\nمثال: ریسک 200\n\n🎁 شانس ۲۲٪ برای برد ۳x", games_keypad)
        return
    
    if text == "🎡 گردونه شانس":
        amounts = [-500, -200, -100, 0, 50, 100, 200, 500, 1000, 2000]
        result = random.choice(amounts)
        result = int(result * user["daily_luck"])
        if result > 0:
            user["cash"] += result
            user["wins"] += 1
        elif result < 0:
            user["cash"] += result
            user["losses"] += 1
        save_data()
        if result > 0:
            await send(uid, f"🎡 **گردونه شانس:** +{format_number(result)} تومان!\n💰 موجودی: {format_number(user['cash'])}", games_keypad)
        elif result < 0:
            await send(uid, f"🎡 **گردونه شانس:** {format_number(result)} تومان!\n💰 موجودی: {format_number(user['cash'])}", games_keypad)
        else:
            await send(uid, "🎡 **گردونه شانس:** هیچی! دوباره امتحان کن.", games_keypad)
        return
    
    # ========== بازی‌های عملیاتی ==========
    if text.startswith("اسلات "):
        try:
            amount = int(text.split()[1])
            if amount <= 0 or amount > user["cash"]:
                await send(uid, "❌ مبلغ نامعتبر!", games_keypad)
                return
            user["cash"] -= amount
            user["total_gambled"] += amount
            symbols = ["🍒", "🍋", "🍇", "⭐", "💎", "7️⃣"]
            result = [random.choice(symbols) for _ in range(3)]
            win = 0
            if result[0] == result[1] == result[2]:
                win = int(amount * 10 * user["daily_luck"])
                user["wins"] += 1
            elif result[0] == result[1] or result[1] == result[2]:
                win = int(amount * 2 * user["daily_luck"])
                user["wins"] += 1
            else:
                user["losses"] += 1
            if win > 0:
                user["cash"] += win
                await send(uid, f"🎰 {' '.join(result)}\n🎉 **برد {format_number(win)} تومانی!** (شانس {user['daily_luck']}x)", games_keypad)
            else:
                await send(uid, f"🎰 {' '.join(result)}\n😢 باختی! {format_number(amount)} تومان ریخت.", games_keypad)
            save_data()
        except:
            await send(uid, "❌ فرمت: `اسلات 100`", games_keypad)
        return
    
    if text.startswith("رولت "):
        try:
            amount = int(text.split()[1])
            if amount <= 0 or amount > user["cash"]:
                await send(uid, "❌ مبلغ نامعتبر!", games_keypad)
                return
            user["cash"] -= amount
            user["total_gambled"] += amount
            if random.randint(1, 6) == 1:
                win = int(amount * 6 * user["daily_luck"])
                user["cash"] += win
                user["wins"] += 1
                await send(uid, f"💥 **رولت روسی:** برد! {format_number(win)} تومان بردی!", games_keypad)
            else:
                user["losses"] += 1
                await send(uid, f"🔫 **رولت روسی:** باختی! {format_number(amount)} تومان ریخت.", games_keypad)
            save_data()
        except:
            await send(uid, "❌ فرمت: `رولت 500`", games_keypad)
        return
    
    if text.startswith("بازی اعداد "):
        parts = text.split()
        if len(parts) != 3:
            await send(uid, "❌ فرمت: `بازی اعداد [1-10] [مبلغ]`", games_keypad)
            return
        try:
            guess = int(parts[1])
            amount = int(parts[2])
            if guess < 1 or guess > 10:
                await send(uid, "❌ عدد باید بین ۱ تا ۱۰ باشه!", games_keypad)
                return
            if amount <= 0 or amount > user["cash"]:
                await send(uid, "❌ مبلغ نامعتبر!", games_keypad)
                return
            user["cash"] -= amount
            user["total_gambled"] += amount
            lucky = random.randint(1, 10)
            multiplier = 0
            if guess == lucky:
                multiplier = 10
            elif abs(guess - lucky) == 1:
                multiplier = 3
            elif abs(guess - lucky) == 2:
                multiplier = 1.5
            if multiplier > 0:
                win = int(amount * multiplier * user["daily_luck"])
                user["cash"] += win
                user["wins"] += 1
                await send(uid, f"🎲 **عدد برنده:** {lucky}\n✅ برد {format_number(win)} تومانی! (ضریب {multiplier}x)", games_keypad)
            else:
                user["losses"] += 1
                await send(uid, f"🎲 **عدد برنده:** {lucky}\n❌ باختی! {format_number(amount)} تومان", games_keypad)
            save_data()
        except:
            await send(uid, "❌ لطفاً اعداد رو درست وارد کن!", games_keypad)
        return
    
    if text.startswith("rps "):
        parts = text.split()
        if len(parts) != 3:
            await send(uid, "❌ فرمت: `rps [سنگ/کاغذ/قیچی] [مبلغ]`", games_keypad)
            return
        choice_map = {"سنگ": 0, "کاغذ": 1, "قیچی": 2}
        user_choice = parts[1]
        if user_choice not in choice_map:
            await send(uid, "❌ انتخاب نامعتبر!", games_keypad)
            return
        try:
            amount = int(parts[2])
            if amount <= 0 or amount > user["cash"]:
                await send(uid, "❌ مبلغ نامعتبر!", games_keypad)
                return
            user["cash"] -= amount
            user["total_gambled"] += amount
            bot_choice = random.choice(list(choice_map.keys()))
            wins = {("سنگ", "قیچی"), ("کاغذ", "سنگ"), ("قیچی", "کاغذ")}
            if user_choice == bot_choice:
                user["cash"] += amount
                await send(uid, f"🎮 شما: {user_choice} | بات: {bot_choice}\n🤝 مساوی! پولت برگشت.", games_keypad)
            elif (user_choice, bot_choice) in wins:
                win = int(amount * 2 * user["daily_luck"])
                user["cash"] += win
                user["wins"] += 1
                await send(uid, f"🎮 شما: {user_choice} | بات: {bot_choice}\n✅ برد {format_number(win)} تومانی!", games_keypad)
            else:
                user["losses"] += 1
                await send(uid, f"🎮 شما: {user_choice} | بات: {bot_choice}\n❌ باختی! {format_number(amount)} تومان", games_keypad)
            save_data()
        except:
            await send(uid, "❌ فرمت صحیح نیست!", games_keypad)
        return
    
    if text.startswith("ریسک "):
        try:
            amount = int(text.split()[1])
            if amount <= 0 or amount > user["cash"]:
                await send(uid, "❌ مبلغ نامعتبر!", games_keypad)
                return
            user["cash"] -= amount
            user["total_gambled"] += amount
            chance = random.random()
            if chance < 0.22:
                win = int(amount * 3 * user["daily_luck"])
                user["cash"] += win
                user["wins"] += 1
                await send(uid, f"⚡ **ریسک:** برد! {format_number(win)} تومان بردی!", games_keypad)
            elif chance < 0.33:
                user["cash"] += amount
                await send(uid, f"⚡ **ریسک:** مساوی! پولت برگشت.", games_keypad)
            else:
                user["losses"] += 1
                await send(uid, f"⚡ **ریسک:** باختی! {format_number(amount)} تومان ریخت.", games_keypad)
            save_data()
        except:
            await send(uid, "❌ فرمت: `ریسک 200`", games_keypad)
        return
    
    # ========== مافیا و دزدی ==========
    if text == "🥷 عملیات مخفی (دزدی)":
        await send(uid, "🥷 **کارتل مافیا**\nاز منوی زیر انتخاب کن:", mafia_keypad)
        return
    
    if text == "🗺️ دزدی از کاربر":
        user_states[uid] = "awaiting_steal_uid"
        await send(uid, "🕵️‍♂️ **آیدی عددی قربانی رو بفرست:**", mafia_keypad)
        return
    
    if text == "🛡️ خرید سپر":
        text_shield = "🛡️ **خرید سپر دفاعی**\n⭐️ ═══════════════ ⭐️\n"
        for name, info in SHIELDS.items():
            text_shield += f"• {name}: {info['count']} عدد | {format_number(info['price'])} تومان\n"
        text_shield += "\n📝 مثال: `خرید سپر عادی`"
        await send(uid, text_shield, mafia_keypad)
        return
    
    if text.startswith("خرید سپر "):
        shield_name = text.replace("خرید سپر ", "")
        if shield_name not in SHIELDS:
            await send(uid, "❌ اسم سپر اشتباهه!", mafia_keypad)
            return
        price = SHIELDS[shield_name]["price"]
        if user["cash"] < price:
            await send(uid, f"❌ پول کافی نداری! نیاز به {format_number(price)} تومان داری.", mafia_keypad)
            return
        user["cash"] -= price
        user["shield"] += SHIELDS[shield_name]["count"]
        save_data()
        await send(uid, f"✅ {shield_name} خریداری شد! {SHIELDS[shield_name]['count']} عدد سپر به تو اضافه شد.", mafia_keypad)
        return
    
    if text == "🔒 وضعیت سپر من":
        await send(uid, f"🛡️ **سپر شما:** {user['shield']} عدد باقی مونده\n💡 هر سپر می‌تونه یک بار دزدی رو دفع کنه.", mafia_keypad)
        return
    
    # ========== ماینینگ ==========
    if text == "⛏️ مزرعه استخراج":
        text_farm = f"⛏️ **مزرعه استخراج**\n⭐️ ═══════════════ ⭐️\n"
        if user["mining_farm"]:
            profit = MINING_FARMS[user["mining_farm"]]["hourly_profit"]
            last = user["mining_last_collect"]
            if time() - last >= 3600:
                text_farm += f"✅ مزرعه {user['mining_farm']} آماده برداشت!\n💰 سود هر ساعت: {format_number(profit)} تومان\n\n🔽 با دکمه `برداشت سود ماین` سودتو بگیر."
            else:
                remain = 3600 - (time() - last)
                text_farm += f"⏳ مزرعه {user['mining_farm']} در حال کار...\n⏰ تا سود بعدی: {int(remain//60)} دقیقه"
        else:
            text_farm += "❌ مزرعه نداری!\n\n**مزارع قابل خرید:**\n"
            for name, info in MINING_FARMS.items():
                text_farm += f"• {name}: {format_number(info['hourly_profit'])} تومان/ساعت | قیمت: {format_number(info['price'])} تومان\n"
            text_farm += "\n📝 مثال: `خرید مزرعه معمولی`"
        await send(uid, text_farm, main_keypad)
        return
    
    if text.startswith("خرید مزرعه "):
        farm_name = text.replace("خرید مزرعه ", "")
        if farm_name not in MINING_FARMS:
            await send(uid, "❌ مزرعه مورد نظر یافت نشد!", main_keypad)
            return
        if user["mining_farm"]:
            await send(uid, "❌ تو قبلاً یه مزرعه داری!", main_keypad)
            return
        price = MINING_FARMS[farm_name]["price"]
        if user["cash"] < price:
            await send(uid, f"❌ پول کافی نداری! {format_number(price)} تومان لازمه.", main_keypad)
            return
        user["cash"] -= price
        user["mining_farm"] = farm_name
        user["mining_last_collect"] = time()
        save_data()
        await send(uid, f"✅ **تبریک!** تو صاحب یک {farm_name} شدی.\n💰 هر ساعت {format_number(MINING_FARMS[farm_name]['hourly_profit'])} تومان سود می‌گیری!", main_keypad)
        return
    
    if text == "برداشت سود ماین":
        if not user["mining_farm"]:
            await send(uid, "❌ مزرعه‌ای نداری!", main_keypad)
            return
        if time() - user["mining_last_collect"] >= 3600:
            profit = int(MINING_FARMS[user["mining_farm"]]["hourly_profit"] * user["daily_luck"])
            user["cash"] += profit
            user["mining_last_collect"] = time()
            save_data()
            await send(uid, f"✅ {format_number(profit)} تومان از مزرعه استخراج کردی! (با شانس {user['daily_luck']}x)", main_keypad)
        else:
            remain = 3600 - (time() - user["mining_last_collect"])
            await send(uid, f"⏳ مزرعه هنوز کار می‌کنه! {int(remain//60)} دقیقه دیگه بیا.", main_keypad)
        return
    
    # ========== انتقال وجه ==========
    if text == "💸 انتقال وجه":
        user_states[uid] = "awaiting_transfer_uid"
        await send(uid, "💸 **آیدی عددی دریافت‌کننده رو بفرست:**", main_keypad)
        return
    
    # ========== پردازش وضعیت‌ها ==========
    state = user_states.get(uid)
    
    if state == "awaiting_name":
        new_name = text.strip()
        if len(new_name) < 2:
            await send(uid, "❌ اسم باید حداقل ۲ حرف باشه.", back_keypad)
            return
        name_exists = any(u.get("name", "").lower() == new_name.lower() and u_id != uid for u_id, u in users_db.items())
        if name_exists:
            await send(uid, "❌ این اسم قبلاً توسط کس دیگه‌ای استفاده شده!", back_keypad)
            return
        user["name"] = new_name
        save_data()
        await send(uid, f"✅ اسمت به **{new_name}** تغییر کرد.", main_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_deposit":
        try:
            amount = int(text)
            if amount <= 0 or amount > user["cash"]:
                await send(uid, "❌ مبلغ نامعتبر!", bank_keypad)
                return
            user["cash"] -= amount
            user["bank"] += amount
            save_data()
            await send(uid, f"✅ {format_number(amount)} تومان به بانک واریز شد.", bank_keypad)
        except:
            await send(uid, "❌ لطفاً عدد معتبر وارد کن!", bank_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_withdraw":
        try:
            amount = int(text)
            if amount <= 0 or amount > user["bank"]:
                await send(uid, "❌ مبلغ نامعتبر!", bank_keypad)
                return
            user["bank"] -= amount
            user["cash"] += amount
            save_data()
            await send(uid, f"✅ {format_number(amount)} تومان از بانک برداشت شد.", bank_keypad)
        except:
            await send(uid, "❌ لطفاً عدد معتبر وارد کن!", bank_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_transfer_uid":
        target_uid = text.strip()
        if target_uid == uid:
            await send(uid, "❌ نمی‌تونی به خودت پول بدی!", main_keypad)
            user_states[uid] = None
            return
        if target_uid not in users_db:
            await send(uid, "❌ کاربر مورد نظر یافت نشد!", main_keypad)
            user_states[uid] = None
            return
        user_states[uid] = f"transfer_to:{target_uid}"
        await send(uid, f"💸 **مبلغ انتقال به {users_db[target_uid]['name']} رو بفرست:**", main_keypad)
        return
    
    if state and state.startswith("transfer_to:"):
        target_uid = state.split(":")[1]
        try:
            amount = int(text)
            if amount <= 0 or amount > user["cash"]:
                await send(uid, "❌ مبلغ نامعتبر!", main_keypad)
                user_states[uid] = None
                return
            target = users_db[target_uid]
            user["cash"] -= amount
            target["cash"] += amount
            save_data()
            await send(uid, f"✅ {format_number(amount)} تومان به {target['name']} ارسال شد.", main_keypad)
            await send(target_uid, f"💰 شما {format_number(amount)} تومان از {user['name']} دریافت کردید.", main_keypad)
        except:
            await send(uid, "❌ لطفاً عدد معتبر وارد کن!", main_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_steal_uid":
        target_uid = text.strip()
        if target_uid == uid:
            await send(uid, "❌ نمی‌تونی از خودت بدزدی!", mafia_keypad)
            user_states[uid] = None
            return
        if target_uid not in users_db:
            await send(uid, "❌ کاربر مورد نظر یافت نشد!", mafia_keypad)
            user_states[uid] = None
            return
        
        target = users_db[target_uid]
        steal_chance = 0.4 * user["daily_luck"]
        
        if target["shield"] > 0:
            target["shield"] -= 1
            user["steals_fail"] += 1
            await send(uid, "🛡️ **دزدی ناموفق!** قربانی سپر داشت.", mafia_keypad)
            if random.random() < 0.3:
                user["in_jail"] = random.randint(1, 3)
                await send(uid, f"🚔 پلیس تو دستگیر کرد! {user['in_jail']} روز در زندان می‌مونی.", mafia_keypad)
        else:
            steal_amount = min(target["cash"], random.randint(100, max(500, int(target["cash"] * 0.2))))
            if random.random() < steal_chance:
                target["cash"] -= steal_amount
                user["cash"] += steal_amount
                user["steals_success"] += 1
                user["total_stolen"] += steal_amount
                await send(uid, f"🥷 **دزدی موفق!** {format_number(steal_amount)} تومان دزدیدی!", mafia_keypad)
                await send(target_uid, f"⚠️ هشدار! {user['name']} از تو {format_number(steal_amount)} تومان دزدید!", mafia_keypad)
            else:
                user["steals_fail"] += 1
                await send(uid, "❌ دزدی ناموفق! فرار کردی ولی پولی به دست نیاوردی.", mafia_keypad)
                if random.random() < 0.2:
                    user["in_jail"] = 1
                    await send(uid, "🚔 پلیس تو دستگیر کرد! ۱ روز در زندان می‌مونی.", mafia_keypad)
        save_data()
        user_states[uid] = None
        return
    
    # ========== دستورات ادمین ==========
    if user.get("is_admin"):
        if text == "💰 افزودن پول به کاربر":
            user_states[uid] = "awaiting_admin_add_money"
            await send(uid, "💰 **فرمت:** `آیدی عددی مبلغ`\nمثال: 123456789 10000", admin_keypad)
            return
        
        if text == "💸 کم کردن پول کاربر":
            user_states[uid] = "awaiting_admin_remove_money"
            await send(uid, "💸 **فرمت:** `آیدی عددی مبلغ`\nمثال: 123456789 5000", admin_keypad)
            return
        
        if text == "🏦 گرفتن دارایی کاربر":
            user_states[uid] = "awaiting_admin_take_assets"
            await send(uid, "🏦 **آیدی عددی کاربر رو بفرست تا تمام دارایی‌اش گرفته بشه:**", admin_keypad)
            return
        
        if text == "💼 تنظیم شغل":
            user_states[uid] = "awaiting_admin_set_job"
            job_list = "\n".join(list(JOBS.keys())[:20])
            await send(uid, f"💼 **فرمت:** `آیدی عددی اسم شغل`\n\nمشاغل موجود:\n{job_list}\n...", admin_keypad)
            return
        
        if text == "❌ حذف شغل کاربر":
            user_states[uid] = "awaiting_admin_remove_job"
            await send(uid, "❌ **آیدی عددی کاربر رو بفرست تا شغلش حذف بشه:**", admin_keypad)
            return
        
        if text == "🛡️ تنظیم سپر":
            user_states[uid] = "awaiting_admin_set_shield"
            await send(uid, "🛡️ **فرمت:** `آیدی عددی تعداد سپر`\nمثال: 123456789 10", admin_keypad)
            return
        
        if text == "📢 ارسال پیام همگانی":
            user_states[uid] = "awaiting_broadcast"
            await send(uid, "📢 **متن پیام همگانی رو بفرست:**", admin_keypad)
            return
        
        if text == "🔄 ریست مسابقه هفتگی":
            for u in users_db.values():
                u["weekly_rank_bonus"] = 0
            save_data()
            await send(uid, "✅ مسابقه هفتگی ریست شد!", admin_keypad)
            return
        
        if text == "📈 آمار پیشرفته":
            total_cash = sum(u["cash"] + u["bank"] for u in users_db.values())
            total_stolen = sum(u.get("total_stolen", 0) for u in users_db.values())
            total_gambled = sum(u.get("total_gambled", 0) for u in users_db.values())
            text_stats = (
                f"📊 **آمار پیشرفته**\n⭐️ ═══════════════ ⭐️\n"
                f"👥 کاربران: {len(users_db)}\n"
                f"💰 کل پول: {format_number(total_cash)} تومان\n"
                f"🥷 کل دزدی: {format_number(total_stolen)} تومان\n"
                f"🎲 کل شرط: {format_number(total_gambled)} تومان\n"
                f"💎 میانگین ثروت: {format_number(total_cash//max(1, len(users_db)))} تومان\n"
            )
            await send(uid, text_stats, admin_keypad)
            return
        
        if text == "🗑️ ریست کامل کاربر":
            user_states[uid] = "awaiting_admin_reset_user"
            await send(uid, "🗑️ **آیدی عددی کاربر رو بفرست تا ریست بشه (همه چیز پاک میشه):**", admin_keypad)
            return
    
    # ========== پردازش دستورات ادمین (ادامه) ==========
    if state == "awaiting_admin_add_money":
        parts = text.split()
        if len(parts) != 2:
            await send(uid, "❌ فرمت: `آیدی مبلغ`", admin_keypad)
            user_states[uid] = None
            return
        target_uid, amount = parts[0], int(parts[1])
        if target_uid not in users_db:
            await send(uid, "❌ کاربر یافت نشد!", admin_keypad)
        else:
            users_db[target_uid]["cash"] += amount
            save_data()
            await send(uid, f"✅ {format_number(amount)} تومان به {users_db[target_uid]['name']} اضافه شد.", admin_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_admin_remove_money":
        parts = text.split()
        if len(parts) != 2:
            await send(uid, "❌ فرمت: `آیدی مبلغ`", admin_keypad)
            user_states[uid] = None
            return
        target_uid, amount = parts[0], int(parts[1])
        if target_uid not in users_db:
            await send(uid, "❌ کاربر یافت نشد!", admin_keypad)
        else:
            users_db[target_uid]["cash"] = max(0, users_db[target_uid]["cash"] - amount)
            save_data()
            await send(uid, f"💸 {format_number(amount)} تومان از {users_db[target_uid]['name']} کم شد.", admin_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_admin_take_assets":
        target_uid = text.strip()
        if target_uid not in users_db:
            await send(uid, "❌ کاربر یافت نشد!", admin_keypad)
        else:
            taken = users_db[target_uid]["cash"] + users_db[target_uid]["bank"]
            users_db[target_uid]["cash"] = 0
            users_db[target_uid]["bank"] = 0
            save_data()
            await send(uid, f"🏦 تمام دارایی {users_db[target_uid]['name']} ( {format_number(taken)} تومان) گرفته شد!", admin_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_admin_set_job":
        parts = text.split()
        if len(parts) != 2 or parts[1] not in JOBS:
            await send(uid, "❌ فرمت: `آیدی اسم شغل`", admin_keypad)
            user_states[uid] = None
            return
        target_uid, job_name = parts[0], parts[1]
        if target_uid not in users_db:
            await send(uid, "❌ کاربر یافت نشد!", admin_keypad)
        else:
            users_db[target_uid]["job"] = job_name
            save_data()
            await send(uid, f"✅ شغل {users_db[target_uid]['name']} به {job_name} تغییر کرد.", admin_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_admin_remove_job":
        target_uid = text.strip()
        if target_uid not in users_db:
            await send(uid, "❌ کاربر یافت نشد!", admin_keypad)
        else:
            users_db[target_uid]["job"] = None
            save_data()
            await send(uid, f"❌ شغل {users_db[target_uid]['name']} حذف شد!", admin_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_admin_set_shield":
        parts = text.split()
        if len(parts) != 2:
            await send(uid, "❌ فرمت: `آیدی تعداد`", admin_keypad)
            user_states[uid] = None
            return
        target_uid, shield_count = parts[0], int(parts[1])
        if target_uid not in users_db:
            await send(uid, "❌ کاربر یافت نشد!", admin_keypad)
        else:
            users_db[target_uid]["shield"] = shield_count
            save_data()
            await send(uid, f"🛡️ سپر {users_db[target_uid]['name']} به {shield_count} عدد تغییر کرد.", admin_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_broadcast":
        success = 0
        for user_id in users_db:
            try:
                await bot.send_message(user_id, f"📢 **پیام همگانی از ادمین:**\n\n{text}")
                success += 1
                await asyncio.sleep(0.1)
            except:
                pass
        await send(uid, f"✅ پیام به {format_number(success)} نفر ارسال شد.", admin_keypad)
        user_states[uid] = None
        return
    
    if state == "awaiting_admin_reset_user":
        target_uid = text.strip()
        if target_uid not in users_db:
            await send(uid, "❌ کاربر یافت نشد!", admin_keypad)
        else:
            # ریست کامل کاربر (به جز ادمین بودن)
            was_admin = users_db[target_uid].get("is_admin", False)
            users_db[target_uid] = {
                "name": f"کاربر{target_uid[-4:]}",
                "cash": 1000,
                "bank": 0,
                "job": None,
                "shield": 1,
                "wins": 0,
                "losses": 0,
                "steals_success": 0,
                "steals_fail": 0,
                "total_gambled": 0,
                "last_salary": 0,
                "in_jail": 0,
                "is_admin": was_admin,
                "referrer": None,
                "referrals": [],
                "mining_farm": None,
                "mining_last_collect": 0,
                "daily_luck": 1.0,
                "last_luck_update": 0,
                "weekly_rank_bonus": 0,
                "total_stolen": 0
            }
            save_data()
            await send(uid, f"🗑️ کاربر {target_uid} با موفقیت ریست شد!", admin_keypad)
        user_states[uid] = None
        return

# ======================= اجرای بات =======================
load_data()
for uid, data in users_db.items():
    data.setdefault("is_admin", False)
    data.setdefault("shield", 0)
    data.setdefault("steals_success", 0)
    data.setdefault("steals_fail", 0)
    data.setdefault("total_gambled", 0)
    data.setdefault("referrals", [])
    data.setdefault("mining_farm", None)
    data.setdefault("mining_last_collect", 0)
    data.setdefault("daily_luck", 1.0)
    data.setdefault("last_luck_update", 0)
    data.setdefault("weekly_rank_bonus", 0)
    data.setdefault("total_stolen", 0)
save_data()

if __name__ == "__main__":
    print("🚀 **ابر بات اقتصاد و ثروت نسخه GODLIKE با موفقیت راه‌اندازی شد!**")
    print("👑 ۸۰ شغل جدید | دزدی | ماینینگ | سیستم شراکت | پنل ادمین کامل")
    asyncio.run(bot.run())