from flask import render_template, request, redirect, url_for, flash, session

db = None


def init_customer_routes(app, database):
    """Initialize customer-specific routes."""
    global db
    db = database

    @app.route("/customer/profile")
    def customer_profile():
        """Shows the logged-in customer's profile details."""
        if session.get("user_type") != "customer":
            flash("You must be a customer to view this page.", "danger")
            return redirect(url_for("index"))

        customerNumber = session.get("user_number")
        
        if not customerNumber:
            flash("Error finding your profile. Please log in again.", "danger")
            return redirect(url_for('login'))
        
        customer_details = db.get_customer_details(customerNumber)
        balance_info = db.get_customer_balance(customerNumber)
        payments = db.get_customer_payments(customerNumber)

        return render_template(
            "customerpage.html",
            customer=customer_details,
            balance=balance_info,
            payments=payments
        )

    @app.route("/customer/orders")
    def customer_orders():
        """Shows the logged-in customer's order history."""
        if session.get("user_type") != "customer":
            flash("You must be a customer to view this page.", "danger")
            return redirect(url_for("index"))

        customerNumber = session.get("user_number")
        
        if not customerNumber:
            flash("Error finding your profile. Please log in again.", "danger")
            return redirect(url_for('login'))
        
        orders = db.get_customer_orders(customerNumber)
        
        return render_template("customer_orders.html", orders=orders)
