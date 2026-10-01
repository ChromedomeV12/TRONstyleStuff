import copy
import unittest
from prepare import BEGIN, END, merge_fixes, merge_settings


class PreserveExports(unittest.TestCase):
    def test_settings_preserve_unrelated_preferences(self):
        original = {'theme': {'engine': 'staticTheme', 'fontFamily': 'Example', 'stylesheet': 'old'},
                    'enabled': False, 'siteList': ['example.com'],
                    'customThemes': [{'url': ['sample.test'], 'theme': {'mode': 0}}],
                    'automation': {'enabled': True}, 'futureField': {'nested': [1, 2]}}
        untouched = copy.deepcopy(original)
        result = merge_settings(original)
        self.assertEqual(original, untouched)
        self.assertEqual(result['theme']['engine'], 'dynamicTheme')
        self.assertEqual(result['theme']['fontFamily'], 'Example')
        self.assertEqual(result['theme']['stylesheet'], 'old')
        for key in original.keys() - {'theme'}:
            self.assertEqual(result[key], original[key])

    def test_fixes_keep_other_directives_and_site_blocks(self):
        sites = '================================\n\nexample.com\n\nCSS\n.x { color: red; }\n'
        original = '*\n\nINVERT\n.logo\n\nCSS\n.keep { color: blue; }\n\nIGNORE CSS URL\n/data/\n\n' + sites
        result = merge_fixes(original)
        self.assertTrue(result.endswith(sites))
        self.assertIn('INVERT\n.logo', result)
        self.assertIn('.keep { color: blue; }', result)
        self.assertIn('IGNORE CSS URL\n/data/', result)
        self.assertLess(result.index(END), result.index('IGNORE CSS URL'))
        self.assertEqual(merge_fixes(result), result)

    def test_missing_css(self):
        result = merge_fixes('*\n\nINVERT\n.logo\n')
        self.assertIn('INVERT\n.logo\n\nCSS\n', result)
        self.assertEqual(result.count(BEGIN), 1)

    def test_refuse_wrong_or_malformed_input(self):
        for text in ['', 'example.com\nCSS\n', '*\nCSS\n' + BEGIN,
                     '*\nCSS\n' + END + BEGIN, '*\nCSS\nCSS\n']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                merge_fixes(text)
        with self.assertRaises(ValueError):
            merge_settings({'enabled': True})


if __name__ == '__main__':
    unittest.main()
