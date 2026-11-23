"""BIT-PUZZLE-EXCALIBUR — a GUI frontend that DRIVES the exlottery engine.

This package does not fork either the C++ engine or the GUI. At runtime it locates:
  * the GUI (the EXCALIBUR-LOTTERY369 panel, `app.py`) — the single source of the UI;
  * the `exlottery` engine binary — a separate project.
and launches the panel pointed at that engine. See README for configuration.
"""
import os
import shutil
import sys
from pathlib import Path

__all__ = ["find_panel_dir", "find_engine", "main"]

PANEL_ENV = "BITPUZZLE_PANEL"      # directory that holds the panel's app.py
ENGINE_ENV = "EXLOTTERY_BIN"       # path to the exlottery executable


def _panel_candidates():
    here = Path(__file__).resolve()
    seen = []
    if os.environ.get(PANEL_ENV):
        seen.append(Path(os.environ[PANEL_ENV]))
    seen.append(here.parent / "panel")                      # bundled copy, if ever vendored
    bases = [here.parents[3] if len(here.parents) > 3 else here.parent,
             Path.home(), Path("/root")]
    for base in bases:
        seen.append(base / "EXCALIBUR-LOTTERY369" / "panel")
    return seen


def find_panel_dir():
    """Directory of the GUI (`app.py`), or None if it can't be located."""
    for cand in _panel_candidates():
        try:
            if cand and (cand / "app.py").is_file():
                return cand.resolve()
        except OSError:
            continue
    return None


def _engine_candidates(panel_dir):
    if os.environ.get(ENGINE_ENV):
        yield Path(os.environ[ENGINE_ENV])
    found = shutil.which("exlottery")
    if found:
        yield Path(found)
    if panel_dir is not None:
        root = panel_dir.parent
        for rel in ("build-opt/exlottery", "build/exlottery", "exlottery", "bin/exlottery"):
            yield root / rel


def find_engine(panel_dir=None):
    """Path to an executable `exlottery`, or None if not found."""
    for cand in _engine_candidates(panel_dir):
        try:
            if cand and cand.is_file() and os.access(cand, os.X_OK):
                return cand.resolve()
        except OSError:
            continue
    return None


def main(argv=None):
    panel_dir = find_panel_dir()
    if panel_dir is None:
        sys.exit(f"GUI não encontrada. Defina {PANEL_ENV}=<dir do painel do EXCALIBUR-LOTTERY369>.")
    sys.path.insert(0, str(panel_dir))
    import app                                   # the LOTTERY369 panel — single GUI source
    if app.tk is None:
        sys.exit("Requer Tk para Python 3 (no Kali: sudo apt install python3-tk).")
    engine = find_engine(panel_dir)
    if engine is None:
        sys.exit(f"Motor 'exlottery' não encontrado. Defina {ENGINE_ENV}=<caminho> ou ponha-o no PATH.\n"
                 "Compile-o no EXCALIBUR-LOTTERY369: cmake -S . -B build && cmake --build build -j4.")
    try:
        root = app.tk.Tk()
        root.title("BIT-PUZZLE-EXCALIBUR")
        app.Panel(root, engine, app.config_path())
    except (ValueError, OSError, app.tk.TclError) as exc:
        sys.exit(f"Não foi possível abrir a interface. {exc}")
    root.mainloop()


if __name__ == "__main__":
    main()
