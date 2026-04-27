# Script para gerar atividade e testar o sistema
# Executar em PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TESTE DO SISTEMA - GRAFANA ATIVO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar conexoes
Write-Host "1. Verificando servicos..." -ForegroundColor Yellow
$services = @{
    "Flask App" = "http://localhost:8080"
    "Prometheus" = "http://localhost:9090"
    "Grafana" = "http://localhost:3000"
    "Kibana" = "http://localhost:5601"
}

foreach ($service in $services.GetEnumerator()) {
    try {
        $response = Invoke-WebRequest -Uri $service.Value -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        Write-Host "   OK - $($service.Name)" -ForegroundColor Green
    } catch {
        Write-Host "   ERRO - $($service.Name)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "2. Gerando requisicoes de teste..." -ForegroundColor Yellow

# Gerar requisicoes de sucesso
for ($i = 0; $i -lt 15; $i++) {
    Write-Host "   Requisicao $($i+1)/15..." -ForegroundColor Gray
    try {
        curl http://localhost:8080/ -UseBasicParsing -ErrorAction SilentlyContinue | Out-Null
        curl http://localhost:8080/health -UseBasicParsing -ErrorAction SilentlyContinue | Out-Null
    } catch { }
    Start-Sleep -Milliseconds 500
}

Write-Host ""
Write-Host "3. Simulando erros..." -ForegroundColor Yellow

# Simular alguns erros
for ($i = 0; $i -lt 3; $i++) {
    Write-Host "   Erro $($i+1)/3..." -ForegroundColor Red
    try {
        curl http://localhost:8080/error -UseBasicParsing -ErrorAction SilentlyContinue | Out-Null
    } catch { }
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  TESTE CONCLUIDO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Acesse os dashboards:" -ForegroundColor Cyan
Write-Host "  - Grafana:    http://localhost:3000" -ForegroundColor Yellow
Write-Host "  - Prometheus: http://localhost:9090" -ForegroundColor Yellow
Write-Host "  - Kibana:     http://localhost:5601" -ForegroundColor Yellow
Write-Host "  - App:        http://localhost:8080" -ForegroundColor Yellow
Write-Host ""
