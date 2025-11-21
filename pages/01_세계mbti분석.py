import streamlit as st
import pandas as pd
import altair as alt

# ----------------------------
# 기본 설정
# ----------------------------
st.set_page_config(
    page_title="🌍 MBTI 국가 분포 TOP/BOTTOM 10",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 MBTI 유형별 국가 분포 Top 10 / Bottom 10")
st.caption("CSV에서 국가별 MBTI 비율을 읽어와, 선택한 유형의 상·하위 10개 국가를 Altair로 시각화합니다.")

# ----------------------------
# 데이터 로드
# ----------------------------
@st.cache_data
def load_data(path="countriesMBTI_16types.csv"):
    df = pd.read_csv(path)
    return df

df = load_data()

# 컬럼 확인
if "Country" not in df.columns:
    st.error("CSV에 'Country' 컬럼이 없습니다. 파일 형식을 확인해주세요.")
    st.stop()

mbti_cols = [c for c in df.columns if c != "Country"]

# ----------------------------
# MBTI 선택 UI
# ----------------------------
selected_mbti = st.selectbox(
    "📌 MBTI 유형을 선택하세요",
    mbti_cols,
    index=0
)

# ----------------------------
# Top 10 / Bottom 10 계산
# ----------------------------
# 숫자 변환(혹시 문자열 섞여있을 경우 대비)
df[selected_mbti] = pd.to_numeric(df[selected_mbti], errors="coerce")

top10 = (
    df[["Country", selected_mbti]]
    .dropna()
    .sort_values(by=selected_mbti, ascending=False)
    .head(10)
    .reset_index(drop=True)
)

bottom10 = (
    df[["Country", selected_mbti]]
    .dropna()
    .sort_values(by=selected_mbti, ascending=True)
    .head(10)
    .reset_index(drop=True)
)

# 퍼센트 표기용 컬럼(원본은 비율 0~1)
top10["percent"] = top10[selected_mbti] * 100
bottom10["percent"] = bottom10[selected_mbti] * 100

# ----------------------------
# Altair 차트 함수
# ----------------------------
def make_bar_chart(data, title, color="#4C78A8"):
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("percent:Q", title=f"{selected_mbti} 비율(%)"),
            y=alt.Y("Country:N", sort="-x", title="국가"),
            tooltip=[
                alt.Tooltip("Country:N", title="국가"),
                alt.Tooltip("percent:Q", title="비율(%)", format=".2f")
            ],
            color=alt.value(color)
        )
        .properties(
            title=title,
            height=420
        )
        .interactive()
    )

# ----------------------------
# 화면 출력
# ----------------------------
st.subheader(f"🏆 {selected_mbti} 비율이 가장 높은 나라 Top 10")
top_chart = make_bar_chart(top10, f"Top 10 Countries for {selected_mbti}", color="#2ca02c")
st.altair_chart(top_chart, use_container_width=True)

st.divider()

st.subheader(f"🪫 {selected_mbti} 비율이 가장 낮은 나라 Bottom 10")
bottom_chart = make_bar_chart(bottom10, f"Bottom 10 Countries for {selected_mbti}", color="#d62728")
st.altair_chart(bottom_chart, use_container_width=True)

# ----------------------------
# 참고 테이블(원하면 유지/삭제 가능)
# ----------------------------
with st.expander("🔎 Top/Bottom 10 데이터 표로 보기"):
    c1, c2 = st.columns(2)
    with c1:
        st.write("Top 10")
        st.dataframe(top10[["Country", selected_mbti, "percent"]])
    with c2:
        st.write("Bottom 10")
        st.dataframe(bottom10[["Country", selected_mbti, "percent"]])
