import unittest

from beetsplug.extendedmetadata import ExtendedMetaDataMatchQuery


class ExtendedMetaDataMatchQueryTest(unittest.TestCase):

    def setUp(self):
        # {"origin":"korea","language":["korean","english"],"vocal_gender":"male"}
        self.extended_metadata = 'EMD: eyJvcmlnaW4iOiJrb3JlYSIsImxhbmd1YWdlIjpbImtvcmVhbiIsImVuZ2xpc2giXSwidm9jYWxfZ2VuZGVyIjoibWFsZSIsICJnZW5yZSI6ImstcG9wIn0='
        self.sut = ExtendedMetaDataMatchQuery(None, None)

    def test_value_match_invalid_pattern(self):
        self.assertFalse(self.sut.value_match('language:,', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:,korean', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:korean,', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:korean,english,', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:!', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:!!japanese', self.extended_metadata))

    def test_value_match_empty_json(self):
        self.assertFalse(self.sut.value_match('origin:', '{}'))

    def test_value_match_empty_non_json(self):
        self.assertFalse(self.sut.value_match('origin:', 'korea'))

    def test_value_match_empty_pattern(self):
        self.assertTrue(self.sut.value_match('origin:', self.extended_metadata))

    def test_value_match_existing_pattern(self):
        self.assertTrue(self.sut.value_match('origin:korea', self.extended_metadata))
        self.assertTrue(self.sut.value_match('genre:k-pop', self.extended_metadata))

    def test_value_match_existing_pattern_different_case(self):
        self.assertTrue(self.sut.value_match('origin:Korea', self.extended_metadata))

    def test_value_match_negated_pattern(self):
        self.assertFalse(self.sut.value_match('origin:!korea', self.extended_metadata))
        self.assertTrue(self.sut.value_match('origin:!usa', self.extended_metadata))

    def test_value_match_array_negated_pattern(self):
        self.assertFalse(self.sut.value_match('language:!korean', self.extended_metadata))
        self.assertTrue(self.sut.value_match('language:!japanese', self.extended_metadata))
        self.assertTrue(self.sut.value_match('language:!korean,english', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:!korean,!english,', self.extended_metadata))

    def test_value_match_array_multiple_existing_pattern(self):
        self.assertTrue(self.sut.value_match('language:korean,japanese', self.extended_metadata))
        self.assertTrue(self.sut.value_match('language:chinese,english', self.extended_metadata))
        self.assertFalse(self.sut.value_match('language:chinese,japanese', self.extended_metadata))

    def test_value_match_array_empty_pattern(self):
        self.assertTrue(self.sut.value_match('language:', self.extended_metadata))

    def test_value_match_non_existing_pattern(self):
        self.assertFalse(self.sut.value_match('origin:usa', self.extended_metadata))

    def test_value_match_array_existing_pattern(self):
        self.assertTrue(self.sut.value_match('language:korean', self.extended_metadata))

    def test_value_match_array_existing_pattern_different_case(self):
        self.assertTrue(self.sut.value_match('language:Korean', self.extended_metadata))

    def test_value_match_array_non_existing_pattern(self):
        self.assertFalse(self.sut.value_match('language:japanese', self.extended_metadata))

    def test_value_match_regex_invalid_pattern(self):
        self.assertFalse(self.sut.value_match('language::^$^', self.extended_metadata))

    def test_value_match_regex_empty_pattern(self):
        self.assertTrue(self.sut.value_match('origin::', self.extended_metadata))

    def test_value_match_regex_existing_pattern(self):
        self.assertTrue(self.sut.value_match('origin::^.*ea$', self.extended_metadata))

    def test_value_match_regex_non_existing_pattern(self):
        self.assertFalse(self.sut.value_match('origin::us.*', self.extended_metadata))

    def test_value_match_array_regex_empty_pattern(self):
        self.assertTrue(self.sut.value_match('language::', self.extended_metadata))

    def test_value_match_array_regex_existing_pattern(self):
        self.assertTrue(self.sut.value_match('language::^.*an$', self.extended_metadata))

    def test_value_match_array_regex_non_existing_pattern(self):
        self.assertFalse(self.sut.value_match('language::ja.*', self.extended_metadata))
