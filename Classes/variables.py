from Classes.base import Base


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
