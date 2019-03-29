import unittest

from beetsplug.extendedmetadata import ExtendedMetaDataMatchQuery


class ExtendedMetaDataMatchQueryTest(unittest.TestCase):

    def setUp(self):
        self.sut = ExtendedMetaDataMatchQuery(None, None)
        # {"origin":"korea","language":"korean","vocal_gender":"female"}
        self.extended_metadata = 'EMD: eyJvcmlnaW4iOiJrb3JlYSIsImxhbmd1YWdlIjoia29yZWFuIiwidm9jYWxfZ2VuZGVyIjoibWFsZSJ9'

    def test_value_match_empty_json(self):
        result = self.sut.value_match('origin:', '{}')
        self.assertFalse(result)

    def test_value_match_empty_non_json(self):
        result = self.sut.value_match('origin:', 'korea')
        self.assertFalse(result)

    def test_value_match_empty_pattern(self):
        result = self.sut.value_match('origin:', self.extended_metadata)
        self.assertTrue(result)

    def test_value_match_regex_empty_pattern(self):
        result = self.sut.value_match('origin::', self.extended_metadata)
        self.assertTrue(result)

    def test_value_match_existing_pattern(self):
        result = self.sut.value_match('origin:korea', self.extended_metadata)
        self.assertTrue(result)

    def test_value_match_existing_pattern_different_case(self):
        result = self.sut.value_match('origin:Korea', self.extended_metadata)
        self.assertTrue(result)

    def test_value_match_regex_existing_pattern(self):
        result = self.sut.value_match('origin::^.*ea$', self.extended_metadata)
        self.assertTrue(result)

    def test_value_match_non_existing_pattern(self):
        result = self.sut.value_match('origin:usa', self.extended_metadata)
        self.assertFalse(result)

    def test_value_match_regex_non_existing_pattern(self):
        result = self.sut.value_match('origin::us.*', self.extended_metadata)
        self.assertFalse(result)

    def test_value_match_array_empty_pattern(self):
        result = self.sut.value_match('language:', self.extended_metadata)
        self.assertTrue(result)

    def test_value_match_array_regex_empty_pattern(self):
        result = self.sut.value_match('language::', self.extended_metadata)
        self.assertTrue(result)

    def test_value_match_array_existing_pattern(self):
        result = self.sut.value_match('language:korean', self.extended_metadata)
        self.assertTrue(result)

    def test_value_match_array_existing_pattern_different_case(self):
        result = self.sut.value_match('language:Korean', self.extended_metadata)
        self.assertTrue(result)

    def test_value_match_array_regex_existing_pattern(self):
        result = self.sut.value_match('language::^.*an$', self.extended_metadata)
        self.assertTrue(result)

    def test_value_match_array_non_existing_pattern(self):
        result = self.sut.value_match('language:english', self.extended_metadata)
        self.assertFalse(result)

    def test_value_match_array_regex_non_existing_pattern(self):
        result = self.sut.value_match('language::en.*', self.extended_metadata)
        self.assertFalse(result)
