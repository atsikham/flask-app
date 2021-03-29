from app import db
from datetime import date, datetime
from sqlalchemy import CheckConstraint


class User(db.Model):
    """
    User model class
    """
    __tablename__ = 'users'
    name = db.Column(db.String(80), primary_key=True)
    birthday = db.Column(db.String(80), nullable=False)

    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday

    def __str__(self):
        return f'{self.name} - {self.birthday}'

    @classmethod
    def get_user(cls, name):
        """
        :param name:
        :return: user with specified name
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def add_or_replace_user(cls, name, dateOfBirth):
        """
        Add a new user or replace an existing one
        :param name: name of the user to add/update
        :param dateOfBirth: birthday in format "YYYY-MM-DD"
        """
        datetime.strptime(dateOfBirth, '%Y-%m-%d').date()
        user = cls.query.filter_by(name=name).first()
        if not user:  # create new user
            new_user = cls(name, dateOfBirth)
            db.session.add(new_user)
        else:  # update existing user
            user.birthday = dateOfBirth
        db.session.commit()
