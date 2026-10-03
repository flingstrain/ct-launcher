# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-10-03

### Fixed

- `guess_game()` mangled deliberate capitalisation: `NieR Automata` came back as
  `Nier Automata` and `Dark Souls III` as `Dark Souls Iii`. Title-casing now leaves any
  token that already carries an uppercase letter past the first character alone.
- Version suffixes glued to the name with underscores or dots survived the strip, so
  `Hades_2_table_v0.9.ct` produced `Hades 2 Table V0 9`. Separators are normalised before
  the version patterns run, and the result is `Hades 2`.

### Added

- Test suite (`tests/test_ct_launcher.py`, 17 cases, standard library `unittest` only)
  covering filename parsing, directory scanning, match ranking and JSON export.
- GitHub Actions CI running the suite on Python 3.9 / 3.11 / 3.13 across Linux, Windows
  and macOS, plus a CLI smoke test and a byte-compile check.
- `pyproject.toml` so the tool can be installed and exposes a `ct-launcher` entry point.

## [0.1.0] — 2026-07-11

### Added

- Initial release: `index`, `list`, `search`, `open` and `export` commands.
- Recursive `.CT` discovery with case-insensitive extension matching.
- Best-effort game-name extraction from table filenames.
- JSON export of the index.
- Zero third-party dependencies; standard library only.

[0.2.0]: https://github.com/flingstrain/ct-launcher/releases/tag/v0.2.0
[0.1.0]: https://github.com/flingstrain/ct-launcher/releases/tag/v0.1.0
