from Classes.base import Base
import re
import pandas as pd


feature = 'Feature'
subfeature = 'Sub Feature'
tc_no = 'Test Cases No.'
tc_name = 'Test Objective'
tag = 'Tag / Requirement Ref.'
priority = 'Priority'
defects = 'Defects'
line_length = 120
test_cases_string = '*** Test Cases ***'
documentation_string = '    [Documentation]    '
tags_string = '    [Tags]'


class Testcases(Base):

    def __init__(self, old_robot_file_path, tag_option):
        Base.__init__(self)
        self.old_robot_file_path = old_robot_file_path
        self.tag_option = tag_option.lower()
        self.generated_testcases = []
        self.script = []

    def __is_not_end_of_tags(self, line):
        return line.startswith('    ...')

    def __is_documentation(self, line):
        return line.startswith(self.__get_documentation_string())

    def __is_tags(self, line):
        return line.startswith(self.__get_tag_string())

    def __is_tc_section(self, line):
        return self.match(line, self.__get_test_cases_string())

    def __is_line_too_long(self, line):
        return len(line) >= self.__get_line_length()

    def __is_tc_generated(self, testcase_no):
        return testcase_no in self.generated_testcases

    def __is_end_of_testcase(self, line):
        return self.is_end_of_section(line) or self.__is_tc_number(line)

    def __is_tc_number(self, line):
        return re.search('^[A-Za-z]+-[0-9]+$', line.strip())

    def __is_tag_added(self, tag, tag_list):
        for t in tag_list:
            if tag.strip().lower() == t.strip().lower():
                return True

    def __is_match_tc_number(self, line, matcher):
        return self.__is_tc_number(line) and self.match(line, matcher)

    def __is_tc_number_and_is_not_generated(self, line):
        return self.__is_tc_number(line) and not self.__is_tc_generated(line)

    def __is_not_test_step_in_tc(self, line):
        return self.__is_documentation(line) or self.__is_tags(line) or (
            self.__is_not_end_of_tags(line))

    def __is_tag(self, inp):
        return re.search('^[-_A-Za-z0-9]+$', inp.strip())

    def __add_single_string_to_tag_list(self, tag_list, string):
        string = str(string)
        tag_list.append(string)
        return tag_list

    def __add_multiple_string_to_tag_list(self, tag_list, str):
        if pd.isnull(str):
            return tag_list
        str_list = str.split(',')
        for i in range(len(str_list)):
            tag_list.append(str_list[i].strip())
        return tag_list

    def __add_new_line_to_tag_list(self, tag_list):
        line = self.__get_tag_string() + '    '
        tag_list = self.remove_duplicate_from_list(tag_list)
        for index in range(len(tag_list)):
            if not self.__is_tag(tag_list[index]):
                continue
            if not self.__is_line_too_long(line + '    ' + tag_list[index]):
                line += tag_list[index].strip() + '    '
            else:
                if index != len(tag_list)-1 and len(tag_list[index]) < 50:
                    line = '    ...    '
                    tag_list.insert(index, '\n    ...    ')
        return tag_list

    def __append_to_list(self, line):
        self.script.append(line)

    def __append_tags_to_list(self, tag_list):
        tag_list = self.remove_duplicate_from_list(tag_list)
        tag_str = self.__get_tag_string()
        for tag in tag_list:
            tag = tag.replace(' ', '')
            if self.__is_tag(tag):
                tag_str += '    ' + tag
            else:
                if not self.__is_tag(self.script[-1]):
                    tag_str += '\n    ...   '
        self.__append_to_list(tag_str)

    def __get_tag_from_excel(self, row):
        tag_list = []
        tag_list = self.__add_single_string_to_tag_list(tag_list, row[feature])
        tag_list = self.__add_single_string_to_tag_list(
            tag_list, row[subfeature])
        tag_list = self.__add_single_string_to_tag_list(
            tag_list, row[priority])
        tag_list = self.__add_multiple_string_to_tag_list(tag_list, row[tag])
        tag_list = self.__add_multiple_string_to_tag_list(
            tag_list, row[defects])
        tag_list = self.remove_duplicate_from_list(tag_list)
        return tag_list

    def __get_tag_from_excel_new_case(self, row):
        tag_list = []
        tag_list = self.__add_single_string_to_tag_list(tag_list, row[feature])
        tag_list = self.__add_single_string_to_tag_list(
            tag_list, row[subfeature])
        tag_list = self.__add_single_string_to_tag_list(
            tag_list, row[priority])
        tag_list = self.__add_multiple_string_to_tag_list(tag_list, row[tag])
        tag_list = self.__add_multiple_string_to_tag_list(
            tag_list, row[defects])
        tag_list = self.__add_single_string_to_tag_list(tag_list, 'NotReady')
        tag_list = self.remove_duplicate_from_list(tag_list)
        return tag_list

    def __append_tag_list_option_y(self, row, found_tc):
        tag_excel = self.__get_tag_list_from_excel_check_existed(row, found_tc)
        tag_list = self.__get_tags_from_tc_number(row[tc_no].strip())
        tag_list = self.__merge_tags_with_existing_tag(tag_list, tag_excel)
        tag_list = self.__add_new_line_to_tag_list(tag_list)
        self.__append_tags_to_list(tag_list)

    def __get_tag_list_from_excel_check_existed(self, row, found_tc):
        if found_tc:
            tag_list = self.__get_tag_from_excel(row)
        else:
            tag_list = self.__get_tag_from_excel_new_case(row)
        tag_list = self.remove_duplicate_from_list(tag_list)
        return tag_list

    def __append_tag_list_option_n(self, row, found_tc):
        tag_list = self.__get_tag_list_from_excel_check_existed(row, found_tc)
        tag_list = self.remove_duplicate_from_list(tag_list)
        self.__add_new_line_to_tag_list(tag_list)
        self.__append_tags_to_list(tag_list)

    def __append_tag_by_tc_no(self, row):
        old_robot_file = open(self.old_robot_file_path)
        found_tc = False
        for line in old_robot_file:
            if self.__is_match_tc_number(line, row[tc_no].strip()):
                found_tc = True
                break
        old_robot_file.close()
        if self.tag_option == 'y':
            self.__append_tag_list_option_y(row, found_tc)
        elif self.tag_option == 'n':
            self.__append_tag_list_option_n(row, found_tc)

    def __append_documentation_to_list(self, testcase_name):
        self.__append_to_list(self.__get_tc_name_string(testcase_name))

    def __append_space_to_last_element_to_list(self):
        if self.script:
            if self.script[-1].strip() != '':
                self.__append_to_list('')

    def __append_tc_number_to_list(self, line):
        self.__append_to_list(line.strip())
        self.generated_testcases.append(line.strip())

    def __append_test_step_to_list(self, testcase_no):
        found_tc = False
        old_robot_file = open(self.old_robot_file_path)
        for line in old_robot_file:
            if self.__is_match_tc_number(line, testcase_no):
                found_tc = True
                continue
            if not found_tc:
                continue
            if self.__is_not_test_step_in_tc(line):
                continue
            if self.__is_end_of_testcase(line):
                break
            self.__append_to_list(line.rstrip())
        if not found_tc:
            self.__append_new_tc_test_step()
        self.__append_space_to_last_element_to_list()

    def __append_new_tc_test_step(self):
        self.script.append('    Log To Console    EMPTY TEST CASE SCRIPT')
        self.script.append('')

    def __get_line_length(self):
        return line_length

    def __get_test_cases_string(self):
        return test_cases_string

    def __get_documentation_string(self):
        return documentation_string

    def __get_tag_string(self):
        return tags_string

    def __get_tag_list_from_line(self, line):
        res_tag_list = []
        tag_str = line.replace('...', '')
        tag_str = line.replace('[Tags]', '')
        tag_list = tag_str.split(' ')
        for tag in tag_list:
            tag = tag.strip()
            if tag != '' and not self.__is_tag_added(tag, res_tag_list):
                res_tag_list.append(tag)
        return res_tag_list

    def __get_tags_from_tc_number(self, testcase_no):
        res_tag_list = []
        found_tag = False
        found_tc = False
        old_robot_file = open(self.old_robot_file_path)
        for line in old_robot_file:
            if not found_tc:
                if self.__is_match_tc_number(line, testcase_no):
                    found_tc = True
                continue
            if self.__is_tags(line):
                found_tag = True
                tag_list = self.__get_tag_list_from_line(line)
                self.append_items_from_list_to_list(tag_list, res_tag_list)
            if found_tag and self.__is_not_end_of_tags(line):
                tag_list = self.__get_tag_list_from_line(line)
                self.append_items_from_list_to_list(tag_list, res_tag_list)
            if self.__is_tc_number(line) and found_tag:
                break
        old_robot_file.close()
        self.remove_duplicate_from_list(res_tag_list)
        return res_tag_list

    def __get_tc_name_string(self, testcase_name):
        res = ''
        line = self.__get_documentation_string()
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

    def __get_testcases_script_from_exisiting_script(self):
        found_tc = False
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip('\n')
            if self.__is_tc_number_and_is_not_generated(line.strip()):
                found_tc = True
                self.__append_to_list(line.strip())
                continue
            if self.__is_end_of_testcase(line) and found_tc:
                if self.__is_tc_number(line) and self.__is_tc_generated(line):
                    found_tc = False
                else:
                    break
            if found_tc:
                self.__append_to_list(line)
        old_robot_file.close()

    def __get_testcases_script_from_testcases_file(self, tc_file_path):
        df = pd.read_excel(tc_file_path, usecols='B, C, D, F, M, Q, Y')
        for index, row in df.iterrows():
            self.__append_tc_number_to_list(row[tc_no].strip())
            self.__append_documentation_to_list(row[tc_name])
            self.__append_tag_by_tc_no(row)
            self.__append_test_step_to_list(row[tc_no].strip())
        self.script.insert(0, self.__get_test_cases_string())

    def __merge_tags_with_existing_tag(self, tag_list, tags_excel_list):
        if not tags_excel_list and tag_list:
            return tag_list
        if not tag_list and tags_excel_list:
            return tags_excel_list
        for i in range(len(tag_list)):
            if not self.in_list(tag_list[i], tags_excel_list):
                tags_excel_list.append(tag_list[i].strip())
        self.remove_duplicate_from_list(tags_excel_list)
        return tags_excel_list

    def generate_testcases_script(self, tc_file_path):
        self.__get_testcases_script_from_testcases_file(tc_file_path)
        self.__get_testcases_script_from_exisiting_script()
