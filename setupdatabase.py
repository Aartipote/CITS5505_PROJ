from app import db
from app.views import User
from app.views import Admin

print("------------- REACHED -------------")
db.create_all()

# creating default accounts for two admins

admin1 = Admin(username="aarti", password="aarti123", email="aarti@pote.com")
db.session.add(admin1)
db.session.commit()

admin2 = Admin(username="reshma", password="reshma123", email="reshma@nair.com")
db.session.add(admin2)
db.session.commit()