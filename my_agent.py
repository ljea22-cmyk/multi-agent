# 게임 추천 에이전트 v3
# 조건 추출 → 게임 분류 → 추천문 작성 → 검토 → 파일 저장

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
USE_LLM_REVIEW = True if GROQ_API_KEY else False

SAMPLE_INPUT = """
장르: RPG
플랫폼: 닌텐도
난이도: 쉬움
플레이어: 싱글
"""

GAME_DB = [
    {
        "title": "스타듀 밸리",
        "genre": ["RPG", "시뮬레이션"],
        "platform": ["PC", "닌텐도", "모바일", "콘솔"],
        "difficulty": "쉬움",
        "player": ["싱글", "멀티"],
        "description": "농장을 가꾸며 마을 사람들과 교류하는 힐링 RPG",
    },
    {
        "title": "젤다의 전설: 야생의 숨결",
        "genre": ["RPG", "어드벤처"],
        "platform": ["닌텐도"],
        "difficulty": "보통",
        "player": ["싱글"],
        "description": "광활한 하이랄을 탐험하는 오픈월드 어드벤처 RPG",
    },
    {
        "title": "젤다의 전설: 티어스 오브 더 킹덤",
        "genre": ["RPG", "어드벤처"],
        "platform": ["닌텐도"],
        "difficulty": "보통",
        "player": ["싱글"],
        "description": "야생의 숨결의 후속작, 더 넓어진 세계와 창의적인 조합 시스템",
    },
    {
        "title": "포켓몬스터 스칼렛/바이올렛",
        "genre": ["RPG"],
        "platform": ["닌텐도"],
        "difficulty": "쉬움",
        "player": ["싱글", "멀티"],
        "description": "오픈월드로 진화한 포켓몬 시리즈 최신작",
    },
    {
        "title": "포켓몬스터 소드/실드",
        "genre": ["RPG"],
        "platform": ["닌텐도"],
        "difficulty": "쉬움",
        "player": ["싱글", "멀티"],
        "description": "영국풍 갈라르 지방을 배경으로 한 포켓몬 시리즈",
    },
    {
        "title": "동물의 숲: 뉴 호라이즌",
        "genre": ["시뮬레이션"],
        "platform": ["닌텐도"],
        "difficulty": "쉬움",
        "player": ["싱글", "멀티"],
        "description": "무인도에서 나만의 마을을 꾸미는 힐링 게임",
    },
    {
        "title": "마리오 오디세이",
        "genre": ["액션", "어드벤처"],
        "platform": ["닌텐도"],
        "difficulty": "쉬움",
        "player": ["싱글"],
        "description": "마리오가 모자를 이용해 세계를 여행하는 3D 액션 게임",
    },
    {
        "title": "마리오 카트 8 디럭스",
        "genre": ["레이싱", "액션"],
        "platform": ["닌텐도"],
        "difficulty": "쉬움",
        "player": ["싱글", "멀티"],
        "description": "친구들과 함께 즐기는 닌텐도 대표 레이싱 게임",
    },
    {
        "title": "슈퍼 마리오 브라더스 원더",
        "genre": ["액션", "어드벤처"],
        "platform": ["닌텐도"],
        "difficulty": "쉬움",
        "player": ["싱글", "멀티"],
        "description": "꽃 왕국을 배경으로 한 신선한 아이디어의 2D 마리오",
    },
    {
        "title": "스플래툰 3",
        "genre": ["액션", "FPS"],
        "platform": ["닌텐도"],
        "difficulty": "보통",
        "player": ["싱글", "멀티"],
        "description": "잉크를 뿌리며 싸우는 닌텐도 팀 슈터 게임",
    },
    {
        "title": "대난투 스매시브라더스 얼티밋",
        "genre": ["액션", "격투"],
        "platform": ["닌텐도"],
        "difficulty": "보통",
        "player": ["싱글", "멀티"],
        "description": "닌텐도 캐릭터들이 총출동하는 격투 게임",
    },
    {
        "title": "피크민 4",
        "genre": ["어드벤처", "전략"],
        "platform": ["닌텐도"],
        "difficulty": "쉬움",
        "player": ["싱글"],
        "description": "귀여운 피크민을 이끌고 행성을 탐험하는 전략 어드벤처",
    },
    {
        "title": "커비 스타 얼라이즈",
        "genre": ["액션", "어드벤처"],
        "platform": ["닌텐도"],
        "difficulty": "쉬움",
        "player": ["싱글", "멀티"],
        "description": "적을 흡수해 능력을 쓰는 귀여운 핑크 악당 커비의 모험",
    },
    {
        "title": "메트로이드 드레드",
        "genre": ["액션", "어드벤처"],
        "platform": ["닌텐도"],
        "difficulty": "어려움",
        "player": ["싱글"],
        "description": "사무스가 위험한 행성을 탐험하는 긴장감 넘치는 액션 게임",
    },
    {
        "title": "파이어 엠블렘 엔게이지",
        "genre": ["RPG", "전략"],
        "platform": ["닌텐도"],
        "difficulty": "보통",
        "player": ["싱글"],
        "description": "전략적 전투와 깊은 스토리를 가진 SRPG",
    },
    {
        "title": "몬스터 헌터 라이즈",
        "genre": ["액션", "RPG"],
        "platform": ["닌텐도", "PC"],
        "difficulty": "보통",
        "player": ["싱글", "멀티"],
        "description": "거대한 몬스터를 사냥하는 액션 RPG",
    },
    {
        "title": "다크 소울 3",
        "genre": ["RPG", "액션"],
        "platform": ["PC", "콘솔"],
        "difficulty": "어려움",
        "player": ["싱글", "멀티"],
        "description": "높은 난이도의 액션 RPG, 죽음을 반복하며 성장하는 게임",
    },
    {
        "title": "위처 3",
        "genre": ["RPG", "액션"],
        "platform": ["PC", "콘솔", "닌텐도"],
        "difficulty": "보통",
        "player": ["싱글"],
        "description": "방대한 세계관과 스토리를 가진 오픈월드 RPG",
    },
    {
        "title": "마인크래프트",
        "genre": ["샌드박스", "어드벤처"],
        "platform": ["PC", "모바일", "콘솔", "닌텐도"],
        "difficulty": "쉬움",
        "player": ["싱글", "멀티"],
        "description": "블록으로 무엇이든 만들 수 있는 샌드박스 게임",
    },
    {
        "title": "발더스 게이트 3",
        "genre": ["RPG"],
        "platform": ["PC", "콘솔"],
        "difficulty": "보통",
        "player": ["싱글", "멀티"],
        "description": "D&D 기반의 깊은 스토리와 전략적 전투를 가진 RPG",
    },
    {
        "title": "엘든 링",
        "genre": ["RPG", "액션"],
        "platform": ["PC", "콘솔"],
        "difficulty": "어려움",
        "player": ["싱글", "멀티"],
        "description": "조지 R.R. 마틴과 협업한 오픈월드 액션 RPG",
    },
    {
        "title": "오버워치 2",
        "genre": ["FPS", "액션"],
        "platform": ["PC", "콘솔"],
        "difficulty": "보통",
        "player": ["멀티"],
        "description": "팀 기반 영웅 슈터 게임",
    },
    {
        "title": "스타크래프트 2",
        "genre": ["전략"],
        "platform": ["PC"],
        "difficulty": "어려움",
        "player": ["싱글", "멀티"],
        "description": "실시간 전략 게임의 대명사",
    },
    {
        "title": "심즈 4",
        "genre": ["시뮬레이션"],
        "platform": ["PC", "콘솔"],
        "difficulty": "쉬움",
        "player": ["싱글"],
        "description": "나만의 캐릭터와 집을 만드는 인생 시뮬레이션 게임",
    },
]


def extract_conditions(text):
    """입력 텍스트에서 게임 조건을 추출한다."""
    conditions = {
        "genre": None,
        "platform": None,
        "difficulty": None,
        "player": None,
    }

    for line in text.strip().split("\n"):
        line = line.strip()
        if "장르:" in line:
            conditions["genre"] = line.split(":", 1)[1].strip()
        elif "플랫폼:" in line:
            conditions["platform"] = line.split(":", 1)[1].strip()
        elif "난이도:" in line:
            conditions["difficulty"] = line.split(":", 1)[1].strip()
        elif "플레이어:" in line:
            conditions["player"] = line.split(":", 1)[1].strip()

    return conditions


def classify_games(conditions):
    """조건에 맞는 게임 후보를 추린다."""
    matched = []

    for game in GAME_DB:
        score = 0
        reasons = []
        warnings = []

        if conditions["platform"] and conditions["platform"] not in game["platform"]:
            continue

        if conditions["genre"] and conditions["genre"] in game["genre"]:
            score += 1
            reasons.append(f"장르 일치: {conditions['genre']}")
        elif conditions["genre"]:
            warnings.append(f"장르가 {conditions['genre']}이 아님")

        if conditions["platform"] and conditions["platform"] in game["platform"]:
            score += 1
            reasons.append(f"플랫폼 일치: {conditions['platform']}")

        if conditions["difficulty"] and conditions["difficulty"] == game["difficulty"]:
            score += 1
            reasons.append(f"난이도 일치: {conditions['difficulty']}")
        elif conditions["difficulty"]:
            warnings.append(f"난이도가 {conditions['difficulty']}이 아님")

        if conditions["player"] and conditions["player"] in game["player"]:
            score += 1
            reasons.append(f"플레이어 일치: {conditions['player']}")
        elif conditions["player"]:
            warnings.append(f"{conditions['player']} 미지원")

        if score >= 2:
            matched.append({
                "title": game["title"],
                "description": game["description"],
                "score": score,
                "reasons": reasons,
                "warnings": warnings,
            })

    matched.sort(key=lambda x: x["score"], reverse=True)
    return matched


def write_recommendations(conditions, matched):
    """추천 목록과 설명을 작성한다."""
    result = []
    result.append("# 게임 추천 결과\n")
    result.append("## 입력 조건")
    result.append(f"- 장르: {conditions['genre']}")
    result.append(f"- 플랫폼: {conditions['platform']}")
    result.append(f"- 난이도: {conditions['difficulty']}")
    result.append(f"- 플레이어: {conditions['player']}")
    result.append("")

    if not matched:
        result.append("## 추천 결과")
        result.append("조건에 맞는 게임을 찾지 못했습니다. 조건을 바꿔서 다시 시도해보세요.")
        return "\n".join(result)

    result.append("## 추천 게임 목록")
    for i, game in enumerate(matched, 1):
        result.append(f"\n### {i}. {game['title']}")
        result.append(f"{game['description']}")
        result.append(f"- 일치 항목: {', '.join(game['reasons'])}")
        if game["warnings"]:
            result.append(f"- 주의사항: {', '.join(game['warnings'])}")

    return "\n".join(result)


def write_user_guide(conditions, matched):
    """사용자 유형별 안내문을 작성한다."""
    result = []
    result.append("# 게임 추천 안내문\n")
    result.append(f"## 조건: 장르={conditions['genre']}, 플랫폼={conditions['platform']}, 난이도={conditions['difficulty']}, 플레이어={conditions['player']}\n")

    if not matched:
        result.append("조건에 맞는 게임을 찾지 못했습니다. 조건을 바꿔서 다시 시도해보세요.")
        return "\n".join(result)

    perfect = [g for g in matched if not g["warnings"]]
    partial = [g for g in matched if g["warnings"]]

    if perfect:
        result.append("## ✅ 조건 완전 일치 추천")
        for game in perfect:
            result.append(f"\n### {game['title']}")
            result.append(f"{game['description']}")
            result.append(f"- 일치 항목: {', '.join(game['reasons'])}")

    if partial:
        result.append("\n## ⚠️ 조건 부분 일치 추천 (참고용)")
        for game in partial:
            result.append(f"\n### {game['title']}")
            result.append(f"{game['description']}")
            result.append(f"- 일치 항목: {', '.join(game['reasons'])}")
            result.append(f"- 주의사항: {', '.join(game['warnings'])}")

    result.append("\n## 📌 주의사항")
    result.append("- 위 추천은 입력 조건 기반이며, 실제 게임과 다를 수 있습니다.")
    result.append("- 부분 일치 게임은 조건을 확인 후 선택하세요.")

    return "\n".join(result)


def review_with_rules(matched):
    """규칙 기반 검토자."""
    issues = []
    for game in matched:
        if game["warnings"]:
            issues.append(f"- {game['title']}: {', '.join(game['warnings'])}")

    result = []
    result.append("# 검토 보고서\n")
    if not issues:
        result.append("## 검토 결과")
        result.append("모든 추천 게임이 입력 조건과 일치합니다.")
    else:
        result.append("## 주의가 필요한 항목")
        result.extend(issues)

    return "\n".join(result)


def review_with_groq(matched):
    """Groq API 기반 검토자."""
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)

    game_list = "\n".join([
        f"- {g['title']}: 일치={', '.join(g['reasons'])}, 주의={', '.join(g['warnings']) if g['warnings'] else '없음'}"
        for g in matched
    ])

    prompt = f"""다음은 게임 추천 결과입니다. 아래 기준으로 검토해줘.
1. 입력 조건과 맞지 않는 항목이 있는가
2. 사용자가 주의해야 할 점이 있는가
3. 추천 결과가 적절한가

추천 결과:
{game_list}

검토 결과를 한국어로 짧게 작성해줘."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )

    review_text = response.choices[0].message.content

    result = []
    result.append("# 검토 보고서 (Groq AI 검토)\n")
    result.append(review_text)
    return "\n".join(result)


def review_recommendations(matched):
    """검토자 에이전트. Groq API 실패 시 규칙 기반으로 fallback."""
    if USE_LLM_REVIEW:
        try:
            print("Groq API로 검토 중...")
            return review_with_groq(matched)
        except Exception as e:
            print(f"Groq API 실패: {e}, 규칙 기반 검토로 전환합니다.")
            return review_with_rules(matched)
    return review_with_rules(matched)


def save_output(content, path):
    """결과를 파일로 저장한다."""
    output_path = Path(path)
    output_path.write_text(content, encoding="utf-8")
    print(f"저장 완료: {output_path}")


def main():
    print("=== 조건 추출 ===")
    conditions = extract_conditions(SAMPLE_INPUT)
    print(conditions)

    print("\n=== 게임 분류 ===")
    matched = classify_games(conditions)
    print(f"후보 게임 {len(matched)}개 발견")
    for g in matched:
        print(f"  - {g['title']} (점수: {g['score']})")

    print("\n=== 추천문 작성 ===")
    result = write_recommendations(conditions, matched)
    print(result)

    print("\n=== 사용자 안내문 작성 ===")
    user_guide = write_user_guide(conditions, matched)
    print(user_guide)

    print("\n=== 검토 ===")
    review = review_recommendations(matched)
    print(review)

    save_output(result, "output.md")
    save_output(user_guide, "output_user_guide.md")
    save_output(review, "review_report.md")


if __name__ == "__main__":
    main()