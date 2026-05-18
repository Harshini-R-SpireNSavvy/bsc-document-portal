# Run from project folder after: gh auth login
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$repoName = "bsc-document-portal"
$gh = Get-Command gh -ErrorAction SilentlyContinue
if (-not $gh) {
    Write-Host "Install GitHub CLI: winget install GitHub.cli"
    exit 1
}

gh auth status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Run: gh auth login"
    exit 1
}

git branch -M main
$remotes = git remote 2>$null
if ($remotes -notcontains "origin") {
    gh repo create $repoName --public --source=. --remote=origin --push
} else {
    git push -u origin main
}

Write-Host ""
Write-Host "Done. Next:"
Write-Host "1. Open https://share.streamlit.io"
Write-Host "2. New app -> select $repoName -> main file: app.py"
Write-Host "3. Add Secrets (GROQ_API_KEY, APP_USERNAME, APP_PASSWORD)"
Write-Host "   See .streamlit/secrets.toml.example"
