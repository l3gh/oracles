import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from engine import Engine


class EngineTests(unittest.TestCase):
    def test_rejects_invalid_encounter_and_device_before_starting(self):
        engine = Engine()
        for encounter, device in [('bad', 0), ('templar', -1), ('atheon', '2')]:
            with self.assertRaises(ValueError):
                engine.start(encounter, device)
        self.assertIsNone(engine.process)

    def test_missing_detector_is_actionable_and_does_not_leave_process(self):
        with tempfile.TemporaryDirectory() as folder:
            engine = Engine(folder)
            with self.assertRaisesRegex(FileNotFoundError, 'detector is missing'):
                engine.start('templar', 0)
            engine.stop()
            self.assertIsNone(engine.process)

    def test_sequence_file_is_validated_and_missing_files_are_tolerated(self):
        with tempfile.TemporaryDirectory() as folder:
            engine = Engine()
            engine.folder = Path(folder)
            self.assertEqual(engine.sequence(), [])
            path = Path(folder) / 'sequence.txt'
            for raw, expected in [('1-2-7', ['1','2','7']), ('Start the encounter!', []),
                                  ('', []), ('1--2', []), ('8', []), ('12', [])]:
                path.write_text(raw)
                self.assertEqual(engine.sequence(), expected)
            engine.folder = None


if __name__ == '__main__':
    unittest.main()
