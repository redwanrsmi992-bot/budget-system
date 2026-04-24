import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. إعدادات المنصة المتكاملة
st.set_page_config(page_title="منصة الإدارة المالية والأداء المؤسسي", layout="wide", page_icon="🏛️")

# تنسيق الواجهة (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; }
    h1, h2, h3 { color: #1e3a8a; font-family: 'Arial'; }
    .stButton>button { background-color: #1e3a8a; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول الموحد
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏛️ منصة التحول الرقمي للإدارة المالية والأداء")
    with st.sidebar:
        st.header("بوابة الدخول")
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل الدخول"):
            if user == "admin" and pw == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
    st.stop()

# 3. إدارة قاعدة البيانات الموحدة
if 'performance_df' not in st.session_state:
    depts = [
        "قطاع الإدارة المالية والتخطيط", "قطاع الإدارة العامة", "قطاع الدفاع والأمن",
        "قطاع القضاء والشؤون الدينية", "قطاع البنية التحتية", "قطاع الصحة والتنمية",
        "قطاع التنمية الزراعية", "قطاع التعليم والموارد البشرية", "قطاع السياحة والاستثمار",
        "قطاع الثقافة والشباب", "وحدة المتابعة والتقييم", "وحدة اللامركزية", 
        "وحدة تطوير الأداء المؤسسي", "وحدة الرقابة الداخلية", 
        "مديرية الدراسات", "مديرية الحاسوب والمعرفة", "مديرية الشؤون الإدارية والمالية"
    ]
    st.session_state.performance_df = pd.DataFrame({
        "الجهة": depts,
        "الإنجاز %": [92, 85, 78, 90, 65, 88, 72, 95, 80, 84, 91, 68, 89, 93, 77, 82, 86],
        "المخصص د": [100000] * 17,
        "المنفق د": [25000] * 17
    })

df = st.session_state.performance_df

# 4. القائمة الجانبية للتنقل
with st.sidebar:
    st.write(f"مرحباً بك: **Admin**")
    st.divider()
    page = st.radio("القائمة الرئيسية:", ["📊 مؤشرات الأداء المؤسسي", "💰 نظام الموازنة والحوالات"])
    st.divider()
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

# --- صفحة مؤشرات الأداء ---
if page == "📊 مؤشرات الأداء المؤسسي":
    st.title("📊 لوحة قياس الأداء والقطاعات")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("متوسط الإنجاز العام", f"{df['الإنجاز %'].mean():.1f}%")
    m2.metric("أعلى قطاع إنجازاً", df.iloc[df['الإنجاز %'].idxmax()]['الجهة'])
    m3.metric("وحدات قيد المتابعة", len(df[df['الإنجاز %'] < 75]))

    col1, col2 = st.columns()
    with col1:
        fig = px.bar(df, x="الجهة", y="الإنجاز %", color="الإنجاز %", 
                     title="مقارنة الإنجاز الفعلي", color_continuous_scale="RdYlGn")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        def color_perf(val):
            color = '#dcfce7' if val >= 90 else ('#fef3c7' if val >= 75 else '#fee2e2')
            return f'background-color: {color}'
        st.write("### تفاصيل المؤشرات")
        st.dataframe(df[['الجهة', 'الإنجاز %']].style.map(color_perf, subset=['الإنجاز %']), use_container_width=True)

# --- صفحة الموازنة والحوالات ---
else:
    st.title("💰 نظام إدارة الحوالات والأوامر المالية")
    
    selected_dept = st.selectbox("اختر الجهة لطلب الحوالة:", df['الجهة'])
    dept_info = df[df['الجهة'] == selected_dept].iloc
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("المتبقي في الموازنة", f"{dept_info['المخصص د'] - dept_info['المنفق د']:,} د")
    col_b.metric("نسبة إنجاز المديرية", f"{dept_info['الإنجاز %']}%")
    
    # ربط ذكي: تنبيه بناءً على الأداء
    if dept_info['الإنجاز %'] < 75:
        col_c.warning("⚠️ تنبيه: الأداء منخفض")
        st.error("تنبيه نظام الأداء: هذه المديرية لديها تعثر في الإنجاز، يرجى مراجعة المبررات قبل الصرف.")
    else:
        col_c.success("✅ الأداء مستقر")

    st.divider()
    amount = st.number_input("المبلغ المطلوب تحويله:", min_value=0, step=1000)
    
    if st.button("🚀 معالجة الطلب"):
        if amount > (dept_info['المخصص د'] - dept_info['المنفق د']):
            st.error("تجاوز السقف المالي المسموح!")
        else:
            with st.status("جاري الربط مع الخزينة وتحديث السجلات..."):
                time.sleep(2)
            idx = df[df['الجهة'] == selected_dept].index
            st.session_state.performance_df.at[idx, 'المنفق د'] += amount
            st.success(f"تم اعتماد الحوالة لـ {selected_dept} بنجاح!")
            st.balloons()
            time.sleep(1)
            st.rerun()
