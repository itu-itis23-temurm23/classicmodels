from flask import render_template, request, redirect, url_for, flash, session

db = None


def init_order_routes(app, database):
    """Initialize order-related routes."""
    global db
    db = database

    @app.route("/order/<int:order_number>")
    def order_detail(order_number):
        order = db.get_order(order_number)
        if not order:
            flash("Order not found.", "danger")
            return redirect(url_for("index"))

        user_type = session.get("user_type")
        user_number = session.get("user_number")

        if user_type == "customer":
            if order["customerNumber"] != user_number:
                flash("Access denied. This is not your order.", "danger")
                return redirect(url_for("index"))

        elif user_type == "employee":
            customer_of_order = db.get_customer_details(order["customerNumber"])
            if (
                not customer_of_order 
                or customer_of_order.get("salesRepEmployeeNumber") != user_number
            ):
                flash("Access denied. You are not the sales rep for this customer.", "danger")
                return redirect(url_for("employee_dashboard"))

        elif not user_type:
            flash("You must be logged in to view order details.", "danger")
            return redirect(url_for("login"))

        order_items = db.get_order_details(order_number)

        return render_template(
            "order_detail.html",
            order=order,
            items=order_items
        )

    @app.route("/order/<int:order_number>/cancel", methods=["POST"])
    def cancel_order(order_number):
        user_type = session.get("user_type")
        user_number = session.get("user_number")

        if not user_type:
            flash("You must be logged in.", "danger")
            return redirect(url_for("login"))

        order = db.get_order(order_number)
        if not order:
            flash("Order not found.", "danger")
            return redirect(url_for("index"))

        if user_type == "customer":
            if order["customerNumber"] != user_number:
                flash("You cannot cancel someone else's order.", "danger")
                return redirect(url_for("customer_orders"))

            if order["status"] != "In Process":
                flash("This order can no longer be cancelled.", "warning")
                return redirect(url_for("order_detail", order_number=order_number))

        db.execute_query(
            "UPDATE orders SET status = 'Cancelled' WHERE orderNumber = %s",
            (order_number,)
        )
        

        flash(f"Order #{order_number} has been cancelled.", "warning")
        return redirect(url_for("order_detail", order_number=order_number))
