# week10_tool_practice

이 문서는 도구 연습을 위한 기록입니다.

목표:

- Playwright CLI 사용법을 연습한다.
- Windows 재현 스크립트(`reproduce_windows.ps1`) 사용 흐름을 문서화한다.

시나리오:

1. 로컬에서 `docs/week-10.html`을 Playwright CLI로 열어 확인한다.
2. Windows 환경에서 `C:\agenticai\multi-agent`을 `C:\muti-agent`로 재현한다.

명령 예시:

```bash
# Playwright CLI로 HTML 열기
playwright-cli open docs/week-10.html
```

```powershell
# Windows에서 복제
.\reproduce_windows.ps1
```

검증:

- Playwright가 브라우저를 열고 페이지를 렌더링하는지 확인.
- 복제본의 `README.md` 및 `requirements.txt`가 올바르게 복사되었는지 확인.

메모:

- Playwright는 MCP 대신 CLI로만 사용합니다.
- Windows 복제는 robocopy 또는 PowerShell 복사 루틴을 사용할 수 있습니다.
