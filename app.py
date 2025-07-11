from flask import Flask, render_template
app = Flask(__name__)
@app.route("/shop", methods=["GET"])
def shop():
 cart = ["12oz Medium Roast", "24oz French Roast","960z Beans"]

 return render_template("shop.html", cart=cart)

