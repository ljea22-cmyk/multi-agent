# 14주차 최종 점검

## GitHub 저장소
- URL: https://github.com/ljea22-cmyk/multi-agent

## 내 에이전트
- 이름: 게임 추천 에이전트
- 해결하려는 문제: 장르, 플랫폼, 난이도 등 조건을 입력하면 맞는 게임을 추천
- 구현 수준: 중급형

## 실행 명령
- python3 my_agent.py
- streamlit run streamlit_app.py

## 생성된 출력 파일
- output.md: 추천 게임 목록
- output_user_guide.md: 완전/부분 일치 분류 안내문
- review_report.md: 검토 보고서 (Groq AI 또는 규칙 기반)

## 에이전트 역할
| 역할 | 함수 | 설명 |
|---|---|---|
| 조건 추출 | extract_conditions | 입력 텍스트에서 장르, 플랫폼, 난이도, 플레이어 조건을 추출한다 |
| 게임 분류 | classify_games | 조건에 맞는 게임 후보를 추린다 |
| 추천문 작성 | write_recommendations | 추천 목록과 설명을 만든다 |
| 안내문 작성 | write_user_guide | 완전/부분 일치로 나눠 안내문을 만든다 |
| 검토 | review_recommendations | Groq API로 검토, 실패 시 규칙 기반으로 fallback |

## 사용한 코딩에이전트
- GitHub Copilot
- Gemini CLI
- Antigravity

## 사용한 API 또는 외부 도구
- Groq API: llama-3.3-70b-versatile 모델로 검토자 역할
- API 키: .env 파일에 저장 (GROQ_API_KEY)
- fallback 동작: Groq API 실패 시 규칙 기반 검토로 자동 전환

## 아직 부족한 점
- 게임 목록이 코드 안에 고정되어 있어 새 게임 추가가 번거롭다
- 자연어 입력은 지원하지 않는다
- 게임 수가 적어 조건에 따라 추천 결과가 없을 수 있다

## 발표 때 보여줄 순서
1. streamlit run streamlit_app.py 실행해서 화면 보여주기
2. 사이드바에서 조건 선택 (예: RPG, 닌텐도, 쉬움, 싱글)
3. 추천받기 버튼 클릭
4. 완전 일치 게임 카드 보여주기
5. 부분 일치 게임 카드 보여주기
6. 검토 보고서 펼쳐서 Groq AI 검토 결과 보여주기
7. 다운로드 버튼으로 결과 저장 보여주기
8. python3 my_agent.py 실행해서 터미널 출력 보여주기
