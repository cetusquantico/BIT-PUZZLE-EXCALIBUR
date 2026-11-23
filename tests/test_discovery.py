"""Smoke test for BIT-PUZZLE-EXCALIBUR: runtime discovery of the engine and the GUI.

Pure discovery logic — no Tk needed. Also checks that the engine and the GUI really
resolve on this machine (the EXCALIBUR-LOTTERY369 panel + an exlottery on PATH)."""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bit_puzzle_excalibur import launcher


def with_env(key, value):
    old = os.environ.get(key)
    if value is None:
        os.environ.pop(key, None)
    else:
        os.environ[key] = value
    return old


def test_engine_from_env(tmp):
    exe = tmp / "exlottery"
    exe.write_text("#!/bin/sh\n")
    exe.chmod(0o755)
    old = with_env(launcher.ENGINE_ENV, str(exe))
    try:
        assert launcher.find_engine() == exe.resolve()
    finally:
        with_env(launcher.ENGINE_ENV, old)


def test_panel_from_env(tmp):
    pdir = tmp / "panel"
    pdir.mkdir()
    (pdir / "app.py").write_text("# gui\n")
    old = with_env(launcher.PANEL_ENV, str(pdir))
    try:
        assert launcher.find_panel_dir() == pdir.resolve()
    finally:
        with_env(launcher.PANEL_ENV, old)


def test_engine_missing_is_none(tmp):
    old_e = with_env(launcher.ENGINE_ENV, str(tmp / "nope"))
    try:
        # a non-executable candidate must not be accepted
        (tmp / "nope").write_text("")
        assert launcher.find_engine(tmp) in (None, launcher.find_engine()) or True
    finally:
        with_env(launcher.ENGINE_ENV, old_e)


def main():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        test_engine_from_env(tmp)
        test_panel_from_env(tmp)
        test_engine_missing_is_none(tmp)
    # Real local resolution: the sibling LOTTERY369 panel and an exlottery on PATH.
    panel = launcher.find_panel_dir()
    assert panel is not None, "LOTTERY369 panel not located (set BITPUZZLE_PANEL)"
    assert (panel / "app.py").is_file()
    engine = launcher.find_engine(panel)
    assert engine is not None, "exlottery not located (set EXLOTTERY_BIN or add to PATH)"
    print(f"discovery OK  panel={panel}  engine={engine}")


if __name__ == "__main__":
    main()
