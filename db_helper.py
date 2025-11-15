import mysql.connector

class DatabaseHandler:
    def __init__(self,host="localhost",user="root",password="",database="classicmodels"):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db.cursor(dictionary=True) # returns results as dict

    def check_customer_number(self, num):
        """
        Check if the customer number exists in customer table.
        Returns:
            - A fetched query
        """
        query = "SELECT * FROM customers WHERE customerNumber = %s"
        return self.execute_query(query, (num,), fetchone=True)
    
    def check_employee_number(self, num):
        """
        Check if the employee number exists in employee table.
        """
        query = "SELECT * FROM employees WHERE employeeNumber = %s"
        return self.execute_query(query, (num,), fetchone=True)

    def get_assigned_customers(self, employee_number):
        """Fetches all customers assigned to a specific Sales Rep."""
        query = "SELECT customerNumber, customerName, city, country FROM customers WHERE salesRepEmployeeNumber = %s"
        return self.execute_query(query, (employee_number,))
    
    def get_customer_details(self, customer_number):
        """
        Fetches all details for a single customer.
        Returns:
            - A single dictionary for the customer, or None
        """
        query = "SELECT * FROM customers WHERE customerNumber = %s"
        return self.execute_query(query, (customer_number,), fetchone=True)

    def get_customer_orders(self, customer_number):
        """
        Fetches all orders for a specific customer, newest first.
        Returns:
            - A list of order dictionaries
        """
        query = "SELECT * FROM orders WHERE customerNumber = %s ORDER BY orderDate DESC"
        return self.execute_query(query, (customer_number,))
    
    def execute_query(self, query, params=None, fetchone=False):
        """
        execute the given query
        Returns:
            - for SELECT: fetched rows
            - for INSERT/UPDATE/DELETE: number of affected rows
        Raises:
            - mysql.connector.Error if the query fails
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # if its a select query
            if query.strip().lower().startswith("select"):
                if not fetchone:
                    result = self.cursor.fetchall()
                else:
                    result = self.cursor.fetchone()
                return result 
            else:
                self.db.commit() # commit changes for insert/update/delete
                return self.cursor.rowcount
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    
    def close(self):
        self.cursor.close()
        self.db.close()
