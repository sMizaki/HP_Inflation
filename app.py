import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ==========================================
# 1. ตั้งค่าหน้าเพจหลัก
# ==========================================
st.set_page_config(page_title="HSR HP Inflation Predictor", page_icon="✨") 

# ==========================================
# 🎨 2. ตกแต่งปุ่มด้วย CSS (ปุ่มใหญ่ & เปลี่ยนสี)
# ==========================================
st.markdown("""
<style>
/* แต่งปุ่ม Primary (ปุ่มโหมดที่ถูกเลือก และ ปุ่มทำนายผล) */
div.stButton > button[kind="primary"] {
    background-color: #4c16e9 !important;
    border-color: #4c16e9 !important;
    color: white !important;
    height: 70px !important;        /* ทำให้ปุ่มสูงและใหญ่ขึ้น */
    font-size: 20px !important;     /* ขยายขนาดตัวอักษร */
    font-weight: bold !important;
    border-radius: 12px !important; /* ลบมุมให้โค้งมน */
    transition: all 0.3s ease;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #360fa3 !important; /* สีเข้มขึ้นเวลาเอาเมาส์ชี้ */
    border-color: #360fa3 !important;
    transform: scale(1.02);         /* เอฟเฟกต์เด้งขยายตัวนิดๆ */
}

/* แต่งปุ่ม Secondary (ปุ่มโหมดที่ยังไม่ได้เลือก) */
div.stButton > button[kind="secondary"] {
    height: 70px !important;
    font-size: 18px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #4c16e9 !important; /* กรอบเปลี่ยนเป็นสีม่วงเวลาชี้ */
    color: #4c16e9 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. แถบด้านข้าง (Sidebar) - ข้อมูลผู้จัดทำ
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>👨‍💻 ผู้จัดทำ</h2>", unsafe_allow_html=True)
    st.image("IMG20240703140738.jpg", use_container_width=True)
    st.markdown("---")
    st.markdown("**ชื่อ-นามสกุล:** เทพทัต ทับทิมไทร")
    st.markdown("**รหัสนักศึกษา:** 664245012")
    st.markdown("**หมู่เรียน:** `66/43")
    st.markdown("---")
    st.info("โปรเจกต์ทำนายอัตราการเฟ้อของ HP ศัตรูในเกม Honkai: Star Rail (Polynomial Regression)")

# ==========================================
# 4. ส่วนหัวเว็บ (Header & Logo)
# ==========================================
st.image("logo.png", width=400)
st.title("End Game Content's Boss HP Inflation Predictor")
st.markdown("---")

# ==========================================
# 5. ส่วนตั้งค่าการทำนาย (เลือกโหมดด้วยปุ่มใหญ่)
# ==========================================
st.subheader("1️⃣ เลือกโหมดเกม")

# ฟังก์ชัน Callback สำหรับเปลี่ยนโหมดแบบทันที (ไม่กระตุก)
if 'selected_mode' not in st.session_state:
    st.session_state.selected_mode = "Memory of Chaos"

def set_mode(mode_name):
    st.session_state.selected_mode = mode_name

# เช็คว่าปุ่มไหนถูกเลือกอยู่ ให้ปุ่มนั้นกลายเป็นแบบ Primary (ซึ่งจะโดน CSS ย้อมเป็นสี #4c16e9)
moc_type = "primary" if st.session_state.selected_mode == "Memory of Chaos" else "secondary"
pf_type = "primary" if st.session_state.selected_mode == "Pure Fiction" else "secondary"
as_type = "primary" if st.session_state.selected_mode == "Apocalyptic Shadow" else "secondary"

# สร้าง 3 ปุ่มเรียงกัน
col1, col2, col3 = st.columns(3)
with col1:
    st.button("⚔️ Memory of Chaos", type=moc_type, use_container_width=True, on_click=set_mode, args=("Memory of Chaos",))
with col2:
    st.button("🎭 Pure Fiction", type=pf_type, use_container_width=True, on_click=set_mode, args=("Pure Fiction",))
with col3:
    st.button("🔥 Apocalyptic Shadow", type=as_type, use_container_width=True, on_click=set_mode, args=("Apocalyptic Shadow",))

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 6. เลือกเวอร์ชันและปุ่มทำนายผล
# ==========================================
st.subheader("2️⃣ เลือกแพตช์เวอร์ชัน")
version = st.number_input(
    "ระบุเลขแพตช์ในอนาคต (เช่น 5.0):",
    min_value=1.0, max_value=15.0, value=5.0, step=0.1, format="%.1f"
)

st.markdown("<br>", unsafe_allow_html=True)
# ปุ่มทำนายผล (เป็น type="primary" อยู่แล้ว จะได้สี #4c16e9 และขนาดใหญ่ตามไปด้วย)
predict_btn = st.button("🚀 เริ่มทำนายผล HP", type="primary", use_container_width=True)
st.markdown("---")

# ==========================================
# 7. ส่วนแสดงผลลัพธ์
# ==========================================
if predict_btn:
    st.subheader("🎯 ผลการพยากรณ์")
    try:
        mode = st.session_state.selected_mode
        
        if mode == "Memory of Chaos":
            model = joblib.load('hsr_moc_model.pkl')
        elif mode == "Pure Fiction":
            model = joblib.load('hsr_pf_model.pkl')
        else:
            model = joblib.load('hsr_as_model.pkl')
            
        # ทำนายผล
        X_pred = np.array([[version]])
        predicted_hp = model.predict(X_pred)[0]
        
        st.metric(
            label=f"เลือดบอสในโหมด {mode} (แพตช์ {version:.1f})", 
            value=f"{predicted_hp:,.0f} HP"
        )
        
        if predicted_hp < 0:
            st.warning("⚠️ คำเตือน: เลือดบอสติดลบ อาจเกิดจากการใส่เลขแพตช์ในอดีตที่ไกลเกินไป")
        else:
            st.success("✨ ทำนายผลสำเร็จเรียบร้อย!")
            
            
    except FileNotFoundError:
        st.error(f"❌ ระบบหาไฟล์โมเดลของโหมด '{mode}' ไม่พบครับ ลองตรวจสอบไฟล์ .pkl ใน GitHub อีกครั้ง")
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")