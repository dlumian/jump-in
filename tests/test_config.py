import unittest
from src.config import Config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = Config()

    def test_default_directory(self):
        self.assertEqual(self.config.directory, '.')

    def test_default_conda_env(self):
        self.assertEqual(self.config.conda_env, 'base')

    def test_update_directory(self):
        new_directory = '/new/directory'
        self.config.update_directory(new_directory)
        self.assertEqual(self.config.directory, new_directory)

    def test_update_conda_env(self):
        new_conda_env = 'my_env'
        self.config.update_conda_env(new_conda_env)
        self.assertEqual(self.config.conda_env, new_conda_env)

    def test_load_config(self):
        self.config.load_config('path/to/config.json')
        self.assertEqual(self.config.directory, 'expected_directory')
        self.assertEqual(self.config.conda_env, 'expected_env')

if __name__ == '__main__':
    unittest.main()