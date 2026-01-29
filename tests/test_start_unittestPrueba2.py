import os
import re
import unittest

def _inner_text(html):
    return re.sub(r"<.*?>", "", html, flags=re.S).strip()


class SimpleHTML:
    def __init__(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            self.html = f.read()

    def find_elements_by_tag_name(self, tag):
        pattern = re.compile(rf"<({tag})(?:\s[^>]*)?>(.*?)</{tag}>", re.S | re.I)
        return [m.group(0) for m in pattern.finditer(self.html)]

    def find_elements_by_class_name(self, cls):
        pattern = re.compile(rf"<([a-z0-9]+)(?:\s[^>]*)?\sclass=[\'\"][^\'\"]*\b{cls}\b[^\'\"]*[\'\"](?:[^>]*)>(.*?)</\1>", re.S | re.I)
        return [m.group(0) for m in pattern.finditer(self.html)]

    def find_elements_by_partial_link_text(self, partial):
        pattern = re.compile(rf"<a(?:\s[^>]*)?>(.*?)</a>", re.S | re.I)
        return [m.group(0) for m in pattern.finditer(self.html) if partial in _inner_text(m.group(0))]


class Part1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = os.path.dirname(os.path.dirname(__file__))
        cls.page = SimpleHTML(os.path.join(root, 'index.html'))

    def test_rows_count(self):
        rows = self.page.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 3)

    def test_class_rojo_present(self):
        rojo = self.page.find_elements_by_class_name('rojo')
        self.assertTrue(rojo)


class Part2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = os.path.dirname(os.path.dirname(__file__))
        cls.page = SimpleHTML(os.path.join(root, 'index.html'))

    def test_partial_link(self):
        found = self.page.find_elements_by_partial_link_text('Link')
        self.assertTrue(len(found) >= 1)

    def test_table_has_name(self):
        pattern = re.compile(r"<table[^>]*\sname=[\'\"]tabla_prueba[\'\"]", re.I)
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'index.html'), 'r', encoding='utf-8') as f:
            html = f.read()
        self.assertTrue(bool(pattern.search(html)))


if __name__ == '__main__':
    unittest.main()
