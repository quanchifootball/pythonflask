from flask import request, url_for
from requests import Response, post
from db import db
from libs.mailgun import Mailgun


class UserModel(db.Model):
    # db.Model is sql alchemy
    # need to declare table and columns
    # of the table that this object is related to
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def send_confirmation_email(self) -> Response:
        # url_root = http://localhost:5000/
        # userconfirm needs to match UserConfirm resource name registerd in app.py
        # user_id is the query param to be embedded in link
        # link is for the user to click in mailgun email
        link = request.url_root[0:-1] + url_for("userconfirm", user_id=self.id)
        subject = "Registration confirmation"
        text = f"Please click the link to confirm your registration: {link}"
        html = f'<html>Please click the link to confirm your registration: <a href="{link}">{link}</a></html>'

        return Mailgun.send_email([self.email], subject, text, html)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        # SQLAlchemy converts results into the model object
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        # SQLAlchemy converts results into the model object
        return cls.query.filter_by(email=email).first()
