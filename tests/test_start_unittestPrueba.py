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

    def find_elements_by_id(self, idval):
        pattern = re.compile(rf"<([a-z0-9]+)(?:\s[^>]*)?\sid=[\'\"]{idval}[\'\"](?:[^>]*)>(.*?)</\1>", re.S | re.I)
        return [m.group(0) for m in pattern.finditer(self.html)]

    def find_elements_by_name(self, name):
        pattern = re.compile(rf"<([a-z0-9]+)(?:\s[^>]*)?\sname=[\'\"]{name}[\'\"](?:[^>]*)>(.*?)</\1>", re.S | re.I)
        return [m.group(0) for m in pattern.finditer(self.html)]

    def find_elements_by_class_name(self, cls):
        pattern = re.compile(rf"<([a-z0-9]+)(?:\s[^>]*)?\sclass=[\'\"][^\'\"]*\b{cls}\b[^\'\"]*[\'\"](?:[^>]*)>(.*?)</\1>", re.S | re.I)
        return [m.group(0) for m in pattern.finditer(self.html)]

    def find_elements_by_css_selector(self, sel):
        sel = sel.strip()
        if sel.startswith('#'):
            return self.find_elements_by_id(sel[1:])
        if sel.startswith('.'):
            return self.find_elements_by_class_name(sel[1:])
        if '.' in sel:
            tag, cls = sel.split('.', 1)
            return [el for el in self.find_elements_by_tag_name(tag) if f'class="{cls}' in el or f"class='{cls}" in el or f' {cls} ' in el]
        return self.find_elements_by_tag_name(sel)

    def find_elements_by_link_text(self, text):
        pattern = re.compile(rf"<a(?:\s[^>]*)?>(\s*{re.escape(text)}\s*)</a>", re.S | re.I)
        return [m.group(0) for m in pattern.finditer(self.html)]

    def find_elements_by_partial_link_text(self, partial):
        pattern = re.compile(rf"<a(?:\s[^>]*)?>(.*?)</a>", re.S | re.I)
        return [m.group(0) for m in pattern.finditer(self.html) if partial in _inner_text(m.group(0))]

    def find_elements_by_xpath(self, xpath):
        m = re.match(r"//([a-zA-Z0-9]+)$", xpath)
        if m:
            return self.find_elements_by_tag_name(m.group(1))
        return []


class TestSimpleFinds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = os.path.dirname(os.path.dirname(__file__))
        cls.page = SimpleHTML(os.path.join(root, 'index.html'))

    def test_find_by_id(self):
        els = self.page.find_elements_by_id('primera')
        self.assertTrue(len(els) >= 1)
        self.assertIn('table', els[0].lower())

    def test_find_by_tag_count_rows(self):
        rows = self.page.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 3)

    def test_find_by_class(self):
        rojo = self.page.find_elements_by_class_name('rojo')
        self.assertTrue(len(rojo) >= 1)
        txt = _inner_text(rojo[0])
        self.assertIn('1', txt)

    def test_find_link_text_and_partial(self):
        exact = self.page.find_elements_by_link_text('Pagina 2')
        self.assertTrue(len(exact) >= 1)
        partial = self.page.find_elements_by_partial_link_text('Link 1')
        self.assertTrue(len(partial) >= 1)

    def test_find_by_name_and_select(self):
        selects = self.page.find_elements_by_name('ingrediente')
        self.assertTrue(len(selects) >= 1)


if __name__ == '__main__':
    unittest.main()
