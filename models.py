from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.Text, default='')
    avatar_color = db.Column(db.String(7), default='#d4af37')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def initials(self):
        return self.username[:2].upper() if self.username else '??'


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), default='')
    category = db.Column(db.String(50), default='City', index=True)
    image_url = db.Column(db.String(500))
    latitude = db.Column(db.Float, default=0.0)
    longitude = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship('DestinationImage', backref='destination',
                             cascade='all, delete-orphan', lazy=True)
    reviews = db.relationship('Review', backref='destination',
                              cascade='all, delete-orphan', lazy=True)

    @property
    def avg_rating(self):
        if not self.reviews:
            return 0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    @property
    def review_count(self):
        return len(self.reviews)


class DestinationImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    replies = db.relationship('Reply', backref='review',
                              cascade='all, delete-orphan', lazy=True,
                              order_by='Reply.created_at')


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('replies', lazy=True))


class TravelPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, default='')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('travel_plans', lazy=True))
    destinations = db.relationship(
        'Destination', secondary='travel_plan_destination',
        backref=db.backref('travel_plans', lazy=True))

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0


travel_plan_destination = db.Table(
    'travel_plan_destination',
    db.Column('travel_plan_id', db.Integer, db.ForeignKey('travel_plan.id'), primary_key=True),
    db.Column('destination_id', db.Integer, db.ForeignKey('destination.id'), primary_key=True),
)


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'destination_id', name='_user_dest_uc'),)

    user = db.relationship('User', backref=db.backref('wishlist_items', lazy=True))
    destination = db.relationship('Destination', backref=db.backref('wished_by', lazy=True))


CATEGORIES = ['Beach', 'Mountain', 'City', 'Adventure', 'Cultural']
