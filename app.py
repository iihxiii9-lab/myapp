import streamlit as st
import requests

st.set_page_config(page_title="تطبيق الطقس", page_icon="🌤️")

st.title("🌤️ تطبيق حالة الطقس")
st.write("أدخل اسم المدينة لمعرفة حالة الطقس الحالية")

API_KEY = "55f09fbb4d8c9adc22960bc9dcfa14e0"

city_name = st.text_input("اسم المدينة (بالعربية أو الإنجليزية):", "")

if st.button("عرض الطقس"):
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
                
                st.subheader(f"حالة الطقس في {city}، {country}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("درجة الحرارة", f"{temp} °C")
                    st.metric("الشعور الفعلي", f"{feels_like} °C")
                with col2:
                    st.metric("الرطوبة", f"{humidity}%")
                    st.metric("سرعة الرياح", f"{wind_speed} م/ث")
                    
                st.info(f"**الوصف:** {description}")
            else:
                st.error(f"خطأ: {data.get('message', 'تعذر جلب البيانات')}")
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {e}")
    else:
        st.warning("يرجى إدخال اسم مدينة صالح.")
