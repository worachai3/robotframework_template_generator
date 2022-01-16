from Classes.base import Base
import re
import pandas as pd


tc_no = 'Test Cases No.'
tc_name = 'Test Cases Name'
tag = 'Tag / Requirement Ref.'
priority = 'Priority'
defects = 'Defects'


class Testcases(Base):

    def __init__(self, old_robot_file_path, testcases_file_path):
        Base.__init__(self)
        self.old_robot_file_path = old_robot_file_path
        self.testcases_file_path = testcases_file_path
        self.found_testcases_section = False
        self.found_testcase = False
        self.found_documentation = False
        self.found_documentation_first_row = False
        self.found_tags = False
        self.found_tags_first_row = False
        self.generated_testcases = []
        self.script = []

    def __set_variables_to_default(self):
        self.found_testcases_section = False
        self.found_testcase = False
        self.found_documentation = False
        self.found_documentation_first_row = False
        self.found_tags = False
        self.found_tags_first_row = False
        self.script = []

    def __is_testcase_generated(self, testcase_no):
        if testcase_no in self.generated_testcases:
            self.found_testcase = False
            self.found_new_testcase = False
            return True
        return False

    def __is_end_of_documentation_or_tags(self, line):
        if (self.found_documentation_first_row or self.found_tags_first_row):
            return line.startswith('    ...')

    def __add_priority_to_tag_str(self, tag_str, priority):
        tag_str += '    ' + priority
        return tag_str

    def __add_tag_to_tag_str(self, tag_str, tags):
        tag_list = tags.split(',')
        if pd.isnull(tags):
            return
        for i in range(len(tag_list)):
            tag_str += '    ' + tag_list[i].strip()
        return tag_str

    def __add_defect_to_tag_str(self, tag_str, defects):
        if pd.isnull(defects):
            return tag_str
        defect_list = str(defects).split(',')
        for i in range(len(defect_list)):
            tag_str += '    ' + defect_list[i].strip()
        return tag_str

    def __add_tag(self, row):
        tag_str = '    [Tags]'
        tag_str = self.__add_priority_to_tag_str(tag_str, row[priority])
        tag_str = self.__add_tag_to_tag_str(tag_str, row[tag])
        tag_str = self.__add_defect_to_tag_str(tag_str, row[defects])
        self.script.append(tag_str)

    def __found_testcases_number(self, line):
        return re.search('^[A-Za-z]+-[0-9]+$', line)

    def __append_testcase_number_to_list(self, line):
        self.found_testcase = True
        self.script.append(line)
        self.generated_testcases.append(line)

    def __append_documentation_to_list(self, row):
        self.found_documentation = True
        self.found_documentation_first_row = True
        self.script.append('    [Documentation]    ' + row[tc_name])

    def __append_tags_to_list(self, row):
        if not self.found_documentation:
            self.found_documentation = True
            self.script.append(
                '    [Documentation]    ' + row[tc_name])
        self.found_tags = True
        self.found_tags_first_row = True
        self.__add_tag(row)

    def __exceptional_case(self, row):
        if not self.found_documentation:
            self.found_documentation = True
            self.script.append('    [Documentation]    ' + row[tc_name])
        if not self.found_tags:
            self.found_tags = True
            self.__add_tag(row)

    def __is_end_of_testcases_section(self, line):
        return line.startswith('***')

    def __append_to_list(self, line):
        self.script.append(line)
        self.found_documentation_first_row = False
        self.found_tags_first_row = False

    def __is_documentation(self, line):
        return line.startswith('    [Documentation]')

    def __is_tags(self, line):
        return line.startswith('    [Tags]')

    def __is_testcase_section(self, line):
        return self.match(line, '*** test cases ***')

    def __set_variables_when_found_new_testcase_number(self, line):
        if re.search('^[A-Za-z]+-[0-9]+$', line):
            if self.found_testcase:
                self.found_testcase = False
                self.found_new_testcase = True
            else:
                self.found_testcase = True

    def __not_found_testcase_or_not_end_of_testcase(self, line):
        if not self.found_testcase and not self.found_new_testcase:
            return True
        return False

    def gen_new_testcase(self, row):
        self.__set_variables_to_default()
        self.script.append(row[tc_no])
        self.script.append('    ' + '[Documentation]' + '    ' + row[tc_name])
        self.__add_tag(row)
        self.script.append('')

    def find_testcase_script_from_testcases_row(self, row):
        self.__set_variables_to_default()
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
        old_robot_file.close()

    def find_testcases_not_generated(self):
        self.__set_variables_to_default()
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip('\n')
            if self.__is_testcase_section(line):
                self.found_testcases_section = True
                continue
            if not self.found_testcases_section:
                continue
            self.__set_variables_when_found_new_testcase_number(line)
            if self.__not_found_testcase_or_not_end_of_testcase(line):
                continue
            if self.__is_testcase_generated(line):
                continue
            if self.__is_end_of_testcases_section(line):
                break
            self.script.append(line)
        old_robot_file.close()

    def generate_testcases_from_testcases_file(self):
        df = pd.read_excel(self.testcases_file_path, usecols='D, E, M, Q, Y')
        for index, row in df.iterrows():
            self.find_testcase_script_from_testcases_row(row)
            if not self.script:
                self.gen_new_testcase(row)
                self.write_list_into_file(self.script, '\n')
                continue
            if index == 0:
                self.script.insert(0, '*** Test Cases ***')
            self.write_list_into_file(self.script, '\n')

    def generate_remaining_testcases(self):
        self.find_testcases_not_generated()
        if not self.script:
            return
        self.write_list_into_file(self.script, '\n')
