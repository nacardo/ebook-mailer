import re


class Book:

    def __init__(self, name):
        self.name = name

    def get_title(self):
        name_no_scores = re.sub('_', ' ', self.name)
        print(name_no_scores)
        if 'by ' in self.name:
            title = re.search(r'[\w\s]*(?=\sby\s)', name_no_scores, re.I)
            if title:
                return title[0]
        else:
            return str(name_no_scores).split('-')[0].strip()

    def get_author(self):

        name_no_scores = re.sub('_', ' ', self.name)
        if 'by ' in self.name:
            pattern = re.compile(r'(?:by\s)[\w\s]*')
            author = re.search(pattern, name_no_scores, re.I)
            if author:
                return author[0]
        else:
            return str(name_no_scores).split('-')[0].strip()

    def strip_extension(self):
        return ''.join(str(self.name).split('.')[:-1])

    def change_extension(self, ext: str):
        new_name = ''.join(str(self.name).split('.')[:-1]) + '.' + ext
        return new_name
