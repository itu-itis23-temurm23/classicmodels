from flask import Flask, render_template, request, redirect, url_for, flash, session
from db_helper import DatabaseHandler
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey" # for flash messages

db = DatabaseHandler(password="") # enter password

@app.route('/')
def index():
    query = ("SELECT productLine, textDescription FROM productlines LIMIT 2")
    productlines = db.execute_query(query)
    return render_template('index.html', productlines=productlines)

# New route for productline pages
@app.route("/products/<product_line>")
def products_by_line(product_line):
    query = "SELECT * FROM products WHERE productLine = %s"
    products = db.execute_query(query, (product_line,))
    return render_template("products.html", products=products, product_line=product_line)


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        number_input = request.form.get("number")
        if not number_input.isdigit():
            flash("Please enter a valid number!", "danger")
            return redirect(url_for("login"))

        number_input = int(number_input)
        customer = db.check_customer_number(number_input)
        if customer:
            # store customer info in session
            session["customer_number"] = customer["customerNumber"]
            flash("Login successful!", "success")
            return index()
        else:
            flash("Number not found!", "danger")

        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out","info")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)