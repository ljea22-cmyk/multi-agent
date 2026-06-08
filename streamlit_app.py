import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from my_agent import extract_conditions, classify_games, write_recommendations, write_user_guide, review_recommendations

st.set_page_config(
    page_title="🎮 게임 추천 에이전트",
    page_icon="🎮",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #f5f5f5;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Ctext y='30' font-size='20' opacity='0.06'%3E🎮%3C/text%3E%3Ctext x='50' y='70' font-size='20' opacity='0.06'%3E⭐%3C/text%3E%3Ctext x='10' y='90' font-size='16' opacity='0.06'%3E🕹️%3C/text%3E%3Ctext x='60' y='20' font-size='16' opacity='0.06'%3E♪%3C/text%3E%3C/svg%3E");
        background-repeat: repeat;
        background-size: 100px 100px;
    }
    .main-header {
        background-color: #E4000F;
        padding: 14px 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    .main-header h1 {
        color: white;
        font-size: 1.8em;
        font-weight: 800;
        margin: 0;
    }
    .main-header p {
        color: white;
        margin: 4px 0 0 0;
        font-size: 0.95em;
    }
    .game-card-perfect {
        background-color: #ffffff;
        border: 2px solid #E4000F;
        border-radius: 14px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 3px 3px 0px #E4000F;
    }
    .game-card-partial {
        background-color: #ffffff;
        border: 2px solid #aaaaaa;
        border-radius: 14px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 3px 3px 0px #aaaaaa;
    }
    .game-title {
        color: #E4000F;
        font-size: 1.0em;
        font-weight: 700;
    }
    .section-header {
        background-color: #E4000F;
        color: white;
        padding: 6px 14px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.95em;
        margin: 12px 0;
        display: inline-block;
    }
    .metric-box {
        background-color: #E4000F;
        color: white;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
    }
    .metric-box h3 {
        font-size: 0.85em;
        margin: 0 0 4px 0;
    }
    .metric-box p {
        font-size: 1.1em;
        font-weight: 700;
        margin: 0;
    }
    .history-card {
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        font-size: 0.85em;
    }
    div[data-testid="stSidebar"] {
        background-color: #E4000F;
    }
    div[data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 히스토리 파일
HISTORY_FILE = Path("search_history.json")

def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_history(conditions, result_count):
    history = load_history()
    history.insert(0, {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "genre": conditions["genre"],
        "platform": conditions["platform"],
        "difficulty": conditions["difficulty"],
        "player": conditions["player"],
        "result_count": result_count,
    })
    history = history[:20]  # 최근 20개만 저장
    save_history(history)

# 헤더
st.markdown("""
<div class="main-header">
    <h1>🎮 게임 추천 에이전트</h1>
    <p>조건을 선택하면 딱 맞는 게임을 추천해드립니다!</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🕹️ 게임 조건 선택")
    st.markdown("---")
    genre = st.selectbox("🎯 장르", ["RPG", "액션", "시뮬레이션", "어드벤처", "FPS", "샌드박스", "전략", "레이싱", "격투"])
    platform = st.selectbox("🖥️ 플랫폼", ["닌텐도", "PC", "콘솔", "모바일"])
    difficulty = st.selectbox("⚡ 난이도", ["쉬움", "보통", "어려움"])
    player = st.selectbox("👥 플레이어", ["싱글", "멀티"])
    st.markdown("---")
    run = st.button("🔍 추천받기", use_container_width=True)
    st.markdown("---")

    # 히스토리
    st.markdown("## 📋 최근 검색")
    history = load_history()
    if history:
        for h in history[:5]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.2); border-radius:8px; padding:6px; margin:4px 0; font-size:0.8em;">
                🕐 {h['time']}<br>
                {h['genre']} / {h['platform']} / {h['difficulty']}<br>
                결과: {h['result_count']}개
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size:0.85em;'>아직 검색 기록이 없습니다</p>", unsafe_allow_html=True)

if run:
    input_text = f"""
장르: {genre}
플랫폼: {platform}
난이도: {difficulty}
플레이어: {player}
"""
    conditions = extract_conditions(input_text)
    matched = classify_games(conditions)

    # 히스토리 저장
    add_history(conditions, len(matched))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <h3>🎯 장르 / 플랫폼</h3>
            <p>{genre} / {platform}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <h3>⚡ 난이도</h3>
            <p>{difficulty}</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <h3>🎮 추천 게임 수</h3>
            <p>{len(matched)}개</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not matched:
        st.warning("⚠️ 조건에 맞는 게임을 찾지 못했습니다. 조건을 바꿔서 다시 시도해보세요.")
    else:
        perfect = [g for g in matched if not g["warnings"]]
        partial = [g for g in matched if g["warnings"]]

        if perfect:
            st.markdown('<div class="section-header">✅ 조건 완전 일치 추천</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(min(len(perfect), 3))
            for i, game in enumerate(perfect):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="game-card-perfect">
                        <div class="game-title">🎮 {game['title']}</div>
                        <p style="color:#444; margin:6px 0; font-size:0.9em;">{game['description']}</p>
                        <p style="color:#E4000F; font-size:0.8em;">✅ {', '.join(game['reasons'])}</p>
                    </div>
                    """, unsafe_allow_html=True)

        if partial:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">⚠️ 조건 부분 일치 추천 (참고용)</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(min(len(partial), 3))
            for i, game in enumerate(partial):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="game-card-partial">
                        <div style="color:#888; font-size:1.0em; font-weight:700;">🎮 {game['title']}</div>
                        <p style="color:#444; margin:6px 0; font-size:0.9em;">{game['description']}</p>
                        <p style="color:#555; font-size:0.8em;">✅ {', '.join(game['reasons'])}</p>
                        <p style="color:#E4000F; font-size:0.8em;">⚠️ {', '.join(game['warnings'])}</p>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("📋 검토 보고서 보기"):
            with st.spinner("검토 중..."):
                review = review_recommendations(matched)
            st.markdown(review)
            st.download_button(
                label="📥 검토 보고서 다운로드",
                data=review,
                file_name="review_report.txt",
                mime="text/plain"
            )

        with st.expander("📄 전체 추천 결과 보기"):
            result = write_recommendations(conditions, matched)
            st.markdown(result)
            st.download_button(
                label="📥 추천 결과 다운로드",
                data=result,
                file_name="output.txt",
                mime="text/plain"
            )

        user_guide = write_user_guide(conditions, matched)
        st.download_button(
            label="📥 안내문 다운로드",
            data=user_guide,
            file_name="output_user_guide.txt",
            mime="text/plain"
        )

        # 통계
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📊 검색 통계 보기"):
            history = load_history()
            if len(history) > 1:
                st.markdown("### 최근 검색 통계")
                genre_counts = {}
                platform_counts = {}
                for h in history:
                    genre_counts[h["genre"]] = genre_counts.get(h["genre"], 0) + 1
                    platform_counts[h["platform"]] = platform_counts.get(h["platform"], 0) + 1

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**장르별 검색 횟수**")
                    for g, c in sorted(genre_counts.items(), key=lambda x: -x[1]):
                        st.markdown(f"- {g}: {c}회")
                with col2:
                    st.markdown("**플랫폼별 검색 횟수**")
                    for p, c in sorted(platform_counts.items(), key=lambda x: -x[1]):
                        st.markdown(f"- {p}: {c}회")
            else:
                st.info("검색을 더 해보면 통계가 나타납니다!")

else:
    st.markdown("""
    <div style="text-align:center; padding:50px; color:#aaa;">
        <h3>👈 왼쪽 사이드바에서 조건을 선택하고</h3>
        <h3>🔍 추천받기 버튼을 눌러주세요!</h3>
    </div>
    """, unsafe_allow_html=True)