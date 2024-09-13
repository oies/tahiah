from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, time
from hijri_converter import convert

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # السماح بالوصول من جميع المصادر
    allow_credentials=True,
    allow_methods=["*"],  # السماح بجميع أنواع الطلبات (GET, POST, PUT, DELETE, ...الخ)
    allow_headers=["*"],  # السماح بجميع الرؤوس
)

# دالة لتحويل التاريخ الميلادي إلى هجري
def get_hijri_date():
    today = datetime.now()
    hijri_date = convert.Gregorian(today.year, today.month, today.day).to_hijri()
    return hijri_date

# تعريف النصوص حسب التوقيت الهجري والميلادي
def get_message_based_on_time():
    now = datetime.now()
    current_time = now.time()
    hijri_date = get_hijri_date()

    hijri_month = hijri_date.month
    hijri_day = hijri_date.day
    current_day = now.weekday()  # 0 = Monday, 6 = Sunday

    # تواريخ وأوقات خاصة بالأيام والأشهر الهجرية
    if hijri_month == 9:  # شهر رمضان
        return "مبارك عليكم الشهر."
    elif hijri_month == 10 and hijri_day <= 5:  # عيد الفطر (أول 5 أيام من شوال)
        return "عيد سعيد."
    elif hijri_month == 12 and hijri_day <= 12:  # الحج (أيام ذو الحجة الأولى حتى يوم 12)
        return "حج مبرور وسعي مشكور."

    # وقت صباح الجمعة
    if current_day == 4 and current_time >= time(0, 0) and current_time <= time(18, 0):  # الجمعة
        return "جمعة طيبة علينا وعليك."
    
    # فترة الصباح من الفجر حتى بعد العصر
    if current_time >= time(3, 0) and current_time <= time(15, 30):  # من الفجر إلى العصر
        return "صبحك الله بكل خير."
    
    # فترة المساء من بعد العصر حتى صلاة الفجر
    if current_time > time(15, 30) or current_time < time(3, 0):  # من بعد العصر حتى الفجر
        return "مساك الله بكل خير."

    # Default message
    return "لا يوجد رسالة مناسبة لهذا الوقت."

# نقطة النهاية (Endpoint) لعرض الرسالة المناسبة
@app.get("/get_message")
def get_message():
    message = get_message_based_on_time()
    return {"message": message}