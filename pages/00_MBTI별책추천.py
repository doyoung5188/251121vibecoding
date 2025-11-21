import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="MBTI 고전 책 추천",
    page_icon="📚",
    layout="centered"
)

# -----------------------------
# 간단한 CSS 스타일 (기본 기능만 활용)
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1rem;
        text-align: center;
        color: #666666;
        margin-bottom: 1.5rem;
    }
    .card {
        border-radius: 18px;
        padding: 1.3rem 1.5rem;
        background: linear-gradient(135deg, #f9f5ff, #f0f9ff);
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        border: 1px solid #e5e5ff;
    }
    .book-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .book-author {
        font-size: 0.95rem;
        color: #555555;
        margin-bottom: 0.8rem;
    }
    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 0.35rem;
        margin-bottom: 0.3rem;
        background-color: #ffffffaa;
        border: 1px solid #ddddff;
    }
    .footer {
        font-size: 0.8rem;
        color: #999999;
        text-align: center;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 추천 데이터 정의
# -----------------------------
RECOMMENDATIONS = {
    "ISTJ": {
        "nickname": "실무형 관리자 🧱",
        "emoji": "📘",
        "books": [
            {
                "title": "노인과 바다",
                "author": "어니스트 헤밍웨이",
                "reason": "끈기와 책임감을 중시하는 ISTJ에게, 포기하지 않고 끝까지 싸우는 노인의 이야기가 깊은 울림을 줍니다."
            },
            {
                "title": "데미안",
                "author": "헤르만 헤세",
                "reason": "질서 속에서도 자기 삶의 의미를 찾으려는 ISTJ에게 내면을 돌아보게 하는 성장 소설입니다."
            }
        ]
    },
    "ISFJ": {
        "nickname": "따뜻한 수호자 🧸",
        "emoji": "📗",
        "books": [
            {
                "title": "작은 아씨들",
                "author": "루이자 메이 올컷",
                "reason": "가족과 주변 사람들을 세심하게 챙기는 ISFJ의 따뜻한 마음과 잘 어울리는 이야기입니다."
            },
            {
                "title": "어린 왕자",
                "author": "앙투안 드 생텍쥐페리",
                "reason": "사람과 관계를 소중히 여기는 ISFJ에게 순수함과 헌신의 의미를 다시 생각하게 해 줍니다."
            }
        ]
    },
    "INFJ": {
        "nickname": "통찰력 있는 이상주의자 🔮",
        "emoji": "📙",
        "books": [
            {
                "title": "데미안",
                "author": "헤르만 헤세",
                "reason": "자기 정체성과 삶의 의미를 깊이 탐구하는 INFJ에게 딱 맞는 내면 성장 이야기입니다."
            },
            {
                "title": "죄와 벌",
                "author": "표도르 도스토옙스키",
                "reason": "도덕·양심·구원 같은 주제를 좋아하는 INFJ에게 고민할 거리를 잔뜩 던져 줍니다."
            }
        ]
    },
    "INTJ": {
        "nickname": "전략가 사색가 ♟️",
        "emoji": "📕",
        "books": [
            {
                "title": "1984",
                "author": "조지 오웰",
                "reason": "구조와 시스템을 분석하는 INTJ가 읽기에 완벽한, 통제 사회에 대한 날카로운 비판 소설입니다."
            },
            {
                "title": "카라마조프가의 형제들",
                "author": "표도르 도스토옙스키",
                "reason": "철학·종교·도덕이 얽힌 거대한 이야기 속에서 INTJ의 사색 본능이 폭발합니다."
            }
        ]
    },
    "ISTP": {
        "nickname": "논리적인 장인 🛠️",
        "emoji": "📘",
        "books": [
            {
                "title": "셜록 홈즈 시리즈",
                "author": "아서 코난 도일",
                "reason": "관찰과 추리에 강한 ISTP에게 추리소설은 두뇌를 깨우는 최고의 놀이터입니다."
            },
            {
                "title": "로빈슨 크루소",
                "author": "다니엘 디포",
                "reason": "문제 해결을 좋아하는 ISTP에게 생존과 개척의 과정이 흥미롭게 다가옵니다."
            }
        ]
    },
    "ISFP": {
        "nickname": "감성적인 예술가 🎨",
        "emoji": "📗",
        "books": [
            {
                "title": "폭풍의 언덕",
                "author": "에밀리 브론테",
                "reason": "강렬한 감정과 분위기를 사랑하는 ISFP에게 어둡고도 아름다운 사랑 이야기가 매력적입니다."
            },
            {
                "title": "나무",
                "author": "베른하르트 슐링크 등(혹은 자연·감성 관련 단편)",
                "reason": "조용한 자연과 감성을 담은 이야기들이 ISFP의 섬세한 마음과 잘 어울립니다."
            }
        ]
    },
    "INFP": {
        "nickname": "꿈꾸는 이상주의자 🌈",
        "emoji": "📙",
        "books": [
            {
                "title": "어린 왕자",
                "author": "앙투안 드 생텍쥐페리",
                "reason": "순수함과 상징, 숨은 의미를 사랑하는 INFP에게는 거의 필독서 같은 작품입니다."
            },
            {
                "title": "안나 카레니나",
                "author": "레프 톨스토이",
                "reason": "사랑, 선택, 삶의 의미를 깊이 고민하는 INFP에게 감정 이입이 저절로 되는 이야기입니다."
            }
        ]
    },
    "INTP": {
        "nickname": "호기심 많은 분석가 🧠",
        "emoji": "📕",
        "books": [
            {
                "title": "소크라테스의 변명",
                "author": "플라톤",
                "reason": "논리와 질문을 사랑하는 INTP에게 철학의 기본기를 맛보게 해 주는 대화편입니다."
            },
            {
                "title": "동물 농장",
                "author": "조지 오웰",
                "reason": "풍자 구조를 분석하며 사회와 권력에 대해 생각해 보기 좋은 짧고 강렬한 고전입니다."
            }
        ]
    },
    "ESTP": {
        "nickname": "액션파 현실주의자 🏃",
        "emoji": "📘",
        "books": [
            {
                "title": "삼국지 (발췌본·청소년판)",
                "author": "나관중 원작",
                "reason": "전략, 전투, 인물들의 활약이 가득한 이야기라 ESTP의 모험심을 자극합니다."
            },
            {
                "title": "오만과 편견",
                "author": "제인 오스틴",
                "reason": "빠른 전개와 재치 있는 대사를 통해 인간관계를 현실적으로 바라보는 눈을 길러 줍니다."
            }
        ]
    },
    "ESFP": {
        "nickname": "흥 많은 분위기 메이커 🎉",
        "emoji": "📗",
        "books": [
            {
                "title": "작은 아씨들",
                "author": "루이자 메이 올컷",
                "reason": "따뜻한 가족과 친구 관계, 일상 속 설렘이 가득해 ESFP의 밝은 에너지와 잘 어울립니다."
            },
            {
                "title": "톰 소여의 모험",
                "author": "마크 트웨인",
                "reason": "장난기와 모험심이 넘치는 톰의 이야기가 ESFP의 성향과 꼭 닮았습니다."
            }
        ]
    },
    "ENFP": {
        "nickname": "열정 가득 아이디어 뱅크 🚀",
        "emoji": "📙",
        "books": [
            {
                "title": "위대한 개츠비",
                "author": "F. 스콧 피츠제럴드",
                "reason": "꿈과 열정, 그리고 그늘까지 모두 담겨 있어 ENFP가 공감하며 읽기 좋은 고전입니다."
            },
            {
                "title": "호밀밭의 파수꾼",
                "author": "J.D. 샐린저",
                "reason": "사회와 어른 세계에 대한 복잡한 감정을 가진 주인공의 시선이 ENFP의 내면과 어울립니다."
            }
        ]
    },
    "ENTP": {
        "nickname": "아이디어 발명가 💡",
        "emoji": "📕",
        "books": [
            {
                "title": "갈매기의 꿈",
                "author": "리처드 바크",
                "reason": "평범함에 도전하는 갈매기의 이야기가, 기존 틀을 깨고 싶은 ENTP의 마음을 시원하게 해 줍니다."
            },
            {
                "title": "동물 농장",
                "author": "조지 오웰",
                "reason": "권력과 시스템을 비틀어 보는 풍자가 ENTP의 날카로운 관찰력과 잘 맞습니다."
            }
        ]
    },
    "ESTJ": {
        "nickname": "체계적인 리더 📊",
        "emoji": "📘",
        "books": [
            {
                "title": "삼국지 (발췌본·청소년판)",
                "author": "나관중 원작",
                "reason": "조직, 전략, 리더십이 중요한 ESTJ에게 인물들의 선택과 판단이 좋은 공부가 됩니다."
            },
            {
                "title": "국가",
                "author": "플라톤",
                "reason": "이상적인 사회 구조에 대한 논의를 읽으며 시스템과 질서에 대해 깊이 생각해 볼 수 있습니다."
            }
        ]
    },
    "ESFJ": {
        "nickname": "다정한 분위기 조율자 🤝",
        "emoji": "📗",
        "books": [
            {
                "title": "연을 쫓는 아이",
                "author": "할레드 호세이니",
                "reason": "우정과 죄책감, 용서를 다루는 이야기라 사람 사이의 관계를 소중히 여기는 ESFJ에게 크게 와닿습니다."
            },
            {
                "title": "작은 아씨들",
                "author": "루이자 메이 올컷",
                "reason": "서로를 위해 희생하고 도와주는 가족 이야기가 ESFJ의 성향과 딱 맞습니다."
            }
        ]
    },
    "ENFJ": {
        "nickname": "열정적인 조언자 🔥",
        "emoji": "📙",
        "books": [
            {
                "title": "죄와 벌",
                "author": "표도르 도스토옙스키",
                "reason": "타인의 마음과 도덕을 깊이 이해하려는 ENFJ에게 주인공의 내적 갈등이 강렬하게 다가옵니다."
            },
            {
                "title": "안네의 일기",
                "author": "안네 프랑크",
                "reason": "어려운 상황에서도 희망과 인간다움을 잃지 않는 모습을 통해 공감과 용기를 얻을 수 있습니다."
            }
        ]
    },
    "ENTJ": {
        "nickname": "야망 넘치는 지도자 🏔️",
        "emoji": "📕",
        "books": [
            {
