# PowerFactory 2024 + VS Code: Connection Setup & Environment Guide

My guide to configuring the Python 3.12 environment and linking the **DIgSILENT PowerFactory 2024** API with Visual Studio Code. This module documents the core setup required for the root runner (`runner_powerfactory.py`) to connect successfully with PowerFactory.

**Reference setup:** PowerFactory 2024 · Python 3.12 · Windows · example project "Nine-bus System"

## Requirements

- DIgSILENT PowerFactory 2024 installed
- Python 3.12 (it must match the `Python\3.12` folder of PowerFactory's API)
- VS Code with the Microsoft **Python** extension
- A project with a Study Case that contains the required command (e.g., `ComLdf` for load flow)

Reference path (adjust it if PowerFactory is installed elsewhere):

```text
PowerFactory API:  C:\Program Files\DIgSILENT\PowerFactory 2024\Python\3.12
```

## Setup Instructions

> Run all setup commands from the root project folder (where `.venv` resides).

**1. Create the virtual environment** with Python 3.12 and open the root folder in VS Code (**File → Open Folder**):

```powershell
py -3.12 -m venv .venv
& ".\.venv\Scripts\python.exe" --version
```

Expected output: `Python 3.12.x`.

**2. Select the interpreter.** Press `Ctrl+Shift+P`, choose **Python: Select Interpreter**, pick the `.venv` of this project, and open a new terminal.

**3. Give the environment access to PowerFactory's API.** The API file is `powerfactory.pyd`, located inside PowerFactory's `Python\3.12` folder. Add a `.pth` file so `.venv` can locate it:

```powershell
$api = "C:\Program Files\DIgSILENT\PowerFactory 2024\Python\3.12"
$sitePackages = & ".\.venv\Scripts\python.exe" -c "import sysconfig; print(sysconfig.get_path('purelib'))"
Set-Content -Path (Join-Path $sitePackages "powerfactory_api.pth") -Value $api
```

**4. Verify the API link:**

```powershell
& ".\.venv\Scripts\python.exe" -c "import powerfactory; print(powerfactory.__file__)"
```

The output must show the full path to `powerfactory.pyd`.

## Troubleshooting

| Problem | What to check |
| ------- | ------------- |
| `No module named 'powerfactory'` | Ensure VS Code uses the project's `.venv` and `powerfactory_api.pth` points to PowerFactory's `Python\3.12` folder |
| `GetApplicationExt()` returns `None` or fails | Another PowerFactory instance may be open. Close it and start `runner_powerfactory.py` from the root |
| Project or Study Case not found | Check exact project name, user permissions, and ensure the project is imported into PowerFactory |
| PowerShell blocks `ejecutar.ps1` | Check execution policies before running PowerShell scripts from VS Code |

---

Made by [@Ryanqg21](https://github.com/Ryanqg21). PowerFactory is a product of DIgSILENT and requires a valid license. This repository includes no PowerFactory files or projects.