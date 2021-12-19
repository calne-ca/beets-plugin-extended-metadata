import unittest

from beetsplug.extendedmetadata import ExtendedMetaDataMatchQuery
from mockito import mock, unstub, when


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
    
    # SINGLE VALUE #
    def test_invalid_pattern(self):
        self.assertFalse(self.query('language::^$^').match(self.emd_item))

    def test_empty_pattern(self):
        self.assertTrue(self.query('origin::').match(self.emd_item))

    def test_existing_pattern(self):
        self.assertTrue(self.query('origin::^.*ea$').match(self.emd_item))

    def test_non_existing_pattern(self):
        self.assertFalse(self.query('origin::us.*').match(self.emd_item))

    # MULTI VALUE #
    def test_array_empty_pattern(self):
        self.assertTrue(self.query('language::').match(self.emd_item))

    def test_array_existing_pattern(self):
        self.assertTrue(self.query('language::^.*an$').match(self.emd_item))

    def test_array_non_existing_pattern(self):
        self.assertFalse(self.query('language::ja.*').match(self.emd_item))
