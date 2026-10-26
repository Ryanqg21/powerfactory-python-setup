
import powerfactory
import time
import contextlib
import io
import traceback
from pathlib import Path

carpeta = Path(__file__).parent
archivo_operacion = carpeta / "operacion.py"
archivo_solicitud = carpeta / "ejecutar.txt"
archivo_salida = carpeta / "resultado.txt"
archivo_estado = carpeta / "estado.txt"

print("Iniciando PowerFactory 2024...")

app = powerfactory.GetApplicationExt()

if app is None:
    raise RuntimeError("No se pudo iniciar PowerFactory.")

# Mostrar la interfaz gráfica de PowerFactory.
app.Show()

print("PowerFactory iniciado correctamente.")
print("No se ha activado ningún proyecto automáticamente.")

# Evitar ejecutar órdenes antiguas.
if archivo_solicitud.exists():
    archivo_solicitud.unlink()

print("\nEsperando órdenes desde VS Code...")
print("Detén el ejecutor con Ctrl+C.")

try:
    while True:
        if archivo_solicitud.exists():
            try:
                solicitud = archivo_solicitud.read_text(
                    encoding="utf-8"
                ).strip()

                if solicitud:
                    # Consumir la orden antes de ejecutar.
                    archivo_solicitud.unlink()

                    print("\nEjecutando operacion.py...")

                    salida = io.StringIO()
                    errores = ""

                    try:
                        codigo_fuente = archivo_operacion.read_text(
                            encoding="utf-8"
                        )

                        codigo = compile(
                            codigo_fuente,
                            str(archivo_operacion),
                            "exec"
                        )

                        entorno = {
                            "__name__": "__main__",
                            "__file__": str(archivo_operacion),
                            "app": app
                        }

                        with contextlib.redirect_stdout(salida):
                            exec(codigo, entorno)

                    except Exception:
                        errores = traceback.format_exc()

                    archivo_salida.write_text(
                        salida.getvalue()
                        + ("\n" + errores if errores else ""),
                        encoding="utf-8"
                    )

                    archivo_estado.write_text(
                        solicitud,
                        encoding="utf-8"
                    )

                    print("Ejecución terminada.")

            except FileNotFoundError:
                pass

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nEjecutor detenido.")
