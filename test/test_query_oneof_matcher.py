import unittest

from beetsplug.extendedmetadata import ExtendedMetaDataMatchQuery
from mockito import mockito, when, mock, unstub


class ExtendedMetaDataMatchQueryTest(unittest.TestCase):

    def setUp(self):
        # {"origin":"korea","language":["korean","english"],"vocal_gender":"male", "genre":"k-pop", "tag":["two words"], "test":"two words", "jpn_word":"けいおん!"}
        self.extended_metadata = 'EMD: eyJvcmlnaW4iOiJrb3JlYSIsImxhbmd1YWdlIjpbImtvcmVhbiIsImVuZ2xpc2giXSwidm9jYWxfZ2VuZGVyIjoibWFsZSIsICJnZW5yZSI6ImstcG9wIiwgInRhZyI6WyJ0d28gd29yZHMiXSwgInRlc3QiOiJ0d28gd29yZHMiLCAianBuX3dvcmQiOiLjgZHjgYTjgYrjgpMhIn0='
        self.emd_item = self.item(self.extended_metadata)
        ExtendedMetaDataMatchQuery.input_field = 'comments'

    def tearDown(self):
        unstub()

    def query(self, val):
        return ExtendedMetaDataMatchQuery(val)

    def item(self, emd):
        item = mock()
        when(item).__getitem__('comments').thenReturn(emd)
        return item

    # INVALID PATTERNS #
    def test_invalid_pattern(self):
        self.assertFalse(self.query('language:,').match(self.emd_item))
        self.assertFalse(self.query('language:,korean').match(self.emd_item))
        self.assertFalse(self.query('language:korean,').match(self.emd_item))
        self.assertFalse(self.query('language:korean,english,').match(self.emd_item))
        self.assertFalse(self.query('language:!').match(self.emd_item))

    def test_empty_json(self):
        self.assertFalse(self.query('origin:').match(self.item('{}')))

    def test_empty_non_json(self):
        self.assertFalse(self.query('origin:').match(self.item('korea')))

    def test_empty_pattern(self):
        self.assertTrue(self.query('origin:').match(self.emd_item))

    # SINGLE VALUE #
    def test_valid_pattern(self):
        self.assertTrue(self.query('origin:korea').match(self.emd_item))
        self.assertTrue(self.query('genre:k-pop').match(self.emd_item))

    def test_different_case(self):
        self.assertTrue(self.query('origin:Korea').match(self.emd_item))

    def test_unicode_characters(self):
        self.assertTrue(self.query('jpn_word:けいおん!').match(self.emd_item))

    def test_negated(self):
        self.assertFalse(self.query('origin:!korea').match(self.emd_item))
        self.assertTrue(self.query('origin:!usa').match(self.emd_item))
        self.assertTrue(self.query('tag:!vocaloid').match(self.emd_item))

    def test_spaces(self):
        self.assertTrue(self.query('tag:two words').match(self.emd_item))
        self.assertTrue(self.query('test:two words').match(self.emd_item))

    # MULTI VALUE #
    def test_array_negated(self):
        self.assertFalse(self.query('language:!korean').match(self.emd_item))
        self.assertTrue(self.query('language:!japanese').match(self.emd_item))
        self.assertTrue(self.query('language:!korean,english').match(self.emd_item))
        self.assertFalse(self.query('language:!korean,!english,').match(self.emd_item))

    def test_array_one_of_match(self):
        self.assertTrue(self.query('language:korean,japanese').match(self.emd_item))
        self.assertTrue(self.query('language:chinese,english').match(self.emd_item))
        self.assertFalse(self.query('language:chinese,japanese').match(self.emd_item))

    def test_tag_exists(self):
        self.assertTrue(self.query('genre').match(self.emd_item))

    def test_non_existing_tag(self):
        self.assertFalse(self.query('xxx').match(self.emd_item))

    def test_array_empty_pattern(self):
        self.assertTrue(self.query('language:').match(self.emd_item))

    def test_non_existing_pattern(self):
        self.assertFalse(self.query('origin:usa').match(self.emd_item))

    def test_array_existing_pattern(self):
        self.assertTrue(self.query('language:korean').match(self.emd_item))

    def test_array_existing_pattern_different_case(self):
        self.assertTrue(self.query('language:Korean').match(self.emd_item))

    def test_array_non_existing_pattern(self):
        self.assertFalse(self.query('language:japanese').match(self.emd_item))
