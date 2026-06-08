# 게임 추천 에이전트 v4 - LangGraph 버전
# 조건 추출 → 게임 분류 → 추천문 작성 → 검토 → (재추천 루프)

from typing import TypedDict
from langgraph.graph import StateGraph, END
from pathlib import Path
from dotenv import load_dotenv
import os

from my_agent import (
    extract_conditions,
    classify_games,
    write_recommendations,
    write_user_guide,
    review_with_rules,
    review_with_groq,
    save_output,
    GROQ_API_KEY,
)

load_dotenv()

# 상태 정의
class GameAgentState(TypedDict):
    input_text: str
    conditions: dict
    matched: list
    recommendations: str
    user_guide: str
    review: str
    attempt: int
    is_ok: bool


# 노드 1: 조건 추출
def extract_node(state: GameAgentState) -> dict:
    print(f"[조건 추출] 시도 {state['attempt'] + 1}회")
    conditions = extract_conditions(state["input_text"])
    print(f"  추출된 조건: {conditions}")
    return {"conditions": conditions}


# 노드 2: 게임 분류
def classify_node(state: GameAgentState) -> dict:
    print("[게임 분류]")
    matched = classify_games(state["conditions"])
    print(f"  후보 게임 {len(matched)}개 발견")
    return {"matched": matched}


# 노드 3: 추천문 작성
def recommend_node(state: GameAgentState) -> dict:
    print("[추천문 작성]")
    recommendations = write_recommendations(state["conditions"], state["matched"])
    user_guide = write_user_guide(state["conditions"], state["matched"])
    return {
        "recommendations": recommendations,
        "user_guide": user_guide,
        "attempt": state["attempt"] + 1,
    }


# 노드 4: 검토
def review_node(state: GameAgentState) -> dict:
    print("[검토]")
    matched = state["matched"]

    if not matched:
        review = "# 검토 보고서\n\n조건에 맞는 게임이 없습니다."
        is_ok = False
    else:
        try:
            if GROQ_API_KEY:
                review = review_with_groq(matched)
            else:
                review = review_with_rules(matched)
        except Exception:
            review = review_with_rules(matched)

        # 완전 일치 게임이 1개 이상이면 통과
        perfect = [g for g in matched if not g["warnings"]]
        is_ok = len(perfect) >= 1

    print(f"  검토 결과: {'통과' if is_ok else '재검토 필요'}")
    return {"review": review, "is_ok": is_ok}


# 노드 5: 저장
def save_node(state: GameAgentState) -> dict:
    print("[결과 저장]")
    save_output(state["recommendations"], "output.md")
    save_output(state["user_guide"], "output_user_guide.md")
    save_output(state["review"], "review_report.md")
    return {}


# 분기 함수
def route(state: GameAgentState) -> str:
    if state["is_ok"]:
        return "save"
    if state["attempt"] >= 3:
        print("[종료] 최대 시도 횟수 초과, 현재 결과로 저장합니다.")
        return "save"
    print("[재시도] 조건을 완화해서 다시 추천합니다.")
    return "classify"


# 그래프 조립
builder = StateGraph(GameAgentState)

builder.add_node("extract", extract_node)
builder.add_node("classify", classify_node)
builder.add_node("recommend", recommend_node)
builder.add_node("review", review_node)
builder.add_node("save", save_node)

builder.set_entry_point("extract")
builder.add_edge("extract", "classify")
builder.add_edge("classify", "recommend")
builder.add_edge("recommend", "review")
builder.add_conditional_edges("review", route, {
    "save": "save",
    "classify": "classify",
})
builder.add_edge("save", END)

graph = builder.compile()


def run_graph(input_text: str):
    initial_state = {
        "input_text": input_text,
        "conditions": {},
        "matched": [],
        "recommendations": "",
        "user_guide": "",
        "review": "",
        "attempt": 0,
        "is_ok": False,
    }
    result = graph.invoke(initial_state)
    return result


if __name__ == "__main__":
    SAMPLE_INPUT = """
장르: RPG
플랫폼: 닌텐도
난이도: 쉬움
플레이어: 싱글
"""
    print("=== LangGraph 게임 추천 에이전트 ===\n")
    result = run_graph(SAMPLE_INPUT)
    print("\n=== 최종 결과 ===")
    print(result["recommendations"])
    print(f"\n총 시도 횟수: {result['attempt']}")