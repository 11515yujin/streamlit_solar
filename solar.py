import streamlit as st
import pandas as pd
import joblib

# 페이지 설정 (넓은 대시보드 레이아웃)
st.set_page_config(page_title="태양광 발전량 예측 시스템", page_icon="📊", layout="wide")

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

# 메인 타이틀 (깔끔하고 전문적인 서체 느낌)
st.title("📊 머신러닝 기반 태양광 발전량 분석 시스템")
st.markdown("<p style='color:#666; font-size:16px; margin-top:-10px;'>Predictive Analytics for Solar Power Generation</p>", unsafe_allow_html=True)
st.markdown("---")

# 입력 섹션 (사이드바 없이 메인 화면에 2열로 배치)
st.markdown("### 🔍 기상 관측 데이터 입력")
col1, col2 = st.columns(2)

with col1:
    st.markdown("<b style='color:#1E3A8A;'>🌡️ 대기 환경 인자</b>", unsafe_allow_html=True)
    temp = st.slider("기온 (°C)", min_value=-20.0, max_value=45.0, value=20.0, step=0.1)
    sun = st.slider("일조 시간 (hr)", min_value=0.0, max_value=15.0, value=6.0, step=0.1)

with col2:
    st.markdown("<b style='color:#1E3A8A;'>💨 역학 및 에너지 인자</b>", unsafe_allow_html=True)
    wind = st.slider("풍속 (m/s)", min_value=0.0, max_value=25.0, value=3.5, step=0.1)
    rad = st.slider("일사량 (MJ/m²)", min_value=0.0, max_value=50.0, value=15.0, step=0.1)

st.markdown("---")

# 데이터 프레임 구축 (순서: 풍속, 일사량, 기온, 일조량)
input_data = pd.DataFrame([[wind, rad, temp, sun]], columns=['풍속', '일사량', '기온', '일조량'])

# 예측 수행 및 음수 방지 처리
prediction = model.predict(input_data)[0]
if prediction < 0: prediction = 0.0

# 결과 출력 섹션 (세련된 기업형 모니터링 카드 디자인)
st.markdown("### 🔮 실시간 시뮬레이션 결과")

res_col1, res_col2 = st.columns([1, 2])

with res_col1:
    # 스트림릿 고급 내장 메트릭 활용
    st.metric(label="예상 전력 발전량 (Predicted Output)", value=f"{prediction:.2f} kW")

with res_col2:
    # 연구실 대시보드 감성의 네이비 블루 카드
    st.markdown(f"""
        <div style="background-color:#F4F6F9; padding:22px; border-radius:10px; border-left:6px solid #0F172A;">
            <b style="color:#0F172A; font-size:15px;">📊 인공지능 분석 요약</b><br>
            <p style="color:#334155; font-size:14px; margin:5px 0 0 0; line-height:1.5;">
                입력된 기상 조건 알고리즘 연산 결과, 해당 환경에서의 기대 전력 출력값은 
                <span style="color:#1E3A8A; font-weight:bold;">{prediction:.2f} kW</span>로 추정됩니다.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("🤖 Gradient Boosting Regressor기반 태양광 발전 예측 모델")
