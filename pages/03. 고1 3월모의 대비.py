import streamlit as st
import random
import time
import sqlite3
from datetime import datetime

# =========================
# 0. 페이지/테마 설정 (귀여운 테마)
# =========================
st.set_page_config(
    page_title="과학 스피드퀴즈 🧪✨",
    page_icon="🧸",
    layout="centered"
)

CUTE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Nanum Gothic', sans-serif;
}
.main {
    background: linear-gradient(180deg, #fff6fb 0%, #f3fbff 100%);
}
.cute-card {
    background: white;
    padding: 1.2rem 1.2rem;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(255, 170, 210, 0.25);
    border: 2px dashed #ffb3d9;
}
.badge {
    display:inline-block;
    padding: 0.25rem_topics 0.6rem;
    border-radius: 999px;
    font-size: 0.9rem;
    background: #ffe6f2;
    margin-right: 0.3rem;
    border: 1px solid #ffb3d9;
}
.small {
    color:#666;
    font-size:0.9rem;
}
.correct {
    color:#10a37f; font-weight:700;
}
.wrong {
    color:#e74c3c; font-weight:700;
}
</style>
"""
st.markdown(CUTE_CSS, unsafe_allow_html=True)

# =========================
# 1. DB(랭킹) 준비 - SQLite
# =========================
def init_db():
    conn = sqlite3.connect("ranking.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            score INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            played_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_score(nickname, score, difficulty):
    conn = sqlite3.connect("ranking.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scores (nickname, score, difficulty, played_at) VALUES (?, ?, ?, ?)",
        (nickname, score, difficulty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_leaderboard(limit=50):
    conn = sqlite3.connect("ranking.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT nickname, score, difficulty, played_at
        FROM scores
        ORDER BY score DESC, played_at ASC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

init_db()

# =========================
# 2. 문제은행 (고1 3월 과학 -> 중3 개념 확인용)
#    원문항 기반으로 개념/정답/해설 요약
#    출처: 2025 3월 고1 과학 문제/해설 :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}
# =========================
QUESTIONS = [
    {
        "id": 1,
        "difficulty": "하",
        "concept": "해륙풍(해풍/육풍)",
        "q": "낮에 바다에서 육지로 부는 바람은 무엇일까?",
        "choices": ["육풍", "해풍", "계절풍", "편서풍"],
        "answer": 1,
        "exp": "낮에는 육지가 더 빨리 가열되어 육지 기압이 낮아져 바다(고기압)→육지(저기압)로 바람이 분다. 이것이 해풍이다."
    },
    {
        "id": 2,
        "difficulty": "하",
        "concept": "빛의 삼원색/달의 위상",
        "q": "빨간색·초록색·파란색 빛은 무엇의 삼원색일까?",
        "choices": ["안료의 삼원색", "빛의 삼원색", "무지개의 삼원색", "자외선의 삼원색"],
        "answer": 1,
        "exp": "빛의 삼원색은 R-G-B이고, 섞이면 다양한 색의 빛이 된다."
    },
    {
        "id": 3,
        "difficulty": "하",
        "concept": "광합성 장소/반응물·생성물",
        "q": "식물이 빛에너지로 CO₂와 물로부터 포도당과 O₂를 만드는 과정은?",
        "choices": ["호흡", "발효", "광합성", "증산"],
        "answer": 2,
        "exp": "광합성은 엽록체에서 일어나며 CO₂+물 → 포도당+O₂."
    },
    {
        "id": 4,
        "difficulty": "하",
        "concept": "흡열/발열 반응",
        "q": "손난로가 따뜻해지는 이유는 반응이 열에너지를 (   )하기 때문이야.",
        "choices": ["흡수", "방출", "저장", "중화"],
        "answer": 1,
        "exp": "철이 산소와 반응할 때 발열하여 주변으로 열을 방출한다."
    },
    {
        "id": 5,
        "difficulty": "하",
        "concept": "생물의 분류(동물/식물/원핵생물)",
        "q": "세균은 어떤 생물계에 속할까?",
        "choices": ["동물계", "식물계", "원핵생물계", "원생생물계"],
        "answer": 2,
        "exp": "세균은 핵막이 없는 원핵생물이다."
    },
    {
        "id": 6,
        "difficulty": "중",
        "concept": "부력",
        "q": "물체에 작용하는 부력의 크기는 주로 무엇에 의해 결정될까?",
        "choices": ["물체의 색", "물체가 잠긴 부피", "물체의 온도", "물의 pH"],
        "answer": 1,
        "exp": "부력은 밀려난 물의 무게와 같고, 물에 잠긴 부피가 클수록 부력이 크다."
    },
    {
        "id": 7,
        "difficulty": "중",
        "concept": "이온 형성",
        "q": "Al 원자가 전자 3개를 잃으면 어떤 이온이 될까?",
        "choices": ["Al⁻", "Al³⁻", "Al³⁺", "Al⁺"],
        "answer": 2,
        "exp": "전자(−) 3개를 잃으면 +3 전하를 띠어 Al³⁺."
    },
    {
        "id": 8,
        "difficulty": "중",
        "concept": "기공/광합성",
        "q": "식물 잎의 기공은 주로 언제 더 많이 열릴까?",
        "choices": ["밤", "낮", "항상 동일", "비 오는 날만"],
        "answer": 1,
        "exp": "낮에 광합성이 활발해서 CO₂ 흡수를 위해 기공이 더 열린다."
    },
    {
        "id": 9,
        "difficulty": "중",
        "concept": "옴의 법칙(전압-전류 비례)",
        "q": "저항이 일정할 때 전압이 2배가 되면 전류는?",
        "choices": ["2배", "1/2배", "4배", "변하지 않음"],
        "answer": 0,
        "exp": "I = V/R 이므로 V가 2배면 I도 2배."
    },
    {
        "id": 10,
        "difficulty": "중",
        "concept": "암석 분류",
        "q": "색이 어둡고 입자가 작은 화성암은?",
        "choices": ["현무암", "화강암", "규암", "석회암"],
        "answer": 0,
        "exp": "현무암은 어둡고 세립질 화성암."
    },
    {
        "id": 11,
        "difficulty": "중",
        "concept": "눈의 구조",
        "q": "눈으로 들어오는 빛의 양을 조절하는 구조는?",
        "choices": ["수정체", "홍채", "망막", "시각신경"],
        "answer": 1,
        "exp": "홍채가 수축/이완하여 동공 크기를 조절."
    },
    {
        "id": 12,
        "difficulty": "중",
        "concept": "염분(psu)",
        "q": "염분 35 psu인 해수 1 kg에 녹아 있는 염류의 양은?",
        "choices": ["35 g", "350 g", "3.5 g", "0.35 g"],
        "answer": 0,
        "exp": "psu는 1 kg당 염류 g 수 → 35 psu = 35 g."
    },
    {
        "id": 13,
        "difficulty": "중",
        "concept": "기체 압력-부피",
        "q": "같은 온도에서 기체의 부피가 줄어들면 압력은?",
        "choices": ["커진다", "작아진다", "변하지 않는다", "0이 된다"],
        "answer": 0,
        "exp": "보일 법칙: P ∝ 1/V."
    },
    {
        "id": 14,
        "difficulty": "상",
        "concept": "열평형/열팽창",
        "q": "온도가 낮던 액체가 물에서 열을 받아 온도가 올라가면 일반적으로 부피는?",
        "choices": ["감소", "증가", "그대로", "불규칙"],
        "answer": 1,
        "exp": "대부분의 액체는 가열되면 열팽창하여 부피가 증가."
    },
    {
        "id": 15,
        "difficulty": "상",
        "concept": "감수분열",
        "q": "정자/난자 형성 과정에서 일어나는 분열은?",
        "choices": ["체세포 분열", "감수 분열", "무분열", "유사 분열"],
        "answer": 1,
        "exp": "생식세포는 감수분열로 염색체 수가 절반이 된다."
    },
    {
        "id": 16,
        "difficulty": "상",
        "concept": "우리 은하 구조",
        "q": "우리 은하의 종류는 무엇일까?",
        "choices": ["타원 은하", "막대 나선 은하", "불규칙 은하", "렌즈 은하"],
        "answer": 1,
        "exp": "우리 은하는 막대 모양 중심부 + 나선팔 구조."
    },
    {
        "id": 17,
        "difficulty": "상",
        "concept": "역학적 에너지 보존",
        "q": "자유낙하에서 위치에너지가 줄어든 만큼 무엇이 증가할까?",
        "choices": ["열에너지", "운동에너지", "빛에너지", "화학에너지"],
        "answer": 1,
        "exp": "공기저항 무시 시 위치E → 운동E로 전환."
    },
    {
        "id": 18,
        "difficulty": "상",
        "concept": "인체 순환/호흡계",
        "q": "폐는 어떤 계통에 속할까?",
        "choices": ["순환계", "소화계", "호흡계", "배설계"],
        "answer": 2,
        "exp": "폐는 산소/이산화탄소 교환을 담당하는 호흡계."
    },
    {
        "id": 19,
        "difficulty": "상",
        "concept": "화학 반응식 계수/질량비",
        "q": "수소와 산소로 물 만들 때 반응 계수는 H₂:O₂:H₂O = ?",
        "choices": ["1:1:1", "2:1:2", "1:2:1", "3:1:3"],
        "answer": 1,
        "exp": "H₂ + O₂ → H₂O 에서 원자수 맞추면 2H₂ + O₂ → 2H₂O."
    },
    {
        "id": 20,
        "difficulty": "상",
        "concept": "천체망원경/상",
        "q": "볼록렌즈로 멀리 있는 천체를 보면 상은 어떻게 보일까?",
        "choices": ["정립", "거꾸로(상하좌우 반전)", "2배 확대만", "색만 변함"],
        "answer": 1,
        "exp": "천체망원경(굴절)에서 상은 상하좌우가 뒤집혀 보인다."
    },
]

# 난이도별 필터
def filter_questions(level):
    return [q for q in QUESTIONS if q["difficulty"] == level]

# =========================
# 3. 세션 상태 초기화
# =========================
if "started" not in st.session_state:
    st.session_state.started = False
if "nickname" not in st.session_state:
    st.session_state.nickname = ""
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "하"
if "quiz_list" not in st.session_state:
    st.session_state.quiz_list = []
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "selected" not in st.session_state:
    st.session_state.selected = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# =========================
# 4. 상단 UI
# =========================
st.markdown("## 🧪 과학 스피드 퀴즈 ✨")
st.markdown("<div class='small'>중3 개념 점검용! 한 문제씩 빠르게 풀고 랭킹에 도전해보자 😺</div>", unsafe_allow_html=True)
st.write("")

# =========================
# 5. 시작 화면
# =========================
if not st.session_state.started:
    st.markdown("<div class='cute-card'>", unsafe_allow_html=True)
    st.markdown("### 🐣 닉네임 입력")
    nickname = st.text_input("게임에서 사용할 닉네임을 적어줘!", max_chars=12, placeholder="예: 곰도리쌤")
    st.markdown("### 🎚️ 난이도 선택")
    difficulty = st.radio("난이도를 골라줘!", ["하", "중", "상"], horizontal=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚀 퀴즈 시작!", use_container_width=True):
            if nickname.strip() == "":
                st.warning("닉네임을 입력해야 시작할 수 있어요! 🙏")
            else:
                st.session_state.nickname = nickname.strip()
                st.session_state.difficulty = difficulty
                st.session_state.quiz_list = filter_questions(difficulty)
                random.shuffle(st.session_state.quiz_list)
                st.session_state.current_idx = 0
                st.session_state.score = 0
                st.session_state.show_result = False
                st.session_state.selected = None
                st.session_state.start_time = time.time()
                st.session_state.started = True
                st.rerun()
    with col2:
        if st.button("🏆 랭킹 보기", use_container_width=True):
            st.session_state.started = "ranking_only"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 6. 랭킹만 보기 모드
# =========================
elif st.session_state.started == "ranking_only":
    st.markdown("### 🏆 현재 랭킹")
    board = get_leaderboard()
    if not board:
        st.info("아직 랭킹이 비어있어! 첫 유저가 되어줘 😺")
    else:
        for i, (name, sc, diff, when) in enumerate(board, start=1):
            st.markdown(
                f"**{i}. {name}**  |  점수: **{sc}점**  |  난이도: {diff}  |  {when}"
            )
    if st.button("⬅️ 돌아가기"):
        st.session_state.started = False
        st.rerun()

# =========================
# 7. 퀴즈 진행 화면
# =========================
else:
    quiz_list = st.session_state.quiz_list
    idx = st.session_state.current_idx
    total = len(quiz_list)

    # 종료 처리
    if idx >= total:
        elapsed = int(time.time() - st.session_state.start_time)
        st.balloons()
        st.markdown("<div class='cute-card'>", unsafe_allow_html=True)
        st.markdown("## 🎉 퀴즈 끝!!")
        st.markdown(f"**{st.session_state.nickname}**의 최종 점수는 **{st.session_state.score}점** 🐻‍❄️✨")
        st.markdown(f"⏱️ 걸린 시간: **{elapsed}초**")

        insert_score(
            st.session_state.nickname,
            st.session_state.score,
            st.session_state.difficulty
        )

        st.markdown("### 🏆 랭킹")
        board = get_leaderboard()
        for i, (name, sc, diff, when) in enumerate(board, start=1):
            medal = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else "🐾"))
            st.markdown(f"{medal} **{i}. {name}**  |  **{sc}점**  |  {diff}")

        colA, colB = st.columns(2)
        with colA:
            if st.button("🔁 다시하기", use_container_width=True):
                st.session_state.started = False
                st.rerun()
        with colB:
            if st.button("✅ 랭킹만 보기", use_container_width=True):
                st.session_state.started = "ranking_only"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        q = quiz_list[idx]

        # 상단 상태바
        elapsed = int(time.time() - st.session_state.start_time)
        st.markdown(
            f"<span class='badge'>난이도 {st.session_state.difficulty}</span>"
            f"<span class='badge'>문제 {idx+1}/{total}</span>"
            f"<span class='badge'>점수 {st.session_state.score}점</span>"
            f"<span class='badge'>⏱️ {elapsed}초</span>",
            unsafe_allow_html=True
        )
        st.write("")

        st.markdown("<div class='cute-card'>", unsafe_allow_html=True)
        st.markdown(f"### Q{idx+1}. {q['q']}")
        st.markdown(f"🧠 개념: **{q['concept']}**")
        st.write("")

        # 선택지
        st.session_state.selected = st.radio(
            "정답을 골라줘!",
            options=list(range(len(q["choices"]))),
            format_func=lambda i: q["choices"][i],
            key=f"radio_{q['id']}_{idx}"
        )

        col1, col2 = st.columns(2)

        # 제출
        with col1:
            if st.button("✅ 제출!", use_container_width=True) and not st.session_state.show_result:
                st.session_state.show_result = True
                if st.session_state.selected == q["answer"]:
                    st.session_state.score += 1

        # 건너뛰기(스피드용)
        with col2:
            if st.button("⏭️ 패스", use_container_width=True) and not st.session_state.show_result:
                st.session_state.show_result = True

        # 결과/해설 표시
        if st.session_state.show_result:
            correct_choice = q["choices"][q["answer"]]
            if st.session_state.selected == q["answer"]:
                st.markdown(f"✨ <span class='correct'>정답!</span> 정답은 **{correct_choice}** 😻", unsafe_allow_html=True)
            else:
                st.markdown(f"💦 <span class='wrong'>오답!</span> 정답은 **{correct_choice}** 😿", unsafe_allow_html=True)

            st.markdown("#### 📝 해설")
            st.info(q["exp"])

            if st.button("➡️ 다음 문제"):
                st.session_state.current_idx += 1
                st.session_state.show_result = False
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
