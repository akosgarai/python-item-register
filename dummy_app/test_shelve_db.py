import unittest

from dummy_app import shelve_db

class SelveDbTests(unittest.TestCase):

    def setUp(self):
        self.db_name = 'test_data.db'
        self.store = shelve_db.ShelveDb(self.db_name)

    def tearDown(self):
        pass

    def test_empty_db(self):
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

if __name__ == "__main__":
    unittest.main()
