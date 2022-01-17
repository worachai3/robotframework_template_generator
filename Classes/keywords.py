from Classes.base import Base


class Keywords(Base):

    def __init__(self, old_robot_file_path):
        Base.__init__(self)
        self.old_robot_file_path = old_robot_file_path
        self.found_keywords = False
        self.script = []

    def find_keywords_script(self):
        self.found_keywords = False
        self.script = []
        if self.is_empty_file(self.old_robot_file_path):
            return
        old_robot_file = open(self.old_robot_file_path, 'r+')
        for line in old_robot_file:
            line = line.strip('\n')
            if self.match(line, '*** keywords ***'):
                self.found_keywords = True
                self.script.append('*** Keywords ***')
                continue
            if not self.found_keywords:
                continue
            if self.is_end_of_section(line):
                break
            self.script.append(line)
        old_robot_file.close()
