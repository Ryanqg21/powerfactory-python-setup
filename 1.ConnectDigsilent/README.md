# PowerFactory 2024 + VS Code: Persistent Runner

My guide to automating **DIgSILENT PowerFactory 2024** from **Visual Studio Code** with Python, using a persistent runner. PowerFactory stays open, I edit a script and run it on demand from a second terminal, without relaunching PowerFactory on every test. It ends with a load flow on the example project to confirm the connection works.

**Reference setup:** PowerFactory 2024 · Python 3.12 · Windows · example project "Nine-bus System"

## Files

| File | Purpose |
| ---- | ------- |
| [`runner_powerfactory.py`](runner_powerfactory.py) | Starts PowerFactory, shows its interface and waits for run requests |
| [`operacion.py`](operacion.py) | The analysis I edit: activates the project and runs a load flow |
| [`ejecutar.ps1`](ejecutar.ps1) | Sends a run request and prints the result in the second terminal |

While it works, the runner creates `ejecutar.txt`, `estado.txt` and `resultado.txt`. They are temporary and not uploaded.

## How it works

The runner and the analysis are separate on purpose:

1. **Terminal 1** runs `runner_powerfactory.py`. It starts one PowerFactory instance with `GetApplicationExt()` and keeps it alive.
2. I edit `operacion.py` and save it. Saving does not run anything.
3. **Terminal 2** runs `ejecutar.ps1`, which writes a request file with a unique ID (a GUID).
4. The runner sees the request, runs `operacion.py` with the shared `app` object, saves the output in `resultado.txt` and marks the request as finished.
5. `ejecutar.ps1` waits for that ID and prints the result.

The runner only starts PowerFactory. The project is activated inside `operacion.py`, so I can change the project or the study without restarting anything.

This setup does not attach to a PowerFactory session that I opened manually before. The instance it reuses is the one the runner starts.

<!-- PEGA AQUÍ: captura de PowerFactory abierto junto a la Terminal 1 mostrando "Esperando órdenes desde VS Code...". Guárdala en la carpeta images con el nombre runner-waiting.png (recorta la ruta de tu usuario) -->
![Runner waiting for requests](images/runner-waiting.png)

## Requirements

- DIgSILENT PowerFactory 2024 installed
- Python 3.12 (it must match the `Python\3.12` folder of PowerFactory's API)
- VS Code with the Microsoft **Python** extension
- A project with a Study Case that contains the load flow command (`ComLdf`). I use the "Nine-bus System" example

Reference path (adjust it if PowerFactory is installed elsewhere):

```
PowerFactory API:  C:\Program Files\DIgSILENT\PowerFactory 2024\Python\3.12
```

## Setup

> Run all commands from the project folder (the one that contains `.venv`).

**1. Create the virtual environment** with Python 3.12 and open the folder in VS Code (**File → Open Folder**):

```powershell
py -3.12 -m venv .venv
& ".\.venv\Scripts\python.exe" --version
```

Expected: Python 3.12.x.

**2. Select the interpreter.** Press `Ctrl+Shift+P`, choose **Python: Select Interpreter**, pick the `.venv` of this project and open a new terminal.

**3. Give the environment access to PowerFactory's API.** The API is `powerfactory.pyd`, inside PowerFactory's `Python\3.12` folder. I add a `.pth` file so the environment can find it:

```powershell
$api = "C:\Program Files\DIgSILENT\PowerFactory 2024\Python\3.12"
$sitePackages = & ".\.venv\Scripts\python.exe" -c "import sysconfig; print(sysconfig.get_path('purelib'))"
Set-Content -Path (Join-Path $sitePackages "powerfactory_api.pth") -Value $api
```

Check it:

```powershell
& ".\.venv\Scripts\python.exe" -c "import powerfactory; print(powerfactory.__file__)"
```

The output must be the path of `powerfactory.pyd`. This only adds a search path and does not modify PowerFactory.

## Usage

**Terminal 1: start the runner** (once per work session):

```powershell
& ".\.venv\Scripts\python.exe" ".\runner_powerfactory.py"
```

PowerFactory opens and the terminal shows "Esperando órdenes desde VS Code...". I keep this terminal open while I work, and I do not run the runner twice, since it would try to create another instance.

**Terminal 2: run the analysis** (every test). I open a new terminal in VS Code, edit and save `operacion.py`, then run:

```powershell
.\ejecutar.ps1
```

The result appears in this terminal. When I finish, I stop the runner with `Ctrl+C` in Terminal 1.

## What `operacion.py` does

[`operacion.py`](operacion.py) runs these steps and stops with a clear error message if one fails:

1. Looks for the "Nine-bus System" project among the user's projects.
2. Activates it with `ActivateProject`.
3. Gets the load flow command `ComLdf` from the active Study Case.
4. Executes it and checks that the return code is `0`.

`print()` output and errors are saved in `resultado.txt`. If my script fails, Terminal 2 shows the traceback and the runner keeps running.

<!-- PEGA AQUÍ: captura de la Terminal 2 con el resultado de .\ejecutar.ps1 (flujo de potencia ejecutado correctamente). Guárdala en la carpeta images con el nombre load-flow-result.png (recorta la ruta de tu usuario) -->
![Load flow result](images/load-flow-result.png)

A return code of `0` means the command ran. It does not guarantee that every result I want is available, so I check the state of the Study Case before reading values.

## Troubleshooting

| Problem | What to check |
| ------- | ------------- |
| `No module named 'powerfactory'` | VS Code uses the project's `.venv` and `powerfactory_api.pth` points to PowerFactory's `Python\3.12` folder |
| `GetApplicationExt()` returns `None` or fails | Another PowerFactory instance may be open. Close it and start the runner only once |
| Project "Nine-bus System" not found | Check the exact name, the user permissions and that the project exists in PowerFactory |
| `GetFromStudyCase('ComLdf')` returns `None` | There must be an active Study Case that contains the load flow command |
| Terminal 2 gets no result | Terminal 1 must still show "Esperando órdenes...", the files must be in the same folder and `.\ejecutar.ps1` must be run from the project folder |
| PowerShell blocks `ejecutar.ps1` | Read the exact message before changing any policy, and do not change the global policy unless needed |
| Old results appear | Check that Terminal 1 printed "Ejecución terminada" for that request |

## Notes

- `operacion.py` must not call `GetApplicationExt()` again. It reuses the `app` variable that the runner provides.
- The runner uses `exec()`, which is fine on a local, controlled machine. I do not run scripts I do not know, because they run with my user's permissions.
- Each run of `operacion.py` starts with new variables, except `app`.

---

Made by [@Ryanqg21](https://github.com/Ryanqg21). PowerFactory is a product of DIgSILENT and requires a valid license. This repository includes no PowerFactory files or projects.