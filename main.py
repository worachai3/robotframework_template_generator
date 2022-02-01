import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QCheckBox


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Robot Template Gen'
        self.left = 10
        self.top = 10
        self.width = 270
        self.height = 200
        self.initUI()
        self.old_robot_file_path = ''
        self.new_robot_file_path = ''
        self.testcase_path = ''
        self.option_checkbox = QCheckBox('Merge tags with old script', self)
        self.option_checkbox.setGeometry(5, 90, 300, 20)

        browse_old_script_button = QPushButton('Old Script', self)
        browse_old_script_button.setGeometry(0, 0, 135, 90)
        browse_old_script_button.clicked.connect(
            lambda: self.get_old_robot_script())

        browse_test_case_button = QPushButton('Test Cases', self)
        browse_test_case_button.setGeometry(135, 0, 135, 90)
        browse_test_case_button.clicked.connect(
            lambda: self.get_test_case_file())

        generate_new_file_button = QPushButton('Generate', self)
        generate_new_file_button.setGeometry(0, 110, 270, 90)
        generate_new_file_button.clicked.connect(
            lambda: self.run_python_script())

        self.show()

    def run_python_script(self):
        if self.option_checkbox.isChecked():
            os.system(
                f'python3 robotframework_template_generator.py {self.testcase_path} {self.old_robot_file_path} new.robot y')
        else:
            os.system(
                f'python3 robotframework_template_generator.py {self.testcase_path} {self.old_robot_file_path} new.robot n')

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def get_old_robot_script(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.old_robot_file_path, _ = QFileDialog.getOpenFileName(
            self, "Old Robot Script File", "", "Robot Script File (*.robot)", options=options)

    def get_new_robot_script(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.new_robot_file_path, _ = QFileDialog.getOpenFileNames(
            self, "New Robot Script File", "", "Robot Script File (*.robot)", options=options)

    def get_test_case_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.testcase_path, _ = QFileDialog.getOpenFileName(
            self, "Test Case File", "", "Excel File (*.xlsx)", options=options)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
