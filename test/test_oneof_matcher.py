import unittest

from beetsplug.extendedmetadata import ExtendedMetaDataMatchQuery


class ExtendedMetaDataMatchQueryTest(unittest.TestCase):

    def setUp(self):
        # {"origin":"korea","language":["korean","english"],"vocal_gender":"male", "genre":"k-pop", "tag":["two words"], "test":"two words", "jpn_word":"けいおん!"}
        self.extended_metadata = 'EMD: eyJvcmlnaW4iOiJrb3JlYSIsImxhbmd1YWdlIjpbImtvcmVhbiIsImVuZ2xpc2giXSwidm9jYWxfZ2VuZGVyIjoibWFsZSIsICJnZW5yZSI6ImstcG9wIiwgInRhZyI6WyJ0d28gd29yZHMiXSwgInRlc3QiOiJ0d28gd29yZHMiLCAianBuX3dvcmQiOiLjgZHjgYTjgYrjgpMhIn0='
        self.sut = ExtendedMetaDataMatchQuery(None, None)

    # INVALID PATTERNS #
    def test_invalid_pattern(self):
        self.assertFalse(self.sut.value_match('language:,', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:,korean', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:korean,', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:korean,english,', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:!', self.extended_metadata))

    def test_empty_json(self):
        self.assertFalse(self.sut.value_match('origin:', '{}'))

    def test_empty_non_json(self):
        self.assertFalse(self.sut.value_match('origin:', 'korea'))

    def test_empty_pattern(self):
        self.assertTrue(self.sut.value_match('origin:', self.extended_metadata))

    # SINGLE VALUE #
    def test_valid_pattern(self):
        self.assertTrue(self.sut.value_match('origin:korea', self.extended_metadata))
        self.assertTrue(self.sut.value_match('genre:k-pop', self.extended_metadata))

    def test_different_case(self):
        self.assertTrue(self.sut.value_match('origin:Korea', self.extended_metadata))

    def test_unicode_characters(self):
        self.assertTrue(self.sut.value_match('jpn_word:けいおん!', self.extended_metadata))

    def test_negated(self):
        self.assertFalse(self.sut.value_match('origin:!korea', self.extended_metadata))
        self.assertTrue(self.sut.value_match('origin:!usa', self.extended_metadata))
        self.assertTrue(self.sut.value_match('tag:!vocaloid', self.extended_metadata))

    def test_spaces(self):
        self.assertTrue(self.sut.value_match('tag:two words', self.extended_metadata))
        self.assertTrue(self.sut.value_match('test:two words', self.extended_metadata))

    # MULTI VALUE #
    def test_array_negated(self):
        self.assertFalse(self.sut.value_match('language:!korean', self.extended_metadata))
        self.assertTrue(self.sut.value_match('language:!japanese', self.extended_metadata))
        self.assertTrue(self.sut.value_match('language:!korean,english', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:!korean,!english,', self.extended_metadata))

    def test_array_one_of_match(self):
        self.assertTrue(self.sut.value_match('language:korean,japanese', self.extended_metadata))
        self.assertTrue(self.sut.value_match('language:chinese,english', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:chinese,japanese', self.extended_metadata))

    def test_array_empty_pattern(self):
        self.assertTrue(self.sut.value_match('language:', self.extended_metadata))

    def test_non_existing_pattern(self):
        self.assertFalse(self.sut.value_match('origin:usa', self.extended_metadata))

    def test_array_existing_pattern(self):
        self.assertTrue(self.sut.value_match('language:korean', self.extended_metadata))

    def test_array_existing_pattern_different_case(self):
        self.assertTrue(self.sut.value_match('language:Korean', self.extended_metadata))

    def test_array_non_existing_pattern(self):
        self.assertFalse(self.sut.value_match('language:japanese', self.extended_metadata))
