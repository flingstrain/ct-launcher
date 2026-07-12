# ct-launcher

**Index, search and open your local Cheat Engine table (`.CT`) collection** — a tiny, dependency-free CLI for people who keep a folder of cheat tables.

- 🔎 **Index & search** your `.CT` files by game name
- ▶️ **Open** a table with one command (launches Cheat Engine on Windows)
- 🗂️ **Export** a JSON index of your collection
- 🪶 **Zero dependencies** — pure Python 3 standard library
- 🔒 **No network, no telemetry** — everything stays local

> Looking for tables to fill your folder? Browse an organized, regularly-updated library at **[CheatTable.net](https://cheattable.net/)**.

## Install

No packages required — just Python 3.8+.

```bash
git clone https://github.com/<you>/ct-launcher.git
cd ct-launcher
python ct_launcher.py --help
```

## Usage

```bash
# scan a folder for .CT files and show a summary
python ct_launcher.py index  "C:\CheatTables"

# list everything, sorted
python ct_launcher.py list   "C:\CheatTables" --sort date

# find a table
python ct_launcher.py search "C:\CheatTables" "baldurs gate"

# open the best match (Windows: opens it in Cheat Engine)
python ct_launcher.py open   "C:\CheatTables" "elden ring"

# export the index to JSON
python ct_launcher.py export "C:\CheatTables" my-tables.json
```

## How it works

`ct-launcher` walks the folder you point it at, finds every `.CT` file, guesses the game
name from the filename, and records size + date. `open` hands the file to your OS, which
launches the associated app — [Cheat Engine](https://www.cheatengine.org/) if `.CT` is
associated with it (the default after installing Cheat Engine).

## Safety

Cheat Engine and tables edit **local** game memory for **single-player** games. Antivirus
software may report a **false positive** because memory-editing resembles malware behavior —
this is expected for the category. Only use tables you trust, back up your saves first, and
never use them in online/multiplayer modes.

## Contributing

Issues and PRs welcome — keep it dependency-free and single-player-focused.

## License

[MIT](LICENSE).
