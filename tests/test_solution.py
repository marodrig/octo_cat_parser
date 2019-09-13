"""
Test case for the coding challenge solution
"""
import unittest
from collections import namedtuple
from solution import Solution
import datetime


class SolutionTestCase(unittest.TestCase):
    """
    Run from the command line
    
    python3 -m unittest tests/test_file_import.py -v
    """

    def setUp(self):
        """
        Setup testing environment
        """
        self.soln = Solution()
        return super().setUp()

    def test_data_file_in_sub_directory_parsed_correctly(self):
        """
        Test we can parse data files in other directories
        """
        self.soln.parse_input_file('data/data1.txt', '|')
        self.assertIsNotNone(self.soln.date_to_freq_dict)

    def test_data_file_is_parsed_correctly(self):
        """
        Test data file is parsed correctly
        """
        self.soln.parse_input_file('data1.txt', '|')
        self.assertIsNotNone(self.soln.date_to_freq_dict)

    def test_parsing_data_with_incorrect_file_name_raises_FileNotFoundError(self):
        """
        Test FileNotFoundException is raised for a file not found
        """
        with self.assertRaises(FileNotFoundError):
            self.soln.parse_input_file('cat.txt', '|')

    def test_none_existing_directory_raises_FileNotFoundError(self):
        """
        Test FileNotFoundException is raised if a non existing directory is used
        """
        with self.assertRaises(FileNotFoundError):
            self.soln.parse_input_file('py-data/data1.txt', '|')

    def test_parsing_data_with_incorrect_token_raises_ValueError(self):
        """
        Test ValueErrorException is raised when the token is not in the file
        """
        with self.assertRaises(ValueError):
            self.soln.parse_input_file('data1.txt', ':')

    def test_add_record_to_dictionary(self):
        """
        Test we can add to our dictionaries
        """
        dummy_record = self.soln.Record(
            epoch=float(1407481200),
            url='www.reddit.com')
        self.soln.add_record_to_dict(dummy_record)
        self.assertDictEqual(
            self.soln.date_to_freq_dict,
            {'08/08/2014 GMT': [{'www.reddit.com': 1},
            {1: {'www.reddit.com'}},
            1]})

    def test_hit_count_increases_for_given_url(self):
        """
        Test the hit count is increased correctly
        """
        dummy_record_1 = self.soln.Record(
            epoch=float(1407478022),
            url='www.reddit.com')
        dummy_record_2 = self.soln.Record(
            epoch=float(1407478021),
            url='www.reddit.com')
        expected_dict = dict()
        expected_dict['08/08/2014 GMT'] = [
            {'www.reddit.com': 2},
            {1: set(), 2: {'www.reddit.com'}},
            2]
        self.soln.add_record_to_dict(dummy_record_1)
        self.soln.add_record_to_dict(dummy_record_2)
        self.assertDictEqual(
            self.soln.date_to_freq_dict,
            expected_dict
            )


    def test_incorrect_epoch_raises_ValueError(self):
        """
        Test ValueError is raised for incorrect epoch time
        """
        dummy_record = self.soln.Record(
            epoch=int(292277026596),
            url='www.fifa.com'
        )
        with self.assertRaises(ValueError):
            self.soln.add_record_to_dict(dummy_record)

    def test_empty_url(self):
        """
        Test url can be empty
        """
        dummy_record = self.soln.Record(
            epoch=float(1407481210),
            url=None
        )
        self.soln.add_record_to_dict(dummy_record)
        self.assertIsNotNone(self.soln.date_to_freq_dict)

    def test_None_epoch_raises_TypeError(self):
        """
        Test TypeError is raised for a None epoch
        """
        dummy_record = self.soln.Record(
            epoch=None,
            url='www.wwe.com'
        )
        with self.assertRaises(TypeError):
            self.soln.add_record_to_dict(dummy_record)

    def test_empty_list_of_epochs_raises_ValueError(self):
        """
        Test an exception is raised if the list of epochs is empty when printing to stdout
        """
        self.soln.epoch_lst = None
        with self.assertRaises(ValueError):
            self.soln.nice_print()

    def test_memory_is_cleared_after_run(self):
        """
        Test we clear the memory we used
        """
        dummy_record = self.soln.Record(
            epoch=float(1407478022),
            url='www.fifa.com'
        )
        self.soln.epoch_lst = [1407478022] 
        self.soln.add_record_to_dict(dummy_record)
        self.soln.nice_print()
        self.assertIsNone(self.soln.date_to_freq_dict)
        self.assertIsNone(self.soln.epoch_lst)
        
    def test_empty_hit_count_dictionary_raises_ValueError(self):
        """
        Test an exception is raised if dictionary is None when printing to stdout
        """
        self.soln.date_to_freq_dict = None
        with self.assertRaises(ValueError):
            self.soln.nice_print()

    def tearDown(self):
        """
        Post test case clean up
        """
        self.soln = None
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()

