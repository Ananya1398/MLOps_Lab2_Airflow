from airflow.www.app import create_app
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.security.sqla.manager import SecurityManager

# Create a Flask app context
app = create_app()
app.app_context().push()

sm: SecurityManager = app.appbuilder.sm

# Check if the user already exists
existing_user = sm.find_user(username="admin")
if existing_user:
    print("User 'admin' already exists.")
else:
    user = sm.add_user(
        username="admin",
        first_name="Admin",
        last_name="User",
        email="admin@example.com",
        role=sm.find_role("Admin"),
        password="admin"
    )
    if user:
        print("User 'admin' created successfully!")
    else:
        print("Failed to create user.")
