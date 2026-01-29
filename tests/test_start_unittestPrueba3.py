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


class TestParted(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = os.path.dirname(os.path.dirname(__file__))
        cls.page = SimpleHTML(os.path.join(root, 'index.html'))

    def test_find_table(self):
        tables = re.findall(r"<table[^>]*id=[\'\"]primera[\'\"]", self.page.html, re.I)
        self.assertTrue(len(tables) >= 1)

    def test_trs_via_xpath_like(self):
        rows = self.page.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 3)


if __name__ == '__main__':
    unittest.main()
