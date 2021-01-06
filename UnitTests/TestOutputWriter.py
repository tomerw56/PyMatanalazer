from unittest import TestCase
from zenlog import log
from unittest.mock import Mock, create_autospec, patch
from PyMatAnalyzer.Utils.OutputWriters.LoggerTestOutputWriter import LoggerTestOutputWriter

class TestOutputWriter(TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_logger_writer(self):
        test_writer=LoggerTestOutputWriter(log)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        test_writer.WriteOutput(value="the_value",headline="the_header")