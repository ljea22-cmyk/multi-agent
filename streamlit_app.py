import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from my_agent import extract_conditions, classify_games, write_recommendations, write_user_guide, review_recommendations

st.set_page_config(
    page_title="🎮 GameMatch AI",
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
    .main-header { background-color: #E4000F; padding: 14px 20px; border-radius: 16px; text-align: center; margin-bottom: 20px; }
    .main-header h1 { color: white; font-size: 1.8em; font-weight: 800; margin: 0; }
    .main-header p { color: white; margin: 4px 0 0 0; font-size: 0.95em; }
    .game-card-perfect { background-color: #ffffff; border: 2px solid #E4000F; border-radius: 14px; padding: 12px; margin: 8px 0; box-shadow: 3px 3px 0px #E4000F; }
    .game-card-partial { background-color: #ffffff; border: 2px solid #aaaaaa; border-radius: 14px; padding: 12px; margin: 8px 0; box-shadow: 3px 3px 0px #aaaaaa; }
    .game-title { color: #E4000F; font-size: 1.0em; font-weight: 700; }
    .section-header { background-color: #E4000F; color: white; padding: 6px 14px; border-radius: 10px; font-weight: 700; font-size: 0.95em; margin: 12px 0; display: inline-block; }
    .metric-box { background-color: #E4000F; color: white; border-radius: 12px; padding: 10px; text-align: center; }
    .metric-box h3 { font-size: 0.85em; margin: 0 0 4px 0; }
    .metric-box p { font-size: 1.1em; font-weight: 700; margin: 0; }
    .wishlist-card { background-color: #fff8f8; border: 2px solid #E4000F; border-radius: 12px; padding: 10px; margin: 5px 0; }
    .sponsor-banner { background: linear-gradient(135deg, #1a1a2e, #16213e); border: 2px solid #E4000F; border-radius: 14px; padding: 15px; text-align: center; margin: 10px 0; color: white; }
</style>
""", unsafe_allow_html=True)

HISTORY_FILE = Path("search_history.json")
WISHLIST_FILE = Path("wishlist.json")
REVIEW_FILE = Path("reviews.json")

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
    history = history[:20]
    save_history(history)

def load_wishlist():
    if WISHLIST_FILE.exists():
        with open(WISHLIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_wishlist(wishlist):
    with open(WISHLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(wishlist, f, ensure_ascii=False, indent=2)

def add_wishlist(game):
    wishlist = load_wishlist()
    titles = [w["title"] for w in wishlist]
    if game["title"] not in titles:
        wishlist.insert(0, {
            "title": game["title"],
            "description": game["description"],
            "added": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        save_wishlist(wishlist)
        return True
    return False

def remove_wishlist(title):
    wishlist = load_wishlist()
    wishlist = [w for w in wishlist if w["title"] != title]
    save_wishlist(wishlist)

def load_reviews():
    if REVIEW_FILE.exists():
        with open(REVIEW_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_review(title, rating, comment):
    reviews = load_reviews()
    if title not in reviews:
        reviews[title] = []
    reviews[title].insert(0, {
        "rating": rating,
        "comment": comment,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

def get_avg_rating(title):
    reviews = load_reviews()
    if title not in reviews or not reviews[title]:
        return None
    ratings = [r["rating"] for r in reviews[title]]
    return sum(ratings) / len(ratings)

GAME_PRICES = {
    "스타듀 밸리": {"닌텐도 eShop": 15000, "Steam": 14000, "쿠팡": 18000},
    "젤다의 전설: 야생의 숨결": {"닌텐도 eShop": 60000, "쿠팡": 55000},
    "젤다의 전설: 티어스 오브 더 킹덤": {"닌텐도 eShop": 65000, "쿠팡": 62000},
    "포켓몬스터 스칼렛/바이올렛": {"닌텐도 eShop": 65000, "쿠팡": 58000},
    "포켓몬스터 소드/실드": {"닌텐도 eShop": 60000, "쿠팡": 45000},
    "동물의 숲: 뉴 호라이즌": {"닌텐도 eShop": 60000, "쿠팡": 50000},
    "마리오 오디세이": {"닌텐도 eShop": 60000, "쿠팡": 52000},
    "마리오 카트 8 디럭스": {"닌텐도 eShop": 60000, "쿠팡": 55000},
    "슈퍼 마리오 브라더스 원더": {"닌텐도 eShop": 65000, "쿠팡": 60000},
    "스플래툰 3": {"닌텐도 eShop": 65000, "쿠팡": 58000},
    "대난투 스매시브라더스 얼티밋": {"닌텐도 eShop": 65000, "쿠팡": 55000},
    "피크민 4": {"닌텐도 eShop": 65000, "쿠팡": 60000},
    "커비 스타 얼라이즈": {"닌텐도 eShop": 60000, "쿠팡": 45000},
    "메트로이드 드레드": {"닌텐도 eShop": 65000, "쿠팡": 58000},
    "파이어 엠블렘 엔게이지": {"닌텐도 eShop": 65000, "쿠팡": 55000},
    "몬스터 헌터 라이즈": {"닌텐도 eShop": 40000, "Steam": 30000, "쿠팡": 35000},
    "다크 소울 3": {"Steam": 60000, "쿠팡": 45000},
    "위처 3": {"Steam": 40000, "닌텐도 eShop": 65000, "쿠팡": 35000},
    "마인크래프트": {"닌텐도 eShop": 35000, "Steam": 30000, "모바일": 10000},
    "발더스 게이트 3": {"Steam": 70000, "쿠팡": 65000},
    "엘든 링": {"Steam": 70000, "쿠팡": 60000},
    "심즈 4": {"Steam": 0},
    "스타크래프트 2": {"Battle.net": 0},
    "오버워치 2": {"Battle.net": 0},
}

GAME_LINKS = {
    "스타듀 밸리": {"Steam": "https://store.steampowered.com/app/413150/Stardew_Valley/", "닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "젤다의 전설: 야생의 숨결": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "젤다의 전설: 티어스 오브 더 킹덤": {"닌텐도 eShop": "https://zelda.nintendo.com/tears-of-the-kingdom/"},
    "포켓몬스터 스칼렛/바이올렛": {"닌텐도 eShop": "https://www.pokemon.com/us/pokemon-video-games/pokemon-scarlet-and-pokemon-violet/"},
    "포켓몬스터 소드/실드": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "동물의 숲: 뉴 호라이즌": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "마리오 오디세이": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "마리오 카트 8 디럭스": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "슈퍼 마리오 브라더스 원더": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "스플래툰 3": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "대난투 스매시브라더스 얼티밋": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "피크민 4": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "커비 스타 얼라이즈": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "메트로이드 드레드": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "파이어 엠블렘 엔게이지": {"닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "몬스터 헌터 라이즈": {"Steam": "https://store.steampowered.com/app/1446780/Monster_Hunter_Rise/", "닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "다크 소울 3": {"Steam": "https://store.steampowered.com/app/374320/DARK_SOULS_III/"},
    "위처 3": {"Steam": "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/", "닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "마인크래프트": {"Steam": "https://store.steampowered.com/app/1672970/Minecraft/", "닌텐도 eShop": "https://www.nintendo.co.kr/"},
    "발더스 게이트 3": {"Steam": "https://store.steampowered.com/app/1086940/Baldurs_Gate_3/"},
    "엘든 링": {"Steam": "https://store.steampowered.com/app/1245620/ELDEN_RING/"},
    "심즈 4": {"Steam": "https://store.steampowered.com/app/1222670/The_Sims_4/"},
    "스타크래프트 2": {"Battle.net": "https://starcraft2.blizzard.com/ko-kr/"},
    "오버워치 2": {"Battle.net": "https://overwatch.blizzard.com/ko-kr/"},
}

SPONSOR_GAMES = [
    {"title": "🌟 젤다의 전설: 티어스 오브 더 킹덤", "desc": "닌텐도 eShop 단독 구매 시 특별 혜택!", "badge": "SPONSORED", "url": "https://zelda.nintendo.com/tears-of-the-kingdom/", "color": "#1a1a2e"},
    {"title": "🌟 엘든 링", "desc": "Steam 최고 평점! 지금 바로 구매하세요", "badge": "SPONSORED", "url": "https://store.steampowered.com/app/1245620/ELDEN_RING/", "color": "#1a0a00"},
    {"title": "🌟 발더스 게이트 3", "desc": "2023 올해의 게임! Steam에서 지금 구매", "badge": "SPONSORED", "url": "https://store.steampowered.com/app/1086940/Baldurs_Gate_3/", "color": "#0a1a00"},
    {"title": "🌟 포켓몬스터 스칼렛/바이올렛", "desc": "닌텐도 공식 파트너 추천! 10% 할인 쿠폰 증정", "badge": "SPONSORED", "url": "https://www.pokemon.com/us/pokemon-video-games/pokemon-scarlet-and-pokemon-violet/", "color": "#1a0010"},
]

if "matched" not in st.session_state:
    st.session_state.matched = []
if "conditions" not in st.session_state:
    st.session_state.conditions = {}
if "ran" not in st.session_state:
    st.session_state.ran = False
if "wish_msg" not in st.session_state:
    st.session_state.wish_msg = {}
if "banner_idx" not in st.session_state:
    st.session_state.banner_idx = 0

st.markdown("""
<div class="main-header">
    <h1>🎮 GameMatch AI</h1>
    <p>조건을 선택하면 딱 맞는 게임을 추천해드립니다!</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🔍 게임 추천", "❤️ 위시리스트", "📊 통계 대시보드", "💼 비즈니스"])

with tab1:
    col_side, col_main = st.columns([1, 3])

    with col_side:
        st.markdown("### 🕹️ 조건 선택")
        genre = st.selectbox("🎯 장르", ["RPG", "액션", "시뮬레이션", "어드벤처", "FPS", "샌드박스", "전략", "레이싱", "격투"])
        platform = st.selectbox("🖥️ 플랫폼", ["닌텐도", "PC", "콘솔", "모바일"])
        difficulty = st.selectbox("⚡ 난이도", ["쉬움", "보통", "어려움"])
        player = st.selectbox("👥 플레이어", ["싱글", "멀티"])
        run = st.button("🔍 추천받기", use_container_width=True)
        st.markdown("---")
        st.markdown("### 📋 최근 검색")
        history = load_history()
        if history:
            for h in history[:5]:
                st.markdown(f"""
                <div style="background:#f9f9f9; border-radius:8px; padding:6px; margin:4px 0; font-size:0.8em; border:1px solid #ddd;">
                    🕐 {h['time']}<br>
                    {h['genre']} / {h['platform']}<br>
                    결과: {h['result_count']}개
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("아직 검색 기록이 없습니다")

    with col_main:
        banner = SPONSOR_GAMES[st.session_state.banner_idx]
        bcol1, bcol2, bcol3 = st.columns([1, 8, 1])
        with bcol1:
            if st.button("◀", key="prev_banner"):
                st.session_state.banner_idx = (st.session_state.banner_idx - 1) % len(SPONSOR_GAMES)
                st.rerun()
        with bcol2:
            st.markdown(f"""
            <div class="sponsor-banner" style="background: linear-gradient(135deg, {banner['color']}, #16213e);">
                <b>{banner['title']}</b><br>
                <span style="font-size:0.9em;">{banner['desc']}</span><br>
                <a href="{banner['url']}" target="_blank" style="background:#E4000F; padding:4px 12px; border-radius:4px; font-size:0.8em; color:white; text-decoration:none; display:inline-block; margin-top:8px;">
                    {banner['badge']} - 구매하러 가기 →
                </a>
                <br><span style="font-size:0.75em; color:#888; margin-top:4px; display:block;">{st.session_state.banner_idx + 1} / {len(SPONSOR_GAMES)}</span>
            </div>
            """, unsafe_allow_html=True)
        with bcol3:
            if st.button("▶", key="next_banner"):
                st.session_state.banner_idx = (st.session_state.banner_idx + 1) % len(SPONSOR_GAMES)
                st.rerun()

        if run:
            input_text = f"\n장르: {genre}\n플랫폼: {platform}\n난이도: {difficulty}\n플레이어: {player}\n"
            conditions = extract_conditions(input_text)
            matched = classify_games(conditions)
            add_history(conditions, len(matched))
            st.session_state.matched = matched
            st.session_state.conditions = conditions
            st.session_state.ran = True
            st.session_state.wish_msg = {}

        if st.session_state.ran:
            matched = st.session_state.matched
            conditions = st.session_state.conditions

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="metric-box"><h3>🎯 장르/플랫폼</h3><p>{conditions.get("genre","")}/{conditions.get("platform","")}</p></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-box"><h3>⚡ 난이도</h3><p>{conditions.get("difficulty","")}</p></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-box"><h3>🎮 추천 수</h3><p>{len(matched)}개</p></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if not matched:
                st.warning("⚠️ 조건에 맞는 게임을 찾지 못했습니다.")
            else:
                perfect = [g for g in matched if not g["warnings"]]
                partial = [g for g in matched if g["warnings"]]

                if perfect:
                    st.markdown('<div class="section-header">✅ 조건 완전 일치 추천</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    cols = st.columns(min(len(perfect), 3))
                    for i, game in enumerate(perfect):
                        with cols[i % 3]:
                            prices = GAME_PRICES.get(game["title"], {})
                            links = GAME_LINKS.get(game["title"], {})
                            price_text = ""
                            link_text = ""
                            if prices:
                                min_price = min(prices.values())
                                min_store = min(prices, key=prices.get)
                                price_text = "<p style='color:green; font-size:0.8em;'>💰 무료!</p>" if min_price == 0 else f"<p style='color:#333; font-size:0.8em;'>💰 최저가: {min_store} {min_price:,}원</p>"
                            if links:
                                link_items = " | ".join([f'<a href="{url}" target="_blank" style="color:#E4000F; font-size:0.8em;">{store}</a>' for store, url in links.items()])
                                link_text = f"<p>🛒 {link_items}</p>"
                            avg = get_avg_rating(game["title"])
                            star_text = f"<p style='font-size:0.85em;'>{'⭐' * round(avg)} {avg:.1f}점</p>" if avg else ""
                            st.markdown(f"""
                            <div class="game-card-perfect">
                                <div class="game-title">🎮 {game['title']}</div>
                                <p style="color:#444; margin:6px 0; font-size:0.9em;">{game['description']}</p>
                                <p style="color:#E4000F; font-size:0.8em;">✅ {', '.join(game['reasons'])}</p>
                                {price_text}{link_text}{star_text}
                            </div>
                            """, unsafe_allow_html=True)
                            msg = st.session_state.wish_msg.get(game["title"], "")
                            if msg:
                                st.caption(msg)
                            if st.button("❤️ 위시리스트", key=f"w_{i}_{game['title']}"):
                                ok = add_wishlist(game)
                                st.session_state.wish_msg[game["title"]] = "✅ 추가됐어요!" if ok else "이미 있어요!"
                                st.rerun()
                            with st.expander("✏️ 리뷰 남기기"):
                                rating = st.slider("별점", 1, 5, 3, key=f"rating_{i}_{game['title']}")
                                comment = st.text_input("한줄 리뷰", key=f"comment_{i}_{game['title']}")
                                if st.button("리뷰 등록", key=f"review_{i}_{game['title']}"):
                                    save_review(game["title"], rating, comment)
                                    st.success("리뷰가 등록됐어요!")

                if partial:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="section-header">⚠️ 조건 부분 일치 추천</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    cols = st.columns(min(len(partial), 3))
                    for i, game in enumerate(partial):
                        with cols[i % 3]:
                            prices = GAME_PRICES.get(game["title"], {})
                            links = GAME_LINKS.get(game["title"], {})
                            price_text = ""
                            link_text = ""
                            if prices:
                                min_price = min(prices.values())
                                min_store = min(prices, key=prices.get)
                                price_text = "<p style='color:green; font-size:0.8em;'>💰 무료!</p>" if min_price == 0 else f"<p style='color:#333; font-size:0.8em;'>💰 최저가: {min_store} {min_price:,}원</p>"
                            if links:
                                link_items = " | ".join([f'<a href="{url}" target="_blank" style="color:#E4000F; font-size:0.8em;">{store}</a>' for store, url in links.items()])
                                link_text = f"<p>🛒 {link_items}</p>"
                            avg = get_avg_rating(game["title"])
                            star_text = f"<p style='font-size:0.85em;'>{'⭐' * round(avg)} {avg:.1f}점</p>" if avg else ""
                            st.markdown(f"""
                            <div class="game-card-partial">
                                <div style="color:#888; font-size:1.0em; font-weight:700;">🎮 {game['title']}</div>
                                <p style="color:#444; margin:6px 0; font-size:0.9em;">{game['description']}</p>
                                <p style="color:#555; font-size:0.8em;">✅ {', '.join(game['reasons'])}</p>
                                <p style="color:#E4000F; font-size:0.8em;">⚠️ {', '.join(game['warnings'])}</p>
                                {price_text}{link_text}{star_text}
                            </div>
                            """, unsafe_allow_html=True)
                            msg = st.session_state.wish_msg.get(game["title"], "")
                            if msg:
                                st.caption(msg)
                            if st.button("❤️ 위시리스트", key=f"wp_{i}_{game['title']}"):
                                ok = add_wishlist(game)
                                st.session_state.wish_msg[game["title"]] = "✅ 추가됐어요!" if ok else "이미 있어요!"
                                st.rerun()
                            with st.expander("✏️ 리뷰 남기기"):
                                rating = st.slider("별점", 1, 5, 3, key=f"rating_p_{i}_{game['title']}")
                                comment = st.text_input("한줄 리뷰", key=f"comment_p_{i}_{game['title']}")
                                if st.button("리뷰 등록", key=f"review_p_{i}_{game['title']}"):
                                    save_review(game["title"], rating, comment)
                                    st.success("리뷰가 등록됐어요!")

                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("📋 검토 보고서 보기"):
                    with st.spinner("검토 중..."):
                        review = review_recommendations(matched)
                    st.markdown(review)
                    st.download_button("📥 검토 보고서 다운로드", data=review, file_name="review_report.txt", mime="text/plain")

                with st.expander("📄 전체 추천 결과 보기"):
                    result = write_recommendations(conditions, matched)
                    st.markdown(result)
                    st.download_button("📥 추천 결과 다운로드", data=result, file_name="output.txt", mime="text/plain")

                user_guide = write_user_guide(conditions, matched)
                st.download_button("📥 안내문 다운로드", data=user_guide, file_name="output_user_guide.txt", mime="text/plain")
        else:
            st.markdown("""
            <div style="text-align:center; padding:30px 0 10px 0; color:#aaa;">
                <h3>👈 왼쪽에서 조건을 선택하고 추천받기 버튼을 눌러주세요!</h3>
            </div>
            """, unsafe_allow_html=True)

            reviews = load_reviews()
            rated_games = []
            for title, review_list in reviews.items():
                if review_list:
                    avg = sum(r["rating"] for r in review_list) / len(review_list)
                    rated_games.append({
                        "title": title,
                        "avg": avg,
                        "count": len(review_list),
                    })
            rated_games.sort(key=lambda x: -x["avg"])

            if rated_games:
                st.markdown('<div class="section-header">⭐ 유저 평점 높은 게임</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                cols = st.columns(min(len(rated_games), 3))
                for i, g in enumerate(rated_games[:6]):
                    with cols[i % 3]:
                        stars = "⭐" * round(g["avg"])
                        links = GAME_LINKS.get(g["title"], {})
                        link_text = ""
                        if links:
                            link_items = " | ".join([f'<a href="{url}" target="_blank" style="color:#E4000F; font-size:0.8em;">{store}</a>' for store, url in links.items()])
                            link_text = f"<p>🛒 {link_items}</p>"
                        st.markdown(f"""
                        <div class="game-card-perfect">
                            <div class="game-title">🎮 {g['title']}</div>
                            <p style="font-size:1.1em; margin:6px 0;">{stars}</p>
                            <p style="color:#888; font-size:0.8em;">{g['avg']:.1f}점 · {g['count']}개 리뷰</p>
                            <p style="color:#555; font-size:0.8em; font-style:italic;">"{reviews[g['title']][0]['comment']}"</p>
                            {link_text}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("아직 리뷰가 없어요! 게임 추천을 받고 리뷰를 남겨보세요 ✏️")

with tab2:
    st.markdown("## ❤️ 나의 위시리스트")
    wishlist = load_wishlist()
    if not wishlist:
        st.info("아직 위시리스트가 비어있어요! 게임 추천을 받고 ❤️ 버튼을 눌러보세요.")
    else:
        st.markdown(f"총 **{len(wishlist)}개** 게임이 저장되어 있습니다.")
        for game in wishlist:
            prices = GAME_PRICES.get(game["title"], {})
            links = GAME_LINKS.get(game["title"], {})
            reviews = load_reviews()
            game_reviews = reviews.get(game["title"], [])
            col1, col2 = st.columns([4, 1])
            with col1:
                price_info = " | ".join([f"{store}: {price:,}원" if price > 0 else f"{store}: 무료" for store, price in prices.items()]) if prices else "가격 정보 없음"
                link_info = " | ".join([f'<a href="{url}" target="_blank" style="color:#E4000F;">{store}에서 구매</a>' for store, url in links.items()]) if links else ""
                avg = get_avg_rating(game["title"])
                star_text = f'<span style="font-size:0.85em;">{"⭐" * round(avg)} {avg:.1f}점 ({len(game_reviews)}개 리뷰)</span><br>' if avg else ""
                st.markdown(f"""
                <div class="wishlist-card">
                    <b>🎮 {game['title']}</b><br>
                    <span style="font-size:0.9em; color:#666;">{game['description']}</span><br>
                    <span style="font-size:0.8em; color:#E4000F;">💰 {price_info}</span><br>
                    {f'<span style="font-size:0.8em;">🛒 {link_info}</span><br>' if link_info else ''}
                    {star_text}
                    <span style="font-size:0.75em; color:#aaa;">추가일: {game['added']}</span>
                </div>
                """, unsafe_allow_html=True)
                if game_reviews:
                    for r in game_reviews[:3]:
                        st.caption(f"{'⭐' * r['rating']} {r['comment']} - {r['date']}")
            with col2:
                if st.button("🗑️ 삭제", key=f"del_{game['title']}"):
                    remove_wishlist(game["title"])
                    st.rerun()

with tab3:
    st.markdown("## 📊 검색 통계 대시보드")
    history = load_history()
    if len(history) < 2:
        st.info("검색을 더 해보면 통계가 나타납니다!")
    else:
        st.markdown(f"총 **{len(history)}번** 검색했습니다.")
        col1, col2 = st.columns(2)
        genre_counts = {}
        platform_counts = {}
        difficulty_counts = {}
        for h in history:
            genre_counts[h["genre"]] = genre_counts.get(h["genre"], 0) + 1
            platform_counts[h["platform"]] = platform_counts.get(h["platform"], 0) + 1
            difficulty_counts[h["difficulty"]] = difficulty_counts.get(h["difficulty"], 0) + 1
        with col1:
            st.markdown("### 🎯 장르별 검색")
            for g, c in sorted(genre_counts.items(), key=lambda x: -x[1]):
                pct = int(c / len(history) * 100)
                st.markdown(f"**{g}**: {c}회 ({pct}%)")
                st.progress(pct / 100)
        with col2:
            st.markdown("### 🖥️ 플랫폼별 검색")
            for p, c in sorted(platform_counts.items(), key=lambda x: -x[1]):
                pct = int(c / len(history) * 100)
                st.markdown(f"**{p}**: {c}회 ({pct}%)")
                st.progress(pct / 100)
        st.markdown("### ⚡ 난이도별 검색")
        cols = st.columns(3)
        for i, (d, c) in enumerate(sorted(difficulty_counts.items(), key=lambda x: -x[1])):
            with cols[i % 3]:
                st.metric(d, f"{c}회")

with tab4:
    st.markdown("## 💼 비즈니스 모델")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 💰 수익화 전략

        **1. 게임사 제휴 광고**
        - 닌텐도, EA, Ubisoft, Blizzard 등과 제휴
        - 추천 결과 상단에 스폰서 게임 노출
        - CPC(클릭당 과금) 또는 CPM(노출당 과금) 모델

        **2. 구독 모델 (프리미엄)**
        - 무료: 기본 추천 5개
        - 프리미엄 (월 3,900원): 무제한 추천 + AI 검토자
        - 비즈니스 (월 19,900원): API 접근 + 데이터 리포트

        **3. 데이터 판매**
        - 게임사에 사용자 선호도 데이터 판매
        - 어떤 장르/플랫폼이 인기있는지 분석 리포트
        """)
    with col2:
        st.markdown("""
        ### 📈 시장 분석

        **타겟 시장**
        - 국내 게임 시장 규모: 약 20조원 (2024)
        - 닌텐도 스위치 국내 판매량: 200만대 이상
        - Steam 국내 월간 사용자: 수백만명

        **경쟁 우위**
        - AI 기반 맞춤형 추천 (멀티플랫폼)
        - 실시간 가격 비교
        - 위시리스트 + 구매 링크 연동

        **예상 수익 (1년차)**
        - 광고 수익: 월 200만원
        - 구독 수익 (1,000명 기준): 월 390만원
        - 데이터 판매: 분기 500만원
        """)

    st.markdown("---")
    st.markdown("## 📢 광고 문의")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border: 2px solid #E4000F; border-radius: 14px; padding: 24px; color: white; margin-bottom: 20px;">
        <h3 style="color: #E4000F; margin-top:0;">🎯 GameMatch AI와 함께 당신의 게임을 홍보하세요!</h3>
        <p style="color: #ccc;">월 수천명의 게임 유저에게 직접 노출되는 AI 기반 게임 추천 플랫폼입니다.<br>
        조건에 맞는 유저에게만 노출되는 정밀 타겟 광고로 높은 전환율을 경험하세요.</p>
    </div>
    """, unsafe_allow_html=True)

    ad_col1, ad_col2, ad_col3 = st.columns(3)
    with ad_col1:
        st.markdown("""
        <div style="background:#fff; border: 2px solid #E4000F; border-radius: 12px; padding: 16px; text-align:center; box-shadow: 3px 3px 0px #E4000F;">
            <h3 style="color:#E4000F;">🥉 베이직</h3>
            <h2 style="color:#333;">월 50만원</h2>
            <hr>
            <p>✅ 메인 배너 노출</p>
            <p>✅ 월 1개 게임 스폰서</p>
            <p>✅ 클릭 통계 제공</p>
            <p>❌ 타겟 노출</p>
            <p>❌ 데이터 리포트</p>
        </div>
        """, unsafe_allow_html=True)
    with ad_col2:
        st.markdown("""
        <div style="background:#fff; border: 2px solid #E4000F; border-radius: 12px; padding: 16px; text-align:center; box-shadow: 3px 3px 0px #E4000F;">
            <h3 style="color:#E4000F;">🥈 스탠다드</h3>
            <h2 style="color:#333;">월 150만원</h2>
            <hr>
            <p>✅ 메인 배너 우선 노출</p>
            <p>✅ 월 3개 게임 스폰서</p>
            <p>✅ 클릭 통계 제공</p>
            <p>✅ 장르/플랫폼 타겟 노출</p>
            <p>❌ 데이터 리포트</p>
        </div>
        """, unsafe_allow_html=True)
    with ad_col3:
        st.markdown("""
        <div style="background:#fff; border: 2px solid #E4000F; border-radius: 12px; padding: 16px; text-align:center; box-shadow: 3px 3px 0px #E4000F;">
            <h3 style="color:#E4000F;">🥇 프리미엄</h3>
            <h2 style="color:#333;">월 300만원</h2>
            <hr>
            <p>✅ 메인 배너 독점 노출</p>
            <p>✅ 무제한 게임 스폰서</p>
            <p>✅ 실시간 클릭 통계</p>
            <p>✅ 정밀 타겟 노출</p>
            <p>✅ 월간 데이터 리포트</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#fff8f8; border: 2px solid #E4000F; border-radius: 12px; padding: 20px; text-align:center;">
        <h3 style="color:#E4000F;">📩 광고 문의</h3>
        <p style="color:#333;">게임사, 퍼블리셔, 개인 개발자 모두 환영합니다!</p>
        <p style="font-size:1.2em;"><b>📧 ljea22@hs.ac.kr</b></p>
        <p style="color:#888; font-size:0.85em;">문의 후 영업일 기준 1-2일 내 답변드립니다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 스폰서 게임 시뮬레이션")
    for sponsor in SPONSOR_GAMES:
        st.markdown(f"""
        <div class="sponsor-banner" style="background: linear-gradient(135deg, {sponsor['color']}, #16213e);">
            <b>{sponsor['title']}</b><br>
            <span style="font-size:0.9em;">{sponsor['desc']}</span><br>
            <a href="{sponsor['url']}" target="_blank" style="background:#E4000F; padding:4px 12px; border-radius:4px; font-size:0.8em; color:white; text-decoration:none; display:inline-block; margin-top:8px;">
                {sponsor['badge']} - 구매하러 가기 →
            </a>
        </div>
        """, unsafe_allow_html=True)