from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Sample data for real estate listings
properties = [
    {'id': 1, 'title': 'Modern Family Home', 'location': 'New York', 'price': '$500,000'},
    {'id': 2, 'title': 'Luxury Condo', 'location': 'San Francisco', 'price': '$850,000'},
    {'id': 3, 'title': 'Cozy Cottage', 'location': 'Austin', 'price': '$300,000'}
]


# Home route: Shows all listings
@app.route('/')
def home():
    return render_template('home.html', properties=properties)


# Property detail route
@app.route('/property/<int:property_id>')
def property_detail(property_id):
    property = next((prop for prop in properties if prop['id'] == property_id), None)
    if property:
        return render_template('property.html', property=property)
    return "Property not found", 404


# Signup form route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # In a real app, here we'd save to a database
        flash('Thank you for signing up! An agent will contact you soon.', 'success')
        return redirect(url_for('home'))

    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
