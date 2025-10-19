import db

def add_item(species, date, amount, place, municipality, description, user_id):
    sql = """INSERT INTO items (species, date, amount, place, municipality,
                        description, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"""
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

def remove_image(item_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND item_id = ?"
    db.execute(sql, [image_id, item_id])

def search_items(query):
    sql = """SELECT id, species, amount, municipality, place
            FROM items
            WHERE place LIKE ? OR municipality LIKE ? OR species LIKE ?
            ORDER BY date DESC, id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like])

def add_comment(item_id, user_id, comment):
    sql = """INSERT INTO comments (item_id, user_id, comment)
            VALUES (?, ?,? )"""
    db.execute(sql, [item_id, user_id, comment])

def get_comments(item_id):
    sql = """SELECT comments.id, comments.comment, users.id user_id, users.username
            FROM comments, users
            WHERE comments.item_id = ? AND comments.user_id = users.id
            ORDER BY comments.id DESC"""
    return db.query(sql, [item_id])

def get_comment(comment_id):
    sql = "SELECT id, item_id, user_id, comment FROM comments WHERE id = ?"
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])
