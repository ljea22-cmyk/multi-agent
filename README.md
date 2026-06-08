# 게임 추천 에이전트

조건을 입력하면 맞는 게임을 추천해주는 멀티에이전트 프로그램입니다.

## 실행 방법

streamlit run streamlit_app.py
python3 my_agent.py

## 출력 파일
- output.md : 추천 게임 목록
- review_report.md : 검토 보고서

## 에이전트 역할
| 역할 | 함수 | 설명 |
|---|---|---|
| 조건 추출 | extract_conditions | 입력 텍스트에서 장르, 플랫폼, 난이도, 플레이어 조건을 추출한다 |
| 게임 분류 | classify_games | 조건에 맞는 게임 후보를 추린다 |
| 추천문 작성 | write_recommendations | 사용자에게 추천 목록과 설명을 만든다 |
| 검토 | review_recommendations | 추천 결과에서 조건 불일치 항목을 점검한다 |

## 구현 수준
기본형: 규칙 기반 함수 에이전트. 외부 API 없이 실행 가능

## 현재 한계
- 게임 목록이 코드 안에 고정되어 있어 새 게임 추가가 번거롭다
- 자연어 입력은 지원하지 않는다
- 게임 수가 적어 조건에 따라 추천 결과가 없을 수 있다
