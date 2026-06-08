# 12주차 과제

## GitHub 저장소
- URL: https://github.com/ljea22-cmyk/multi-agent

## 내 에이전트
- 에이전트 이름: 게임 추천 에이전트
- 에이전트 유형: 정보 추출형
- 해결하려는 문제: 게임 조건을 입력받아 맞는 게임을 추천
- 입력 자료: 장르, 플랫폼, 난이도, 플레이어 조건 텍스트
- 결과 파일: output.md, output_user_guide.md, review_report.md

## 중간 정보 구조
| key | 의미 |
|---|---|
| title | 게임 제목 |
| description | 게임 설명 |
| score | 조건 일치 점수 |
| reasons | 일치 항목 목록 |
| warnings | 주의사항 목록 |

## 판단/처리 기준
- 기준 1: 플랫폼 조건이 있으면 반드시 일치해야 함
- 기준 2: 점수 2점 이상인 게임만 추천
- 기준 3: 점수 높은 순으로 정렬

## 실행 명령
- python3 my_agent.py

## 실행 결과 요약
- 입력 항목: 장르, 플랫폼, 난이도, 플레이어
- 만들어진 중간 정보: 게임별 점수, 일치 항목, 주의사항
- 판단/처리 결과: 조건 완전 일치 / 부분 일치로 분류
- 생성된 파일: output.md, output_user_guide.md, review_report.md

## 오늘 수정한 함수
| 함수 | 역할 | 수정 내용 |
|---|---|---|
| extract_conditions | 입력 분석 | 장르, 플랫폼, 난이도, 플레이어 추출 |
| classify_games | 판단/처리 | 플랫폼 필터링, 점수 기반 분류 |
| write_user_guide | 결과 저장 | 완전/부분 일치 분리 안내문 작성 |

## LLM 또는 외부 도구
- LLM 보조 사용: 없음
- 외부 도구/API: 없음
- fallback 동작: 해당 없음

## 코딩에이전트에게 준 지시 2개
1. 플랫폼 조건이 맞지 않으면 아예 제외하도록 수정
2. output_user_guide.md 저장 기능 추가

## 남은 문제
- [ ] Streamlit 화면 추가
- [ ] 검토자 에이전트 개선
