import streamlit as st
import pandas as pd
import joblib

# 페이지 설정 (태양광 느낌의 아이콘과 넓은 레이아웃)
st.set_page_config(page_title="태양광 발전량 예측 시스템", page_icon="☀️", layout="wide")

# 모델 불러오기
@st.cache_resource
def load_model():
    try:
        return joblib.load("solar.pkl")
    except Exception as e:
        return e

model_result = load_model()

if isinstance(model_result, Exception):
    st.error(f"⚠️ 모델 로드 실패: {model_result}")
    st.stop()
else:
    model = model_result

# 메인 타이틀
st.title("☀️ 머신러닝 기반 태양광 발전량 분석 시스템")
st.markdown("<p style='color:#666; font-size:16px; margin-top:-10px;'>Predictive Analytics for Solar Power Generation</p>", unsafe_allow_html=True)
st.markdown("---")

# 데이터 입력 폼
with st.form(key="solar_prediction_form"):
    st.markdown("### 🔍 기상 관측 데이터 입력")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<b style='color:#E65100;'>🌡️ 대기 환경 인자</b>", unsafe_allow_html=True)
        temp = st.slider("기온 (°C)", min_value=-20.0, max_value=45.0, value=20.0, step=0.1)
        sun = st.slider("일조 시간 (hr)", min_value=0.0, max_value=15.0, value=6.0, step=0.1)

    with col2:
        st.markdown("<b style='color:#E65100;'>💨 역학 및 에너지 인자</b>", unsafe_allow_html=True)
        wind = st.slider("풍속 (m/s)", min_value=0.0, max_value=25.0, value=3.5, step=0.1)
        rad = st.slider("일사량 (MJ/m²)", min_value=0.0, max_value=50.0, value=15.0, step=0.1)
        
    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button("🚀 발전량 예측하기", use_container_width=True)

# 버튼 클릭 시 연산 및 결과 출력
if submit_button:
    st.markdown("---")
    st.markdown("### 🔮 실시간 시뮬레이션 결과")
    
    input_data = pd.DataFrame([[wind, rad, temp, sun]], columns=['풍속', '일사량', '기온', '일조량'])
    
    prediction = model.predict(input_data)[0]
    if prediction < 0: prediction = 0.0

    # 🛠️ 2023년 공표 최신 전력배출계수 기반 탄소 감축량만 계산 (0.4173 kg CO2eq/kWh)
    co2_reduction = prediction * 0.4173

    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        st.metric(label="예상 전력 발전량 (Predicted Output)", value=f"{prediction:.2f} kW")
        # 소나무 문구 삭제 후 깔끔하게 환경 지표만 노출
        st.caption(f"🌱 해당 전력 생산 시 온실가스 감축량: 약 {co2_reduction:.3f} kg CO₂eq")

    with res_col2:
        st.markdown(f"""
            <div style="background-color:#FFFDE7; padding:22px; border-radius:10px; border-left:6px solid #F57C00;">
                <b style="color:#E65100; font-size:15px;">☀️ 인공지능 분석 요약</b><br>
                <p style="color:#4E342E; font-size:14px; margin:5px 0 0 0; line-height:1.5;">
                    설정하신 기상 데이터를 기반으로 알고리즘을 연산한 결과, 
                    해당 환경에서의 최종 기대 전력 출력값은 <span style="color:#E65100; font-weight:bold;">{prediction:.2f} kW</span>로 분석되었습니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if temp >= 30.0:
            st.markdown("<br>", unsafe_allow_html=True)
            st.warning("⚠️ **[에너지공학적 특이사항]** 현재 설정된 기온이 30°C 이상으로 높습니다. 일반적인 실리콘 태양전지는 패널 표면 온도가 상승할 수록 효율 계수(Temperature Coefficient)에 의해 전력 출력이 다소 저하될 수 있음을 유의하십시오.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("🤖 모델: Gradient Boosting Regressor | 탄소 감축 근거: 공표된 2023년 전력배출계수 (0.4173 tCO2eq/MWh)")
