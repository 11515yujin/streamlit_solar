import streamlit as st
import pandas as pd
import joblib

@st.cache_resource
def load_model(): return joblib.load("realsolar.pkl")

try: gb_model = load_model()
except Exception as e: st.error(f"모델 로드 오류: {e}"); gb_model = None

AVG_SOLAR_OUTPUT = 684.75 
st.title("태양광 발전량 예측 시스템")

# 캡처를 위해 사이드바(Sidebar)로 입력창을 몰아서 화면을 넓게 쓰거나 메인에 조밀하게 배치
st.subheader("기상 정보 설정")
col1, col2 = st.columns(2)  # 2열 배치로 세로 길이 단축
with col1:
    wind_speed = st.slider("풍속 (m/s)", 0.0, 20.0, 2.0, 0.1)
    sunshine = st.slider("일조량 (hr)", 0.0, 1.0, 0.5, 0.1)
    radiation = st.slider("일사량 (MJ/m²)", 0.0, 5.0, 1.0, 0.1)
with col2:
    temperature = st.slider("기온 (°C)", -20.0, 45.0, 20.0, 0.1)
    humidity = st.slider("상대습도 (%)", 0, 100, 50, 1)

if st.button("발전량 예측하기"):
    if gb_model is not None:
        try:
            input_data = pd.DataFrame([[wind_speed, sunshine, radiation, temperature, humidity]], columns=['풍속', '일조량', '일사량', '기온', '상대습도'])
            predicted_production = gb_model.predict(input_data.values)[0]
        except ValueError:
            input_data_4 = pd.DataFrame([[wind_speed, sunshine, radiation, temperature]], columns=['풍속', '일조량', '일사량', '기온'])
            predicted_production = gb_model.predict(input_data_4.values)[0]
        
        if predicted_production < 0: predicted_production = 0.0
        co2_reduction = (predicted_production * 1000) * 0.4173
        
        # 결과 창도 나란히 배치해서 한눈에 보이게 수정
        st.markdown("---")
        res1, res2 = st.columns(2)
        with res1: st.metric(label="[AI 예측 발전량]", value=f"{predicted_production:.2f} kW")
        with res2: st.metric(label="[탄소중립] 예상 탄소 감축량", value=f"{co2_reduction:,.2f} kg CO₂eq")
        
        if predicted_production < AVG_SOLAR_OUTPUT:
            st.warning(f"[경보] 예측량({predicted_production:.2f}kW)이 과거 평균({AVG_SOLAR_OUTPUT:.2f}kW)보다 낮습니다. 대기 전력을 점검하십시오.")
        else:
            st.success(f"[정상] 발전량이 과거 평균({AVG_SOLAR_OUTPUT:.2f}kW) 이상이므로 전력망이 안정적입니다.")
    else: st.error("realsolar.pkl 로드 실패")
