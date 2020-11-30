from sys import int_info
import unittest
from application.classes.config_cls import Config


class TestConfig(unittest.TestCase):
    """Validate methods of Config class
    """

    def test_platform(self):
        con = Config()
        res = con.platform
        self.assertIsInstance(res, str)

    def test_save_path(self):
        con = Config()
        import os
        cws = os.getcwd()
        res = con.save_path
        self.assertEqual(cws, res)

    def test_start_date(self):
        con = Config()
        start_date = '01-01-2020'
        res = con.start_date
        self.assertEqual(res, start_date)

    def test_start_hour(self):
        con = Config()
        start_hour = '00:00:00'
        res = con.start_hour
        self.assertEqual(res, start_hour)

    def test_check_config_file(self):
        con = Config()
        import os
        path = os.getcwd()
        file = os.path.join(path, 'config.ini')
        self.assertTrue(os.path.exists(file))

    def test_create_config_file(self):
        import os
        path = os.getcwd()
        file = os.path.join(path, 'config.ini')
        if os.path.exists(file):
            os.remove(file)
        con = Config()
        self.assertTrue(os.path.exists(file))

    def test_change_save_path(self):
        con = Config()
        initial_path = con.save_path
        con.change_save_path('C:/Users')
        self.assertEqual(con.save_path, 'C:/Users')
        con.change_save_path(initial_path)


if __name__ == "__main__":
    unittest.main()
