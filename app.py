import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ==========================================
# 1. ตั้งค่าหน้าเพจหลัก
# ==========================================
# เอา layout="wide" ออก เพื่อให้เนื้อหาจัดเรียงตรงกลางเป็นแนวตั้งสวยงาม
st.set_page_config(page_title="HSR HP Predictor", page_icon="✨") 

# ==========================================
# 2. แถบด้านข้าง (Sidebar) - ข้อมูลผู้จัดทำ
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>👨‍💻 ผู้จัดทำ</h2>", unsafe_allow_html=True)
    
    # รูปโปรไฟล์
    st.image("https://api.dicebear.com/7.x/adventurer/svg?seed=Felix", use_container_width=True)
    st.markdown("---")
    
    # ข้อมูลส่วนตัว
    st.markdown("**ชื่อ-นามสกุล:** เทพทัต ทับทิมไทร")
    st.markdown("**รหัสนักศึกษา:** `[ใส่รหัสนักศึกษาของคุณ]`")
    st.markdown("**หมู่เรียน:** `[ใส่หมู่เรียนของคุณ]`")
    st.markdown("---")
    st.info("โปรเจกต์ทำนายอัตราเงินเฟ้อ HP ศัตรูในเกม Honkai: Star Rail (Linear Regression)")

# ==========================================
# 3. ส่วนหัวเว็บ (Header & Logo)
# ==========================================
# ใส่รูป Logo เกม (ดึงจากอินเทอร์เน็ต)
st.image("https://upload.wikimedia.org/wikipedia/en/thumb/5/52/Honkai_Star_Rail_logo.png/800px-Honkai_Star_Rail_logo.png", width=250)

st.title("Boss HP Predictor")
st.markdown("---")

# ==========================================
# 4. ส่วนตั้งค่าการทำนาย (เรียงเป็นแนวตั้ง)
# ==========================================
st.subheader("1️⃣ เลือกโหมดเกม")

# สร้าง Session State เพื่อให้ Streamlit จำว่าเรากดปุ่มโหมดไหนไว้
if 'selected_mode' not in st.session_state:
    st.session_state.selected_mode = "Memory of Chaos" # ค่าเริ่มต้น

# สร้างปุ่ม 3 ปุ่มเรียงกันในแนวนอน
btn1, btn2, btn3 = st.columns(3)
if btn1.button("⚔️ Memory of Chaos", use_container_width=True):
    st.session_state.selected_mode = "Memory of Chaos"
if btn2.button("🎭 Pure Fiction", use_container_width=True):
    st.session_state.selected_mode = "Pure Fiction"
if btn3.button("🔥 Apocalyptic Shadow", use_container_width=True):
    st.session_state.selected_mode = "Apocalyptic Shadow"

# แสดงให้ผู้ใช้เห็นว่าตอนนี้เลือกโหมดไหนอยู่
st.info(f"✅ โหมดที่เลือกปัจจุบัน: **{st.session_state.selected_mode}**")

st.markdown("<br>", unsafe_allow_html=True) # เว้นบรรทัด
st.subheader("2️⃣ เลือกแพตช์เวอร์ชัน")

# ช่องใส่ตัวเลข (มีปุ่ม + -)
version = st.number_input(
    "ระบุเลขแพตช์ในอนาคต (เช่น 5.0):",
    min_value=1.0, 
    max_value=15.0, 
    value=5.0, 
    step=0.1, 
    format="%.1f"
)

st.markdown("<br>", unsafe_allow_html=True)

# ปุ่มกดทำนายผล (ปุ่มใหญ่)
predict_btn = st.button("🚀 เริ่มทำนายผล HP", type="primary", use_container_width=True)

st.markdown("---")

# ==========================================
# 5. ส่วนแสดงผลลัพธ์ (อยู่ด้านล่างสุดเสมอ)
# ==========================================
if predict_btn:
    st.subheader("🎯 ผลการพยากรณ์")
    try:
        # เลือกไฟล์โมเดลตามโหมดที่จำไว้ใน st.session_state
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
        
        # กล่องโชว์ผลลัพธ์ตัวใหญ่ๆ
        st.metric(
            label=f"เลือดบอสในโหมด {mode} (แพตช์ {version:.1f})", 
            value=f"{predicted_hp:,.0f} HP"
        )
        
        if predicted_hp < 0:
            st.warning("⚠️ คำเตือน: เลือดบอสติดลบ อาจเกิดจากการใส่เลขแพตช์ในอดีตที่ไกลเกินไป")
        else:
            st.success("✨ ทำนายผลสำเร็จเรียบร้อย!")
            st.balloons()
            
    except FileNotFoundError:
        st.error(f"❌ ระบบหาไฟล์โมเดลของโหมด '{mode}' ไม่พบครับ ลองตรวจสอบไฟล์ .pkl ใน GitHub อีกครั้ง")
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")