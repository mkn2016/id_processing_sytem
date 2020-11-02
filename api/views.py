from functools import wraps
from typing import NoReturn, Union

from bcrypt import hashpw, gensalt, checkpw
from flask import Blueprint, render_template, redirect, url_for, request, g, jsonify, session, current_app, \
    send_from_directory, abort
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature, BadTimeSignature
from qrcode import QRCode, constants
from rethinkdb import r

from api.extensions import mail

auth = Blueprint("auth", __name__, template_folder="templates", static_url_path="/static")


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "student_id" not in session:
            return redirect(url_for("auth.login", next=request.url))
        return func(*args, **kwargs)

    return wrapper


def encode_data_to_file(data_to_encode: Union[dict, str], file_name: str) -> NoReturn:
    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.tobytes()
    img.save(file_name)


@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_data = request.get_json()

        student_id = student_data["student_id"]
        password = student_data["password"]

        student = r.table("students").get(int(student_id)).run(g.con)

        if student is None:
            return jsonify({"error": "Student with that id was not found in the system"}), 404
        else:
            if "password" in student.keys():
                authenticated = checkpw(password.encode("utf-8"), student["password"])

                if authenticated:
                    result = r.table("students").get(int(student_id)).update({
                        "credit_points": r.row["credit_points"] + 10
                    }).run(g.con)

                    if result["replaced"] == 1:
                        session["student_id"] = student["id"]
                        student_doc_2 = r.table("students").get(int(student_id)).run(g.con)
                        student_doc = {
                            "id": student_doc_2["id"],
                            "expiry_date": student_doc_2["expiry_date"],
                            "status": student_doc_2["status"],
                            "credit_points": student_doc_2["credit_points"],
                        }
                        file_name = current_app.config["STUDENT_IMAGES"] + str(session["student_id"]) + ".png"

                        encode_data_to_file(student_doc, file_name)
                        return jsonify({"data": "Login Successful. 10 Credit Points Awarded"}), 200
                    elif result["errors"] != 0:
                        session["student_id"] = student["id"]
                        student_doc_2 = r.table("students").get(int(student_id)).run(g.con)
                        student_doc = {
                            "id": student_doc_2["id"],
                            "expiry_date": student_doc_2["expiry_date"],
                            "status": student_doc_2["status"],
                            "credit_points": student_doc_2["credit_points"],
                        }
                        file_name = current_app.config["STUDENT_IMAGES"] + str(session["student_id"]) + ".png"

                        encode_data_to_file(student_doc, file_name)
                        return jsonify({"data": "Login Successful. 10 Credit Points Was not Awarded"}), 200
                    else:
                        session["student_id"] = student["id"]
                        student_doc_2 = r.table("students").get(int(student_id)).run(g.con)
                        student_doc = {
                            "id": student_doc_2["id"],
                            "expiry_date": student_doc_2["expiry_date"],
                            "status": student_doc_2["status"],
                            "credit_points": student_doc_2["credit_points"],
                        }
                        file_name = current_app.config["STUDENT_IMAGES"] + str(session["student_id"]) + ".png"

                        encode_data_to_file(student_doc, file_name)
                        return jsonify({"data": "Login Successful"}), 200
                else:
                    return jsonify({"error": "Invalid credentials"}), 401
            else:
                return jsonify({"error": "Password has not been set, please register before proceesing to login"}), 400
    else:
        return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        student_data = request.get_json()

        student_id = student_data["student_id"]
        password = student_data["password"]

        student = r.table("students").get(int(student_id)).run(g.con)
        if student is None:
            return jsonify({"error": "Student with that id was not found in the system"}), 404
        else:
            if "password" in student.keys():
                return jsonify(
                    {"error": "Account already exists and password was already set. Redirecting to login..."}), 406
            else:
                encrypted_password = hashpw(password.encode("utf-8"), gensalt(14))

                result = r.table("students").get(int(student_id)).update({"password": encrypted_password}).run(g.con)

                if result["errors"] != 0:
                    return jsonify({"error": "Something happened. Could not save password"}), 400
                else:
                    return jsonify({"data": "Records saved successfully"}), 200

    else:
        return render_template("register.html")


@auth.route("/images/<image>")
def send_image(image):
    try:
        return send_from_directory(current_app.config['STUDENT_IMAGES'], image, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@auth.route("/profile", methods=["GET"])
@login_required
def profile():
    if "student_id" in session:
        student = r.table("students").get(session["student_id"]).run(g.con)
        return render_template("profile.html", student=student, image_name=str(session["student_id"]) + ".png")
    return jsonify({"error": "Login required"})


def send_mail(subject, to, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    password_reset_url = url_for("auth.reset_with_token",
                                 token=password_reset_serializer.dumps(user_email, salt="password-reset-salt"),
                                 _external=True)

    html = render_template('email_password_reset.html', password_reset_url=password_reset_url)

    send_mail('Password Reset Requested', user_email, html)


@auth.route("/reset_password", methods=["GET", "POST"])
def reset():
    if request.method == "POST":
        email_address = request.form["email"]
        send_password_reset_email(email_address)
        emails = r.table("students").pluck("email").coerce_to("array").run(g.con)

        if not email_address in [doc["email"] for doc in emails]:
            return jsonify({"error": "Email address was not found in our system"}), 404
        else:
            send_password_reset_email(email_address)
            return jsonify({"data": "Please Check your email for a password reset link"}), 200
    else:
        return render_template("reset.html")


@auth.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=10)
    except (SignatureExpired, BadTimeSignature, BadSignature):
        return jsonify(
            {"error": 'The password reset link is invalid or has expired. Please resend the link again'}), 400
        return redirect(url_for("auth.reset"))

    doc_result = r.table("students").filter({"email": email}).coerce_to("array").run(g.con)

    if doc_result:
        if request.method == "POST":
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]

            if password != confirm_password or confirm_password != password:
                return jsonify({"error": "Passwords do not match"}), 406
            else:
                password = password.encode("utf-8")
                hashed_password = hashpw(password, gensalt(14))
                result = r.table("students").get(doc_result[0]["id"]).update({"password": hashed_password}).run(g.con)
                if result["errors"] != 0:
                    return jsonify({"error": "Password was not updated"}), 406
                elif result["replaced"] == 1:
                    # return jsonify({"data": "Password has been updated successfully"}), 200
                    return redirect(url_for("auth.login"))
        else:
            return render_template('reset_password_with_token.html', token=token)
    else:
        return jsonify({"error": "Email is invalid"}), 404


@auth.route("/logout")
@login_required
def logout():
    session.pop("student_id", None)
    return redirect(url_for("auth.login"))
