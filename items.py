import db

def add_item(species, amount, place, city, description, user_id):
    sql = "INSERT INTO items (species, amount, place, city, description, user_id) VALUES (?, ?, ?, ?, ?, ?)"
    db.execute(sql, [species, amount, place, city, description, user_id])

def get_items():
    sql = "SELECT id, species, city FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.species,
                    items.amount,
                    items.place,
                    items.city,
                    items.description,
                    users.id user_id,
                    users.username
             FROM items
             JOIN users ON items.user_id = users.id
             WHERE items.id = ?"""
    result = db.query(sql, [item_id])
    if result:
        return result[0]
    return None

def update_item(item_id, species, amount, place, city, description):
    sql = """UPDATE items SET species = ?,
                                amount = ?,
                                place = ?,
                                city = ?,
                                description = ?
            WHERE id = ?"""
    db.execute(sql, [species, amount, place, city, description, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])