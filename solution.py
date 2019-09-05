import os
import datetime
import heapq
from collections import namedtuple


def file_location_user():
    """
    Ask user for file name.
    """
    cwd = os.getcwd()
    print("Please keep in mind your current location when opening data file:\nCurrent working directory: {0}\n".format(cwd))
    print("Type QUIT to exit.\n")
    file_location = input("Please enter the file name: ")
    if file_location and file_location != 'QUIT':
        return file_location
    elif file_location == 'QUIT':
        exit(1)
    else:
        raise IOError("File name can't be empty.")


def parse_input_file(file_name):
    """
    Read input from file and store in a min Heap.
    """
    py_heap = []
    Record = namedtuple('Record', ['epoch', 'url'])
    with open(file_name, 'r') as infile:
        for line in infile:
            (epoch_time, url) = line.split('|')
            rec = Record(epoch=float(epoch_time), url=url.strip())
            heapq.heappush(py_heap, rec)
    create_counter_dict(py_heap)


def create_counter_dict(py_heap):
    """
    Populate a dictionary of dictionaries from the min heap.
    """
    py_count_dict = {}
    while py_heap:
        rec = heapq.heappop(py_heap)
        try:
            date_stamp = datetime.datetime.fromtimestamp(rec.epoch).strftime('%m/%d/%Y GMT') 
        except (OverflowError, ValueError) as e:
            print(e)
            print(e.args)
        if not py_count_dict or date_stamp not in py_count_dict.keys():
            py_count_dict[date_stamp] = {rec.url: 1}
        elif date_stamp in py_count_dict.keys() and rec.url not in py_count_dict[date_stamp].keys():
            py_count_dict[date_stamp][rec.url] = 1 
        elif date_stamp in py_count_dict.keys() and py_count_dict[date_stamp][rec.url]:
            py_count_dict[date_stamp][rec.url] += 1
    if py_count_dict:
        return py_count_dict
    else:
        raise ValueError('Could not build a dictionary.')


def nice_print(py_count_dict):
    """
    Print the url/ hit count from the dictionary for each date, in decreasing order of hit count.
    """
    py_lst = []
    if py_count_dict:
        for key, value in py_count_dict.items():
            # Print date first
            print(key)
            # iterate dictionary values for a specific date, and add them to a list.
            for url, count in value.items():
                py_lst.append((url, count))
            # O(N*logN)
            # Sort the list of url/hit tuples in decreasing order.
            py_lst.sort(key=lambda tup: tup[1], reverse=True)
            # - iterate and print each element in the list.
            for rec in py_lst:
                print("url: {0} Hit count: {1}".format(rec[0], rec[1]))
            # empty list for next date.
            py_lst = []
    else:
        raise ValueError('Dictionary cannot be None.')


try:
    file_location = file_location_user()
except IOError as ioe:
    print("Error: {}".format(ioe))

