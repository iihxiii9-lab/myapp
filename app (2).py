import streamlit as st
import requests
import pandas as pd

# إعدادات الصفحة والتصميم
st.set_page_config(
    page_title="مستكشف الطقس الاحترافي",
    page_icon="🌤️",
    layout="wide"
)

# إضافة تنسيقات CSS جليلة لتحسين المظهر والألوان
st.markdown("""
    <style>
    .main-title {
        font-size: 2.8rem;
        color: #1E88E5;
        text-align: center;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #555555;
        text-align: center;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        height: 48px;
    }
    </style>
""", unsafe_allow_html=1)

# العنوان الرئيس
st.markdown('<div class="main-title">🌤️ مستكشف الطقس اللحظي</div>', unsafe_allow_html=1)
st.markdown('<div class="sub-title">استعلم عن حالة الطقس لجميع المدن وتابع سجل بحثك بكل سهولة</div>', unsafe_allow_html=1)

API_KEY = "55f09fbb4d8c9adc22960bc9dcfa14e0"

# تهيئة سجل البحث في جلسة Streamlit (Session State)
if 'history' not in st.session_state:
    st.session_state.history = []

# إدخال المدينة
col_input, col_btn = st.columns([3, 1])

with col_input:
    city_name = st.text_input("اسم المدينة أو الدولة:", "", placeholder="مثال: الرياض، دبي، القاهرة، London...")

with col_btn:
    st.write(" ") # موازنة المحاذاة العمودية
    st.write(" ")
    search_clicked = st.button("بحث عن الطقس")

if search_clicked:
    if city_name.strip():
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'ar'
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                city = data['name']
                country = data['sys']['country']
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                wind_speed = data['wind']['speed']
                
                # عرض نتائج البحث الحالية
                st.markdown("---")
                st.subheader(f"📍 النتائج الحالية: {city}، {country}")
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("🌡️ الحرارة", f"{temp} °C")
                c2.metric("🤔 الشعور الفعلي", f"{feels_like} °C")
                c3.metric("💧 الرطوبة", f"{humidity}%")
                c4.metric("💨 سرعة الرياح", f"{wind_speed} م/ث")
                
                st.success(f"**حالة الجو:** {description.capitalize()}")
                
                # إضافة نتيجة البحث إلى سجل البحث (تجنب التكرار المتتالي بمرونة)
                new_record = {
                    "المدينة/الدولة": f"{city} ({country})",
                    "درجة الحرارة (°C)": temp,
                    "الشعور الفعلي (°C)": feels_like,
                    "الرطوبة (%)": humidity,
                    "سرعة الرياح (م/ث)": wind_speed,
                    "الوصف": description
                }
                
                # حفظ في السجل في بداية القائمة (الأحدث أولاً)
                st.session_state.history.insert(0, new_record)
                
            else:
                st.error(f"⚠️ خطأ: {data.get('message', 'تعذر جلب البيانات. تأكد من صحة اسم المدينة.')}")
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال بالشبكة: {e}")
    else:
        st.warning("يرجى إدخال اسم مدينة أو دولة أولاً.")

# عرض سجل عمليات البحث السابقة في جدول منظم
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 سجل المدن المبحوث عنها")
    
    # تحويل السجل إلى DataFrame لتقديمه في جدول منسق
    df_history = pd.DataFrame(st.session_state.history)
    
    st.dataframe(
        df_history,
        use_container_width=1,
        hide_index=1
    )
    
    if st.button("🗑️ مسح سجل البحث"):
        st.session_state.history = []
        st.rerun()
