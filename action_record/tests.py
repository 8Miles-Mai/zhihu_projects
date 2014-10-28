import unittest
import common
import env
# Create your tests here.

class CommonTestCase(unittest.TestCase):

    def testCreate_data_file(self):
        self.assertTrue(common.create_data_file(20, 20))

    def testInit_data_for_test(self):
        self.assertTrue(common.init_data_for_test(env.TEST_DATA_FILE_PATH))

    def testGet_action_record(self):
        user_id = 4
        print('----------Test get action record. user_id = %s----------' % user_id)
        result = common.get_action_record(str(user_id), 0, 20)
        print result
        return True

    def testSet_item_anonymity(self):
        print('----------Test set item anonymity.----------')
        user_id = 4
        item_id = 50
        print('----------Set user_id = %s, item_id = %s to anonymity.----------' % (user_id, item_id))
        common.set_item_anonymity(str(user_id), str(item_id))
        item_id = 80
        print('----------Set user_id = %s, item_id = %s to anonymity.----------' % (user_id, item_id))
        common.set_item_anonymity(str(user_id), str(item_id))
        result = common.get_action_record(str(user_id), 0, 20)
        print result
        return True

    def testUnset_item_anonymity(self):
        print('----------Test unset item anonymity.----------')
        user_id = 4
        item_id = 50
        print('----------Unset user_id = %s, item_id = %s from anonymity.----------' % (user_id, item_id))
        common.set_item_anonymity(str(user_id), str(item_id))
        result = common.get_action_record(str(user_id), 0, 20)
        print result
        return True

# Test
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(CommonTestCase('testGet_action_record'))
    suite.addTest(CommonTestCase('testSet_item_anonymity'))
    suite.addTest(CommonTestCase('testUnset_item_anonymity'))
    runner = unittest.TextTestRunner()
    runner.run(suite)