# PowerShell script to build the Python project

Write-Host "Cleaning old build artifacts..." -ForegroundColor Cyan
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "*.egg-info") { Remove-Item -Recurse -Force "*.egg-info" }

Write-Host "Building project (sdist and bdist_wheel)..." -ForegroundColor Cyan
python setup.py sdist bdist_wheel

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful! Artifacts are in the 'dist' folder." -ForegroundColor Green
} else {
    Write-Host "Build failed." -ForegroundColor Red
}
