import streamlit as st
import pandas as pd
import joblib

# 화면 넓게 쓰기 설정
st.set_page_config(layout="wide")

@st.cache_resource
def load_model(): return joblib.load("realsolar.pkl")

try: gb_model = load_model()
except Exception as e: st.error(f"모델 로드 오류: {e}"); gb_model = None

AVG_SOLAR_OUTPUT = 684.75 
st.title("☀️ 태양광 발전량 예측 시스템")

# 좌우 대형 3분할 레이아웃으로 스크롤 차단
main_col1, main_col2, main_col3 = st.columns([1.2, 1.2, 1.5])

with main_col1:
    st.subheader("☀️ 기상 정보 1")
    wind_speed = st.slider("☀️ 풍속 (m/s)", 0.0, 20.0, 2.0, 0.1)
    sunshine = st.slider("☀️ 일조량 (hr)", 0.0, 1.0, 0.5, 0.1)
    radiation = st.slider("☀️ 일사량 (MJ/m²)", 0.0, 5.0, 1.0, 0.1)

with main_col2:
    st.subheader("☀️ 기상 정보 2")
    temperature = st.slider("☀️ 기온 (°C)", -20.0, 45.0, 20.0, 0.1)
    humidity = st.slider("☀️ 상대습도 (%)", 0, 100, 50, 1)
    st.write("") 
    predict_btn = st.button("☀️ 발전량 예측하기", use_container_width=True)

with main_col3:
    st.subheader("☀️ 예측 결과 및 분석")
    if predict_btn:
        if gb_model is not None:
            try:
                input_data = pd.DataFrame([[wind_speed, sunshine, radiation, temperature, humidity]], columns=['풍속', '일조량', '일사량', '기온', '상대습도'])
                predicted_production = gb_model.predict(input_data.values)[0]
            except ValueError:
                input_data_4 = pd.DataFrame([[wind_speed, sunshine, radiation, temperature]], columns=['풍속', '일조량', '일사량', '기온'])
                predicted_production = gb_model.predict(input_data_4.values)[0]
            
            if predicted_production < 0: predicted_production = 0.0
            co2_reduction = (predicted_production * 1000) * 0.4173
            
            # 결과 지표 배치
            res_col1, res_col2 = st.columns(2)
            with res_col1: st.metric(label="☀️ AI 예측 발전량", value=f"{predicted_production:.2f} kW")
            with res_col2: st.metric(label="☀️ 예상 탄소 감축량", value=f"{co2_reduction:,.2f} kg")
            
            st.markdown("---")
            if predicted_production < AVG_SOLAR_OUTPUT:
                st.warning(f"☀️ [계통 경보] 현재 예측량({predicted_production:.2f}kW)이 과거 전체 평균치({AVG_SOLAR_OUTPUT:.2f}kW)보다 낮습니다. 대기 전력 확보 및 계통 분배 예비율을 점검하십시오.")
            else:
                st.success(f"☀️ [정상] 발전량이 과거 평균치({AVG_SOLAR_OUTPUT:.2f}kW) 이상이므로 전력망이 안정적으로 운영 중입니다.")
        else:
            st.error("☀️ realsolar.pkl 파일을 로드할 수 없습니다.")
    else:
        st.info("☀️ 왼쪽에서 조건을 조절한 후 [발전량 예측하기] 버튼을 눌러주세요.")
