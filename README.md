# 게임 추천 에이전트

## 한 문장 설명
장르, 플랫폼, 난이도 조건을 입력하면 맞는 게임을 추천해주는 멀티에이전트 프로그램입니다.

## 해결하려는 문제
게임을 고를 때 장르, 플랫폼, 난이도 등 조건이 많아 선택이 어렵다.
조건을 입력하면 맞는 게임을 자동으로 추천해주는 에이전트를 만들었다.

## 실행 방법

Streamlit 화면 실행 (기본)
streamlit run streamlit_app.py

터미널 실행 (보조)
python3 my_agent.py

## 입력 파일
- sample_input.txt : 입력 예시

## 출력 파일
- output.md : 추천 게임 목록
- output_user_guide.md : 완전/부분 일치 분류 안내문
- review_report.md : 검토 보고서

## 에이전트 역할
| 역할 | 함수 | 설명 |
|---|---|---|
| 조건 추출 | extract_conditions | 입력 텍스트에서 장르, 플랫폼, 난이도, 플레이어 조건을 추출한다 |
| 게임 분류 | classify_games | 조건에 맞는 게임 후보를 추린다 |
| 추천문 작성 | write_recommendations | 추천 목록과 설명을 만든다 |
| 안내문 작성 | write_user_guide | 완전/부분 일치로 나눠 안내문을 만든다 |
| 검토 | review_recommendations | 조건 불일치 항목을 점검한다 |

## 사용한 코딩에이전트
- GitHub Copilot
- Gemini CLI
- Antigravity

## 구현 수준
- 기본형: 규칙 기반 함수 에이전트. 외부 API 없이 실행 가능

## 사용한 API 또는 외부 도구
- 없음

## 현재 한계
- 게임 목록이 코드 안에 고정되어 있어 새 게임 추가가 번거롭다
- 자연어 입력은 지원하지 않는다
- 게임 수가 적어 조건에 따라 추천 결과가 없을 수 있다
