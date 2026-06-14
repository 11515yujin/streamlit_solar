import streamlit as st
import pandas as pd
import joblib

# ☀️ 페이지 설정
st.set_page_config(page_title="태양광 발전량 예측 시스템", page_icon="☀️", layout="wide")

# ☀️ 모델 불러오기
@st.cache_resource
def load_model():
    try:
        return joblib.load("solar.pkl")
    except Exception as e:
        return e

model_result = load_model()

if isinstance(model_result, Exception):
    st.error(f"☀️ 모델 로드 실패: {model_result}")
    st.stop()
else:
    model = model_result

# ☀️ 메인 타이틀
st.title("☀️ 머신러닝 기반 태양광 발전량 분석 시스템")
st.markdown("<p style='color:#666; font-size:16px; margin-top:-10px;'>Predictive Analytics for Solar Power Generation</p>", unsafe_allow_html=True)
st.markdown("---")

# ☀️ 데이터 입력 폼
with st.form(key="solar_prediction_form"):
    st.markdown("### ☀️ 기상 정보 입력")
    col1, col2 = st.columns(2)

    with col1:
        temp = st.slider("기온 (°C)", min_value=-20.0, max_value=45.0, value=20.0, step=0.1)
        sun = st.slider("일조 시간 (hr)", min_value=0.0, max_value=15.0, value=6.0, step=0.1)

    with col2:
        wind = st.slider("풍속 (m/s)", min_value=0.0, max_value=25.0, value=3.5, step=0.1)
        rad = st.slider("일사량 (MJ/m²)", min_value=0.0, max_value=50.0, value=15.0, step=0.1)
        
    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button("☀️ 발전량 예측하기", use_container_width=True)

# ☀️ 버튼 클릭 시 연산 및 결과 출력
if submit_button:
    st.markdown("---")
    st.markdown("### ☀️ 실시간 시뮬레이션 결과")
    
    input_data = pd.DataFrame([[wind, rad, temp, sun]], columns=['풍속', '일사량', '기온', '일조량'])
    
    prediction = model.predict(input_data)[0]
    if prediction < 0: prediction = 0.0

    # ☀️ 화석연료 전력 배출 계수 대비 탄소 감축량 연산 (x1000 스케일 적용)
    co2_reduction = (prediction * 1000) * 0.4173

    # ☀️ 메인 지표 레이아웃
    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric(label="☀️ 예상 전력 발전량 (Predicted Output)", value=f"{prediction:.2f} kW")

    with metric_col2:
        # 🛠️ 문구 수정 완료! 직관적이고 이해하기 쉬운 라벨로 변경
        st.metric(label="☀️ 태양광 에너지를 사용했을 때 감축할 수 있는 탄소량", value=f"{co2_reduction:,.2f} kg CO₂eq")

    st.markdown("<br>", unsafe_allow_html=True)

    # ☀️ 분석 요약 박스
    st.markdown(f"""
        <div style="background-color:#FFFDE7; padding:22px; border-radius:10px; border-left:6px solid #F57C00;">
            <b style="color:#E65100; font-size:15px;">☀️ 인공지능 분석 및 탄소 배출 계수 산정 요약</b><br>
            <p style="color:#4E342E; font-size:14px; margin:5px 0 0 0; line-height:1.5;">
                설정하신 기상 조건을 기반으로 모델이 예측한 최종 전력 출력값은 <b>{prediction:.2f} kW</b>입니다.<br>
                정부 지침 및 글로벌 탄소 회계 기준(GHG Protocol Scope 2)에 의거하여, 자가소비형 태양광 발전 전력의 배출 계수는 <b>0 tCO₂eq/MWh</b>으로 처리됩니다. <br>
                따라서 일반 한전 계통 전력을 사용할 때와 비교하여, 본 시스템의 발전량만큼 <b>100% 간접 배출량이 상쇄</b>되므로 총 <span style="color:#E65100; font-weight:bold;">{co2_reduction:,.2f} kg CO₂eq</span>의 온실가스를 감축하는 효과를 창출합니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # ☀️ 고온 주의 알림 (30도 이상일 때)
    if temp >= 30.0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.warning("☀️ [에너지공학적 특이사항] 현재 설정된 기온이 30°C 이상으로 높습니다. 일반적인 실리콘 태양전지는 패널 표면 온도가 상승할 수록 효율 계수(Temperature Coefficient)에 의해 전력 출력이 다소 저하될 수 있음을 유의하십시오.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("☀️ 모델: Gradient Boosting Regressor | 탄소 감축 근거: 공표된 2023년 전력배출계수 (0.4173 tCO2eq/MWh) 및 GHG Protocol Scope 2 지침")
