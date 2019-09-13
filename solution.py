"""
Solution to the coding challenge

To run type: python3 solution.py and follow usage instructions
"""
import os
import datetime
from collections import namedtuple


class Solution(object):
    """
    Solution for the coding challenge
    """
    DATE_FMT = '%m/%d/%Y GMT'

    def __init__(self):
        """
        Initialization of the class
        """
        self.Record = namedtuple('Record', ['epoch', 'url'])
        self.epoch_lst = []
        # Mapping of data
        #  Date               url: hits               hits: set of urls, high_hit_count
        # {'08/08/2014 GMT': [{'www.reddit.com': 1}, {1:{'www.reddit.com'}}, 1]
        self.date_to_freq_dict = dict()
        super().__init__()

    def start_main(self):
        """
        Begins execution of the solution to the coding challenge
        """
        file_location, token = '', ''
        try:
            file_location, token = self.file_location_user()
            self.parse_input_file(file_location, token)
            self.nice_print()
        except (IOError, ValueError) as err:
            print("Error: {0}".format(err))
            print(err.args)

    def file_location_user(self):
        """
        Ask user for file name.
        """
        cwd = os.getcwd()
        file_location = ''
        token = ''
        print("Usage:\nEnter the location of the data file, followed by the separator used in the file.\n")
        print("Please keep in mind your current location when opening data file:\nCurrent working directory: {0}\n".format(cwd))
        print("Type QUIT to exit.\n")
        user_args = input("Please enter the file name: ").split()
        if len(user_args) < 2:
            token = '|'
        else:
            token = user_args[1]
        file_location = user_args[0]
        if file_location and file_location != 'QUIT':
            return file_location, token
        elif file_location == 'QUIT':
            exit(0)
        else:
            raise IOError("File name can't be empty.")

    def parse_input_file(self, file_name, token):
        """
        Parse date file using a token as separator
        """
        with open(file_name, 'r') as infile:
            for line in infile:
                if line.strip():
                    if token not in line:
                        raise ValueError(
                              'Token: {0} not found in {1}.'.format(
                                  token,
                                  line.strip()
                                  ))
                    (epoch_time, url) = line.split(token.strip())
                    rec = self.Record(epoch=float(epoch_time), url=url.strip())
                    self.epoch_lst.append(rec.epoch)
                    self.add_record_to_dict(rec)

    def add_record_to_dict(self, rec):
        """
        Add record to our dictionaries
        """
        date_stamp = ''
        if rec:
            try:
                date_stamp = datetime.datetime.fromtimestamp(rec.epoch).strftime(self.DATE_FMT)
            except (OverflowError, ValueError, OSError) as e:
                raise e
                print(e)
                print(e.args)
                # exit(1)
            if date_stamp not in self.date_to_freq_dict.keys():
                self.date_to_freq_dict[date_stamp] = [
                    {rec.url: 1},
                    {int(1): {rec.url}},
                    int(1)]
            else:
                dict_entry = self.date_to_freq_dict[date_stamp]
                if rec.url in dict_entry[0].keys():
                    prev_hit_cnt = dict_entry[0][rec.url]
                    # remove url from set of previous hit cnt
                    dict_entry[1][prev_hit_cnt].discard(rec.url)
                    # increate the hit count of the url
                    dict_entry[0][rec.url] += 1
                    # add url to set of corresponding hit count
                    curr_hit_cnt = dict_entry[0][rec.url]
                    if curr_hit_cnt in dict_entry[1]:
                        dict_entry[1][curr_hit_cnt].add(rec.url)
                    else:
                        dict_entry[1][curr_hit_cnt] = {rec.url}
                else:
                    dict_entry[0][rec.url] = 1
                    dict_entry[1][1].add(rec.url)
                # update the max number of hits for the current date_stamp
                if dict_entry[0][rec.url] > self.date_to_freq_dict[date_stamp][2]:
                    self.date_to_freq_dict[date_stamp][2] = dict_entry[0][rec.url]
            if not self.date_to_freq_dict:
                raise ValueError('Could not build a dictionary.')

    def nice_print(self):
        """
        Print the url/ hit count from the dictionary for each date, in decreasing order of hit count.
        """
        if not self.epoch_lst:
            raise ValueError('Empty list of Linux Epochs.')
        if not self.date_to_freq_dict:
            raise ValueError('Empty dictinary of hit count to url.')
        self.epoch_lst.sort()
        date_lst = map(
            lambda x: datetime.datetime.fromtimestamp(x).strftime(
                self.DATE_FMT),
                self.epoch_lst
            )
        for date in date_lst:
            if date in self.date_to_freq_dict.keys():
                print(date)
                url_hit_cnt = self.date_to_freq_dict[date][0]
                hit_to_url_dict = self.date_to_freq_dict[date][1]
                curr_num_hits = self.date_to_freq_dict[date][2]
                while hit_to_url_dict[curr_num_hits]:
                    url_from_set = hit_to_url_dict[curr_num_hits].pop()
                    url_hits = url_hit_cnt[url_from_set]
                    print("{0} {1}".format(url_from_set, url_hits))
                    # decrease the number of hits if the current bucket is empty
                    if not hit_to_url_dict[curr_num_hits]:
                        curr_num_hits -= 1
                    # if we get to 0 we break from while loop
                    if curr_num_hits == 0:
                        break
                # clear the entry in the dictionary for the date
                del self.date_to_freq_dict[date]
        # clear our data structures if the GC wants to check
        if self.date_to_freq_dict == {}:
            self.date_to_freq_dict = None
            self.epoch_lst = None


if __name__ == "__main__":
    soln = Solution()
    soln.start_main()

