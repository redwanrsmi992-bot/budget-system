import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. إعدادات المنصة الرسمية
st.set_page_config(page_title="منصة الأداء والموازنة الذكية", layout="wide", page_icon="🏛️")

# --- تنسيق الواجهة الاحترافي (CSS) ---
st.markdown("""
    <style>
    /* خلفية التطبيق */
    .stApp { background-color: #f8fafc; }
    
    /* تنسيق بطاقات الأرقام الملونة */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        border-right: 5px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* تنسيق القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #1e3a8a;
    }
    section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
        color: white !important;
    }
    
    /* العناوين الرئيسية */
    h1 { color: #1e3a8a; font-family: 'Arial'; border-right: 8px solid #1e3a8a; padding-right: 15px; }
    
    /* الأزرار */
    .stButton>button {
        background-color: #1e3a8a;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        height: 3em;
        border: None;
    }
    .stButton>button:hover { background-color: #3b82f6; color: white; }
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
                st.error("البيانات غير صحيحة")
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
        "الإنجاز %": [92, 85, 88, 70, 95, 65, 80, 89, 72, 84, 91, 78, 96, 82, 87, 93, 86],
        "المخصص د": [100000] * 17,
        "المنفق د": [45000, 30000, 50000, 20000, 60000, 15000, 40000, 55000, 25000, 48000, 32000, 28000, 50000, 35000, 42000, 58000, 44000]
    })

df = st.session_state.df

# 4. القائمة الجانبية للتنقل
with st.sidebar:
    st.write("---")
    page = st.radio("القائمة الرئيسية:", ["📊 مؤشرات الأداء المؤسسي", "💰 الموازنة والحوالات"])
    st.write("---")
    st.caption("مطور النظام: وحدة تطوير الأداء")
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

# --- صفحة الأداء ---
if page == "📊 مؤشرات الأداء المؤسسي":
    st.title("📊 لوحة قياس الأداء والقطاعات")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("متوسط الإنجاز العام", f"{df['الإنجاز %'].mean():.1f}%")
    m2.metric("أعلى قطاع إنجازاً", df.iloc[df['الإنجاز %'].idxmax()]['الجهة'])
    m3.metric("وحدات قيد المتابعة", len(df[df['الإنجاز %'] < 75]))

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
