"""The run ledger: its route field, its gates, its evidence rule and its schema.

Moved here from `.claude/skills/descript-projects/scripts/`, where it sat beside a run.py that had
left, so every case failed on a missing file. usage: python3 -m unittest test_run
"""
import json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, "run.py")
sys.path.insert(0, HERE)
import schema


def call(*args):
    return subprocess.run([sys.executable, RUN, *args], capture_output=True, text=True)


class Route(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def ledger(self):
        return json.load(open(os.path.join(self.dir, "RUN.json")))

    def test_init_defaults_to_descript(self):
        call("init", self.dir, "--code", "EC51")
        self.assertEqual(self.ledger()["route"], "descript")

    def test_init_takes_a_local_route_and_a_cut(self):
        call("init", self.dir, "--code", "EC51", "--route", "local", "--cut", "/tmp/x/cut.json")
        run = self.ledger()
        self.assertEqual(run["route"], "local")
        self.assertEqual(run["cut"], "/tmp/x/cut.json")

    def test_init_refuses_an_unknown_route(self):
        out = call("init", self.dir, "--route", "sideways")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("route must be", out.stderr + out.stdout)

    def test_a_ledger_without_a_route_still_loads(self):
        call("init", self.dir, "--code", "EC51")
        run = self.ledger()
        del run["route"]
        json.dump(run, open(os.path.join(self.dir, "RUN.json"), "w"))
        out = call("show", self.dir)
        self.assertEqual(out.returncode, 0)
        self.assertEqual(self.ledger()["route"], "descript")

    def test_the_local_table_names_the_cut_not_a_composition(self):
        call("init", self.dir, "--route", "local", "--cut", "/tmp/x/cut.json")
        md = open(os.path.join(self.dir, "RUN.md")).read()
        self.assertIn("/tmp/x/cut.json", md)
        self.assertNotIn("composition", md)

    def test_start_still_refuses_out_of_order(self):
        call("init", self.dir, "--route", "local", "--cut", "/tmp/x/cut.json")
        out = call("start", self.dir, "3")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("is not done", out.stderr + out.stdout)

    def test_done_still_refuses_evidence_naming_no_command(self):
        call("init", self.dir, "--route", "local", "--cut", "/tmp/x/cut.json")
        call("start", self.dir, "0")
        out = call("done", self.dir, "0", "--evidence", "looks fine to me")
        self.assertNotEqual(out.returncode, 0)


class Evidence(unittest.TestCase):
    """Bug (e): `done` matched a command's last word as a substring, so "shortcut" proved `cut`."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        call("init", self.dir, "--code", "EC51")
        call("start", self.dir, "0")
        self.proof = os.path.join(self.dir, "tracks.txt")
        open(self.proof, "w").write("CAM muted\nMIC live\ngates: clean\n")

    def ledger(self):
        return json.load(open(os.path.join(self.dir, "RUN.json")))

    def test_a_word_that_only_contains_a_command_is_not_evidence(self):
        call("done", self.dir, "0", "--evidence", "descript tracks clean", "--file", self.proof)
        call("start", self.dir, "1")
        out = call("done", self.dir, "1", "--evidence", "the shortcut looks fine", "--file", self.proof)
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertNotEqual(self.ledger()["passes"][1]["state"], "done")

    def test_naming_a_command_without_anything_checkable_is_refused(self):
        out = call("done", self.dir, "0", "--evidence", "descript tracks read clean")
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn("--file", out.stderr)
        self.assertNotEqual(self.ledger()["passes"][0]["state"], "done")

    def test_a_file_that_does_not_exist_is_refused(self):
        out = call("done", self.dir, "0", "--evidence", "descript tracks clean",
                   "--file", os.path.join(self.dir, "nope.txt"))
        self.assertEqual(out.returncode, 2)
        self.assertIn("nope.txt", out.stderr)

    def test_a_saved_output_is_recorded_with_its_hash(self):
        out = call("done", self.dir, "0", "--evidence", "descript tracks clean", "--file", self.proof)
        self.assertEqual(out.returncode, 0, out.stderr)
        p = self.ledger()["passes"][0]
        self.assertEqual(p["state"], "done")
        self.assertEqual(p["proof"]["file"], self.proof)
        self.assertEqual(p["proof"]["sha256"], schema.sha256(self.proof))

    def test_a_run_command_is_executed_and_its_output_kept(self):
        out = call("done", self.dir, "0", "--evidence", "descript tracks clean",
                   "--run", "echo descript tracks: gates clean")
        self.assertEqual(out.returncode, 0, out.stderr)
        p = self.ledger()["passes"][0]
        self.assertEqual(p["proof"]["run"], "echo descript tracks: gates clean")
        self.assertIn("gates clean", open(p["proof"]["file"]).read())

    def test_a_run_command_that_fails_is_not_evidence(self):
        out = call("done", self.dir, "0", "--evidence", "descript tracks clean",
                   "--run", "descript tracks; exit 3")
        self.assertEqual(out.returncode, 2)
        self.assertNotEqual(self.ledger()["passes"][0]["state"], "done")


class Ledger(unittest.TestCase):
    """RUN.json is validated at read and write, and the pass list is passes.json."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "RUN.json")

    def test_a_bad_ledger_exits_2_naming_the_path(self):
        call("init", self.dir, "--code", "EC51")
        run = json.load(open(self.path))
        run["passes"][2]["state"] = "finished"
        json.dump(run, open(self.path, "w"))
        out = call("show", self.dir)
        self.assertEqual(out.returncode, 2)
        self.assertIn('RUN.json: passes[2].state must be one of "", "started", "done", "blocked"',
                      out.stderr)
        self.assertNotIn("Traceback", out.stderr)

    def test_the_passes_are_the_ones_in_passes_json(self):
        call("init", self.dir, "--code", "EC51")
        want = [p["key"] for p in schema.passes()]
        self.assertEqual(len(json.load(open(self.path))["passes"]), len(want))
        md = open(os.path.join(self.dir, "RUN.md")).read()
        for key in want:
            self.assertIn("| %s -" % key, md)

    def test_an_older_ledger_with_fewer_passes_reaches_the_last_one(self):
        call("init", self.dir, "--code", "EC51")
        run = json.load(open(self.path))
        run["passes"] = run["passes"][:8]
        json.dump(run, open(self.path, "w"))
        last = len(schema.passes()) - 1
        out = call("block", self.dir, str(last), "--why", "not yet")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(json.load(open(self.path))["passes"][last]["state"], "blocked")


if __name__ == "__main__":
    unittest.main()
