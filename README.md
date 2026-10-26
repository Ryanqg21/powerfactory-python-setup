# PowerFactory 2024 + VS Code: Modular & Persistent Architecture

My guide to scaling and modularizing the automation of **DIgSILENT PowerFactory 2024** from **Visual Studio Code** with Python, using a persistent runner and a universal trigger. PowerFactory stays open, while distinct engineering studies are organized into subfolders and executed on demand from the root terminal without restarting the application.

**Reference setup:** PowerFactory 2024 · Python 3.12 · Windows · Example project "Nine-bus System"

## Project Structure

| Path / File | Purpose |
| ----------- | ------- |
| [`1.ConnectDigsilent/runner_powerfactory.py`](1.ConnectDigsilent/runner_powerfactory.py) | Starts PowerFactory once, shows its interface, and waits for run requests |
| [`2.Flujo_de_Potencia/calcular_flujo.py`](2.Flujo_de_Potencia/calcular_flujo.py) | Specific engineering study (e.g., load flow analysis) |
| [`ejecutar.ps1`](ejecutar.ps1) | Universal PowerShell trigger supporting dynamic path routing |
| `ejecutar.txt`, `estado.txt`, `resultado.txt` | Temporary communication files (ignored by git) |

## How it Works

The architecture separates the heavy connection engine from specific calculations:

1. **Terminal 1** runs `runner_powerfactory.py` from the root, starting PowerFactory with `GetApplicationExt()` to keep it alive.
2. I edit and save my engineering scripts inside their respective thematic subfolders (e.g., load flows, short circuits).
3. **Terminal 2** runs `ejecutar.ps1`, passing an optional path parameter to target any operation script dynamically.
4. The runner reads the order, executes the requested script using the shared `app` object via `exec()`, and writes the output to `resultado.txt`.
5. `ejecutar.ps1` waits for synchronization and prints the result directly in the terminal.

## Usage

**Terminal 1: Start the runner** (once per session, from the root folder):

```powershell
& ".\.venv\Scripts\python.exe" ".\1.ConnectDigsilent\runner_powerfactory.py"
```

**Terminal 2: Run an analysis** (every test). You can execute the default operation or target any subfolder dynamically:

- **Default operation:**
  ```powershell
  .\ejecutar.ps1
  ```

- **Specific subfolder operation:**
  ```powershell
  .\ejecutar.ps1 -RutaOperacion "2.Flujo_de_Potencia\calcular_flujo.py"
  ```

---

Made by [@Ryanqg21](https://github.com/Ryanqg21). PowerFactory is a product of DIgSILENT and requires a valid license. This repository includes no PowerFactory files or projects.