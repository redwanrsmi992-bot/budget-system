import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="منظومة الحوالات الوطنية", layout="wide", page_icon="🏛️")

# 1. نظام الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏛️ نظام إعادة هندسة الحوالات المالية")
    user = st.sidebar.text_input("اسم المستخدم")
    pw = st.sidebar.text_input("كلمة المرور", type="password")
    if st.sidebar.button("دخول"):
        if user == "admin" and pw == "2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# 2. البيانات المالية
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "بند الإنفاق": ["الرواتب والأجور", "المشاريع الإنشائية", "النفقات التشغيلية"],
        "المخصص السنوي": [1000000, 500000, 200000],
        "المنفق حالياً": [400000, 100000, 50000]
    })

df = st.session_state.df
df['المتبقي'] = df['المخصص السنوي'] - df['المنفق حالياً']

# 3. واجهة العرض
st.title("🏛️ لوحة التحكم في الحوالات")
m1, m2, m3 = st.columns(3)
m1.metric("إجمالي الموازنة", f"{df['المخصص السنوي'].sum():,} د")
m2.metric("الإنفاق الفعلي", f"{df['المنفق حالياً'].sum():,} د")
m3.metric("السيولة المتاحة", f"{df['المتبقي'].sum():,} د")

fig = px.bar(df, x="بند الإنفاق", y=["المنفق حالياً", "المتبقي"], title="تحليل المخصصات", barmode="stack", color_discrete_sequence=['#1e3a8a', '#cbd5e1'])
st.plotly_chart(fig, use_container_width=True)

# 4. محرك الأتمتة
st.write("### 🤖 بوابة المعالجة الآلية")
c1, c2 = st.columns(2)
with c1:
    selected = st.selectbox("اختر البند", df['بند الإنفاق'])
    amt = st.number_input("المبلغ المطلوب", min_value=0, step=1000)
with c2:
    is_proj = "المشاريع" in selected
    up = st.file_uploader("تقرير الإنجاز") if is_proj else "لا يتطلب"

if st.button("🚀 تنفيذ الحوالة"):
    current_rem = df.loc[df['بند الإنفاق'] == selected, 'المتبقي'].values[0]
    if amt > current_rem:
        st.error("⛔ تجاوز السقف المسموح!")
    elif is_proj and up is None:
        st.warning("⚠️ مطلوب تقرير إنجاز!")
    else:
        with st.status("جاري الصرف..."): time.sleep(1)
        st.session_state.df.loc[st.session_state.df['بند الإنفاق'] == selected, 'المنفق حالياً'] += amt
        st.success("✅ تم الاعتماد!")
        st.balloons()
        time.sleep(1)
        st.rerun()
