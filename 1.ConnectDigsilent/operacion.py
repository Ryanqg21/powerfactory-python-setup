
print("========== FLUJO DE POTENCIA ==========")

# 1. Buscar el proyecto
usuario = app.GetCurrentUser()
proyectos = usuario.GetContents("*.IntPrj", 1)

proyecto = next(
    (p for p in proyectos if p.loc_name == "Nine-bus System"),
    None
)

if proyecto is None:
    raise RuntimeError("No se encontró el proyecto Nine-bus System.")

# 2. Activar el proyecto
resultado = app.ActivateProject(proyecto.loc_name)

if resultado != 0:
    raise RuntimeError(
        f"Error al activar el proyecto. Código: {resultado}"
    )

print("Proyecto activado:", proyecto.loc_name)

# 3. Obtener el comando de flujo de potencia
flujo = app.GetFromStudyCase("ComLdf")

if flujo is None:
    raise RuntimeError(
        "No se encontró el comando de flujo de potencia (ComLdf)."
    )

# 4. Ejecutar el flujo de potencia
resultado = flujo.Execute()

if resultado != 0:
    raise RuntimeError(
        f"Error al ejecutar el flujo de potencia. Código: {resultado}"
    )

barras = app.GetCalcRelevantObjects("*.ElmTerm")
print(f"Barras encontradas: {len(barras)}")

for barra in barras:
    try:
        tension = barra.GetAttribute("m:u")
        angulo = barra.GetAttribute("m:phiu")
        print(f"{barra.loc_name}: {tension:.4f} p.u. | {angulo:.4f} grados")
    except Exception as error:
        print(f"{barra.loc_name}: no se pudo leer ({error})")

print("Flujo de potencia ejecutado correctamente.")
print("========== FIN ==========")
