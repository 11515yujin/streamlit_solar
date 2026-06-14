import streamlit as st
import pandas as pd
import joblib

# 페이지 설정 (귀여운 아이콘과 제목)
st.set_page_config(page_title="태양광 발전 예측", page_icon="☀️", layout="centered")

# 모델 불러오기 (정확히 'solar.pkl' 지정)
@st.cache_resource
def load_model():
    return joblib.load("solar.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"⚠️ 모델 파일을 불러오지 못했습니다. 'solar.pkl' 파일이 같은 폴더에 있는지 확인해주세요! 에러: {e}")
    st.stop()

# 메인 화면 디자인
st.title("☀️ AI 태양광 발전량 예측기")
st.write("기상 데이터를 슬라이더로 조절하여 실시간 발전량을 확인해보세요!")
st.markdown("---")

# 입력 섹션 (드래그 가능한 슬라이더)
st.subheader("🔍 기상 데이터 입력")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🌡️ 환경 요인")
    temp = st.slider("기온 (°C)", min_value=-20.0, max_value=45.0, value=20.0, step=0.1)
    sun = st.slider("일조량 (hr)", min_value=0.0, max_value=15.0, value=6.0, step=0.1)

with col2:
    st.markdown("#### 💨 에너지 요인")
    wind = st.slider("풍속 (m/s)", min_value=0.0, max_value=25.0, value=3.5, step=0.1)
    rad = st.slider("일사량 (MJ/m²)", min_value=0.0, max_value=50.0, value=15.0, step=0.1)

st.markdown("---")

# 예측 수행 및 결과 출력 (코랩 컬럼 순서: 풍속, 일사량, 기온, 일조량)
input_data = pd.DataFrame([[wind, rad, temp, sun]], columns=['풍속', '일사량', '기온', '일조량'])

if st.button("🚀 발전량 예측하기", use_container_width=True):
    prediction = model.predict(input_data)[0]
    
    # 귀여운 축하 풍선 효과
    st.balloons()
    
    # 결과 박스 디자인
    st.markdown(f"""
        <div style="background-color:#FFF9C4; padding:30px; border-radius:20px; border:3px dashed #FBC02D; text-align:center;">
            <h2 style="color:#F57F17; margin:0;">📊 예측 결과</h2>
            <p style="font-size:20px; color:#444;">오늘의 날씨 정보로 계산된 예상 발전량은?</p>
            <h1 style="color:#E65100; font-size:60px; margin:10px 0;">{prediction:.2f} <span style="font-size:30px;">kW</span></h1>
        </div>
    """, unsafe_allow_html=True)

# 하단 정보
st.caption("🤖 이 앱은 Gradient Boosting 알고리즘을 기반으로 제작되었습니다.")
