import os
import unittest

from test.beets_container import BeetsContainer


class BeetsIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.beets = BeetsContainer(music_dir=self.path('beets/music'),
                                    config_dir=self.path('beets/config'),
                                    package_src_dirs=[self.path('../beetsplug')])
        self.beets.start()

    @staticmethod
    def path(rel_path):
        script_dir = os.path.dirname(__file__)
        return os.path.join(script_dir, rel_path)

    def tearDown(self):
        self.beets.stop()

    def test_missing_options_prints_help(self):
        self.assertEqual('Usage: beet emd [options]', self.beets.command('emd -a tag1:test1')[0])
        self.assertEqual('Usage: beet emd [options]', self.beets.command('emd -q artist:Title')[0])
        self.assertEqual('Usage: beet emd [options]', self.beets.command('emd --help')[0])

    def test_invalid_syntax_prints_syntax_error(self):
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -r tag1:tag2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -r tag1 tag2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -r tag1,tag2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -r tag1>tag2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -r tag1:test1/tag2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -r tag1/tag2:test2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -r tag1/tag2:'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -a tag1'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -a tag1:'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -u tag1/tag2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -u tag1:test1/tag2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -u tag1:/tag2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -u tag1:test1>tag2:test2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -u tag1:test1:tag2:test2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -u tag1:test1 tag2:test2'))
        self._prints_syntax_exception(self.beets.command('emd -q title:"Title 1" -u tag1:test1,tag2:test2'))

    @staticmethod
    def _prints_syntax_exception(command_result):
        for line in command_result:
            if 'Exception: Invalid syntax' in line:
                return True
        return False

    def test_add_new_tag(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1')

        tagged_with_test1 = self.beets.list("x:tag1:test1")
        self.assertEqual(1, len(tagged_with_test1))
        self.assertTrue(tagged_with_test1[0].endswith('Title 1'))

    def test_add_new_tag_with_spaces(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:"test 1"')

        tagged_with_test1 = self.beets.list('x:tag1:"test 1"')
        self.assertEqual(1, len(tagged_with_test1))
        self.assertTrue(tagged_with_test1[0].endswith('Title 1'))

    def test_add_value_to_existing_tag(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1')
        self.beets.command('emd -q title:"Title 1" -a tag1:test2')

        tagged_with_test1 = self.beets.list("x:tag1:test1")
        self.assertEqual(1, len(tagged_with_test1))
        self.assertTrue(tagged_with_test1[0].endswith('Title 1'))

        tagged_with_test2 = self.beets.list("x:tag1:test2")
        self.assertEqual(1, len(tagged_with_test2))
        self.assertTrue(tagged_with_test2[0].endswith('Title 1'))

    def test_add_tags_to_multiple_files(self):
        self.beets.command('emd -q title:Title -a tag1:test1')
        self.assertEqual(3, len(self.beets.list("x:tag1:test1")))

    def test_add_multiple_tag_values(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1,test2')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1 x:tag1:test2")))

    def test_add_multiple_tags(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1 -a tag2:test2')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1 x:tag2:test2")))

    def test_remove_tag(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1')
        self.assertEqual(1, len(self.beets.list("x:tag1")))

        self.beets.command('emd -q title:"Title 1" -d tag1')
        self.assertEqual(0, len(self.beets.list("x:tag1")))

    def test_remove_value_from_tag(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1,test2')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1 x:tag1:test2")))

        self.beets.command('emd -q title:"Title 1" -d tag1:test1')
        self.assertEqual(0, len(self.beets.list("x:tag1:test1 x:tag1:test2")))
        self.assertEqual(1, len(self.beets.list("x:tag1:test2")))

    def test_remove_last_value_from_tag(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1")))

        self.beets.command('emd -q title:"Title 1" -d tag1:test1')
        self.assertEqual(0, len(self.beets.list("x:tag1")))

    def test_remove_tags_from_multiple_files(self):
        self.beets.command('emd -q title:Title -a tag1:test1')
        self.beets.command('emd -q title:Title -d tag1:test1')
        self.assertEqual(0, len(self.beets.list("x:tag1:test1")))

    def test_remove_multiple_tag_values(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1,test2,test3')
        self.beets.command('emd -q title:"Title 1" -d tag1:test1,test3')
        self.assertEqual(1, len(self.beets.list("x:tag1:test2 x:tag1:!test1 x:tag1:!test3")))

    def test_remove_multiple_tag(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1 -a tag2:test2 -a tag3:test3')
        self.beets.command('emd -q title:"Title 1" -d tag1 -d tag3')
        self.assertEqual(1, len(self.beets.list("x:tag2")))
        self.assertEqual(0, len(self.beets.list("x:tag1")))
        self.assertEqual(0, len(self.beets.list("x:tag3")))

    def test_rename_tag(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1')
        self.beets.command('emd -q title:"Title 1" -r tag1/tag2')
        self.assertEqual(1, len(self.beets.list("x:tag2")))
        self.assertEqual(0, len(self.beets.list("x:tag1")))

    def test_update_tag_value(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1')
        self.beets.command('emd -q title:"Title 1" -u tag1:test1/tag1:test2')
        self.assertEqual(1, len(self.beets.list("x:tag1:test2")))
        self.assertEqual(0, len(self.beets.list("x:tag1:test1")))

    def test_move_tag_value(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1')
        self.beets.command('emd -q title:"Title 1" -u tag1:test1/tag2:test1')
        self.assertEqual(1, len(self.beets.list("x:tag2:test1")))
        self.assertEqual(0, len(self.beets.list("x:tag1:test1")))

    def test_move_and_update_tag_value(self):
        self.beets.command('emd -q title:"Title 1" -a tag1:test1')
        self.beets.command('emd -q title:"Title 1" -u tag1:test1/tag2:test2')
        self.assertEqual(1, len(self.beets.list("x:tag2:test2")))
        self.assertEqual(0, len(self.beets.list("x:tag1:test1")))
