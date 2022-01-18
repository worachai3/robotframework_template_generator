import os
import re
import sys
import pandas as pd
from Classes.settings import Settings
from Classes.keywords import Keywords
from Classes.variables import Variables
from Classes.testcases import Testcases


err_missing_param = '''Error: Missing parameter(s).
please run command \'./run.sh -h\' to see how to use script.'''
err_found_dup = 'Please remove duplicated test cases before running script'


class RobotTemplateGenerator():

    def __init__(self):
        self.new_robot_file = open(new_robot_file_path, 'w+')

    def write_list_into_file(self, list, splitter):
        for line in list:
            self.new_robot_file.write(line + splitter)

    def generate_testcases_section(self):
        testcases = Testcases(old_robot_file_path, tag_option)
        testcases.generate_testcases_script(testcases_file_path)
        if not testcases.script:
            return
        self.write_list_into_file(testcases.script, '\n')

    def generate_variables_section(self):
        variables = Variables(old_robot_file_path)
        variables.generate_variables_script()
        if not variables.script:
            return
        self.write_list_into_file(variables.script, '\n')

    def generate_keywords_section(self):
        keywords = Keywords(old_robot_file_path)
        keywords.generate_keywords_script()
        if not keywords.script:
            return
        self.write_list_into_file(keywords.script, '\n')

    def generate_settings_section(self):
        settings = Settings(old_robot_file_path)
        settings.generate_settings_script()
        if not settings.script:
            return
        self.write_list_into_file(settings.script, '\n')

    def generate_robot_template(self):
        self.generate_settings_section()
        self.generate_variables_section()
        self.generate_testcases_section()
        self.generate_keywords_section()


def set_file_path():
    try:
        global testcases_file_path
        global old_robot_file_path
        global new_robot_file_path
        global tag_option
        testcases_file_path = sys.argv[1]
        old_robot_file_path = sys.argv[2]
        new_robot_file_path = sys.argv[3]
        tag_option = sys.argv[4]
    except IndexError:
        print(err_missing_param)
        sys.exit(1)


def check_testcases_duplicate_in_old_script():
    testcases_dictionary = {}
    if os.stat(old_robot_file_path).st_size == 0:
        return
    old_robot_file = open(old_robot_file_path, 'r+')
    for line in old_robot_file:
        line = line.strip()
        if re.search('^[A-Za-z]+-[0-9]+$', line.strip()):
            if line in testcases_dictionary:
                testcases_dictionary[line] += 1
            else:
                testcases_dictionary[line] = 0
    for testcase_no, amount in testcases_dictionary.items():
        if amount > 0:
            print('{} is duplicated {} time(s) in old script.'.format(
                    testcase_no, amount))
            print(err_found_dup)
            sys.exit(1)


def check_testcases_duplicate_in_testcases_file():
    testcases_dictionary = {}
    if os.stat(testcases_file_path).st_size == 0:
        return
    df = pd.read_excel(testcases_file_path, usecols='D')
    for index, row in df.iterrows():
        tc_no = row["Test Cases No."].strip()
        if tc_no in testcases_dictionary:
            testcases_dictionary[tc_no] += 1
        else:
            testcases_dictionary[tc_no] = 0
    for testcase_no, amount in testcases_dictionary.items():
        if amount > 0:
            print('{} is duplicated {} time(s) in test cases excel.'.format(
                    testcase_no, amount))
            print(err_found_dup)
            sys.exit(1)


def main():
    set_file_path()
    check_testcases_duplicate_in_old_script()
    check_testcases_duplicate_in_testcases_file()
    robot_template_generator = RobotTemplateGenerator()
    robot_template_generator.generate_robot_template()
    robot_template_generator.new_robot_file.close()


if __name__ == '__main__':
    main()
