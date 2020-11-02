from datetime import datetime

formatted_dated = datetime.now().strftime("%d-%m-%Y")
formatted_date_time = datetime.now().strftime("%d-%m-%Y %X")


def parse_audit_logs(id_: int, who: str, audit_type: str, to=None) -> dict:
    if audit_type == "login":
        message = f"{who} logged in at {formatted_date_time}."
        return {"id": id_, "audit_trails": message, "audit_type": "login", "date_added": formatted_dated}
    elif audit_type == "logout":
        message = f"{who} logged out at {formatted_date_time}."
        return {"id": id_, "audit_trails": message, "audit_type": "logout", "date_added": formatted_dated}
    elif audit_type == "failed_login":
        message = f"{who} tried to login in at {formatted_date_time}. Exceeded login attempts."
        return {"id": id_, "audit_trails": message, "audit_type": "failed_login", "date_added": formatted_dated}
    elif audit_type == "edit":
        message = f"{who} edited {to} at {formatted_date_time}."
        return {"id": id_, "audit_trails": message, "audit_type": "edit", "date_added": formatted_dated}
    elif audit_type == "add":
        message = f"{who} added {to} at {formatted_date_time}."
        return {"id": id_, "audit_trails": message, "audit_type": "add", "date_added": formatted_dated}
