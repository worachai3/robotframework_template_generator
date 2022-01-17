import os


class Base:

    def is_empty_file(self, file):
        return os.stat(file).st_size == 0

    def match(self, line, str):
        return line.lower() == str.lower()
