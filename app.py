import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="منصة الموازنة والأداء", layout="wide", page_icon="🏛️")

# 1. نظام الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏛️ منصة التحول الرقمي للإدارة المالية")
    user = st.sidebar.text_input("اسم المستخدم")
    pw = st.sidebar.text_input("كلمة المرور", type="password")
    if st.sidebar.button("دخول"):
        if user == "admin" and pw == "2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# 2. قاعدة البيانات
if 'df' not in st.session_state:
    depts = [
        "قطاع الإدارة المالية والتخطيط", "قطاع الإدارة العامة", "قطاع الدفاع والأمن",
        "قطاع القضاء والشؤون الدينية", "قطاع البنية التحتية", "قطاع الصحة والتنمية",
        "قطاع التنمية الزراعية", "قطاع التعليم والموارد البشرية", "قطاع السياحة والاستثمار",
        "قطاع الثقافة والشباب", "وحدة المتابعة والتقييم", "وحدة اللامركزية", 
        "وحدة تطوير الأداء المؤسسي", "وحدة الرقابة الداخلية", 
        "مديرية الدراسات", "مديرية الحاسوب والمعرفة", "مديرية الشؤون الإدارية والمالية"
    ]
    st.session_state.df = pd.DataFrame({
        "الجهة": depts,
        "الإنجاز %": [92, 85, 70, 88, 65, 95, 80, 91, 77, 83, 90, 82, 89, 74, 93, 86, 79],
        "المخصص د": [100000] * 17,
        "المنفق د": [40000] * 17
    })

df = st.session_state.df

# 3. القائمة الجانبية
page = st.sidebar.radio("القائمة الرئيسية:", ["📊 مؤشرات الأداء", "💰 نظام الموازنة"])

# --- صفحة الأداء ---
if page == "📊 مؤشرات الأداء":
    st.title("📊 لوحة قياس الأداء المؤسسي")
    m1, m2 = st.columns(2)
    m1.metric("متوسط الإنجاز", f"{df['الإنجاز %'].mean():.1f}%")
    m2.metric("وحدات تحت المتابعة", len(df[df['الإنجاز %'] < 75]))
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df, x="الجهة", y="الإنجاز %", color="الإنجاز %", color_continuous_scale="RdYlGn")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # السطر المعدل بمسافة صحيحة
        st.dataframe(df[['الجهة', 'الإنجاز %']].style.background_gradient(axis=0, gmap=df['الإنجاز %'], cmap='RdYlGn', subset=['الإنجاز %']), use_container_width=True)

# --- صفحة الموازنة ---
else:
    st.title("💰 نظام الحوالات والأوامر المالية")
    selected = st.selectbox("اختر الجهة:", df['الجهة'])
    row = df[df['الجهة'] == selected].iloc[0]
    rem = row['المخصص د'] - row['المنفق د']
    
    c1, c2, c3 = st.columns(3)
    c1.metric("المتبقي", f"{rem:,} د")
    c2.metric("الإنجاز", f"{row['الإنجاز %']}%")
    
    if row['الإنجاز %'] < 75:
        c3.warning("⚠️ أداء منخفض")
        st.error("تنبيه: المديرية متعثرة في الإنجاز، يرجى التدقيق قبل الصرف.")
    else:
        c3.success("✅ أداء مستقر")

    amt = st.number_input("المبلغ المطلوب:", min_value=0, step=1000)
    if st.button("🚀 تنفيذ الحوالة"):
        if amt > rem:
            st.error("تجاوز السقف المالي!")
        else:
            with st.status("جاري المعالجة..."): 
                time.sleep(1)
            st.session_state.df.loc[st.session_state.df['الجهة'] == selected, 'المنفق د'] += amt
            st.success("✅ تم الاعتماد!")
            st.balloons()
            time.sleep(1)
            st.rerun()
