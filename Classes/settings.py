from Classes.base import Base


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
