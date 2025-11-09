#!/usr/bin/env bash
DB=classicmodels
USER="${1:-root}"
echo "This will create DB '$DB' and import schema files. You will be prompted for MySQL password."
read -s -p "MySQL password: " PASS
echo
export MYSQL_PWD="$PASS"

# Create database with utf8mb4
mysql -u "$USER" --default-character-set=utf8mb4 -e "CREATE DATABASE IF NOT EXISTS ${DB} CHARACTER SET utf8mb4 COLLATE=utf8mb4_general_ci;" || { echo "Failed to create database ${DB}"; unset MYSQL_PWD; exit 1; }

for f in tables/productlines.sql tables/products.sql tables/offices.sql tables/employees.sql tables/customers.sql tables/orders.sql tables/orderdetails.sql tables/payments.sql; do
  echo "Importing $f ..."
  mysql -u "$USER" --default-character-set=utf8mb4 "$DB" < "$f" || { echo "Import failed at $f"; unset MYSQL_PWD; exit 2; }
done

unset MYSQL_PWD
echo "Import finished."