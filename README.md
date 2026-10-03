# ct-launcher

[![tests](https://github.com/flingstrain/ct-launcher/actions/workflows/ci.yml/badge.svg)](https://github.com/flingstrain/ct-launcher/actions/workflows/ci.yml)
[![python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Index, search and open your local **Cheat Engine table** (`.CT`) collection from the command
line. One file, standard library only — no pip install required, no network calls, no
telemetry.

If you keep a folder of tables, you have probably hit this: forty files named
`DS3_table_v1.2_final.ct`, no idea which game each one is for. `ct-launcher` reads the
filenames, works out the game names, and lets you search and open them.

## Install

Nothing to install — download the single file and run it:

```bash
curl -O https://raw.githubusercontent.com/flingstrain/ct-launcher/main/ct_launcher.py
python ct_launcher.py index ~/CheatTables
```

Or install it properly to get a `ct-launcher` command on your PATH:

```bash
pip install git+https://github.com/flingstrain/ct-launcher.git
ct-launcher index ~/CheatTables
```

Requires Python 3.9 or newer. Tested on Linux, Windows and macOS.

## Usage

```
ct_launcher.py index  [DIR]            scan DIR (default: .) and print what was found
ct_launcher.py list   [DIR] [--sort]   list every table; --sort name|date|size
ct_launcher.py search DIR QUERY        find tables by game or filename
ct_launcher.py open   DIR QUERY        open the best match (Windows hands it to Cheat Engine)
ct_launcher.py export DIR [OUT.json]   write the index to JSON
```

### Examples

Scan a collection:

```console
$ ct-launcher index ~/CheatTables
Indexed 2 cheat table(s) in /home/me/CheatTables
  Elden Ring                                   2.0 KB  2026-10-03  (Elden Ring.ct)
  Hades 2                                      1.0 KB  2026-10-03  (rpg/Hades_2_table_v0.9.ct)
```

Find one:

```console
$ ct-launcher search ~/CheatTables hades
Hades 2                                      rpg/Hades_2_table_v0.9.ct
```

Open it — on Windows this launches Cheat Engine with the table loaded:

```console
$ ct-launcher open ~/CheatTables hades
Opening: Hades 2  (/home/me/CheatTables/rpg/Hades_2_table_v0.9.ct)
```

Export the index for use elsewhere:

```console
$ ct-launcher export ~/CheatTables index.json
Wrote 2 table(s) to index.json
```

Each JSON entry looks like this:

```json
{
  "file": "rpg/Hades_2_table_v0.9.ct",
  "path": "/home/me/CheatTables/rpg/Hades_2_table_v0.9.ct",
  "game": "Hades 2",
  "size_kb": 1.0,
  "modified": "2026-10-03"
}
```

## How the game name is worked out

`guess_game()` normalises separators, then strips the noise table filenames collect:

| Filename | Detected game |
|---|---|
| `Dark Souls III Cheat Table v1.2.ct` | `Dark Souls III` |
| `Hades_2_table_v0.9.ct` | `Hades 2` |
| `cyberpunk-2077-cheat-table.ct` | `Cyberpunk 2077` |
| `Stardew Valley trainer by Rando.ct` | `Stardew Valley` |
| `NieR Automata v1.0.17.ct` | `NieR Automata` |
| `Portal 2.ct` | `Portal 2` |

Deliberate capitalisation is preserved: `III` does not become `Iii`, and `GTA` does not
become `Gta`. Bare sequel numbers are kept — `Portal 2` is not reduced to `Portal`.

It is a heuristic over filenames, so it will not be right for every name in the wild. If
you find a case it gets wrong, an issue with the filename is genuinely useful.

## Tests

```bash
python -m unittest discover -s tests -v
```

17 cases, standard library only. CI runs them on Python 3.9 / 3.11 / 3.13 across Linux,
Windows and macOS on every push.

## Scope

What this tool does **not** do: it does not download tables, it does not modify them, it
does not touch any game, and it makes no network requests. It reads filenames and opens
files with your system's default handler. The `.CT` files themselves remain whatever you
put in the folder.

Tables are for **single-player / offline** play. Using them in online or multiplayer modes
can get an account banned. Back up your saves before using cheats.

## Related

- [awesome-cheat-engine-tables](https://github.com/flingstrain/awesome-cheat-engine-tables) — where to find tables and tooling
- [awesome-game-trainers](https://github.com/flingstrain/awesome-game-trainers) — the trainer side of the same niche
- [Guides](https://flingstrain.github.io/) — how tables and trainers work, in plain English
- [Cheat Engine](https://www.cheatengine.org/) — the engine that actually runs these tables

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports with a real filename that parses badly
are the most useful contribution.

## Licence

[MIT](LICENSE).
