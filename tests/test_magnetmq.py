import unittest
from magnetmq import is_magnet_link

class TestIsMagnetLink(unittest.TestCase):
    def test_valid_magnet_link(self):
        self.assertTrue(is_magnet_link("magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567"))
        self.assertTrue(is_magnet_link("magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef0123456789abcdef"))
        self.assertTrue(is_magnet_link("magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567&dn=example"))
    
    def test_invalid_magnet_link(self):
        self.assertFalse(is_magnet_link("magxxnet:?xt=urn:btih:0123456789abcdef0123456789abcdef0123456"))
        self.assertFalse(is_magnet_link("magnet:?xt=urn:btih:!0123456789abcdef0123456789abcdef0123456789abcdeg"))
        self.assertFalse(is_magnet_link("https://example.com"))
