from flask import Flask, render_template, request, redirect, url_for, flash
from database.db_init import db
from models.Property import Property
from models.Inquiry import Inquiry
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Ensure the database folder exists
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', 'real_estate.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# Create tables and add sample data when the app starts
with app.app_context():
    db.create_all()
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


# Home route: Shows all listings
@app.route('/')
def home():
    properties = Property.query.all()
    return render_template('home.html', properties=properties)


# Property detail route
@app.route('/property/<int:property_id>')
def property_detail(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('property.html', property=property)


# Route to book the property
@app.route('/book/<int:property_id>')
def book_property(property_id):
    property = Property.query.get_or_404(property_id)
    property.booked = True
    db.session.commit()
    flash('The property has been booked. Please fill out the form to confirm your booking.', 'success')
    return redirect(url_for('signup'))


# Signup form route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # Save inquiry to the database
        new_inquiry = Inquiry(name=name, email=email, phone=phone, message=message)
        db.session.add(new_inquiry)
        db.session.commit()

        flash('Thank you for signing up! An agent will contact you soon.', 'success')
        return redirect(url_for('home'))

    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
