# 게임 추천 에이전트 v1
# 조건 추출 → 게임 분류 → 추천문 작성 → 파일 저장

from pathlib import Path

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
        "title": "스플래툰 3",
        "genre": ["액션", "FPS"],
        "platform": ["닌텐도"],
        "difficulty": "보통",
        "player": ["싱글", "멀티"],
        "description": "잉크를 뿌리며 싸우는 닌텐도 팀 슈터 게임",
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

        # 플랫폼 조건이 있으면 반드시 일치해야 함
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


def review_recommendations(matched):
    """추천 결과를 검토한다."""
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

    print("\n=== 검토 ===")
    review = review_recommendations(matched)
    print(review)

    save_output(result, "output.md")
    save_output(review, "review_report.md")


if __name__ == "__main__":
    main()