# Professional HTMLTestRunner-rv Release Script
# Usage: .\publish.ps1

$ErrorActionPreference = "Stop"

function Show-Step($Message) {
    Write-Host "`n>> $Message" -ForegroundColor Cyan
}

function Confirm-Action($Question) {
    $choice = Read-Host "$Question (y/n)"
    return $choice.ToLower() -eq 'y'
}

Write-Host "--- HTMLTestRunner-rv Project Manager ---" -ForegroundColor Green

# 1. Environment Setup
if (Confirm-Action "Update all build & doc dependencies?") {
    Show-Step "Installing/Updating tools..."
    python -m pip install --upgrade pip build twine mkdocs mkdocstrings[python] --quiet
    python -m pip install -r requirements.txt --quiet
}

# 2. Build Distribution
if (Confirm-Action "Build project (sdist/wheel)?") {
    Show-Step "Cleaning old builds..."
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    
    Show-Step "Creating new build artifacts..."
    python -m build
    
    Show-Step "Verifying artifacts with twine..."
    python -m twine check dist/*
}

# 3. Deploy Documentation
if (Confirm-Action "Deploy documentation to GitHub Pages?") {
    Show-Step "Building and deploying docs..."
    mkdocs gh-deploy --force
}

# 4. Upload to PyPI
if (Confirm-Action "Publish to PyPI?") {
    Show-Step "Uploading to PyPI (requires API Token)..."
    python -m twine upload dist/*
}

Write-Host "`nDone! Your project is up to date." -ForegroundColor Green
