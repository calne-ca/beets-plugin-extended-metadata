import unittest

from beetsplug.extendedmetadata import ExtendedMetaDataMatchQuery


class ExtendedMetaDataMatchQueryTest(unittest.TestCase):

    def setUp(self):
        # {"origin":"korea","language":["korean","english"],"vocal_gender":"male", "genre":"k-pop", "tag":["two words"], "test":"two words", "jpn_word":"けいおん!"}
        self.extended_metadata = 'EMD: eyJvcmlnaW4iOiJrb3JlYSIsImxhbmd1YWdlIjpbImtvcmVhbiIsImVuZ2xpc2giXSwidm9jYWxfZ2VuZGVyIjoibWFsZSIsICJnZW5yZSI6ImstcG9wIiwgInRhZyI6WyJ0d28gd29yZHMiXSwgInRlc3QiOiJ0d28gd29yZHMiLCAianBuX3dvcmQiOiLjgZHjgYTjgYrjgpMhIn0='
        self.sut = ExtendedMetaDataMatchQuery(None, None)

    # SINGLE VALUE #
    def test_invalid_pattern(self):
        self.assertFalse(self.sut.value_match('language::^$^', self.extended_metadata))

    def test_empty_pattern(self):
        self.assertTrue(self.sut.value_match('origin::', self.extended_metadata))

    def test_existing_pattern(self):
        self.assertTrue(self.sut.value_match('origin::^.*ea$', self.extended_metadata))

    def test_non_existing_pattern(self):
        self.assertFalse(self.sut.value_match('origin::us.*', self.extended_metadata))

    # MULTI VALUE #
    def test_array_empty_pattern(self):
        self.assertTrue(self.sut.value_match('language::', self.extended_metadata))

    def test_array_existing_pattern(self):
        self.assertTrue(self.sut.value_match('language::^.*an$', self.extended_metadata))

    def test_array_non_existing_pattern(self):
        self.assertFalse(self.sut.value_match('language::ja.*', self.extended_metadata))
