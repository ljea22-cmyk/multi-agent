# reproduce_windows.ps1
# Windows에서 원본 폴더(C:\agenticai\multi-agent)를 대상으로 복제본 C:\muti-agent를 생성하는 스크립트
# 사용법: 저장소 루트(또는 스크립트 위치)에서 PowerShell을 열고 다음을 실행하세요:
#   .\reproduce_windows.ps1

param(
    [string]$Source = "C:\agenticai\multi-agent",
    [string]$Target = "C:\muti-agent"
)

Write-Host "Source: $Source"
Write-Host "Target: $Target"

if (-Not (Test-Path $Source)) {
    Write-Host "원본 폴더가 존재하지 않습니다: $Source" -ForegroundColor Red
    exit 1
}

# Create target folder if missing
if (-Not (Test-Path $Target)) {
    New-Item -ItemType Directory -Path $Target | Out-Null
    Write-Host "대상 폴더를 생성했습니다: $Target"
}

# Use robocopy for robust copying. Exclude .git by default.
$exclude = ".git"
$robocopyArgs = @($Source, $Target, "/E", "/XD", $exclude)
$rc = Start-Process -FilePath robocopy -ArgumentList $robocopyArgs -NoNewWindow -Wait -PassThru
if ($rc.ExitCode -ge 8) {
    Write-Host "robocopy 실패 (exit code: $($rc.ExitCode))." -ForegroundColor Red
    exit $rc.ExitCode
}
Write-Host "파일 복사 완료. (robocopy exit code: $($rc.ExitCode))"

# Simple in-file replacements for a few documentation files to point to the new path
$filesToPatch = @('.github/copilot-instructions.md', 'context.md', 'todo.md', 'AGENTS.md')
foreach ($f in $filesToPatch) {
    $srcPath = Join-Path $Target $f
    if (Test-Path $srcPath) {
        (Get-Content $srcPath) -replace 'C:\\agenticai\\multi-agent', $Target | Set-Content $srcPath
        Write-Host "Patched paths in $srcPath"
    }
}

Write-Host "재현 완료: $Target"
Write-Host "다음: 대상 폴더에서 Python 가상환경을 만들고 의존성을 설치하세요."
