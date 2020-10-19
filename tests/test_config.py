import unittest
from application.config_cls import Config
from testfixtures import TempDirectory


class TestConfig(unittest.TestCase):

    def test_platform(self):
        con = Config([])
        res = con.platform
        self.assertIsInstance(res, str)

    @tempdir()
    def test_folder_path(dir):
        con = Config([])
        res = con.folder_path
        self.assertEqual(dir.path, res)

    def test_start_date(self):
        con = Config([])
        start_date = '01-01-2020'
        res = con.start_date
        self.assertEqual(res, start_date)

    def test_start_hour(self):
        con = Config([])
        start_hour = '00:00:00'
        res = con.start_hour
        self.assertEqual(res, start_hour)

    def test_config_file_check(self):
        pass


if __name__ == "__main__":
    unittest.main()
