import unittest
from solution import Solution


class SolutionTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.soln = Solution()

    def test_data_file_correctly_parsed(self):
        """
        """
        py_heap = self.soln.parse_input_file('data1.txt', '|')
        self.assertIsNotNone(py_heap)

    def test_data_file_parsing_raises_file_not_found_exception_for_not_existing_file(self):
        """
        """
        with self.assertRaises(FileNotFoundError):
            self.soln.parse_input_file('cat.txt', '|')

    def test_data_file_parsing_raises_value_error_exception_incorrect_token(self):
        """
        """
        with self.assertRaises(ValueError):
            self.soln.parse_input_file('data1.txt', ':')

    def tearDown(self):
        """
        """
        self.soln = None
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()

