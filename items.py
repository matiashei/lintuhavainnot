import db

def add_item(species, amount, place, city, description, user_id):
    sql = "INSERT INTO items (species, amount, place, city, description, user_id) VALUES (?, ?, ?, ?, ?, ?)"
    db.execute(sql, [species, amount, place, city, description, user_id])