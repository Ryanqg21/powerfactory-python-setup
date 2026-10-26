
$solicitud = [guid]::NewGuid().ToString()
$estado = Join-Path $PSScriptRoot "estado.txt"
$salida = Join-Path $PSScriptRoot "resultado.txt"
$orden = Join-Path $PSScriptRoot "ejecutar.txt"

Set-Content -Path $orden -Value $solicitud

while (!(Test-Path $estado) -or
       (Get-Content $estado -Raw).Trim() -ne $solicitud) {
    Start-Sleep -Milliseconds 200
}

Write-Host "`n===== RESULTADOS DE operacion.py ====="
Get-Content $salida
Write-Host "===== FIN ====="
