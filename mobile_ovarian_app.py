import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64

# 设置适合手机屏幕的页面配置
st.set_page_config(
    page_title="卵巢癌风险评估",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义手机端CSS样式
def set_mobile_style():
    st.markdown(f"""
    <style>
        /* 基础样式 */
        .stApp {{
            max-width: 100%;
            padding: 10px;
            background-color: #fef6f9;
            font-family: 'Arial', sans-serif;
        }}
        
        /* 标题样式 */
        .stMarkdown h1 {{
            color: #e75480;
            font-size: 24px;
            text-align: center;
            margin-bottom: 15px;
        }}
        
        /* 卡片样式 */
        .card {{
            background: white;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(233,84,128,0.1);
            margin-bottom: 15px;
            border-left: 4px solid #e75480;
        }}
        
        /* 输入框样式 */
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select {{
            border-radius: 12px !important;
            border: 1px solid #ffcce0 !important;
            padding: 10px !important;
        }}
        
        /* 按钮样式 */
        .stButton>button {{
            background-color: #e75480;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-size: 16px;
            width: 100%;
            transition: all 0.3s;
        }}
        
        .stButton>button:hover {{
            background-color: #d43d6d;
            box-shadow: 0 4px 12px rgba(233,84,128,0.3);
        }}
        
        /* 风险指示器 */
        .low-risk {{
            color: #4CAF50;
            background-color: #e8f5e9;
            padding: 10px;
            border-radius: 10px;
        }}
        
        .medium-risk {{
            color: #FFC107;
            background-color: #fff8e1;
            padding: 10px;
            border-radius: 10px;
        }}
        
        .high-risk {{
            color: #F44336;
            background-color: #ffebee;
            padding: 10px;
            border-radius: 10px;
        }}
        
        /* 移动端优化 */
        @media (max-width: 600px) {{
            .stSlider {{
                width: 100% !important;
            }}
            .stRadio > div {{
                flex-direction: column;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

set_mobile_style()

# 应用标题
st.markdown("""
<div class="card">
<h1 style="text-align:center;">🌸 卵巢癌风险评估</h1>
<p style="text-align:center; color:#666;">填写您的信息获取个性化风险评估</p>
</div>
""", unsafe_allow_html=True)

# 患者信息输入
with st.expander("👩 基本信息", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("姓名", "李女士")
        age = st.slider("年龄", 30, 80, 45)
    with col2:
        height = st.number_input("身高(cm)", 140, 200, 160)
        weight = st.number_input("体重(kg)", 30, 120, 60)
    
    bmi = weight / ((height/100)**2)
    st.progress(int(min(bmi, 40)/40*100), f"BMI指数: {bmi:.1f} ({'正常' if 18.5 <= bmi <= 24 else '偏高'})")

# 风险因素
with st.expander("⚠️ 风险因素"):
    st.markdown("**请选择所有符合的情况:**")
    
    col1, col2 = st.columns(2)
    with col1:
        family_history = st.checkbox("家族病史", True)
        no_pregnancy = st.checkbox("未生育/未哺乳", True)
        smoking = st.checkbox("长期吸烟")
    with col2:
        hormone_therapy = st.checkbox("激素治疗")
        endometriosis = st.checkbox("子宫内膜异位")
        pcos = st.checkbox("多囊卵巢综合征")
    
    menstrual = st.selectbox("月经状况", ["规律", "不规律", "已绝经（自然）", "已绝经（手术）"])

# 血检报告
with st.expander("💉 血检指标"):
    input_method = st.radio("输入方式", ["手动输入", "上传报告照片"])
    
    if input_method == "手动输入":
        col1, col2 = st.columns(2)
        with col1:
            ca125 = st.number_input("CA-125 (U/mL)", 0, 500, 35)
            he4 = st.number_input("HE4 (pmol/L)", 0, 500, 80)
        with col2:
            afp = st.number_input("AFP (ng/mL)", 0, 20, 5)
            cea = st.number_input("CEA (ng/mL)", 0, 10, 2)
    else:
        uploaded_file = st.file_uploader("上传血检报告", type=["jpg", "png"])
        if uploaded_file is not None:
            st.image(uploaded_file, use_column_width=True)
            st.warning("照片解析功能需配合OCR服务使用，当前为演示模式")

# 风险评估模型
def calculate_risk():
    risk = 0
    
    # 基础风险
    risk += (age - 30) * 0.5
    
    # BMI风险
    if bmi > 28: risk += 10
    
    # 生活习惯风险
    if family_history: risk += 25
    if no_pregnancy: risk += 20
    if smoking: risk += 15
    if hormone_therapy: risk += 15
    if endometriosis: risk += 10
    if pcos: risk += 5
    
    # 月经状况
    if "绝经" in menstrual: risk += 10
    
    # 血检指标
    if ca125 > 35: risk += (ca125 - 35) * 0.3
    if he4 > 80: risk += (he4 - 80) * 0.2
    
    return min(100, risk)

# 评估按钮
if st.button("开始风险评估", type="primary"):
    risk_score = calculate_risk()
    
    st.markdown("---")
    st.markdown("### 📊 评估结果")
    
    # 风险等级显示
    if risk_score < 30:
        st.markdown(f'<div class="low-risk">低风险 (评分: {risk_score:.0f}/100)</div>', unsafe_allow_html=True)
        st.markdown("""
        - ✅ 当前风险较低
        - 🔍 建议每年常规妇科检查
        """)
    elif risk_score < 60:
        st.markdown(f'<div class="medium-risk">中风险 (评分: {risk_score:.0f}/100)</div>', unsafe_allow_html=True)
        st.markdown("""
        - ⚠️ 需要关注的风险因素
        - 🩺 建议6个月复查CA-125
        - 🏥 考虑专科咨询
        """)
    else:
        st.markdown(f'<div class="high-risk">高风险 (评分: {risk_score:.0f}/100)</div>', unsafe_allow_html=True)
        st.markdown("""
        - ❗ 建议立即就医
        - 🔬 需要进一步检查
        - 💊 考虑预防性措施
        """)
    
    # 个性化建议
    st.markdown("### 📋 个性化建议")
    if family_history:
        st.markdown("- 🧬 建议进行BRCA基因检测")
    if no_pregnancy:
        st.markdown("- 🍼 母乳喂养可降低风险")
    if ca125 > 35:
        st.markdown(f"- 🧪 CA-125偏高 ({ca125} U/mL)，建议3个月后复查")
    
    # 可视化图表
    chart_data = pd.DataFrame({
        '因素': ['年龄', '遗传', '生育史', '血检指标'],
        '贡献': [
            (age - 30) * 0.5,
            25 if family_history else 0,
            20 if no_pregnancy else 0,
            max((ca125 - 35) * 0.3, 0) + max((he4 - 80) * 0.2, 0)
        ]
    })
    st.bar_chart(chart_data.set_index('因素'))

# 底部信息
st.markdown("---")
st.caption("""
⚠️ 免责声明: 本评估结果仅供参考，不能替代专业医疗诊断。
""")
