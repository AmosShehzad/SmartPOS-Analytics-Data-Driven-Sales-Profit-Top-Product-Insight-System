"""
Database module for Shop Management System
Handles SQLite3 initialization and all database operations
File: db.py
"""

import sqlite3
import os
from datetime import datetime, date

DB_PATH = "shop_database.db"

def init_database():
    """Initialize database with all required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Inventory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            purchase_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Customers table with address field
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT DEFAULT '',
            remaining_amount REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, phone)
        )
    """)
    
    # Check if address column exists (for existing databases)
    cursor.execute("PRAGMA table_info(customers)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'address' not in columns:
        try:
            cursor.execute("ALTER TABLE customers ADD COLUMN address TEXT DEFAULT ''")
            conn.commit()
            print("✓ Added 'address' column to customers table")
        except sqlite3.OperationalError:
            print("✓ Address column already exists")
    
    # Sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity_sold INTEGER NOT NULL,
            purchase_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            profit_loss REAL NOT NULL,
            customer_name TEXT,
            customer_phone TEXT,
            amount_paid REAL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_name) REFERENCES inventory(product_name)
        )
    """)
    
    conn.commit()
    conn.close()

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

# ==================== ANALYTICS FUNCTIONS ====================

def get_todays_sales():
    """Calculate total sales amount for today"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        today = date.today().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT SUM(selling_price * quantity_sold) 
            FROM sales 
            WHERE DATE(sale_date) = ?
        """, (today,))
        result = cursor.fetchone()
        return result[0] if result[0] else 0
    except Exception as e:
        print(f"Error fetching today's sales: {e}")
        return 0
    finally:
        conn.close()

def get_todays_transactions():
    """Count number of transactions today"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        today = date.today().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT COUNT(*) 
            FROM sales 
            WHERE DATE(sale_date) = ?
        """, (today,))
        result = cursor.fetchone()
        return result[0] if result[0] else 0
    except Exception as e:
        print(f"Error fetching today's transactions: {e}")
        return 0
    finally:
        conn.close()

def get_total_products():
    """Count total number of products in inventory"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM inventory")
        result = cursor.fetchone()
        return result[0] if result[0] else 0
    except Exception as e:
        print(f"Error fetching total products: {e}")
        return 0
    finally:
        conn.close()

# ==================== PRODUCT FUNCTIONS ====================

def add_product(product_name, category, quantity, purchase_price, selling_price):
    """Add new product to inventory"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO inventory (product_name, category, quantity, purchase_price, selling_price)
            VALUES (?, ?, ?, ?, ?)
        """, (product_name, category, quantity, purchase_price, selling_price))
        conn.commit()
        return True, "Product added successfully"
    except sqlite3.IntegrityError:
        return False, "Product already exists"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_all_products():
    """Fetch all products from inventory"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, product_name, category, quantity, purchase_price, selling_price FROM inventory")
    products = cursor.fetchall()
    conn.close()
    return products

def update_product(product_id, product_name, category, quantity, purchase_price, selling_price):
    """Update product details"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE inventory SET product_name=?, category=?, quantity=?, purchase_price=?, selling_price=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (product_name, category, quantity, purchase_price, selling_price, product_id))
        conn.commit()
        return True, "Product updated successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_product(product_id):
    """Delete product from inventory"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM inventory WHERE id=?", (product_id,))
        conn.commit()
        return True, "Product deleted successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def update_inventory_quantity(product_name, quantity_change):
    """Update inventory quantity"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE inventory SET quantity = quantity + ?, updated_at=CURRENT_TIMESTAMP
            WHERE product_name=?
        """, (quantity_change, product_name))
        conn.commit()
        return True, "Inventory updated"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_product_by_name(product_name):
    """Get product details by name"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, product_name, category, quantity, purchase_price, selling_price FROM inventory
        WHERE product_name=?
    """, (product_name,))
    product = cursor.fetchone()
    conn.close()
    return product

# ==================== CUSTOMER FUNCTIONS ====================

def add_customer(name, phone, address=""):
    """Add new customer with optional address"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)", (name, phone, address))
        conn.commit()
        return True, "Customer added"
    except sqlite3.IntegrityError:
        return False, "Customer already exists"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_all_customers():
    """Fetch all customers with address"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, address, remaining_amount FROM customers")
    customers = cursor.fetchall()
    conn.close()
    return customers

def get_customer_by_id(customer_id):
    """Fetch single customer by ID with address"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, address, remaining_amount FROM customers WHERE id=?", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    return customer

def update_customer(customer_id, name=None, phone=None, address=None):
    """Update customer details"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Build dynamic update query
        updates = []
        params = []
        
        if name is not None:
            updates.append("name=?")
            params.append(name)
        if phone is not None:
            updates.append("phone=?")
            params.append(phone)
        if address is not None:
            updates.append("address=?")
            params.append(address)
        
        if not updates:
            return False, "No fields to update"
        
        params.append(customer_id)
        query = f"UPDATE customers SET {', '.join(updates)} WHERE id=?"
        
        cursor.execute(query, params)
        conn.commit()
        return True, "Customer updated successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def update_customer_remaining(name, phone, amount):
    """Update customer remaining amount"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE customers SET remaining_amount = remaining_amount + ?
            WHERE name=? AND phone=?
        """, (amount, name, phone))
        conn.commit()
        return True, "Customer updated"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_customer(customer_id):
    """Delete customer"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
        conn.commit()
        return True, "Customer deleted"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

# ==================== SALES FUNCTIONS ====================

def add_sale(product_name, quantity, purchase_price, selling_price, customer_name=None, customer_phone=None, amount_paid=None):
    """Record a sale"""
    profit_loss = (selling_price - purchase_price) * quantity
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO sales (product_name, quantity_sold, purchase_price, selling_price, profit_loss, customer_name, customer_phone, amount_paid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (product_name, quantity, purchase_price, selling_price, profit_loss, customer_name, customer_phone, amount_paid))
        conn.commit()
        return True, "Sale recorded"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_all_sales():
    """Fetch all sales"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_name, quantity_sold, purchase_price, selling_price, profit_loss, customer_name, customer_phone,sale_date
        FROM sales ORDER BY sale_date DESC
    """)
    sales = cursor.fetchall()
    conn.close()
    return sales

def get_low_stock_products(threshold=5):
    """Get products with low stock"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, quantity FROM inventory WHERE quantity <= ?", (threshold,))
    products = cursor.fetchall()
    conn.close()
    return products

def get_total_profit_loss():
    """Calculate total profit/loss"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(profit_loss) FROM sales")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] else 0