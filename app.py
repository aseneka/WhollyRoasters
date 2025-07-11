from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
app.config['SECRET_KEY']='aseneka'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
with app.app_context():

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), index=True, unique=True)
        password = db.Column(db.String(128))

    def __repr__(self):
        return f'User {self.username}'
    
    class ShippingInfo(db.Model):
        ship_id = db.Column(db.Integer, primary_key=True)
        full_name = db.Column(db.String(50))
        address = db.Column(db.String(50))
        user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"{self.full_name}'s address is {self.address}."

    db.create_all()
    ShippingInfo.query.delete()

    user1 = User(username="coffeeaddict", password="1234")
    user2 = User(username="brujabrews", password="5678")
    user3 = User(username="kagunza", password="4567")
    user4 = User(username="elly", password="3433")
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.commit()

    ship1 = ShippingInfo(full_name="Claudia Reyes", address="Amsterdam 210, CDMX, Mexico", user_id=2)
    ship2 = ShippingInfo(full_name="Roy Latte", address="Beau St, Bath BA1 1QY, UK", user_id=1)

    db.session.add(ship1)
    db.session.add(ship2)
    db.session.commit()

@app.route("/admin", methods=["GET"])
def admin():
    db_users = User.query.all()
    db_shippers = ShippingInfo.query.all()

    users = []
    for db_user in db_users:
        users.append({
            "username": db_user.username, 
            "id": db_user.id
        })

    shippers = []
    for db_shipper in db_shippers:
        shippers.append({
            "full_name": db_shipper.full_name, 
            "address": db_shipper.address, 
            "user_id": db_shipper.user_id
        })

    return jsonify({
        "users": users, 
        "shippers": shippers
    })

## replace the /register route
@app.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()
    user_match = User.query.filter_by(username=json_data['uname']).first()
    if user_match:
        return jsonify({'Message': 'User already exists!'})

    new_user = User(username = json_data['uname'], password = json_data['pword'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'Message': 'A new user was created!'}) 
