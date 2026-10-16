"""The boundary files: the validator's messages, and every script refusing a bad file with exit 2.

A script that reads an agent-written file used to fail wherever the bad value was first touched,
with a traceback, or not at all. usage: python3 -m unittest test_schema
"""
import json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import schema

DOC = {"compositions": [{"id": "c1", "name": "SEQ", "timeline": {
    "superTau": {"taus": [
        {"id": "t1", "text": {"string": "So that ClickUp, your project tool, could talk to Notion."},
         "audioSegment": {"offset": 0, "duration": 4.0}},
        {"id": "t2", "text": {"string": "And that is the whole argument in one sentence."},
         "audioSegment": {"offset": 4.0, "duration": 3.0}}]},
    "cards": {"components": []}}}],
    "mediaLibrary": {"mediaRefs": []}}


def write(d, name, value):
    p = os.path.join(d, name)
    json.dump(value, open(p, "w"))
    return p


def script(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=HERE)


class Messages(unittest.TestCase):
    def errs(self, value, name):
        return schema.message(name + ".json", schema.validate(value, schema.schema(name)))

    def test_a_wrong_type_names_the_path(self):
        pins = [{"from": "a b c", "media": "x.mp4"}] * 3 + [{"from": "d e f", "media": 3}]
        self.assertEqual(self.errs(pins, "pins"), "pins.json: [3].media must be a string")

    def test_a_misspelt_key_is_refused(self):
        self.assertIn("pins.json: [0].form is not allowed here",
                      self.errs([{"from": "a", "media": "x", "form": "b"}], "pins"))

    def test_a_pin_needs_media_or_a_zoom(self):
        self.assertEqual(self.errs([{"from": "a"}], "pins"), "pins.json: [0].media is required")

    def test_an_enum_lists_what_it_takes(self):
        self.assertEqual(self.errs([{"i": 1, "line": "x", "adds": "shape"}], "briefs"),
                         'briefs.json: [0].adds must be one of "quantity", "consequence", '
                         '"structure", "recognition"')

    def test_a_needle_of_the_wrong_kind_says_what_it_can_be(self):
        self.assertEqual(self.errs(["ok", 4], "needles"),
                         "needles.json: [1] must be a string or an array or an object")

    def test_the_root_has_no_path(self):
        self.assertEqual(self.errs({"from": "a"}, "pins"), "pins.json: must be an array")

    def test_every_real_shape_passes(self):
        self.assertEqual(schema.validate(json.load(open(os.path.join(HERE, "needles.example.json"))),
                                         schema.schema("needles")), [])
        self.assertEqual(schema.validate([[3, "a line", "structure"],
                                          {"i": 0, "line": "x", "adds": "quantity", "shows": "y"}],
                                         schema.schema("briefs")), [])

    def test_the_pass_list_is_ordered_by_id(self):
        passes = schema.passes()
        self.assertEqual([p["id"] for p in passes], list(range(len(passes))))


class Scripts(unittest.TestCase):
    """Each reader exits 2 with the named fault, never a traceback."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.doc = write(self.dir, "doc.json", DOC)

    def refused(self, out, fault):
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn(fault, out.stderr)
        self.assertNotIn("Traceback", out.stderr)

    def test_visuals_refuses_a_brief_with_a_bad_adds(self):
        briefs = write(self.dir, "briefs.json", [{"i": 0, "line": "ClickUp", "adds": "shape"}])
        self.refused(script("visuals.py", "check", self.doc, briefs), "briefs.json: [0].adds")

    def test_visuals_refuses_a_bad_plan(self):
        briefs = write(self.dir, "briefs.json", [{"i": 0, "line": "ClickUp", "adds": "structure"}])
        pins = write(self.dir, "pins.json", [{"from": "ClickUp", "zoom": "Cam 110"}])
        self.refused(script("visuals.py", "check", self.doc, briefs, "--plan", pins),
                     "pins.json: [0].zoom must be a number")

    def test_restate_refuses_a_needle_that_is_a_number(self):
        needles = write(self.dir, "needles.json", ["So that", 7])
        self.refused(script("restate.py", self.doc, "--check", needles), "needles.json: [1]")

    def test_candidates_refuses_a_needle_with_no_text(self):
        needles = write(self.dir, "needles.json", [{"b": 1}])
        self.refused(script("candidates.py", self.doc, "--check", needles), "needles.json: [0].t is required")

    def test_candidates_reads_the_pair_shape_restate_reads(self):
        needles = write(self.dir, "needles.json", [[0, "So that ClickUp"]])
        out = script("candidates.py", self.doc, "--check", needles)
        self.assertNotIn("Traceback", out.stderr)

    def test_prove_cuts_refuses_a_bad_needle(self):
        needles = write(self.dir, "needles.json", [{"from": ""}])
        self.refused(script("prove_cuts.py", self.doc, needles), "needles.json: [0].from must not be empty")

    def test_pins_resolve_refuses_before_reading_the_clipboard(self):
        pins = write(self.dir, "pins.json", [{"from": "x", "media": "a.mp4", "layut": "B Roll"}])
        self.refused(script("pins.py", "resolve", pins), "pins.json: [0].layut is not allowed here")

    def test_resolve_refuses_a_phrase_with_no_text(self):
        phrases = write(self.dir, "p.phrases.json", [{"txt": "one last thing"}])
        self.refused(script("resolve.py", phrases), "p.phrases.json: [0].text is required")

    def test_a_file_that_is_not_json_is_named(self):
        bad = os.path.join(self.dir, "needles.json")
        open(bad, "w").write("[\"a\",")
        self.refused(script("restate.py", self.doc, "--check", bad), "needles.json: not valid JSON")

    def test_sequence_plan_writes_a_file_the_schema_accepts(self):
        out = os.path.join(self.dir, "pins.json")
        run = script("sequence.py", "plan", self.doc, "--out", out)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(schema.validate(json.load(open(out)), schema.schema("pins")), [])


if __name__ == "__main__":
    unittest.main()
