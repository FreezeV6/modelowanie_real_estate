from database.db_init import db


class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)  # Optional field for more property details
    booked = db.Column(db.Boolean, default=False)  # New field to mark if the property is booked
