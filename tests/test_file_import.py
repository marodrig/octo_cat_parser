import unittest
from solution import Solution


class SolutionTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.soln = Solution()

    def test_file_opening(self):
        """
        """
        py_heap = self.soln.parse_input_file('data1.txt', '|')
        self.assertIsNotNone(py_heap)

    def test_file_opening_raises_exception_for_incorrect_name(self):
        """
        """
        self.assertRaises(FileNotFoundError, self.soln.parse_input_file('cat.txt', token='|'))

    def tearDown(self):
        """
        """
        self.soln = None
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()

