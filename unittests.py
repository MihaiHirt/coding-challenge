import unittest
import tempfile
import os
from task import parse_log_file

class TestLogParser(unittest.TestCase):

    # create a temporary file in order to write the options of testing
    def create_temp_log(self, content):
        tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        tmp.write(content)
        tmp.close()
        return tmp.name

    # test 1 - verify the duration
    def test_ok_duration(self):
        log = (
            "12:00:00,scheduled task.py TaskA, START,123\n"
            "12:04:00,scheduled task.py TaskA, END,123\n"
        )
        filename = self.create_temp_log(log)
        results = parse_log_file(filename)
        # os.remove(filename)
        self.assertEqual(results, [])

    # test 2- verify the WARNING status for a job
    def test_warning_duration(self):
        log = (
            "12:00:00,background job JobX, START,456\n"
            "12:06:00,background job JobX, END,456\n"
        )
        filename = self.create_temp_log(log)
        results = parse_log_file(filename)
        # os.remove(filename)
        self.assertEqual(results[0]["status"], "WARNING")

    # test 3 - verify the ERROR status for a job
    def test_error_duration(self):
        log = (
            "12:00:00,scheduled task TaskB, START,789\n"
            "12:20:01,scheduled task TaskB, END,789\n"
        )
        filename = self.create_temp_log(log)
        results = parse_log_file(filename)
        # os.remove(filename)
        self.assertEqual(results[0]['status'], 'ERROR')

    # test 4 - verify the possibility a job has START line missing
    def test_missing_start_job(self):
        log = (
            "12:10:00,background job JobZ, END,999\n"
        )
        filename = self.create_temp_log(log)
        results = parse_log_file(filename)
        # os.remove(filename)
        self.assertEqual(results, [])

    # test 5 - verify the possibility a job has END line missing
    def test_missing_end_job(self):
        log = (
            "12:10:00,background job JobZ, START,999\n"
        )
        filename = self.create_temp_log(log)
        results = parse_log_file(filename)
        # os.remove(filename)
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()
