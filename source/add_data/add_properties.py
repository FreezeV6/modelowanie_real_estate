from source.database.db_init import db
from source.models.Property import Property


def add_properties():
    # Create tables and add sample data when the app starts
    if not Property.query.first():
        initial_properties = [
            Property(title='Modern Family Home', location='New York', price='$500,000',
                     description='A spacious family home in the heart of New York.'),
            Property(title='Luxury Condo', location='San Francisco', price='$850,000',
                     description='A beautiful condo with stunning views of the city.'),
            Property(title='Cozy Cottage', location='Austin', price='$300,000',
                     description='A charming cottage with modern amenities.'),
            Property(title='Beachfront Villa', location='Miami', price='$1,200,000',
                     description='A luxurious villa with a private beach in Miami.'),
            Property(title='Mountain Retreat', location='Denver', price='$750,000',
                     description='A cozy retreat with beautiful mountain views in Denver.')
        ]
        db.session.bulk_save_objects(initial_properties)
        db.session.commit()
