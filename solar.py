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

# ☀️ 상단 타이틀 구역
st.markdown("<h2 style='margin-bottom:0px;'>☀️ 머신러닝 기반 태양광 발전량 분석 시스템</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#666; font-size:14px; margin-top:0px; margin-bottom:10px;'>Predictive Analytics for Solar Power Generation</p>", unsafe_allow_html=True)

# ☀️ 좌우 2분할 레이아웃
main_col1, main_col2 = st.columns([1, 1.2])

# --- 왼쪽 구역: 입력 폼 ---
with main_col1:
    with st.form(key="solar_prediction_form"):
        st.markdown("<h4 style='margin-top:0px;'>☀️ 기상 정보 입력</h4>", unsafe_allow_html=True)
        
        input_col1, input_col2 = st.columns(2)
        with input_col1:
            temp = st.slider("기온 (°C)", min_value=-20.0, max_value=45.0, value=20.0, step=0.1)
            # 🛠️ '일조 시간'에서 실제 변수명인 '일조량'으로 수정 완료!
            sun = st.slider("일조량", min_value=0.0, max_value=15.0, value=6.0, step=0.1)
        with input_col2:
            wind = st.slider("풍속 (m/s)", min_value=0.0, max_value=25.0, value=3.5, step=0.1)
            # 🛠️ 실제 변수명인 '일사량' 유지 및 배치 확인!
            rad = st.slider("일사량 (MJ/m²)", min_value=0.0, max_value=50.0, value=15.0, step=0.1)
            
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        submit_button = st.form_submit_button("☀️ 발전량 예측하기", use_container_width=True)

# --- 오른쪽 구역: 예측 결과 ---
with main_col2:
    st.markdown("<h4 style='margin-top:0px;'>☀️ 실시간 시뮬레이션 결과</h4>", unsafe_allow_html=True)
    
    if submit_button:
        # 🛠️ 중요: 실제 학습시킨 데이터셋 변수 순서인 ['풍속', '일사량', '기온', '일조량']을 완벽하게 맞춤!
        input_data = pd.DataFrame([[wind, rad, temp, sun]], columns=['풍속', '일사량', '기온', '일조량'])
        
        prediction = model.predict(input_data)[0]
        if prediction < 0: prediction = 0.0

        # 탄소 감축량 계산
        co2_reduction = (prediction * 1000) * 0.4173

        # 결과 지표 노출
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="☀️ 예상 전력 발전량", value=f"{prediction:.2f} kW")
        with res_col2:
            st.metric(label="☀️ 태양광 에너지 사용 시 감축 탄소량", value=f"{co2_reduction:,.2f} kg")

        # 분석 요약 박스
        st.markdown(f"""
            <div style="background-color:#FFFDE7; padding:15px; border-radius:8px; border-left:5px solid #F57C00; margin-top:10px;">
                <b style="color:#E65100; font-size:14px;">☀️ 인공지능 분석 및 탄소 배출 계수 산정 요약</b><br>
                <p style="color:#4E342E; font-size:13px; margin:3px 0 0 0; line-height:1.4;">
                    예측 전력 출력값은 <b>{prediction:.2f} kW</b>입니다. 정부 지침(GHG Protocol Scope 2)에 의거하여 자가소비형 태양광의 배출 계수는 <b>0 tCO₂eq/MWh</b>이므로, 한전 전력 대비 <b>100% 간접 배출량이 상쇄</b>되어 총 <b>{co2_reduction:,.2f} kg CO₂eq</b>의 온실가스를 감축합니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if temp >= 30.0:
            st.warning("☀️ [주의] 기온 30°C 이상 고온 구간으로, 온도 계수에 의해 패널 효율이 저하될 수 있습니다.")
            
    else:
        st.info("👈 왼쪽에서 기상 정보를 입력한 후 [☀️ 발전량 예측하기] 버튼을 눌러주세요!")

# 최하단 풋터
st.markdown("<hr style='margin-top:20px; margin-bottom:5px;'>", unsafe_allow_html=True)
st.caption("☀️ 모델: Gradient Boosting Regressor | 근거: 공표된 2023년 전력배출계수 (0.4173 tCO2eq/MWh)")
