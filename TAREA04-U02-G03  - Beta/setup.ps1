# Script de Instalacion - Sistema de Firma Digital
# Grupo 3 - Criptografia

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Sistema de Firma Digital - Instalacion" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python no encontrado" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Crear entorno virtual
Write-Host "2. Creando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Remove-Item -Recurse -Force venv
}
python -m venv venv
Write-Host "Entorno virtual creado" -ForegroundColor Green
Write-Host ""

# Instalar dependencias
Write-Host "3. Instalando dependencias..." -ForegroundColor Yellow
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\pip.exe install -r requirements.txt
Write-Host ""

# Completado
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Instalacion completada!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para usar el sistema:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  cd src" -ForegroundColor White
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
