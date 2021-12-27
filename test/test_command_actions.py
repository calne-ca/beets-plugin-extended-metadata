import unittest

from beetsplug.emd.command.actions.add_action import AddExpression
from beetsplug.emd.command.actions.copy_action import CopyExpression
from beetsplug.emd.command.actions.delete_action import DeleteExpression
from beetsplug.emd.command.actions.rename_action import RenameExpression
from beetsplug.emd.command.actions.update_action import UpdateExpression


class CommandActionsTest(unittest.TestCase):

    def test_update_expression(self):
        expression = UpdateExpression('tag1:test1/tag2:test2')
        self.assertEqual('tag1', expression.source_tag)
        self.assertEqual('test1', expression.source_value)
        self.assertEqual('tag2', expression.destination_tag)
        self.assertEqual('test2', expression.destination_value)

    def test_add_expression_special_characters(self):
        self.assertEqual(['test.1'], UpdateExpression('tag1:test.1/tag2:test.2').source_value)
        self.assertEqual(['test.2'], UpdateExpression('tag1:test.1/tag2:test.2').destination_value)
        self.assertEqual(["test'1"], UpdateExpression("tag1:test'1/tag2:test'2").source_value)
        self.assertEqual(["test'2"], UpdateExpression("tag1:test'1/tag2:test'2").destination_value)
        self.assertEqual(["!test1"], UpdateExpression("tag1:!test1/tag2:!test2").source_value)
        self.assertEqual(["!test2"], UpdateExpression("tag1:!test1/tag2:!test2").destination_value)
        self.assertEqual(["test;1"], UpdateExpression("tag1:test;1/tag2:test;2").source_value)
        self.assertEqual(["test;2"], UpdateExpression("tag1:test;1/tag2:test;2").destination_value)
        self.assertEqual(["test/1"], UpdateExpression("tag1:test/1/tag2:test/2").source_value)
        self.assertEqual(["test/2"], UpdateExpression("tag1:test/1/tag2:test/2").destination_value)

    def test_update_expression_invalid_expression(self):
        self.assertRaises(Exception, lambda: UpdateExpression(''))
        self.assertRaises(Exception, lambda: UpdateExpression('tag1/test1'))
        self.assertRaises(Exception, lambda: UpdateExpression('tag1:test1'))
        self.assertRaises(Exception, lambda: UpdateExpression('tag1:test1:tag2:test2'))
        self.assertRaises(Exception, lambda: UpdateExpression('!tag1:test1:tag2:test2'))
        self.assertRaises(Exception, lambda: UpdateExpression('tag1:test1:!tag2:test2'))

    def test_copy_expression(self):
        expression = CopyExpression('tag1/tag2')
        self.assertEqual('tag1', expression.source_tag)
        self.assertTrue(expression.is_source_emd)
        self.assertEqual('tag2', expression.destination_tag)
        self.assertTrue(expression.is_destination_emd)

    def test_copy_expression_from_file_metadata(self):
        expression = CopyExpression('.tag1/tag2')
        self.assertEqual('tag1', expression.source_tag)
        self.assertFalse(expression.is_source_emd)
        self.assertEqual('tag2', expression.destination_tag)
        self.assertTrue(expression.is_destination_emd)

    def test_copy_expression_to_file_metadata(self):
        expression = CopyExpression('tag1/.tag2')
        self.assertEqual('tag1', expression.source_tag)
        self.assertTrue(expression.is_source_emd)
        self.assertEqual('tag2', expression.destination_tag)
        self.assertFalse(expression.is_destination_emd)

    def test_copy_expression_from_and_to_file_metadata(self):
        expression = CopyExpression('.tag1/.tag2')
        self.assertEqual('tag1', expression.source_tag)
        self.assertFalse(expression.is_source_emd)
        self.assertEqual('tag2', expression.destination_tag)
        self.assertFalse(expression.is_destination_emd)

    def test_copy_expression_invalid_expression(self):
        self.assertRaises(Exception, lambda: CopyExpression(''))
        self.assertRaises(Exception, lambda: CopyExpression('tag1:test1/test1:test2'))
        self.assertRaises(Exception, lambda: CopyExpression('tag1:tag2'))

    def test_add_expression(self):
        expression = AddExpression('tag1:test1')
        self.assertEqual('tag1', expression.tag)
        self.assertEqual(['test1'], expression.values)

    def test_add_expression_multiple_values(self):
        expression = AddExpression('tag1:test1,test2,test3')
        self.assertEqual('tag1', expression.tag)
        self.assertEqual(['test1', 'test2', 'test3'], expression.values)

    def test_add_expression_special_characters(self):
        self.assertEqual(['test.1'], AddExpression('tag1:test.1').values)
        self.assertEqual(["test'1"], AddExpression("tag1:test'1").values)
        self.assertEqual(["!test1"], AddExpression("tag1:!test1").values)
        self.assertEqual(["test;1"], AddExpression("tag1:test;1").values)
        self.assertEqual(["test/1"], AddExpression("tag1:test/1").values)

    def test_add_expression_invalid_expression(self):
        self.assertRaises(Exception, lambda: AddExpression(''))
        self.assertRaises(Exception, lambda: AddExpression('tag1'))
        self.assertRaises(Exception, lambda: AddExpression('tag1:'))
        self.assertRaises(Exception, lambda: AddExpression('tag1/test1'))
        self.assertRaises(Exception, lambda: AddExpression('!tag1:test1'))

    def test_delete_expression(self):
        expression = DeleteExpression('tag1:test1')
        self.assertEqual('tag1', expression.tag)
        self.assertEqual(['test1'], expression.values)

    def test_delete_expression_no_value(self):
        expression = DeleteExpression('tag1')
        self.assertEqual('tag1', expression.tag)
        self.assertEqual([], expression.values)

    def test_delete_expression_multiple_values(self):
        expression = DeleteExpression('tag1:test1,test2,test3')
        self.assertEqual('tag1', expression.tag)
        self.assertEqual(['test1', 'test2', 'test3'], expression.values)

    def test_delete_expression_special_characters(self):
        self.assertEqual(['test.1'], DeleteExpression('tag1:test.1').values)
        self.assertEqual(["test'1"], DeleteExpression("tag1:test'1").values)
        self.assertEqual(["!test1"], DeleteExpression("tag1:!test1").values)
        self.assertEqual(["test;1"], DeleteExpression("tag1:test;1").values)
        self.assertEqual(["test/1"], DeleteExpression("tag1:test/1").values)

    def test_delete_expression_invalid_expression(self):
        self.assertRaises(Exception, lambda: DeleteExpression(''))
        self.assertRaises(Exception, lambda: DeleteExpression('tag1:'))
        self.assertRaises(Exception, lambda: DeleteExpression('tag1/test1'))
        self.assertRaises(Exception, lambda: DeleteExpression('!tag1:test1'))

    def test_rename_expression(self):
        expression = RenameExpression('tag1/tag2')
        self.assertEqual('tag1', expression.old_tag)
        self.assertEqual('tag2', expression.new_tag)

    def test_rename_expression_invalid_expression(self):
        self.assertRaises(Exception, lambda: RenameExpression(''))
        self.assertRaises(Exception, lambda: RenameExpression('tag1'))
        self.assertRaises(Exception, lambda: RenameExpression('tag1/'))
        self.assertRaises(Exception, lambda: RenameExpression('tag1:tag2'))
        self.assertRaises(Exception, lambda: RenameExpression('tag1/!tag2'))
        self.assertRaises(Exception, lambda: RenameExpression('!tag1/tag2'))
        self.assertRaises(Exception, lambda: RenameExpression('tag1:tag2,tag3'))
