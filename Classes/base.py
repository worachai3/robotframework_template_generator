import os


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
        res = [i for n, i in enumerate(list) if i not in list[:n]]
        return res
