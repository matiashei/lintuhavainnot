import db

def add_item(species, amount, place, city, description, user_id):
    sql = "INSERT INTO items (species, amount, place, city, description, user_id) VALUES (?, ?, ?, ?, ?, ?)"
    db.execute(sql, [species, amount, place, city, description, user_id])

def get_items():
    sql = "SELECT id, species, city FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.species,
                    items.amount,
                    items.place,
                    items.city,
                    items.description,
                    users.username
             FROM items
             JOIN users ON items.user_id = users.id
             WHERE items.id = ?"""
    result = db.query(sql, [item_id])
    if result:
        return result[0]
    return None
