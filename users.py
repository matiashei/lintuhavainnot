import db

def get_user(user_id):
    sql = """SELECT id, username
             FROM users
             WHERE id = ?"""
    result = db.query(sql, [user_id])
    if result:
        return result[0]
    return None

def get_items(user_id):
    sql = "SELECT id, species, amount, city FROM items WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])