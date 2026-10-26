# PowerFactory 2024 + VS Code: Modular & Persistent Architecture

My guide to scaling and modularizing the automation of **DIgSILENT PowerFactory 2024** from **Visual Studio Code** with Python, using a persistent runner and a universal trigger. PowerFactory stays open in the background, while distinct engineering studies are organized into thematic subfolders and executed on demand from the root terminal without restarting the application.

**Reference setup:** PowerFactory 2024 · Python 3.12 · Windows · Example project "Nine-bus System"

## Project Structure

| Path / File | Purpose |
| ----------- | ------- |
| [`runner_powerfactory.py`](runner_powerfactory.py) | Persistent runner at the root: starts PowerFactory once and listens for run requests |
| [`ejecutar.ps1`](ejecutar.ps1) | Universal PowerShell trigger at the root: sends dynamic execution orders |
| [`1.ConnectDigsilent/`](1.ConnectDigsilent/) | Module containing connection guidelines, environment setup, and API documentation |
| [`2.Flujo_de_Potencia/calcular_flujo.py`](2.Flujo_de_Potencia/calcular_flujo.py) | Specific engineering study (e.g., load flow analysis) |
| `ejecutar.txt`, `estado.txt`, `resultado.txt` | Temporary communication files created at the root (ignored by git) |

## How it Works

The architecture separates the heavy connection engine from specific calculations:

1. **Terminal 1** runs `runner_powerfactory.py` from the root, starting PowerFactory with `GetApplicationExt()` to keep it alive.
2. I edit and save my engineering scripts inside their respective subfolders (e.g., load flows, short circuits).
3. **Terminal 2** runs `ejecutar.ps1` from the root, passing an optional path parameter to target any operation script dynamically.
4. The runner reads the order, executes the requested script using the shared `app` object via `exec()`, and writes the output to `resultado.txt`.
5. `ejecutar.ps1` waits for synchronization and prints the result directly in Terminal 2.

## Usage

**Terminal 1: Start the runner** (once per session, from the root folder):

```powershell
& ".\.venv\Scripts\python.exe" ".\runner_powerfactory.py"