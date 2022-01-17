from Classes.base import Base
import re
import pandas as pd


feature = 'Feature'
subfeature = 'Sub Feature'
tc_no = 'Test Cases No.'
tc_name = 'Test Cases Name'
tag = 'Tag / Requirement Ref.'
priority = 'Priority'
defects = 'Defects'


class Testcases(Base):

    def __init__(self, old_robot_file_path):
        Base.__init__(self)
        self.old_robot_file_path = old_robot_file_path
        self.found_testcases_section = False
        self.found_new_testcase = False
        self.found_testcase = False
        self.found_documentation = False
        self.found_documentation_first_row = False
        self.found_tags = False
        self.found_tags_first_row = False
        self.generated_testcases = []
        self.script = []

    def __set_all_variables_to_default(self):
        self.found_testcases_section = False
        self.found_new_testcase = False
        self.found_testcase = False
        self.found_documentation = False
        self.found_documentation_first_row = False
        self.found_tags = False
        self.found_tags_first_row = False
        self.script = []

    def __set_found_variables_to_false(self):
        self.found_testcases_section = False
        self.found_new_testcase = False
        self.found_testcase = False
        self.found_documentation = False
        self.found_documentation_first_row = False
        self.found_tags = False
        self.found_tags_first_row = False

    def __set_variables_when_found_new_testcase_number(self, line):
        if self.__found_testcases_number(line):
            if self.found_testcase:
                self.found_testcase = False
                self.found_new_testcase = True
            else:
                self.found_testcase = True

    def __is_not_found_testcase_or_is_not_end_of_testcase(self):
        return not self.found_testcase and not self.found_new_testcase

    def __is_end_of_documentation_or_tags(self, line):
        if (self.found_documentation_first_row or self.found_tags_first_row):
            return line.startswith('    ...')

    def __is_end_of_testcases_section(self, line):
        return line.startswith('***')

    def __is_documentation(self, line):
        return line.startswith('    [Documentation]')

    def __is_tags(self, line):
        return line.startswith('    [Tags]')

    def __is_testcase_section(self, line):
        return self.match(line, '*** test cases ***')

    def __is_name_too_long(self, name):
        return len(name) >= 120

    def __is_testcase_generated(self, testcase_no):
        return testcase_no in self.generated_testcases

    def __add_single_string_to_tag_str(self, tag_str, string):
        string = str(string)
        tag_str += '    ' + string
        return tag_str

    def __add_multiple_string_to_tag_str(self, tag_str, str):
        if pd.isnull(str):
            return tag_str
        str_list = str.split(',')
        for i in range(len(str_list)):
            tag_str += '    ' + str_list[i].strip()
        return tag_str

    def __add_tag(self, row):
        tag_str = '    [Tags]'
        tag_str = self.__add_single_string_to_tag_str(tag_str, row[feature])
        tag_str = self.__add_single_string_to_tag_str(tag_str, row[subfeature])
        tag_str = self.__add_single_string_to_tag_str(tag_str, row[priority])
        tag_str = self.__add_multiple_string_to_tag_str(tag_str, row[tag])
        tag_str = self.__add_multiple_string_to_tag_str(tag_str, row[defects])
        tag_str = self.__add_single_string_to_tag_str(tag_str, 'NotReady')
        self.script.append(tag_str)

    def __append_testcase_number_to_list(self, line):
        self.found_testcase = True
        self.script.append(line)
        self.generated_testcases.append(line)

    def __append_documentation_to_list(self, row):
        self.found_documentation = True
        self.found_documentation_first_row = True
        self.script.append(self.__get_testcase_name_string(row[tc_name]))

    def __append_tags_to_list(self, row):
        if not self.found_documentation:
            self.found_documentation = True
            self.script.append(self.__get_testcase_name_string(row[tc_name]))
        self.found_tags = True
        self.found_tags_first_row = True
        self.__add_tag(row)

    def __append_space_to_last_element_to_list(self):
        if self.script:
            if self.script[-1].strip() != '':
                self.__append_to_list('')

    def __append_to_list(self, line):
        self.script.append(line)
        self.found_documentation_first_row = False
        self.found_tags_first_row = False

    def __exceptional_case(self, row):
        if not self.found_documentation:
            self.found_documentation = True
            self.script.append(self.__get_testcase_name_string(row[tc_name]))
        if not self.found_tags:
            self.found_tags = True
            self.__add_tag(row)

    def __found_testcases_number(self, line):
        return re.search('^[A-Za-z]+-[0-9]+$', line.strip())

    def __get_testcase_name_string(self, testcase_name):
        res = ''
        line = '    [Documentation]    '
        testcase_name_list = testcase_name.split()
        for index in range(len(testcase_name_list)):
            if not self.__is_name_too_long(line + testcase_name_list[index]):
                line += testcase_name_list[index].strip() + ' '
                res += testcase_name_list[index].strip() + ' '
            else:
                if testcase_name_list[index] != testcase_name_list[-1]:
                    line = '    ...    '
                    res += '\n    ...    '
        res = self.__get_documentation_string() + res
        return res

    def __get_documentation_string(self):
        return '    ' + '[Documentation]' + '    '

    def __gen_new_testcase(self, row):
        self.script.append(row[tc_no])
        self.script.append(self.__get_testcase_name_string(row[tc_name]))
        self.__add_tag(row)
        self.script.append('    Log To Console    EMPTY TEST CASE SCRIPT')
        self.script.append('')

    def __check_testcases_duplicate(self):
        testcases_dictionary = {}
        if self.is_empty_file(self.old_robot_file_path):
            return
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip()
            if self.__found_testcases_number(line):
                if line in testcases_dictionary:
                    testcases_dictionary[line] += 1
                else:
                    testcases_dictionary[line] = 0
        for testcase_no, amount in testcases_dictionary.items():
            if amount > 0:
                print('{} is duplicated {} time(s) in old script.'.format(
                    testcase_no, amount))

    def __find_testcase_script_from_testcases_row(self, row):
        self.__set_found_variables_to_false()
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip('\n')
            if self.match(line, row[tc_no]):
                self.__append_testcase_number_to_list(line)
                continue
            if not self.found_testcase:
                continue
            if self.__found_testcases_number(line):
                break
            if self.__is_documentation(line):
                if self.found_documentation:
                    continue
                self.__append_documentation_to_list(row)
                continue
            if self.__is_tags(line):
                if self.found_tags:
                    continue
                self.__append_tags_to_list(row)
                continue
            if self.__is_end_of_documentation_or_tags(line):
                continue
            self.__exceptional_case(row)
            if self.__is_end_of_testcases_section(line):
                break
            self.__append_to_list(line)
        self.__append_space_to_last_element_to_list()
        old_robot_file.close()

    def __find_testcases_script_from_testcases_file(self, testcases_file_path):
        df = pd.read_excel(testcases_file_path, usecols='B, C, D, E, M, Q, Y')
        self.__check_testcases_duplicate()
        for index, row in df.iterrows():
            if not self.is_empty_file(self.old_robot_file_path):
                self.__find_testcase_script_from_testcases_row(row)
            if not self.found_testcase:
                self.__gen_new_testcase(row)
        self.script.insert(0, '*** Test Cases ***')

    def __generate_testcases_script_from_testcases_file(self, tc_file_path):
        pass
        # read excel file
        df = pd.read_excel(tc_file_path, usecols='D, E, M, Q, Y')
        # for index, row in excel:
        for index, row in df.iterrows():
            self.__append_testcase_number_to_list(row[tc_no])
            self.__append_documentation_to_list(row[tc_no])
            self.__append_tags_to_list(row[tc_no])
            self.__append_test_step_to_list(row[tc_no])
        self.script.insert(0, '*** Test Cases ***')

    def __append_testcase_number_to_list_from_existing(self, tc_no):
        pass

    def __append_documentation_to_list_from_existing(self, tc_no):
        pass

    def __append_tags_to_list_from_existing(self, tc_no):
        pass

    def __append_test_step_to_list_fromexisting(self, tc_no):
        pass

    def __generate_testcases_script_from_exisiting_script(self, tc_file_path):
        pass
        # open old robot file
        old_robot_file = open(self.old_robot_file_path, 'r+')
        # for line in old robot_file:
        for line in old_robot_file:
            if self.__found_testcases_number(line):
                if not self.__is_testcase_generated(line):
                    self.__append_existing_testcase(line)
        old_robot_file.close()

    def __find_testcases_not_generated(self):
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip('\n')
            if self.__is_testcase_section(line):
                self.found_testcases_section = True
                continue
            if not self.found_testcases_section:
                continue
            self.__set_variables_when_found_new_testcase_number(line)
            if self.__is_not_found_testcase_or_is_not_end_of_testcase():
                continue
            if self.__is_testcase_generated(line):
                self.found_testcase = False
                self.found_new_testcase = False
                continue
            if self.__is_end_of_testcases_section(line):
                break
            self.script.append(line)
        old_robot_file.close()

    def find_testcases_script(self, tc_file_path):
        self.__set_all_variables_to_default()
        self.__find_testcases_script_from_testcases_file(tc_file_path)
        self.__find_testcases_not_generated()
