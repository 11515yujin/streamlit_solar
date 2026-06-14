import streamlit as st
import pandas as pd
import joblib

# 1. 모델 로드
@st.cache_resource
def load_model():
    return joblib.load("solar.pkl")

try:
    gb_model = load_model()
except Exception as e:
    st.error(f"모델을 불러오는 중 오류가 발생했습니다: {e}")
    gb_model = None

# 과거 전체 평균 발전량 기준값 설정
AVG_SOLAR_OUTPUT = 684.75 

st.title("태양광 발전량 예측 시스템")
st.write("기상 데이터를 입력하면 AI 모델 기반으로 발전량을 예측합니다.")

# 2. 사용자 입력 받기
st.subheader("기상 정보 입력")
wind_speed = st.number_input("풍속 (m/s)", min_value=0.0, value=2.0, step=0.1)
sunshine = st.number_input("일조량 (hr)", min_value=0.0, value=0.5, step=0.1)
radiation = st.number_input("일사량 (MJ/m²)", min_value=0.0, value=1.0, step=0.1)
temperature = st.number_input("기온 (°C)", value=20.0, step=0.1)
humidity = st.number_input("상대습도 (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0)

# 3. 예측 실행 버튼
if st.button("발전량 예측하기"):
    if gb_model is not None:
        # 지정된 변수 순서 매칭
        input_data = pd.DataFrame(
            [[wind_speed, sunshine, radiation, temperature, humidity]],
            columns=['풍속', '일조량', '일사량', '기온', '상대습도']
        )
        
        # 예측
        predicted_production = gb_model.predict(input_data)[0]
        
        # 물리적으로 불가능한 음수 발전량 0 처리
        if predicted_production < 0: 
            predicted_production = 0.0
            
        # 탄소 감축량 산출 (2023년 공표 계수 0.4173 kg CO2eq/kWh 적용, kW -> MW 스케일 업)
        co2_reduction = (predicted_production * 1000) * 0.4173
        
        # 결과 출력
        st.markdown("---")
        st.subheader("예측 결과")
        st.metric(label="AI 예측 발전량", value=f"{predicted_production:.2f} kW")
        st.metric(label="예상 탄소 감축량", value=f"{co2_reduction:,.2f} kg CO₂eq")
        
        # 전력 계통 안정화 선제 경보 모듈
        st.markdown("---")
        if predicted_production < AVG_SOLAR_OUTPUT:
            st.warning(
                f"[계통 안정화 경보] 현재 예측량({predicted_production:.2f} kW)이 과거 전체 평균치({AVG_SOLAR_OUTPUT:.2f} kW)보다 낮습니다.\n\n"
                "안내: 전력망 불안정성에 대비하여 대기 전력 확보 및 계통 분배 예비율을 점검하십시오."
            )
        else:
            st.success(f"[정상] 발전량이 과거 평균치({AVG_SOLAR_OUTPUT:.2f} kW) 이상이므로 전력망이 안정적으로 운영 중입니다.")
    else:
        st.error("모델이 로드되지 않아 예측을 수행할 수 없습니다.")
