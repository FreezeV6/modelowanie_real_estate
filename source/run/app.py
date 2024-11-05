from source.database.db_init import db
from source.models.Property import Property
from source.models.Inquiry import Inquiry
from source.add_data.add_properties import add_properties
from source.utils.consts import TEMPLATE_DIR, STATIC_DIR, DB_PATH, KEY
from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = KEY

# Ensure the database folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    add_properties()

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
