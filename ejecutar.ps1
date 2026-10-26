param(
    [string]$RutaOperacion = "operacion.py" # Si no le dices nada, usa operacion.py por defecto
)

$solicitud = [guid]::NewGuid().ToString()
$estado = Join-Path $PSScriptRoot "estado.txt"
$salida = Join-Path $PSScriptRoot "resultado.txt"
$orden = Join-Path $PSScriptRoot "ejecutar.txt"

# Guardamos el GUID en la línea 1 y la ruta del archivo en la línea 2
$contenidoOrden = "$solicitud`n$RutaOperacion"
Set-Content -Path $orden -Value $contenidoOrden

while (!(Test-Path $estado) -or
       (Get-Content -Path $estado -TotalCount 1).Trim() -ne $solicitud) {
    Start-Sleep -Milliseconds 200
}

Write-Host "`n===== RESULTADOS DE $RutaOperacion ====="
Get-Content $salida
Write-Host "===== FIN ====="