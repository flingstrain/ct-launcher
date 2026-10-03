"""Tests for ct-launcher.

Standard library only (unittest), matching the project's zero-dependency promise.

Run from the repository root:

    python -m unittest discover -s tests -v
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import ct_launcher as ctl  # noqa: E402


class GuessGameTests(unittest.TestCase):
    """Filename -> game name. These are the cases real collections actually produce."""

    def test_strips_cheat_table_and_version(self):
        self.assertEqual(ctl.guess_game("Dark Souls III Cheat Table v1.2.ct"), "Dark Souls III")

    def test_plain_name_untouched(self):
        self.assertEqual(ctl.guess_game("Elden Ring.CT"), "Elden Ring")

    def test_version_glued_with_underscores(self):
        # separators are normalised before the version strip, so v0.9 is still removed
        self.assertEqual(ctl.guess_game("Hades_2_table_v0.9.ct"), "Hades 2")

    def test_strips_author_credit(self):
        self.assertEqual(ctl.guess_game("Stardew Valley trainer by Rando.ct"), "Stardew Valley")

    def test_keeps_bare_sequel_number(self):
        self.assertEqual(ctl.guess_game("Portal 2.ct"), "Portal 2")

    def test_dashes_become_spaces(self):
        self.assertEqual(ctl.guess_game("cyberpunk-2077-cheat-table.ct"), "Cyberpunk 2077")

    def test_preserves_deliberate_capitalisation(self):
        # str.title() would mangle these into "Nier" and "Gta"
        self.assertEqual(ctl.guess_game("NieR Automata v1.0.17.ct"), "NieR Automata")
        self.assertEqual(ctl.guess_game("GTA V.ct"), "GTA V")

    def test_falls_back_to_stem_when_everything_is_stripped(self):
        # "table" alone would reduce to an empty string; the stem is returned instead
        self.assertEqual(ctl.guess_game("table.ct"), "table")


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, rel, content=b"x" * 2048):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
        return p

    def test_finds_ct_files_recursively(self):
        self._write("Elden Ring.ct")
        self._write("rpg/Hades 2.ct")
        tables = ctl.scan(self.root)
        self.assertEqual(len(tables), 2)
        self.assertEqual({t["game"] for t in tables}, {"Elden Ring", "Hades 2"})

    def test_extension_match_is_case_insensitive(self):
        self._write("Portal 2.CT")
        self.assertEqual(len(ctl.scan(self.root)), 1)

    def test_ignores_other_files(self):
        self._write("readme.txt")
        self._write("trainer.exe")
        self.assertEqual(ctl.scan(self.root), [])

    def test_entry_fields(self):
        self._write("Elden Ring.ct", b"y" * 1024)
        t = ctl.scan(self.root)[0]
        self.assertEqual(set(t), {"file", "path", "game", "size_kb", "modified"})
        self.assertEqual(t["size_kb"], 1.0)
        self.assertTrue(Path(t["path"]).is_absolute())
        self.assertEqual(t["file"], "Elden Ring.ct")
        self.assertRegex(t["modified"], r"^\d{4}-\d{2}-\d{2}$")

    def test_empty_directory(self):
        self.assertEqual(ctl.scan(self.root), [])


class MatchTests(unittest.TestCase):
    TABLES = [
        {"game": "Elden Ring", "file": "elden_ring.ct"},
        {"game": "Portal 2", "file": "portal2.ct"},
        {"game": "Hades", "file": "hades_elden_note.ct"},
    ]

    def test_game_name_match_ranks_above_filename_match(self):
        hits = ctl._match(self.TABLES, "elden")
        self.assertEqual([h["game"] for h in hits], ["Elden Ring", "Hades"])

    def test_no_match_returns_empty(self):
        self.assertEqual(ctl._match(self.TABLES, "zzz"), [])

    def test_match_is_case_insensitive(self):
        self.assertEqual(ctl._match(self.TABLES, "PORTAL")[0]["game"], "Portal 2")


class ExportTests(unittest.TestCase):
    def test_export_writes_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Elden Ring.ct").write_bytes(b"z" * 512)
            out = root / "index.json"
            # bound outside the class body: a class body is not a closure scope
            dir_arg, out_arg = str(root), str(out)

            class Args:
                dir = dir_arg
                out = out_arg

            ctl.cmd_export(Args())
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["game"], "Elden Ring")


if __name__ == "__main__":
    unittest.main(verbosity=2)
