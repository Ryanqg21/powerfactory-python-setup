# PowerFactory 2024 + VS Code: Persistent Runner & API Setup

My guide to automating **DIgSILENT PowerFactory 2024** from **Visual Studio Code** with Python, using a persistent runner. PowerFactory stays open, I edit an engineering script and run it on demand from a second terminal without relaunching PowerFactory on every test.

**Reference setup:** PowerFactory 2024 · Python 3.12 · Windows · example project "Nine-bus System"

## Files

| File | Purpose |
| ---- | ------- |
| [`runner_powerfactory.py`](runner_powerfactory.py) | Starts PowerFactory, shows its interface, and waits for run requests from the root |

While it works, the runner reads orders from `ejecutar.txt` and manages `estado.txt` and `resultado.txt` at the root folder level. They are temporary and not uploaded.

## How it works

The connection engine and the analysis are separated on purpose:

1. **Terminal 1** runs `runner_powerfactory.py` from the root project folder. It starts one PowerFactory instance with `GetApplicationExt()`, displays the GUI, and keeps the session alive.
2. I edit and save my operation script in its corresponding subfolder (e.g., `2.Flujo_de_Potencia/calcular_flujo.py`).
3. **Terminal 2** runs `ejecutar.ps1` from the root, writing a request file (`ejecutar.txt`) containing a unique ID (GUID) and the relative path of the script to execute.
4. The runner detects the request, reads the script path, compiles and executes the code with the shared `app` object using `exec()`, captures the output into `resultado.txt`, and marks the request as finished in `estado.txt`.
5. `ejecutar.ps1` waits for that specific ID and prints the output in Terminal 2.

The runner only starts PowerFactory. The project is activated inside each specific operation script, so I can change the project or the study without restarting the runner.

This setup does not attach to a PowerFactory session opened manually before. The instance it reuses is the one started by `runner_powerfactory.py`.

![Runner waiting for requests](images/runner-waiting.png)

## Requirements

- DIgSILENT PowerFactory 2024 installed
- Python 3.12 (it must match the `Python\3.12` folder of PowerFactory's API)
- VS Code with the Microsoft **Python** extension
- A project with a Study Case that contains the required command (e.g., `ComLdf` for load flow)

Reference path (adjust it if PowerFactory is installed elsewhere):

```
PowerFactory API:  C:\Program Files\DIgSILENT\PowerFactory 2024\Python\3.12
```

## Setup

> Run all commands from the root project folder (the one that contains `.venv`).

**1. Create the virtual environment** with Python 3.12 and open the folder in VS Code (**File → Open Folder**):

```powershell
py -3.12 -m venv .venv
& ".\.venv\Scripts\python.exe" --version
```

Expected: Python 3.12.x.

**2. Select the interpreter.** Press `Ctrl+Shift+P`, choose **Python: Select Interpreter**, pick the `.venv` of this project, and open a new terminal.

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

**Terminal 1: start the runner** (once per work session, executed from the root folder):

```powershell
& ".\.venv\Scripts\python.exe" ".\1.ConnectDigsilent\runner_powerfactory.py"
```

PowerFactory opens and the terminal shows "Esperando órdenes desde la raíz...". I keep this terminal open while I work, and I do not run the runner twice, since it would try to create another instance.

**Terminal 2: run the analysis** (every test from the root folder):

```powershell
.\ejecutar.ps1 -RutaOperacion "2.Flujo_de_Potencia\calcular_flujo.py"
```

The result appears in Terminal 2. When I finish, I stop the runner with `Ctrl+C` in Terminal 1.

![Load flow result](images/load-flow-result.png)

## Troubleshooting

| Problem | What to check |
| ------- | ------------- |
| `No module named 'powerfactory'` | VS Code uses the project's `.venv` and `powerfactory_api.pth` points to PowerFactory's `Python\3.12` folder |
| `GetApplicationExt()` returns `None` or fails | Another PowerFactory instance may be open. Close it and start the runner only once |
| Project or Study Case not found | Check the exact name, user permissions, and that the project exists in PowerFactory |
| Terminal 2 gets no result | Terminal 1 must show "Esperando órdenes...", the communication files must be generated at the root, and `.\ejecutar.ps1` must be run from the root folder |
| PowerShell blocks `ejecutar.ps1` | Read the exact message before changing execution policy |

## Notes

- Operation scripts must not call `GetApplicationExt()` again. They reuse the `app` variable provided by the runner.
- The runner uses `exec()`, which is fine on a local, controlled machine.
- Each run starts with a clean execution scope, maintaining only the active `app` instance.

---

Made by [@Ryanqg21](https://github.com/Ryanqg21). PowerFactory is a product of DIgSILENT and requires a valid license. This repository includes no PowerFactory files or projects.