import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QCheckBox, QTextEdit, QLabel
import PyQt5.QtGui as QtGui
import re
import pandas as pd

err_missing_param = '''Error: Missing parameter(s).
please run command \'./run.sh -h\' to see how to use script.'''
err_found_dup = 'Please remove duplicated test cases before running script'

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

class Base:

    def is_end_of_section(self, line):
        return line.startswith('***')

    def is_empty_file(self, file):
        return os.stat(file).st_size == 0

    def match(self, line, str):
        return line.lower().strip() == str.lower().strip()

    def append_items_from_list_to_list(self, list1, list2):
        for item in list1:
            list2.append(item)
        return list2

    def in_list(self, item, lis):
        for tag in lis:
            if item.strip().lower() == tag.strip().lower():
                return True

    def remove_duplicate_from_list(self, list):
        res = [i for n, i in enumerate(
            list) if i not in list[:n] and i != '...']
        return res

class Testcases(Base):

    def __init__(self, old_robot_file_path, tag_option):
        Base.__init__(self)
        self.old_robot_file_path = old_robot_file_path
        self.tag_option = tag_option.lower()
        self.generated_testcases = []
        self.script = []

    def __is_not_end_of_tags(self, line):
        return re.search('\.\.\.', line)

    def __is_documentation(self, line):
        return re.search('\[Documentation]', line)

    def __is_tags(self, line):
        return re.search('\[Tags]', line)

    def __is_tc_section(self, line):
        return self.match(line, self.__get_test_cases_string())

    def __is_line_too_long(self, line):
        return len(line) >= self.__get_line_length()

    def __is_tc_generated(self, testcase):
        return testcase in self.generated_testcases

    def __is_end_of_testcase(self, line):
        return self.is_end_of_section(line) or self.__is_tc(line.rstrip())

    def __is_tc_number(self, line):
        return re.search('^[A-Za-z]+-[0-9]+$', line.rstrip())

    def __is_tc(self, line):
        return re.search('^[A-Za-z-0-9]+[ A-Za-z-0-9]+$', line.rstrip())

    def __is_tag_added(self, tag, tag_list):
        for t in tag_list:
            if tag.strip().lower() == t.strip().lower():
                return True

    def __is_match_tc_number(self, line, matcher):
        return self.__is_tc_number(line) and self.match(line, matcher)

    def __is_tc_number_and_is_not_generated(self, line):
        return self.__is_tc_number(line) and not self.__is_tc_generated(line)

    def __is_tc_and_is_not_generated(self, line):
        return self.__is_tc(line) and not self.__is_tc_generated(line)

    def __is_not_test_step_in_tc(self, line, found_tag, found_doc):
        return self.__is_documentation(line) or self.__is_tags(line) or ((
            found_tag or found_doc) and self.__is_not_end_of_tags(line))

    def __is_tag(self, inp):
        return re.search('^[-_A-Za-z0-9!@#$%^&*(). ]+$', inp.strip())

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
        tag_str = self.__get_tag_string()
        for tag in tag_list:
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
        tag_list = self.__add_new_line_to_tag_list(tag_list)
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
        found_tag = False
        found_doc = False
        old_robot_file = open(self.old_robot_file_path)
        for line in old_robot_file:
            if self.__is_match_tc_number(line, testcase_no):
                found_tc = True
                continue
            if not found_tc:
                continue
            if self.__is_tags(line):
                found_tag = True
                found_doc = False
            if self.__is_documentation(line):
                found_doc = True
                found_tag = False
            if self.__is_not_test_step_in_tc(line, found_tag, found_doc):
                continue
            found_doc = False
            found_tag = False
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
        tag_list = tag_str.split('    ')
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
                continue
            if not found_tag:
                continue
            if self.__is_not_end_of_tags(line):
                tag_list = self.__get_tag_list_from_line(line)
                self.append_items_from_list_to_list(tag_list, res_tag_list)
                continue
            else:
                break
        old_robot_file.close()
        self.remove_duplicate_from_list(res_tag_list)
        return res_tag_list

    def __get_tc_name_string(self, testcase_name):
        res = ''
        line = self.__get_documentation_string()
        testcase_name_list = testcase_name.split('\n')

        for index in range(len(testcase_name_list)):
            words = testcase_name_list[index].split(' ')
            for word in words:
                if not self.__is_line_too_long(line):
                    line += word + ' '
                    res += word + ' '
                else:
                    line = '    ...    ' + word + ' '
                    res += '\n    ...    ' + word + ' '
            if index < len(testcase_name_list)-1:
                line = '    ...    '
                res += '\n    ...    '
        res = self.__get_documentation_string() + res
        return res

    def __get_testcases_script_from_exisiting_script(self):
        found_tc = False
        found_tc_section = False
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.rstrip('\n')
            if found_tc_section and line.startswith('***'):
                break
            if self.__is_tc_section(line.strip()):
                found_tc_section = True
                continue
            if not found_tc_section:
                continue
            if self.__is_tc_and_is_not_generated(line):
                found_tc = True
                self.__append_to_list(line)
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
        df = pd.read_excel(tc_file_path)

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

class Settings(Base):

    def __init__(self, old_robot_file_path):
        Base.__init__(self)
        self.old_robot_file_path = old_robot_file_path
        self.script = []

    def generate_settings_script(self):
        found_settings_section = False
        self.script = []
        if self.is_empty_file(self.old_robot_file_path):
            self.script.append('*** Settings ***\n\n')
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip('\n')
            if self.match(line, '*** settings ***'):
                found_settings_section = True
                self.script.append('*** Settings ***')
                continue
            if not found_settings_section:
                continue
            if self.is_end_of_section(line):
                break
            self.script.append(line)
        old_robot_file.close()

class Variables(Base):

    def __init__(self, old_robot_file_path):
        Base.__init__(self)
        self.old_robot_file_path = old_robot_file_path
        self.script = []

    def generate_variables_script(self):
        found_variables_section = False
        self.script = []
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip('\n')
            if self.match(line, '*** variables ***'):
                found_variables_section = True
                self.script.append('*** Variables ***')
                continue
            if not found_variables_section:
                continue
            if self.is_end_of_section(line):
                break
            self.script.append(line)
        old_robot_file.close()

class Keywords(Base):

    def __init__(self, old_robot_file_path):
        Base.__init__(self)
        self.old_robot_file_path = old_robot_file_path
        self.script = []

    def generate_keywords_script(self):
        found_keywords = False
        self.script = []
        if self.is_empty_file(self.old_robot_file_path):
            return
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip('\n')
            if self.match(line, '*** keywords ***'):
                found_keywords = True
                self.script.append('*** Keywords ***')
                continue
            if not found_keywords:
                continue
            if self.is_end_of_section(line):
                break
            self.script.append(line)
        old_robot_file.close()

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

def set_file_path(testcases,old,new,tag):
        global testcases_file_path
        global old_robot_file_path
        global new_robot_file_path
        global tag_option
        global no_old
        if(old == ''):
            no_old = True
            old = '/tmp/old.robot'
            os.system(f'touch {old}')
        else:
            no_old = False
        testcases_file_path = testcases
        old_robot_file_path = old
        new_robot_file_path = new
        tag_option = tag

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


def run_robot_main(testcases,old,new,tag):
    set_file_path(testcases,old,new,tag)
    check_testcases_duplicate_in_old_script()
    check_testcases_duplicate_in_testcases_file()
    robot_template_generator = RobotTemplateGenerator()
    robot_template_generator.generate_robot_template()
    robot_template_generator.new_robot_file.close()
    if no_old:
        os.system('rm /tmp/old.robot')

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Robot Template Generator'
        self.left = 10
        self.top = 10
        self.width = 1185
        self.height = 140
        self.setFixedSize(self.width, self.height)
        self.initUI()
        self.old_robot_file_path = ''
        self.new_robot_file_path = ''
        self.testcase_path = ''

        self.show()

    def run_python_script(self):
        if self.option_checkbox.isChecked():
            try:
                if self.new_robot_file_path != '' and self.testcase_path != '':
                    run_robot_main(self.testcase_path,self.old_robot_file_path,f'{self.new_robot_file_path}/new.robot','y')
                if self.new_robot_file_path == '':
                    self.new_script_file_path_text.setText('Please select directory for new robot file')
                else:
                    self.new_script_file_path_text.setText(
                        f'{self.new_robot_file_path}/new.robot')
                if self.testcase_path == '':
                    self.testcase_file_path_text.setText('Please select testcase file')
                else:
                    self.testcase_file_path_text.setText(self.testcase_path)
            except Exception as e:
                print(e)
        else:
            try:
                if self.new_robot_file_path != '' and self.testcase_path != '':
                    run_robot_main(self.testcase_path,self.old_robot_file_path,f'{self.new_robot_file_path}/new.robot','n')
                if self.new_robot_file_path == '':
                    self.new_script_file_path_text.setText('Please select directory for new robot file')
                else:
                    self.new_script_file_path_text.setText(
                        f'{self.new_robot_file_path}/new.robot')
                if self.testcase_path == '':
                    self.testcase_file_path_text.setText('Please select testcase file')
                else:
                    self.testcase_file_path_text.setText(self.testcase_path)
            except Exception as e:
                print(e)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.option_checkbox = QCheckBox(
            'Merge tags in test cases file with old script', self)
        self.option_checkbox.setGeometry(5, 105, 300, 20)

        self.new_script_file_path_text = QTextEdit(self)
        self.old_script_file_path_text = QTextEdit(self)
        self.testcase_file_path_text = QTextEdit(self)

        self.new_script_file_path_text.setReadOnly(True)
        self.old_script_file_path_text.setReadOnly(True)
        self.testcase_file_path_text.setReadOnly(True)

        self.new_script_file_path_text.setFont(QtGui.QFont('Arial', 10))
        self.old_script_file_path_text.setFont(QtGui.QFont('Arial', 10))
        self.testcase_file_path_text.setFont(QtGui.QFont('Arial', 10))

        self.testcase_file_path_text.setGeometry(90, 5, 1005, 30)
        self.old_script_file_path_text.setGeometry(90, 36, 1005, 30)
        self.new_script_file_path_text.setGeometry(90, 67, 1005, 30)

        self.old_script_file_path_label = QLabel(self)
        self.old_script_file_path_label.setText('Old Script')
        self.old_script_file_path_label.setGeometry(10, 37, 90, 30)
        self.browse_old_script_button = QPushButton('Browse', self)
        self.browse_old_script_button.setGeometry(1095, 37, 90, 30)
        self.browse_old_script_button.clicked.connect(
            lambda: self.get_old_robot_script())

        self.new_script_file_path_label = QLabel(self)
        self.new_script_file_path_label.setText('New Script')
        self.new_script_file_path_label.setGeometry(10, 67, 90, 30)
        self.browse_new_script_button = QPushButton('Browse', self)
        self.browse_new_script_button.setGeometry(1095, 67, 90, 30)
        self.browse_new_script_button.clicked.connect(
            lambda: self.get_new_robot_script())

        self.test_case_file_path_label = QLabel(self)
        self.test_case_file_path_label.setText('Test Cases')
        self.test_case_file_path_label.setGeometry(10, 6, 90, 30)
        self.browse_test_case_button = QPushButton('Browse', self)
        self.browse_test_case_button.setGeometry(1095, 6, 90, 30)
        self.browse_test_case_button.clicked.connect(
            lambda: self.get_test_case_file())

        self.generate_new_file_button = QPushButton('Generate', self)
        self.generate_new_file_button.setGeometry(550, 100, 90, 30)
        self.generate_new_file_button.clicked.connect(
            lambda: self.run_python_script())

    def get_old_robot_script(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.old_robot_file_path, _ = QFileDialog.getOpenFileName(
            self, "Old Robot Script File", "", "Robot Script File (*.robot)", options=options)
        self.old_script_file_path_text.setText(self.old_robot_file_path)

    def get_new_robot_script(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.new_robot_file_path = QFileDialog.getExistingDirectory(
            self, "Select Directory")
        if self.new_robot_file_path == '':
            self.new_script_file_path_text.setText('Please select directory for new robot file')
        else:
            self.new_script_file_path_text.setText(
                f'{self.new_robot_file_path}/new.robot')

    def get_test_case_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.testcase_path, _ = QFileDialog.getOpenFileName(
            self, "Test Case File", "", "Excel File (*.xlsx)", options=options)
        if self.testcase_path == '':
            self.testcase_file_path_text.setText('Please select testcase file')
        else:
            self.testcase_file_path_text.setText(self.testcase_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
