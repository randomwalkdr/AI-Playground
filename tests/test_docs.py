import unittest

class TestDocumentation(unittest.TestCase):
    def test_markdown_formatting(self):
        with open('BEST_PRACTICES.md', 'r') as f:
            content = f.read()
            self.assertIn("def validate_data_against_schema", content)
            self.assertIn("[Input Data Validation](#input-data-validation)", content)

if __name__ == '__main__':
    unittest.main()
