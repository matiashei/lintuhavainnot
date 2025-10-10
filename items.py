import db

def add_item(species, date, amount, place, municipality, description, user_id):
    sql = "INSERT INTO items (species, date, amount, place, municipality, description, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [species, date, amount, place, municipality, description, user_id])

def get_items():
    sql = "SELECT id, species, date, amount, municipality FROM items ORDER BY date DESC, id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.species,
                    items.date,
                    items.amount,
                    items.place,
                    items.municipality,
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

def update_item(item_id, species, date, amount, place, municipality, description):
    sql = """UPDATE items SET species = ?,
                                date = ?,
                                amount = ?,
                                place = ?,
                                municipality = ?,
                                description = ?
            WHERE id = ?"""
    db.execute(sql, [species, date, amount, place, municipality, description, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def get_images(item_id):
    sql = "SELECT id FROM images WHERE item_id = ?"
    return db.query(sql, [item_id])

def add_image(item_id, image):
    sql = "INSERT INTO images (item_id, image) VALUES (?, ?)"
    db.execute(sql, [item_id, image])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def search_items(query):
    sql = """SELECT id, species, amount, municipality, place
            FROM items
            WHERE place LIKE ? OR municipality LIKE ? OR species LIKE ?
            ORDER BY date DESC, id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like])