import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QCheckBox, QTextEdit, QLabel
import PyQt5.QtGui as QtGui


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Robot Template Gen'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 125
        self.setFixedSize(self.width, self.height)
        self.initUI()
        self.old_robot_file_path = ''
        self.new_robot_file_path = ''
        self.testcase_path = ''

        self.show()

    def run_python_script(self):
        if self.option_checkbox.isChecked():
            os.system(
                f'python3 robotframework_template_generator.py {self.testcase_path} {self.old_robot_file_path} {self.new_robot_file_path}/new.robot y')
        else:
            os.system(
                f'python3 robotframework_template_generator.py {self.testcase_path} {self.old_robot_file_path} {self.new_robot_file_path}/new.robot n')

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.option_checkbox = QCheckBox(
            'Merge tags in test cases file with old script', self)
        self.option_checkbox.setGeometry(5, 95, 300, 20)

        self.new_script_file_path_text = QTextEdit(self)
        self.old_script_file_path_text = QTextEdit(self)
        self.testcase_file_path_text = QTextEdit(self)

        self.new_script_file_path_text.setReadOnly(True)
        self.old_script_file_path_text.setReadOnly(True)
        self.testcase_file_path_text.setReadOnly(True)

        self.new_script_file_path_text.setFont(QtGui.QFont('Arial', 10))
        self.old_script_file_path_text.setFont(QtGui.QFont('Arial', 10))
        self.testcase_file_path_text.setFont(QtGui.QFont('Arial', 10))

        self.testcase_file_path_text.setGeometry(90, 0, 1005, 30)
        self.old_script_file_path_text.setGeometry(90, 30, 1005, 30)
        self.new_script_file_path_text.setGeometry(90, 60, 1005, 30)

        self.old_script_file_path_label = QLabel(self)
        self.old_script_file_path_label.setText('Old Script')
        self.old_script_file_path_label.setGeometry(10, 30, 90, 30)
        self.browse_old_script_button = QPushButton('Browse', self)
        self.browse_old_script_button.setGeometry(1100, 30, 90, 30)
        self.browse_old_script_button.clicked.connect(
            lambda: self.get_old_robot_script())

        self.new_script_file_path_label = QLabel(self)
        self.new_script_file_path_label.setText('New Script')
        self.new_script_file_path_label.setGeometry(10, 60, 90, 30)
        self.browse_new_script_button = QPushButton('Browse', self)
        self.browse_new_script_button.setGeometry(1100, 60, 90, 30)
        self.browse_new_script_button.clicked.connect(
            lambda: self.get_new_robot_script())

        self.test_case_file_path_label = QLabel(self)
        self.test_case_file_path_label.setText('Test Cases')
        self.test_case_file_path_label.setGeometry(10, 0, 90, 30)
        self.browse_test_case_button = QPushButton('Browse', self)
        self.browse_test_case_button.setGeometry(1100, 0, 90, 30)
        self.browse_test_case_button.clicked.connect(
            lambda: self.get_test_case_file())

        self.generate_new_file_button = QPushButton('Generate', self)
        self.generate_new_file_button.setGeometry(550, 92, 90, 30)
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
        self.new_script_file_path_text.setText(
            f'{self.new_robot_file_path}/new.robot')

    def get_test_case_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.testcase_path, _ = QFileDialog.getOpenFileName(
            self, "Test Case File", "", "Excel File (*.xlsx)", options=options)
        self.testcase_file_path_text.setText(self.testcase_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
