import unittest
from collections import namedtuple
from solution import Solution


class SolutionTestCase(unittest.TestCase):
    """
    Run from the command line
    python3 -m unittest tests/test_file_import.py -v
    """

    def setUp(self):
        """
        """
        self.soln = Solution()
        return super().setUp()

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

    def test_create_dictionary_from_heap(self):
        """
        """
        py_heap = self.soln.parse_input_file('data1.txt', '|')
        py_dictionary = self.soln.create_counter_dict(py_heap)
        self.assertIsNotNone(py_dictionary)

    def test_overflow_exception_raised_for_incorrect_epoch_time(self):
        """
        """
        Record = namedtuple('Record', ['epoch', 'url'])
        py_heap = [Record(epoch=float(-100), url='www.nba.com')]
        with self.assertRaises(OverflowError):
            py_dict = self.soln.create_counter_dict(py_heap)

    def tearDown(self):
        """
        """
        self.soln = None
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()

