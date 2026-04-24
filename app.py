import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. إعدادات المنصة الرسمية
st.set_page_config(page_title="منصة الأداء والموازنة الذكية", layout="wide", page_icon="🏛️")

# --- تنسيق الواجهة الاحترافي وضمان وضوح الأرقام (CSS) ---
st.markdown("""
    <style>
    /* خلفية التطبيق */
    .stApp { background-color: #f8fafc; }
    
    /* تنسيق بطاقات الأرقام لجعلها بارزة */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        border-right: 10px solid #1e3a8a;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    
    /* جعل الأرقام سوداء داكنة جداً وعريضة للوضوح على الموبايل */
    div[data-testid="stMetricValue"] > div {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 2.2rem !important;
        text-shadow: 0.5px 0.5px #e2e8f0;
    }
    
    /* جعل تسمية العنوان فوق الرقم واضحة */
    div[data-testid="stMetricLabel"] > label {
        color: #1e3a8a !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }

    /* تنسيق القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #1e3a8a;
    }
    section[data-testid="stSidebar"] .stMarkdown p, 
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* العناوين الرئيسية في الصفحة */
    h1, h2, h3 { 
        color: #1e3a8a !important; 
        font-family: 'Arial'; 
        font-weight: 900 !important;
    }

    /* أزرار التنفيذ */
    .stButton>button {
        background-color: #1e3a8a;
        color: white !important;
        border-radius: 12px;
        font-weight: bold;
        height: 3.5em;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .stButton>button:hover { background-color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول الآمن
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏛️ منصة التحول الرقمي للإدارة المالية")
    st.markdown("### بوابة الدخول الموحدة - إدارة تطوير الأداء")
    with st.sidebar:
        st.write("## تسجيل الدخول")
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if user == "admin" and pw == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.sidebar.error("البيانات غير صحيحة")
    st.stop()

# 3. قاعدة البيانات الموحدة
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
        "الإنجاز %": [92, 85, 78, 95, 60, 88, 72, 90, 68, 82, 94, 76, 91, 89, 70, 84, 87],
        "المخصص د": [500000] * 17,
        "المنفق د": [150000] * 17
    })

df = st.session_state.df

# 4. القائمة الجانبية للتنقل
with st.sidebar:
    st.write("---")
    page = st.radio("القائمة الرئيسية:", ["📊 مؤشرات الأداء المؤسسي", "💰 الموازنة والحوالات"])
    st.write("---")
    st.caption("مطور النظام: وحدة تطوير الأداء المؤسسي")
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

# --- صفحة الأداء ---
if page == "📊 مؤشرات الأداء المؤسسي":
    st.title("📊 لوحة قياس الأداء والقطاعات")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("متوسط الإنجاز العام", f"{df['الإنجاز %'].mean():.1f}%")
    m2.metric("أعلى قطاع إنجازاً", df.iloc[df['الإنجاز %'].idxmax()]['الجهة'])
    m3.metric("وحدات تحت المتابعة", len(df[df['الإنجاز %'] < 75]))

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df, x="الجهة", y="الإنجاز %", color="الإنجاز %", 
                     title="تحليل مقارنة الأداء", color_continuous_scale="RdYlGn")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write("### تفاصيل المؤشرات")
        st.dataframe(df[['الجهة', 'الإنجاز %']], use_container_width=True, height=400)

# --- صفحة الموازنة ---
else:
    st.title("💰 إدارة الحوالات والأوامر المالية")
    selected = st.selectbox("اختر الجهة لطلب الحوالة:", df['الجهة'])
    row = df[df['الجهة'] == selected].iloc[0]
    rem = row['المخصص د'] - row['المنفق د']
    
    c1, c2, c3 = st.columns(3)
    c1.metric("المتبقي في الموازنة", f"{rem:,} د")
    c2.metric("نسبة الإنجاز الحالي", f"{row['الإنجاز %']}%")
    
    if row['الإنجاز %'] < 75:
        c3.warning("⚠️ تنبيه: الأداء منخفض")
        st.error("تنبيه نظام الأداء: هذه الجهة متعثرة، يرجى مراجعة المبررات قبل الصرف.")
    else:
        c3.success("✅ أداء مستقر")

    st.write("---")
    amt = st.number_input("المبلغ المطلوب تحويله (دينار):", min_value=0, step=1000)
    if st.button("🚀 تنفيذ واعتماد الحوالة"):
        if amt > rem:
            st.error("تجاوز السقف المالي المسموح!")
        else:
            with st.status("جاري المعالجة والربط مع الخزينة..."): time.sleep(1.5)
            st.session_state.df.loc[st.session_state.df['الجهة'] == selected, 'المنفق د'] += amt
            st.success("✅ تم الاعتماد وتحديث السجلات فوراً!")
            st.balloons()
            time.sleep(1)
            st.rerun()
