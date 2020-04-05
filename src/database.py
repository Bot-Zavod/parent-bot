import sqlite3

class DbInterface:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread = False)
        self.cursor = self.conn.cursor()

    # def getGames(self, type=None, age=None, amount=None, location=None, props=None):
    #     sql = "SELECT DISTINCT Id FROM Games WHERE "
    #     args = [type]
    #     sql += 'Type=?'
    #     if age is not None:
    #         sql += 'AND (Age=? OR Age is NULL)'
    #         args.append(age)
    #     if amount is not None:
    #         sql += 'AND (Amount=? OR Amount is NULL)'
    #         args.append(amount)
    #     if location is not None:
    #         sql += 'AND (Location=? OR Location is NULL)'
    #         args.append(location)
    #     if props is not None:
    #         sql += 'AND (Props=? OR Props is NULL)'
    #         args.append(props)
    #     self.cursor.execute(sql, args)
    #     data = self.cursor.fetchall()
    #     return data if len(data) == 0 else tuple(d[0] for d in data)

    def authorizeUser(self, payment_id, chat_id, day, time, username, email):
        """ Inserts user to the table of paid users
        
        To make insertion more reliable
        you should provide arguments by name
        .authorizeUser(payment_id = 1, chat_id = 1,day = 1, time = 1, username = "lol", email = "kek")
        
        return if insertion was succesfull(True) or not (False)"""
        sql = 'INSERT INTO Payments (payment_id, chat_id, day, time, username, email) VALUES (?,?,?,?,?,?)'
        args = [payment_id, chat_id, day, time, username, email]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("User exists")
            return False

    def checkUser(self, chat_id):
        """ Checks out if provided user in our payments tables
        return boolean answer"""
        sql = 'SELECT EXISTS(SELECT * from Payments Where Chat_id = ?)'
        args = [chat_id]
        self.cursor.execute(sql, args)
        return True if self.cursor.fetchall()[0][0] == 1 else False

    
# tests
# DbInterface('database.db')\
#     .authorizeUser(payment_id = 1, chat_id = 1,day = 1, time = 1, username = "lol", email = "kek")
# print(DbInterface('database.db').checkUser(1))