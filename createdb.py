#!/usr/bin/env python
from datetime import datetime
from korform2 import db, user_datastore

db.create_all()

# Create default roles
admin_role = user_datastore.create_role(name="Admin")

# Create a default admin account
admin_user = user_datastore.create_user(email='admin@localhost', password='password', active=True, confirmed_at=datetime.utcnow())

# Make the default admin an admin
user_datastore.add_role_to_user(admin_user, admin_role)

# Save changes
db.session.commit()
