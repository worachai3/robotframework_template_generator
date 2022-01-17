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
        self.tag_option = 'y'
        self.found_testcases_section = False
        self.found_new_testcase = False
        self.found_testcase = False
        self.generated_testcases = []
        self.script = []

    def __set_variables_when_found_new_testcase_number(self, line):
        if self.__is_testcase_number(line):
            if self.found_testcase:
                self.found_testcase = False
                self.found_new_testcase = True
            else:
                self.found_testcase = True

    def __is_not_found_testcase_or_is_not_end_of_testcase(self):
        return not self.found_testcase and not self.found_new_testcase

    def __is_not_end_of_tags(self, line):
        return line.startswith('    ...')

    def __is_documentation(self, line):
        return line.startswith('    [Documentation]')

    def __is_tags(self, line):
        return line.startswith('    [Tags]')

    def __is_testcase_section(self, line):
        return self.match(line, '*** test cases ***')

    def __is_line_too_long(self, line):
        return len(line) >= 120

    def __is_testcase_generated(self, testcase_no):
        return testcase_no in self.generated_testcases

    def __is_end_of_testcase(self, line):
        if self.__is_testcase_number(line):
            return True
        return self.is_end_of_section(line)

    def __is_testcase_number(self, line):
        return re.search('^[A-Za-z]+-[0-9]+$', line.strip())

    def __is_match_testcase_number(self, line, matcher):
        return self.__is_testcase_number(line) and self.match(line, matcher)

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

    def __add_tag_from_excel(self, row):
        tag_str = '    [Tags]'
        tag_str = self.__add_single_string_to_tag_str(tag_str, row[feature])
        tag_str = self.__add_single_string_to_tag_str(tag_str, row[subfeature])
        tag_str = self.__add_single_string_to_tag_str(tag_str, row[priority])
        tag_str = self.__add_multiple_string_to_tag_str(tag_str, row[tag])
        tag_str = self.__add_multiple_string_to_tag_str(tag_str, row[defects])
        self.script.append(tag_str)

    def __add_tag_from_excel_new_case(self, row):
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

    def __append_documentation_to_list(self, testcase_name):
        self.script.append(self.__get_testcase_name_string(testcase_name))

    def __append_tags_to_list(self, tag_list):
        tag_str = '    [Tags]'
        for tag in tag_list:
            tag = tag.strip()
            tag_str += '    ' + tag
        self.script.append(tag_str)

    def __append_space_to_last_element_to_list(self):
        if self.script:
            if self.script[-1].strip() != '':
                self.__append_to_list('')

    def __append_to_list(self, line):
        self.script.append(line)

    def __append_test_step_to_list(self, testcase_no):
        found_testcase = False
        old_robot_file = open(self.old_robot_file_path)
        for line in old_robot_file:
            if self.__is_match_testcase_number(line, testcase_no):
                found_testcase = True
                continue
            if not found_testcase:
                continue
            if self.__is_documentation(line):
                continue
            if self.__is_tags(line):
                continue
            if self.__is_not_end_of_tags(line):
                continue
            if self.__is_end_of_testcase(line):
                break
            self.script.append(line.rstrip())
        if not found_testcase:
            self.__append_new_testcase_test_step()
        self.__append_space_to_last_element_to_list()

    def __append_testcase_number_to_list_(self, tc_no):
        self.__append_testcase_number_to_list(tc_no)

    def __append_new_testcase_test_step(self):
        self.script.append('    Log To Console    EMPTY TEST CASE SCRIPT')
        self.script.append('')

    def __append_tags_to_list_(self, row):
        old_robot_file = open(self.old_robot_file_path)
        found_testcase = False
        for line in old_robot_file:
            if self.__is_match_testcase_number(line, row[tc_no]):
                found_testcase = True
                break
        old_robot_file.close()
        tag_excel = '{}, {}, {}'.format(
            row[feature], row[subfeature], row[priority])
        if not pd.isnull(row[tag]):
            tag_excel += ', {}'.format(row[tag])
        if not pd.isnull(row[defects]):
            tag_excel += ', {}'.format(row[defects])
        if not found_testcase:
            tag_excel += ', NotReady'
        tag_excel = tag_excel.replace(' ', '')

        if self.tag_option == 'y':
            tag_list = self.__get_tags_from_testcase_number(row[tc_no])
            tag_list = self.__merge_tags_with_existing_tag(tag_list, tag_excel)
            self.__append_tags_to_list(tag_list)
        elif self.tag_option == 'n':
            self.__add_tag_from_excel(row)

    def __merge_tags_with_existing_tag(self, tag_list, tags_excel):
        if pd.isnull(tags_excel):
            return tag_list
        tags_excel = tags_excel.strip(' ')
        tags_excel_list = tags_excel.split(',')
        if not tag_list:
            return tags_excel_list
        for i in range(len(tag_list)):
            if not self.in_list(tag_list[i], tags_excel_list):
                tags_excel_list.append(tag_list[i].strip())
        return tags_excel_list

    def __check_testcases_duplicate(self):
        testcases_dictionary = {}
        if self.is_empty_file(self.old_robot_file_path):
            return
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip()
            if self.__is_testcase_number(line):
                if line in testcases_dictionary:
                    testcases_dictionary[line] += 1
                else:
                    testcases_dictionary[line] = 0
        for testcase_no, amount in testcases_dictionary.items():
            if amount > 0:
                print('{} is duplicated {} time(s) in old script.'.format(
                    testcase_no, amount))

    def __get_testcase_name_string(self, testcase_name):
        res = ''
        line = '    [Documentation]    '
        testcase_name_list = testcase_name.split()
        for index in range(len(testcase_name_list)):
            if not self.__is_line_too_long(line + testcase_name_list[index]):
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

    def __get_tag_list_from_line(self, line):
        res_tag_list = []
        tag_str = line.strip('   ...   ')
        tag_list = tag_str.split(' ')
        for tag in tag_list:
            tag = tag.strip()
            if tag != '' and tag != '[Tags]':
                res_tag_list.append(tag)
        return res_tag_list

    def __get_tags_from_testcase_number(self, testcase_no):
        res_tag_list = []
        found_tag = False
        found_testcase = False
        old_robot_file = open(self.old_robot_file_path)
        for line in old_robot_file:
            if not found_testcase:
                if self.__is_match_testcase_number(line, testcase_no):
                    found_testcase = True
                continue
            if self.__is_tags(line):
                found_tag = True
                tag_list = self.__get_tag_list_from_line(line)
                self.append_items_from_list_to_list(tag_list, res_tag_list)
            if found_tag and self.__is_not_end_of_tags(line):
                tag_list = self.__get_tag_list_from_line(line)
                self.append_items_from_list_to_list(tag_list, res_tag_list)
            if self.__is_testcase_number(line) and found_tag:
                break
        old_robot_file.close()
        return res_tag_list

    def __get_testcases_script_from_exisiting_script(self):
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
            if self.is_end_of_section(line):
                break
            self.script.append(line)
        old_robot_file.close()

    def __get_testcases_script_from_testcases_file(self, tc_file_path):
        df = pd.read_excel(tc_file_path, usecols='B, C, D, E, M, Q, Y')
        self.__check_testcases_duplicate()
        for index, row in df.iterrows():
            self.__append_testcase_number_to_list_(row[tc_no])
            self.__append_documentation_to_list(row[tc_name])
            self.__append_tags_to_list_(row)
            self.__append_test_step_to_list(row[tc_no])
        self.script.insert(0, '*** Test Cases ***')

    def find_testcases_script(self, tc_file_path):
        self.__get_testcases_script_from_testcases_file(tc_file_path)
        self.__get_testcases_script_from_exisiting_script()
