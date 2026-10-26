import powerfactory
import time
import contextlib
import io
import traceback
from pathlib import Path

# Definir la raíz del proyecto (subiendo un nivel desde 1.ConnectDigsilent)
raiz_proyecto = Path(__file__).resolve().parent

# Los archivos de comunicación ahora están centralizados en la RAÍZ
archivo_solicitud = raiz_proyecto / "ejecutar.txt"
archivo_salida = raiz_proyecto / "resultado.txt"
archivo_estado = raiz_proyecto / "estado.txt"

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

print("\nEsperando órdenes desde la raíz...")
print("Detén el ejecutor con Ctrl+C.")

try:
    while True:
        if archivo_solicitud.exists():
            try:
                # Leer el contenido en líneas: Línea 1 = GUID, Línea 2 = Ruta del script
                contenido = archivo_solicitud.read_text(encoding="utf-8").splitlines()
                
                if len(contenido) >= 2:
                    solicitud = contenido[0].strip()
                    ruta_relativa_script = contenido[1].strip()
                elif len(contenido) == 1:
                    # Compatibilidad por si solo manda el GUID (asume operacion.py por defecto)
                    solicitud = contenido[0].strip()
                    ruta_relativa_script = "operacion.py"
                else:
                    solicitud = ""
                    ruta_relativa_script = ""

                if solicitud:
                    # Consumir la orden antes de ejecutar.
                    archivo_solicitud.unlink()

                    # Construir la ruta completa del script a ejecutar
                    archivo_operacion = raiz_proyecto / ruta_relativa_script
                    print(f"\nEjecutando {ruta_relativa_script}...")

                    salida = io.StringIO()
                    errores = ""

                    try:
                        if not archivo_operacion.exists():
                            raise FileNotFoundError(f"No se encontró el archivo: {archivo_operacion}")

                        codigo_fuente = archivo_operacion.read_text(encoding="utf-8")

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

            except Exception as e:
                print(f"Error procesando la orden: {e}")

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nEjecutor detenido.")