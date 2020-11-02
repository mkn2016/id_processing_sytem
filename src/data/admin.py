from src.data import dated

admin_dummy_data = [
    {
        "id": 1,
        "first_name": "Martin",
        "last_name": "Ndirangu",
        "password": "admin",
        "date_created": dated,
        "date_modified": dated,
        "role": "super-admin",
        "status": "active"
    },
    {
        "id": 2,
        "first_name": "Sospeter",
        "last_name": "Kirwa",
        "password": "admin",
        "role": "admin",
        "status": "suspended",
        "date_created": dated,
        "date_modified": dated
    },
    {
        "id": 3,
        "first_name": "Moses",
        "last_name": "Maingi",
        "password": "admin",
        "date_created": dated,
        "date_modified": dated,
        "role": "moderator",
        "status": "deactivated"
    },
    {
        "id": 4,
        "first_name": "Michelle",
        "last_name": "Kimani",
        "password": "admin",
        "date_created": dated,
        "date_modified": dated,
        "role": "moderator",
        "status": "active"
    }
]
