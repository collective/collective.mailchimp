
import unittest


class TestUnit(unittest.TestCase):
    def test_list_id_allowed(self):
        from collective.mailchimp.browser.newsletter import CHARS_ALLOWED as allowed

        self.assertTrue(allowed("abcde12345"))
        self.assertTrue(allowed("12345ABCDE"))
        self.assertTrue(allowed("4f17c3b08a"))
        self.assertTrue(allowed("html"))
        self.assertTrue(allowed("plain-text"))
        self.assertTrue(allowed("text/plain"))
        self.assertTrue(allowed("maurits@example.org"))
        self.assertTrue(allowed("maurits+test@example.org"))
        self.assertFalse(allowed("abcde1234' hack em"))
        self.assertFalse(allowed("abcde1234;"))
        self.assertFalse(allowed("abcde1234?"))
