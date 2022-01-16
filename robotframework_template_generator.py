import sys
from Classes.settings import Settings
from Classes.keywords import Keywords
from Classes.variables import Variables
from Classes.testcases import Testcases


testcases_file_path = sys.argv[1]
old_robot_file_path = sys.argv[2]
new_robot_file_path = sys.argv[3]


class RobotTemplateGenerator():

    def __init__(self):
        self.new_robot_file = open(new_robot_file_path, 'w+')

    def write_list_into_file(self, list, splitter):
        for line in list:
            self.new_robot_file.write(line + splitter)

    def generate_testcases_section(self):
        testcases = Testcases(testcases_file_path,
                              old_robot_file_path, self.new_robot_file)
        testcases.generate_testcases_from_testcases_file()
        testcases.generate_remaining_testcases()

    def generate_variables_section(self):
        variables = Variables(old_robot_file_path)
        variables.find_variables_script()
        if not variables.script:
            return
        self.write_list_into_file(variables.script, '\n')

    def generate_keywords_section(self):
        keywords = Keywords(old_robot_file_path)
        keywords.find_keywords_script()
        if not keywords.script:
            return
        self.write_list_into_file(keywords.script, '\n')

    def generate_settings_section(self):
        settings = Settings(old_robot_file_path)
        settings.find_settings_script()
        if not settings.script:
            return
        self.write_list_into_file(settings.script, '\n')

    def generate_robot_template(self):
        self.generate_settings_section()
        self.generate_variables_section()
        self.generate_testcases_section()
        self.generate_keywords_section()


def main():
    robot_template_generator = RobotTemplateGenerator()
    robot_template_generator.generate_robot_template()
    robot_template_generator.new_robot_file.close()


if __name__ == '__main__':
    main()
