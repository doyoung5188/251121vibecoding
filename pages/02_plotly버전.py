import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# Page config
# ---------------------------------------
st.set_page_config(
    page_title="🌍 MBTI 나라 Top/Bottom 10",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 MBTI 유형별 나라 분포 Top & Bottom 10")
st.caption("CSV에서 MBTI 비율을 불러와 상위/하위 10개 나라를 인터랙티브 그래프로 보여줘요!")

# ---------------------------------------
# Load data
# ---------------------------------------
@st.cache_data
def load_data():
    # 같은 폴더에 있다고 가정
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# ---------------------------------------
# Validate columns
# ---------------------------------------
if "Country" not in df.columns:
    st.error("CSV에 'Country' 컬럼이 없습니다. 컬럼명을 확인해 주세요!")
    st.stop()

mbti_cols = [c for c in df.columns if c != "Country"]

if len(mbti_cols) == 0:
    st.error("Country를 제외한 MBTI 컬럼을 찾지 못했어요. CSV 구조를 확인해 주세요!")
    st.stop()

# ---------------------------------------
# MBTI selector
# ---------------------------------------
st.subheader("🧠 MBTI를 선택해 주세요")
selected_mbti = st.selectbox(
    "어떤 MBTI를 보고 싶나요?",
    mbti_cols,
    index=0
)

# ---------------------------------------
# Prepare top/bottom 10
# ---------------------------------------
plot_df = df[["Country", selected_mbti]].dropna()
plot_df = plot_df.sort_values(by=selected_mbti, ascending=False)

top10 = plot_df.head(10).sort_values(by=selected_mbti, ascending=True)   # barh 보기 깔끔하게
bottom10 = plot_df.tail(10).sort_values(by=selected_mbti, ascending=True)

# ---------------------------------------
# Top 10 chart
# ---------------------------------------
st.markdown("---")
st.subheader(f"🏆 {selected_mbti} 비율이 가장 높은 나라 TOP 10")

fig_top = px.bar(
    top10,
    x=selected_mbti,
    y="Country",
    orientation="h",
    text=selected_mbti,
    title=f"Top 10 Countries for {selected_mbti}",
)

fig_top.update_traces(texttemplate="%{text:.2%}", textposition="outside")
fig_top.update_layout(
    xaxis_title="비율",
    yaxis_title="나라",
    height=500,
    margin=dict(l=50, r=50, t=60, b=40)
)

st.plotly_chart(fig_top, use_container_width=True)

# ---------------------------------------
# Bottom 10 chart
# ---------------------------------------
st.markdown("---")
st.subheader(f"🥲 {selected_mbti} 비율이 가장 낮은 나라 BOTTOM 10")

fig_bottom = px.bar(
    bottom10,
    x=selected_mbti,
    y="Country",
    orientation="h",
    text=selected_mbti,
    title=f"Bottom 10 Countries for {selected_mbti}",
)

fig_bottom.update_traces(texttemplate="%{text:.2%}", textposition="outside")
fig_bottom.update_layout(
    xaxis_title="비율",
    yaxis_title="나라",
    height=500,
    margin=dict(l=50, r=50, t=60, b=40)
)

st.plotly_chart(fig_bottom, use_container_width=True)

# ---------------------------------------
# Optional: show raw data
# ---------------------------------------
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(df, use_container_width=True)
