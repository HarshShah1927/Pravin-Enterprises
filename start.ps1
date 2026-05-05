# Start the Pravin Enterprises Django app with automatic setup checks.
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot
$venvPython = Join-Path $projectRoot 'venv\Scripts\python.exe'

if (-Not (Test-Path $venvPython)) {
    Write-Host 'Creating virtual environment...' -ForegroundColor Cyan
    python -m venv venv
}

$python = $venvPython

$process = Start-Process -FilePath $python -ArgumentList '-c', "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('django') else 1)" -NoNewWindow -Wait -PassThru
if ($process.ExitCode -ne 0) {
    Write-Host 'Installing dependencies from requirements.txt...' -ForegroundColor Cyan
    & $python -m pip install -r requirements.txt
}

if (-Not (Test-Path (Join-Path $projectRoot '.env'))) {
    Write-Host 'Copying .env.example to .env...' -ForegroundColor Cyan
    Copy-Item -Path (Join-Path $projectRoot '.env.example') -Destination (Join-Path $projectRoot '.env')
    Write-Host 'Please edit .env with your Twilio/Email credentials before use.' -ForegroundColor Yellow
}

Write-Host 'Applying database migrations...' -ForegroundColor Cyan
& $python manage.py migrate

Write-Host 'Starting Django development server...' -ForegroundColor Cyan
& $python manage.py runserver
