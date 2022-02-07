#!/usr/bin/python3
import re
import sys

tc_no_list = []

old_script_path = sys.argv[1]
new_script_path = sys.argv[2]
mapping_path = sys.argv[3]

mapping = open(mapping_path, 'r+')
for line_in_new_file in mapping:
    testcase_no_to_be_replace = line_in_new_file.split(',')
    old_tc_no = testcase_no_to_be_replace[0].replace('\ufeff', '')
    new_tc_no = testcase_no_to_be_replace[1].replace('\n', '')
    tc_no_list.append([old_tc_no, new_tc_no])
mapping.close()
old_script = open(old_script_path, 'r+')
new_script = open(new_script_path, 'w+')
for line in old_script:
    for tc_no in tc_no_list:
        line = re.sub(f'^{tc_no[0]}', tc_no[1], line)
        new_script.write(line)
old_script.close()
new_script.close()
