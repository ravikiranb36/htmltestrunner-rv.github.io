# PowerShell script to build and deploy documentation to GitHub Pages

Write-Host "Checking for mkdocs installation..." -ForegroundColor Cyan
if (-not (Get-Command "mkdocs" -ErrorAction SilentlyContinue)) {
    Write-Host "mkdocs is not installed. Installing mkdocs..." -ForegroundColor Yellow
    pip install mkdocs mkdocs-material
}

Write-Host "Building documentation..." -ForegroundColor Cyan
mkdocs build

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful! Documentation is in the 'site' folder." -ForegroundColor Green
    
    $confirm = Read-Host "Do you want to deploy documentation to GitHub Pages? (y/n)"
    if ($confirm -eq 'y') {
        Write-Host "Deploying to GitHub Pages..." -ForegroundColor Cyan
        mkdocs gh-deploy --force
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Deployment successful!" -ForegroundColor Green
        } else {
            Write-Host "Deployment failed." -ForegroundColor Red
        }
    } else {
        Write-Host "Deployment skipped." -ForegroundColor Yellow
    }
} else {
    Write-Host "Documentation build failed." -ForegroundColor Red
}
