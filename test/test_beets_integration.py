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

    def test_wrong_usage_prints_help(self):
        self._assert_prints_help('emd artist:Title')
        self._assert_prints_help('emd -a tag1:test1')
        self._assert_prints_help('emd artist:Title -z')
        self._assert_prints_help('emd --add tag1:test1')
        self._assert_prints_help('emd --query artist:Title --zzz')
        self._assert_prints_help('emd --help')

    def _assert_prints_help(self, command):
        result = self.beets.command(command)
        self.assertEqual('Usage: beet emd <query> [options]', result[0])
        self.assertEqual('Options:', result[1])
        self.assertEqual(22, len(result))

    def test_invalid_syntax_prints_syntax_error(self):
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -r tag1:tag2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -r tag1 tag2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -r tag1,tag2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -r tag1>tag2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -r tag1:test1/tag2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -r tag1/tag2:test2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -r tag1/tag2:'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -a tag1'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -a tag1:'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -u tag1/tag2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -u tag1:test1/tag2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -u tag1:/tag2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -u tag1:test1>tag2:test2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -u tag1:test1:tag2:test2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -u tag1:test1 tag2:test2'))
        self._prints_syntax_exception(self.beets.command('emd -y title:"Title 1" -u tag1:test1,tag2:test2'))

    @staticmethod
    def _prints_syntax_exception(command_result):
        for line in command_result:
            if 'Exception: Invalid syntax' in line:
                return True
        return False

    def test_empty_query(self):
        result = self.beets.command("emd -y '' -a tag2:test2")
        self.assertEqual("Artist 1 - Album 1 - Title 1", result[0])
        self.assertEqual("Artist 2 - Album 2 - Title 2", result[1])
        self.assertEqual("Artist 3 - Album 3 - Title 3", result[2])

    def test_query_without_results(self):
        result = self.beets.command("emd -y title:Title x:tag1:test1 -a tag2:test2")
        self.assertEqual("No items found matching query '\"title:Title\" \"x:tag1:test1\"'", result[0])

    def test_query_multi_query_with_spaces(self):
        result = self.beets.command("emd title:'Title 1' album:'Album 1' -a tag1:test1")
        self.assertEqual("Artist 1 - Album 1 - Title 1", result[1])

    def test_show_emd(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.assertTrue('"tag1": "test1"' in self.beets.command('emd -y title:"Title 1" -s')[1])
        self.assertTrue('"tag1": ["test1", "test2"]' in self.beets.command('emd -y title:"Title 1" -a tag1:test2 -s')[1])

    def test_unicode_values(self):
        self.assertTrue('"vocals": "初音ミク"' in self.beets.command('emd -y title:"Title 1" -a vocals:初音ミク -s')[1])
        self.assertTrue('"vocals": "初音ミク"' in self.beets.command('emd -y title:"Title 2" -a vocals:"\u521d\u97f3\u30df\u30af" -s')[1])

    def test_user_confirmation(self):
        result = self.beets.command('emd title:"Title 1" -s')
        self.assertEqual('Artist 1 - Album 1 - Title 1', result[0])
        self.assertEqual('{}', result[1])

        result = self.beets.command('emd title:"Title 1" -a tag1:test1 -a tag2:test2 -d tag3 -u tag4:test4/tag5:test4 -u tag5:test5/tag5:test6 -u tag6:test6/tag7:test7 -s -r tag8/tag9 -c .comments/lyrics')

        self.assertEqual('Matching items:', result[0])
        self.assertEqual('Artist 1 - Album 1 - Title 1', result[1])
        self.assertEqual('Actions:', result[2])
        self.assertEqual("=> Move value 'test4' from tag 'tag4' to tag 'tag5'", result[3])
        self.assertEqual("=> Change value 'test5' from tag 'tag5' to 'test6'", result[4])
        self.assertEqual("=> Change value 'test6' from tag 'tag6' to 'test7' and move it to tag 'tag7'", result[5])
        self.assertEqual("=> Rename tag 'tag8' to 'tag9'", result[6])
        self.assertEqual("=> Add values ['test1'] to tag 'tag1'", result[7])
        self.assertEqual("=> Add values ['test2'] to tag 'tag2'", result[8])
        self.assertEqual("=> Copy value from normal tag 'comments' to tag 'lyrics'", result[9])
        self.assertEqual("=> Delete tag 'tag3'", result[10])
        self.assertEqual('=> Show resulting extended meta data', result[11])

        # We cannot test the manual user input because piping yes into the command doesn't work for some reason
        self.assertTrue('Are you sure you want to apply the listed actions to 1 listed items (yes/no)?' in result[12])
        self.assertTrue('EOFError' in result[len(result) - 1])

    def test_add_new_tag(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')

        tagged_with_test1 = self.beets.list("x:tag1:test1")
        self.assertEqual(1, len(tagged_with_test1))
        self.assertTrue(tagged_with_test1[0].endswith('Title 1'))

    def test_add_new_tag_with_spaces(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:"test 1"')

        tagged_with_test1 = self.beets.list('x:tag1:"test 1"')
        self.assertEqual(1, len(tagged_with_test1))
        self.assertTrue(tagged_with_test1[0].endswith('Title 1'))

        self.beets.command('emd -y x:tag1:"test 1" -a tag2:"test 2"')

        tagged_with_test2 = self.beets.list('x:tag2:"test 2"')
        self.assertEqual(1, len(tagged_with_test2))
        self.assertTrue(tagged_with_test2[0].endswith('Title 1'))

    def test_add_value_to_existing_tag(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.beets.command('emd -y title:"Title 1" -a tag1:test2')

        tagged_with_test1 = self.beets.list("x:tag1:test1")
        self.assertEqual(1, len(tagged_with_test1))
        self.assertTrue(tagged_with_test1[0].endswith('Title 1'))

        tagged_with_test2 = self.beets.list("x:tag1:test2")
        self.assertEqual(1, len(tagged_with_test2))
        self.assertTrue(tagged_with_test2[0].endswith('Title 1'))

    def test_add_tags_to_multiple_files(self):
        self.beets.command('emd -y title:Title -a tag1:test1')
        self.assertEqual(3, len(self.beets.list("x:tag1:test1")))

    def test_add_multiple_tag_values(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1,test2')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1 x:tag1:test2")))

    def test_add_multiple_tags(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1 -a tag2:test2')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1 x:tag2:test2")))

    def test_remove_tag(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.assertEqual(1, len(self.beets.list("x:tag1")))

        self.beets.command('emd -y title:"Title 1" -d tag1')
        self.assertEqual(0, len(self.beets.list("x:tag1")))

    def test_remove_value_from_tag(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1,test2')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1 x:tag1:test2")))

        self.beets.command('emd -y title:"Title 1" -d tag1:test1')
        self.assertEqual(0, len(self.beets.list("x:tag1:test1 x:tag1:test2")))
        self.assertEqual(1, len(self.beets.list("x:tag1:test2")))

    def test_remove_last_value_from_tag(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1")))

        self.beets.command('emd -y title:"Title 1" -d tag1:test1')
        self.assertEqual(0, len(self.beets.list("x:tag1")))

    def test_remove_tags_from_multiple_files(self):
        self.beets.command('emd -y title:Title -a tag1:test1')
        self.beets.command('emd -y title:Title -d tag1:test1')
        self.assertEqual(0, len(self.beets.list("x:tag1:test1")))

    def test_remove_multiple_tag_values(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1,test2,test3')
        self.beets.command('emd -y title:"Title 1" -d tag1:test1,test3')
        self.assertEqual(1, len(self.beets.list("x:tag1:test2 x:tag1:!test1 x:tag1:!test3")))

    def test_remove_multiple_tag(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1 -a tag2:test2 -a tag3:test3')
        self.beets.command('emd -y title:"Title 1" -d tag1 -d tag3')
        self.assertEqual(1, len(self.beets.list("x:tag2")))
        self.assertEqual(0, len(self.beets.list("x:tag1")))
        self.assertEqual(0, len(self.beets.list("x:tag3")))

    def test_rename_tag(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.beets.command('emd -y title:"Title 1" -r tag1/tag2')
        self.assertEqual(1, len(self.beets.list("x:tag2")))
        self.assertEqual(0, len(self.beets.list("x:tag1")))

    def test_update_tag_value(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.beets.command('emd -y title:"Title 1" -u tag1:test1/tag1:test2')
        self.assertEqual(1, len(self.beets.list("x:tag1:test2")))
        self.assertEqual(0, len(self.beets.list("x:tag1:test1")))

    def test_update_tag_value_without_changes(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.beets.command('emd -y title:"Title 1" -u tag1:test1/tag1:test1')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1")))

    def test_move_tag_value(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.beets.command('emd -y title:"Title 1" -u tag1:test1/tag2:test1')
        self.assertEqual(1, len(self.beets.list("x:tag2:test1")))
        self.assertEqual(0, len(self.beets.list("x:tag1:test1")))

    def test_move_and_update_tag_value(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.beets.command('emd -y title:"Title 1" -u tag1:test1/tag2:test2')
        self.assertEqual(1, len(self.beets.list("x:tag2:test2")))
        self.assertEqual(0, len(self.beets.list("x:tag1:test1")))

    def test_copy_tag_value(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.beets.command('emd -y title:"Title 1" -c tag1/tag2')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1")))
        self.assertEqual(1, len(self.beets.list("x:tag2:test1")))

        self.beets.command('emd -y title:"Title 2" -c .album/tag3')
        self.assertEqual(1, len(self.beets.list("album:'Album 2'")))
        self.assertEqual(1, len(self.beets.list("x:tag3:'Album 2'")))

        self.assertEqual(0, len(self.beets.list("album_artist:'Artist 3'")))
        self.beets.command('emd -y title:"Title 3" -c .artist/.album_artist')
        self.assertEqual(1, len(self.beets.list("album_artist:'Artist 3'")))
        self.assertEqual(1, len(self.beets.list("artist:'Artist 3'")))

    def test_copy_tag_value_without_changes(self):
        self.beets.command('emd -y title:"Title 1" -a tag1:test1')
        self.beets.command('emd -y title:"Title 1" -c tag1/tag1')
        self.assertEqual(1, len(self.beets.list("x:tag1:test1")))

        self.beets.command('emd -y title:"Title 1" -c .title/.title')
        self.assertEqual(1, len(self.beets.list('title:"Title 1"')))

    def test_copy_tag_value_emd_storage_tag(self):
        self.assertEqual(1, len(self.beets.list("comments:'Comment 1'")))
        self.beets.command("emd -y comments:'Comment 1' -c .comments/tag1")
        self.assertEqual(0, len(self.beets.list("comments:'Comment 1'")))
        self.assertEqual(1, len(self.beets.list("x:tag1:'Comment 1'")))

    def test_special_characters(self):
        self.beets.command('emd -y artist:"Artist 1" -a tag1:"test:;!\'/ 1"')
        self.assertEqual(1, len(self.beets.list('x:tag1:"test:;!\'/ 1"')))
        self.assertEqual('{"tag1": "test:;!\'/ 1"}', self.beets.command('emd x:tag1:"test:;!\'/ 1" -s')[1])
