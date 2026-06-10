import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import joblib

# 페이지 기본 설정
st.set_page_config(
    page_title="태양광 발전량 예측 시스템",
    layout="wide"
)

# 격자 배경 및 상단 오렌지 햇살 효과 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=300;400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #0A192F;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 40px 40px;
        color: #E2E8F0;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem !important;
    }
    
    /* 시작 버튼 디자인 */
    div.stButton > button:first-child {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        font-weight: 500 !important;
        font-size: 15px !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        width: 100% !important;
        transition: all 0.4s ease !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #334155 !important;
        border-color: #ED8936 !important;
        box-shadow: 0 0 15px rgba(237, 137, 54, 0.2) !important;
    }
    
    /* 최상단 오렌지 햇살 애니메이션 효과 */
    @keyframes orangeSunlightDown {
        0% {
            opacity: 0;
            transform: translateY(-100%) scaleX(0.5);
            filter: blur(20px);
        }
        30% {
            opacity: 0.5;
            filter: blur(8px);
        }
        100% {
            opacity: 0.1;
            transform: translateY(0) scaleX(1);
            filter: blur(15px);
        }
    }
    
    .orange-sunlight {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 500px;
        background: radial-gradient(circle at 50% 0%, rgba(255, 243, 224, 0.7) 0%, rgba(237, 137, 54, 0.3) 40%, rgba(237, 137, 54, 0) 80%);
        animation: orangeSunlightDown 2.5s ease-out forwards;
        pointer-events: none;
        z-index: 9999;
    }
    
    [data-testid="stMetricContainer"], div[data-border="true"] {
        background-color: rgba(15, 23, 42, 0.7) !important;
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 15px !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("태양광 에너지 발전량 예측 시스템")
st.caption("기상 분석 모델 기반의 실시간 전력 생성량 예측 대시보드")
st.markdown("---")

# ----------------------------------------------------------------
# AI 모델 로드 구역
# ----------------------------------------------------------------
@st.cache_resource
def load_real_model():
    return joblib.load("solar.pkl")

gb_model = load_real_model()

# 알려주신 진짜 과거 데이터 평균 수치
과거_평균_발전량 = 684.7460707648402

# ----------------------------------------------------------------
# 기상 데이터 입력 레이아웃 (여기에 진짜 수치 옵션들이 다 들어있습니다)
# ----------------------------------------------------------------
st.subheader("기상 관측 데이터 입력")

input_col1, input_col2 = st.columns(2)

with input_col1:
    풍속 = st.slider("풍속 (m/s)", min_value=0.0, max_value=25.0, value=4.0, step=0.1)
    일사량 = st.slider("일사량 (MJ/m²)", min_value=0.0, max_value=40.0, value=20.0, step=0.1)

with input_col2:
    기온 = st.slider("기온 (°C)", min_value=-20.0, max_value=45.0, value=22.0, step=0.1)
    일조량 = st.slider("일조량 (hr)", min_value=0.0, max_value=14.0, value=8.0, step=0.1)

st.markdown("---")
시작_버튼 = st.button("태양광 발전 예측 시작")

# ----------------------------------------------------------------
# 연산 및 결과 시각화 구역
# ----------------------------------------------------------------
if 시작_버튼:
    st.markdown('<div class="orange-sunlight"></div>', unsafe_allow_html=True)
    time.sleep(1.0)
    
    input_data = pd.DataFrame(
        [[풍속, 일사량, 기온, 일조량]],
        columns=['풍속', '일사량', '기온', '일조량']
    )
    
    # 모델 결과 추론 및 음수 방지 처리
    원래_예측값 = gb_model.predict(input_data)[0]
    예측_발전량 = max(0.0, 원래_예측값)
    
    st.subheader("예측 결과 분석")
    col_metric1, col_metric2 = st.columns(2)
    
    with col_metric1:
        with st.container(border=True):
            st.markdown("<small style='color:#94A3B8;'>GB 모델 예측 발전량</small>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='color:#F8FAFC; margin: 10px 0;'>{예측_발전량:.2f} <span style='font-size:16px; font-weight:normal;'>kW</span></h2>", unsafe_allow_html=True)
            
    with col_metric2:
        with st.container(border=True):
            st.markdown("<small style='color:#94A3B8;'>과거 평균 발전량 대비 차이</small>", unsafe_allow_html=True)
            차이 = 예측_발전량 - 과거_평균_발전량
            부호 = "+" if 차이 >= 0 else ""
            st.markdown(f"<h2 style='color:#94A3B8; margin: 10px 0;'>{부호}{차이:.2f} <span style='font-size:16px; font-weight:normal;'>kW</span></h2>", unsafe_allow_html=True)

    st.write("")

    # 과거 평균 발전량과 예측치 가로 막대 비교
    with st.container(border=True):
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#F8FAFC; margin-bottom:10px;'>과거 평균 발전량 비교 지표</p>", unsafe_allow_html=True)
        
        항목 = ['과거 평균 발전량', 'GB 모델 예측치']
        수치 = [과거_평균_발전량, 예측_발전량]
        
        fig_bar = go.Figure(go.Bar(
            y=항목,
            x=수치,
            orientation='h',
            marker_color=['#4A5568', '#ED8936'], 
            text=[f" {v:.2f} kW" for v in 수치],
            textposition='outside',
            textfont=dict(color='#F8FAFC', size=12)
        ))
        
        # 은은한 흰빛의 세로 기준선 매칭
        fig_bar.add_shape(
            type="line", x0=과거_평균_발전량, y0=-0.5, x1=과거_평균_발전량, y1=1.5,
            line=dict(color="#CBD5E1", width=1.5, dash="solid")
        )
        
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=200,
            margin=dict(l=10, r=80, t=10, b=10),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(tickfont=dict(color='#E2E8F0', size=12))
        )
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align: center; padding: 40px 0;">
                <h4 style="font-weight: 500; color: #F8FAFC;">기상 변수 설정 대기 중</h4>
                <p style="color: #64748B; font-size: 13px; max-width: 400px; margin: 8px auto 0 auto;">
                    화면 상단의 수치 슬라이더를 조정한 뒤 하단의 버튼을 실행하면 대시보드 연산 및 기상 스캔이 시작됩니다.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )