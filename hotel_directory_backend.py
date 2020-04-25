import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS hotels (id INTEGER PRIMARY KEY, title text, price float, available boolean, rating float)"
        )
        self.conn.commit()

    def insert(self, title, price, available, rating):
        self.cur.execute(
            "INSERT INTO hotels VALUES (NULL,?,?,?,?)",
            (title, price, available, rating),
        )
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM hotels")
        rows = self.cur.fetchall()
        return rows

    def search(self, title="", price="", available="", rating=""):
        self.cur.execute(
            "SELECT * FROM hotels WHERE title=? or price=? or available=? or rating=?",
            (title, price, available, rating),
        )
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM hotels WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, title, price, available, rating):
        self.cur.execute(
            "UPDATE hotels SET title=? , price=? , available=? , rating=? WHERE id=?",
            (title, price, available, rating, id),
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()
