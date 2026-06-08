# 게임 추천 에이전트 v0
# 조건 추출 → 게임 분류 → 추천문 작성

SAMPLE_INPUT = """
장르: RPG
플랫폼: PC
난이도: 쉬움
플레이어: 싱글
"""

GAME_DB = [
    {
        "title": "스타듀 밸리",
        "genre": ["RPG", "시뮬레이션"],
        "platform": ["PC", "모바일", "콘솔"],
        "difficulty": "쉬움",
        "player": ["싱글", "멀티"],
        "description": "농장을 가꾸며 마을 사람들과 교류하는 힐링 RPG",
    },
    {
        "title": "포켓몬스터 에메랄드",
        "genre": ["RPG"],
        "platform": ["콘솔"],
        "difficulty": "쉬움",
        "player": ["싱글"],
        "description": "포켓몬을 모으고 배틀하는 클래식 RPG",
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
        "platform": ["PC", "콘솔"],
        "difficulty": "보통",
        "player": ["싱글"],
        "description": "방대한 세계관과 스토리를 가진 오픈월드 RPG",
    },
    {
        "title": "마인크래프트",
        "genre": ["샌드박스", "어드벤처"],
        "platform": ["PC", "모바일", "콘솔"],
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
        "title": "오버워치 2",
        "genre": ["FPS", "액션"],
        "platform": ["PC", "콘솔"],
        "difficulty": "보통",
        "player": ["멀티"],
        "description": "팀 기반 영웅 슈터 게임",
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

        if conditions["genre"] and conditions["genre"] in game["genre"]:
            score += 1
            reasons.append(f"장르 일치: {conditions['genre']}")
        elif conditions["genre"]:
            warnings.append(f"장르가 {conditions['genre']}이 아님")

        if conditions["platform"] and conditions["platform"] in game["platform"]:
            score += 1
            reasons.append(f"플랫폼 일치: {conditions['platform']}")
        elif conditions["platform"]:
            warnings.append(f"플랫폼이 {conditions['platform']}이 아님")

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


if __name__ == "__main__":
    main()