import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. ตั้งค่าหน้าเพจหลัก (Page Config)
# ==========================================
st.set_page_config(
    page_title="HSR HP Predictor",
    page_icon="✨",
    layout="wide"
)

# ==========================================
# 2. แถบด้านข้าง (Sidebar) - ข้อมูลผู้จัดทำ
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>👨‍💻 ผู้จัดทำ</h2>", unsafe_allow_html=True)
    
    # ใส่รูปโปรไฟล์ (เปลี่ยน URL เป็นรูปของคุณเอง หรือใส่ไฟล์รูปเช่น "profile.jpg" ไว้ในโฟลเดอร์เดียวกัน)
    st.image("https://api.dicebear.com/7.x/adventurer/svg?seed=Felix", use_container_width=True)
    
    st.markdown("---")
    # ข้อมูลส่วนตัว
    st.markdown("**ชื่อ-นามสกุล:** เทพทัต ทับทิมไทร")
    st.markdown("**รหัสนักศึกษา:** `[ใส่รหัสนักศึกษาของคุณ]`")
    st.markdown("**หมู่เรียน:** `[ใส่หมู่เรียนของคุณ]`")
    
    st.markdown("---")
    st.info("โปรเจกต์นี้ใช้ Machine Learning (Linear Regression) ในการพยากรณ์อัตราการเติบโตของ HP ศัตรูในเกม Honkai: Star Rail")

# ==========================================
# 3. ส่วนเนื้อหาหลัก (Main Content)
# ==========================================
st.title("✨ Honkai: Star Rail - Boss HP Predictor")
st.markdown("ระบบทำนายเงินเฟ้อ HP ของบอสในแพตช์อนาคต")

# สร้าง Layout แบ่งเป็น 2 คอลัมน์
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("⚙️ ตั้งค่าการทำนาย")
    # เลือกโหมด
    mode = st.selectbox(
        "เลือกโหมดเกม (Game Mode):",
        ["Memory of Chaos", "Pure Fiction", "Apocalyptic Shadow"]
    )
    
    # เลื่อนเลือกแพตช์เวอร์ชัน
    version = st.slider("เลือกแพตช์เวอร์ชันในอนาคต (Patch Version):", min_value=1.0, max_value=10.0, value=5.0, step=0.1)
    
    predict_btn = st.button("🚀 ทำนายผล HP", type="primary", use_container_width=True)

# ==========================================
# 4. ฟังก์ชันทำนายผล
# ==========================================
if predict_btn:
    try:
        # เลือกไฟล์โมเดลตามโหมดที่ผู้ใช้เลือก
        if mode == "Memory of Chaos":
            model = joblib.load('hsr_moc_model.pkl')
            mode_color = "purple"
        elif mode == "Pure Fiction":
            model = joblib.load('hsr_pf_model.pkl')
            mode_color = "orange"
        else:
            model = joblib.load('hsr_as_model.pkl')
            mode_color = "red"
            
        # ทำการทำนาย (Model ต้องการ input เป็น 2D array)
        X_pred = np.array([[version]])
        predicted_hp = model.predict(X_pred)[0]
        
        # แสดงผลลัพธ์
        with col2:
            st.subheader("🎯 ผลการพยากรณ์")
            # โชว์ตัวเลขสวยๆ ด้วย st.metric
            st.metric(
                label=f"เลือดบอสในแพตช์ {version:.1f} ({mode})", 
                value=f"{predicted_hp:,.0f} HP"
            )
            
            if predicted_hp < 0:
                st.error("คำเตือน: โมเดลอาจจะทำนายคลาดเคลื่อน เนื่องจากเป็นการทำนายย้อนกลับไปแพตช์เก่ามากๆ")
            else:
                st.success("ทำนายผลสำเร็จ!")
                st.balloons() # เอฟเฟกต์ลูกโป่งลอยขึ้นมาตอนทำนายเสร็จ
                
    except FileNotFoundError:
        with col2:
            st.error(f"❌ ไม่พบไฟล์โมเดลสำหรับ {mode} กรุณาตรวจสอบว่ามีไฟล์ .pkl อยู่ในโฟลเดอร์เดียวกับ app.py หรือไม่")
    except Exception as e:
        with col2:
            st.error(f"เกิดข้อผิดพลาด: {e}")