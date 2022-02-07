#!/usr/bin/python3
import sys

tc_no_list = []

new_tc_no_file = open(sys.argv[2], "r+")
for line_in_new_file in new_tc_no_file:
    testcase_no_to_be_replace = line_in_new_file.split(',')
    old_tc_no = testcase_no_to_be_replace[0].replace('\ufeff', '')
    new_tc_no = testcase_no_to_be_replace[1].replace('\n', '')
    tc_no_list.append([old_tc_no, new_tc_no])
new_tc_no_file.close()

file_to_be_replace = open(sys.argv[1], "r+")
new_tc_file = open(sys.argv[3], "w+")
for line in file_to_be_replace:
    testcase_no = line.strip()
    for tc in tc_no_list:
        if tc[0] != testcase_no:
            not_found = True
            continue
        if tc[0] == testcase_no:
            not_found = False
            new_tc_file.write(tc[1] + '\n')
            print("{} -----> {}".format(tc[0], tc[1]))
            break
    if not_found:
        new_tc_file.write(line)

file_to_be_replace.close()
new_tc_file.close()
