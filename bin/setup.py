from bin.variables import db, Reset

print("[+] Creating database tables...")
db.create_users_db()
db.create_items_db()

print("[+] Creating items...")
from Items.item_handler import import_items_to_database, increase_amount_owned_of_item
if Reset:
    import_items_to_database()