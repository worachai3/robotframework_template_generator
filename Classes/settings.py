from Classes.base import Base


class Settings(Base):

    def __init__(self, old_robot_file_path):
        Base.__init__(self)
        self.old_robot_file_path = old_robot_file_path
        self.found_settings_section = False
        self.script = []

    def find_settings_script(self):
        self.found_settings_section = False
        self.script = []
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip('\n')
            if self.match(line, '*** settings ***'):
                self.found_settings_section = True
                self.script.append('*** Settings ***')
                continue
            if not self.found_settings_section:
                continue
            if line.startswith('***'):
                break
            self.script.append(line)
        old_robot_file.close()
