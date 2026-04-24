import streamlit as st
import pandas as pd
import plotly.express as px
import time

# إعدادات النظام الرسمية
st.set_page_config(page_title="منظومة الحوالات الوطنية", layout="wide", page_icon="🏛️")

# تنسيق الواجهة (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { background-color: #1e3a8a; color: white; border-radius: 8px; font-weight: bold; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; }
    h1, h2 { color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# نظام الدخول الآمن
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏛️ نظام إعادة هندسة الحوالات المالية")
    st.sidebar.title("بوابة الدخول")
    user = st.sidebar.text_input("اسم المستخدم")
    pw = st.sidebar.text_input("كلمة المرور", type="password")
    if st.sidebar.button("دخول"):
        if user == "admin" and pw == "2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.sidebar.error("خطأ في البيانات")
    st.stop()

# إدارة البيانات
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "البند": ["الرواتب والأجور", "المشاريع الإنشائية", "النفقات التشغيلية"],
        "المخصص": [1000000, 500000, 200000],
        "المنفق": [400000, 100000, 50000]
    })

df = st.session_state.df
df['المتبقي'] = df['المخصص'] - df['المنفق']

# واجهة العرض
st.title("🏛️ لوحة التحكم في الحوالات المؤتمتة")
st.markdown("---")

col_m = st.columns(3)
col_m[0].metric("إجمالي الموازنة", f"{df['المخصص'].sum():,} د")
col_m[1].metric("الإنفاق الفعلي", f"{df['المنفق'].sum():,} د")
col_m[2].metric("السيولة المتاحة", f"{df['المتبقي'].sum():,} د")

# الرسم البياني
fig = px.bar(df, x="البند", y=["المنفق", "المتبقي"], title="تحليل استهلاك البنود", barmode="stack", color_discrete_sequence=['#1e3a8a', '#cbd5e1'])
st.plotly_chart(fig, use_container_width=True)

# بوابة الأتمتة
st.write("### 🤖 معالجة الحوالات الذكية")
c1, c2 = st.columns(2)
with c1:
    item = st.selectbox("بند الصرف", df['البند'])
    amt = st.number_input("المبلغ المطلوب", min_value=0, step=1000)
with c2:
    report = st.file_uploader("تقرير الإنجاز (للمشاريع)") if "المشاريع" in item else "لا يتطلب"

if st.button("🚀 تنفيذ الحوالة آلياً"):
    row = df[df['البند'] == item].iloc[0]
    if amt > row['المتبقي']:
        st.error(f"⛔ رفض: تجاوز السقف القانوني. المتاح {row['المتبقي']:,} د")
    elif "المشاريع" in item and report is None:
        st.warning("⚠️ مرفوض: يجب إرفاق تقرير إنجاز فني.")
    else:
        with st.status("جاري المعالجة..."): time.sleep(2)
        idx = df[df['البند'] == item].index
st.session_state.df.loc[st.session_state.df['بند الإنفاق'] == selected_item, 'المنفق حالياً'] += req_amount        st.success("✅ تم الاعتماد وتحديث الخزينة فوراً.")
        st.balloons()
        time.sleep(1)
        st.rerun()
