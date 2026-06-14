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
    st.error(f"모델 로드 오류: {e}")
    gb_model = None

# 실제 데이터셋의 과거 전체 평균 발전량 기준값 설정 (실제 df가 정의되어 있어야 합니다)
try:
    AVG_SOLAR_OUTPUT = df['발전량'].mean()
except NameError:
    # 만약 df가 로드되지 않은 환경을 대비한 백업용 평균값입니다. 상황에 맞게 쓰시면 됩니다.
    AVG_SOLAR_OUTPUT = 684.75

st.title("태양광 발전량 예측 시스템")
st.write("새로운 기상 데이터를 입력하면 발전량을 예측합니다.")

# 2. 사용자 입력 받기 (슬라이더 형식)
st.subheader("기상 정보 설정")
wind_speed = st.slider("풍속을 입력하세요 (m/s)", 0.0, 20.0, 2.0, 0.1)
sunshine = st.slider("일조량을 입력하세요 (hr)", 0.0, 1.0, 0.5, 0.1)
radiation = st.slider("일사량을 입력하세요 (MJ/m²)", 0.0, 5.0, 1.0, 0.1)
temperature = st.slider("기온을 입력하세요 (°C)", -20.0, 45.0, 20.0, 0.1)
humidity = st.slider("상대습도를 입력하세요 (%)", 0, 100, 50, 1)

# 3. 예측 실행 버튼
if st.button("발전량 예측하기"):
    if gb_model is not None:
        # DataFrame으로 변환
        input_data = pd.DataFrame(
            [[wind_speed, sunshine, radiation, temperature, humidity]],
            columns=['풍속', '일조량', '일사량', '기온', '상대습도']
        )
        
        try:
            # 3. 예측 (gb_model 사용 - Feature Name 불일치 에러 방지를 위해 .values 사용)
            predicted_production = gb_model.predict(input_data.values)[0]
            
            # 물리적으로 불가능한 음수 발전량은 0으로 처리한다.
            if predicted_production < 0: 
                predicted_production = 0.0
            
            # 대규모 단지 스케일 환산 및 전력 배출 계수 기반 탄소 감축량 산출한다.
            co2_reduction = (predicted_production * 1000) * 0.4173
            
            # 4. 종합 결과를 출력한다.
            st.markdown("---")
            st.subheader("종합 결과")
            st.metric(label="[AI 예측 발전량]", value=f"{predicted_production:.2f} kW")
            st.metric(label="[탄소중립 효과] 예상 탄소 감축량", value=f"{co2_reduction:,.2f} kg CO₂eq")
            
            # 평균보다 낮을 시 경고를 보낸다.
            st.markdown("---")
            if predicted_production < AVG_SOLAR_OUTPUT:
                st.warning(
                    f"[계통 안정화 경보] 현재 예측량({predicted_production:.2f} kW)이 과거 전체 평균치({AVG_SOLAR_OUTPUT:.2f} kW)보다 낮습니다.\n\n"
                    "안내: 전력망 불안정성에 대비하여 대기 전력 확보 및 계통 분배 예비율을 점검하십시오."
                )
            else:
                st.success(f"[정상] 발전량이 과거 평균치({AVG_SOLAR_OUTPUT:.2f} kW) 이상이므로 전력망이 안정적으로 운영 중입니다.")
                
        except Exception as e:
            st.error(f"예측 도중 오류가 발생했습니다: {e}")
    else:
        st.error("모델 파일(solar.pkl)을 로드할 수 없습니다.")
