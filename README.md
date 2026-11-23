# BIT-PUZZLE-EXCALIBUR

*[Versão em português: LEIAME.md](LEIAME.md)*

A desktop GUI for building and running **volantes** (byte wheels) against the public
**Bitcoin puzzle challenge** — a visual front-end for the EXCALIBUR `exlottery` engine.

It is a **thin frontend**: it does not contain or fork the search engine. At launch it
locates the GUI and the `exlottery` binary and drives them. One engine, one GUI — no
copied code.

## What it does

- Build a wheel by clicking bytes on a 16×16 grid (first byte + shared bytes), with a live
  count, the legal range per puzzle, and import/export of byte lists.
- **Honest odds, live:** as you pick bytes it shows the **coverage** (= the real chance the
  key is in your wheel) and the **sweep time** — the numbers the scam "finders" hide.
- **Run from the GUI:** start the search, watch progress, rate and the verified result;
  **checkpoint/resume** survives a stop or a reboot.
- **History overlay (honest):** tint the grid by how often each byte appears in the public
  **solved** keys — it comes out as flat noise, a visual *proof* that no byte is hotter than
  another — and reveal any solved key's bytes on the grid. It is a proof, not a hint.

## Architecture

```
BIT-PUZZLE-EXCALIBUR  (this package: launcher + packaging + docs)
        │  locates at runtime
        ├── GUI    → EXCALIBUR-LOTTERY369/panel/app.py   (single source of the UI)
        └── engine → exlottery                            (separate project; the C++ core)
```

Nothing is copied: the GUI stays in its repo and the engine stays its own binary. This
keeps a single source for each and avoids a fork that would drift out of sync.

## Install & run

Requirements: Python 3.8+, Tk (`sudo apt install python3-tk`), and the `exlottery`
engine built from EXCALIBUR-LOTTERY369.

```bash
pip install -e .
bit-puzzle-excalibur
# or, without installing:
PYTHONPATH=src python -m bit_puzzle_excalibur
```

The launcher finds the engine and the GUI automatically. Override with environment
variables when they live elsewhere:

```bash
export EXLOTTERY_BIN=/path/to/exlottery          # the engine binary
export BITPUZZLE_PANEL=/path/to/LOTTERY369/panel # the GUI directory (holds app.py)
```

Build the engine if you don't have it yet:

```bash
cd ../EXCALIBUR-LOTTERY369
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j4
```

## Intended use

For the intentionally public Bitcoin puzzle challenge and for studying how an interval
search behaves — use it only on keys you own or on targets published to be solved. The
coverage readout exists so the bet is always honest about its (astronomically small) odds.
This is **not** a tool to recover someone else's wallet, and it cannot be: real keys are
full 256-bit uniform draws.

## License

[MIT](LICENSE) for this launcher. The engine and the GUI carry their own licenses.
