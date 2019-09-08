import unittest

from dummy_app import shelve_db

class SelveDbTests(unittest.TestCase):

    def setUp(self):
        self.db_name = 'test_data.db'
        self.store = shelve_db.ShelveDb(self.db_name)
        self.store.open()
        self.store.cleanup()

    def tearDown(self):
        pass

    def test_empty_db(self):
        self.store.open()
        items = self.store.get_all()
        self.store.cleanup()
        self.assertEqual(len(items), 0)

    def test_one_item_in_db(self):
        self.store.open()
        self.store.db['test-key'] = 'test-value'
        items = self.store.get_all()
        self.store.cleanup()
        self.assertEqual(len(items), 1)

    def test_multiple_items_in_db(self):
        self.store.open()
        self.store.db['test-key-1'] = 'test-value-1'
        self.store.db['test-key-2'] = 'test-value-2'
        self.store.db['test-key-3'] = 'test-value-3'
        self.store.db['test-key-4'] = 'test-value-4'
        items = self.store.get_all()
        self.store.cleanup()
        self.assertEqual(len(items), 4)

    def test_get_one_existing_key(self):
        self.store.open()
        testKey = 'test-key'
        testValue = 'test-value'
        self.store.db[testKey] = testValue
        item = self.store.get_one(testKey)
        self.store.cleanup()
        self.assertEqual(item, testValue)

    def test_get_one_non_existing_key(self):
        self.store.open()
        testKey = 'test-key'
        self.store.db[testKey] = 'test-value'
        with self.assertRaises(Exception) as ex:
            self.store.get_one('non-existing-key')

        self.store.cleanup()
        self.assertEqual(ex.exception.args[0], 404)

    def test_upsert_insertion(self):
        self.store.open()
        testKey = 'test-key'
        testValue = 'test-value'
        items = self.store.get_all()
        self.assertEqual(len(items), 0)
        self.store.upsert(testKey, testValue)
        items = self.store.get_all()
        self.assertEqual(len(items), 1)
        item = self.store.get_one(testKey)
        self.store.cleanup()
        self.assertEqual(item, testValue)

    def test_upsert_update(self):
        self.store.open()
        testKey = 'test-key'
        testValue = 'test-value'
        items = self.store.get_all()
        self.assertEqual(len(items), 0)
        self.store.upsert(testKey, testValue)
        item = self.store.get_one(testKey)
        self.assertEqual(item, testValue)
        testValue = 'test-value-updated'
        self.store.upsert(testKey, testValue)
        items = self.store.get_all()
        self.assertEqual(len(items), 1)
        item = self.store.get_one(testKey)
        self.store.cleanup()
        self.assertEqual(item, testValue)

    def test_delete_existing(self):
        self.store.open()
        testKey = 'test-key'
        testValue = 'test-value'
        self.store.db[testKey] = testValue
        self.store.delete(testKey)
        items = self.store.get_all()
        self.assertEqual(len(items), 0)
        self.store.cleanup()

    def test_delete_non_existing(self):
        self.store.open()
        testKey = 'test-key'
        with self.assertRaises(Exception) as ex:
            self.store.delete(testKey)
        self.store.cleanup()
        self.assertEqual(ex.exception.args[0], 404)

    def test_tear_down(self):
        self.assertFalse(self.store.opened)
        self.store.open()
        self.assertTrue(self.store.opened)
        self.store.teardown_db(Exception())
        self.assertFalse(self.store.opened)

    def test_get(self):
        self.assertFalse(self.store.opened)
        _ = self.store.get()
        self.assertTrue(self.store.opened)


if __name__ == "__main__":
    unittest.main()
