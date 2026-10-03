# Contributing

## The most useful bug report

`guess_game()` is a heuristic over filenames, so the failure mode that matters is a real
filename it parses badly. If you have one, open an issue with:

- the exact filename, copied verbatim
- what `ct-launcher` returned
- what the game actually is

That is enough to turn into a test case. You do not need to supply a fix.

Please do **not** attach the `.CT` file itself — the filename is all that is needed, and
many table authors ask that their files not be redistributed.

## Development

No dependencies, no build step:

```bash
git clone https://github.com/flingstrain/ct-launcher.git
cd ct-launcher
python -m unittest discover -s tests -v
```

Requires Python 3.9+.

## House rules for code

- **Standard library only.** The zero-dependency promise is the point of the tool; a pull
  request that adds a third-party package will be declined.
- **Add a test with behaviour changes.** Especially for `guess_game()` — add your case to
  `GuessGameTests` so it cannot regress.
- **Keep it one module.** `ct_launcher.py` is deliberately a single file people can
  download and run. Splitting it into a package is out of scope.
- **No network calls, no telemetry.** The tool reads local files; it should stay that way.
- Follow the existing style: type hints on public helpers, docstrings explaining *why*
  rather than restating the code.

## Pull request checklist

1. `python -m unittest discover -s tests` passes.
2. New or changed behaviour has a test.
3. `CHANGELOG.md` has an entry under *Unreleased* describing the change.
4. The CLI still works end to end — run `index`, `search` and `export` against a folder.

CI runs the suite on Python 3.9 / 3.11 / 3.13 across Linux, Windows and macOS, so platform
assumptions tend to surface there.

## Out of scope

- Downloading, hosting or redistributing cheat tables.
- Anything aimed at online or multiplayer cheating.
- A GUI. There are better tools for that; this one is for the terminal.

## Licence

Contributions are released under the [MIT licence](LICENSE).
