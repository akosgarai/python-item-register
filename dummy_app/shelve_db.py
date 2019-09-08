import shelve

class ShelveDb:

    def __init__(self, name):
        self.name = name
        self.opened = False

    def open(self):
        if not self.opened:
            self.db = shelve.open(self.name)

        self.opened = True

    def get(self):
        self.open()
        return self.db

    def teardown_db(self, exception):
        if self.opened:
            self.db.close()

        self.opened = False

    def get_all(self):
        self.open()
        keys = list(self.db.keys())

        data = []

        for key in keys:
            data.append(self.db[key])

        return data

    def get_one(self, key):
        self.open()
        if not (key in self.db):
            raise Exception(404)

        return self.db[key]

    def upsert(self, key, value):
        self.open()
        self.db[key] = value

    def delete(self, key):
        self.open()
        if not (key in self.db):
            raise Exception(404)

        del self.db[key]

    def cleanup(self):
        if self.opened:
            self.db.clear()
            self.db.close()

        self.opened = False
