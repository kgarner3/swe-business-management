from hash_utilities import HashUtilities
from database import get_connection

# Customer class handles customer authentication and database operations
class Customer:
    """Initialize a Customer object with profile and login information"""
    def __init__(self, fN="", lN="", pN="", addr="", email="", custID=-1,
                 uName="", passwordHash="", salt="", mustChangePassword=False):
        self.firstName = fN
        self.lastName = lN
        self.phoneNumber = pN
        self.address = addr
        self.email = email
        self.customerID = custID
        self.userName = uName
        self.passwordHash = passwordHash
        self.salt = salt
        self.mustChangePassword = mustChangePassword
    
    def changePassword(self, newPassword):
        """Update customer's password (hash + salt) and clear must-change flag"""
        if not newPassword or self.customerID == -1:
            return False

        # Hash new password and update flags
        self.passwordHash, self.salt = HashUtilities.hash_password(newPassword)
        self.mustChangePassword = False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Save updated credentials to database
            cursor.execute('''
                UPDATE customers
                SET passwordHash = ?, salt = ?, mustChangePassword = ?
                WHERE Customer_ID = ?
            ''', (self.passwordHash, self.salt, 0, self.customerID))

            conn.commit()

            if cursor.rowcount == 0:
                conn.close()
                return False

            conn.close()
            return True

        except:
            conn.close()
            return False

    @staticmethod
    def authenticateCustomer(userName, password):
        """Verify login credentials and return customer ID + password change status"""
        if not userName or not password:
            return None

        conn = get_connection()
        cursor = conn.cursor()

        # Fetch stored credentials for username
        cursor.execute('''
            SELECT Customer_ID, passwordHash, salt, mustChangePassword
            FROM customers
            WHERE username = ?
        ''', (userName,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        # Compare hashed password with stored hash
        entered_hash = HashUtilities.hash_with_salt(password, row["salt"])

        if entered_hash == row["passwordHash"]:
            return {
                "customerID": row["Customer_ID"],
                "mustChangePassword": bool(row["mustChangePassword"])
            }

        return None

    def createCustomerInDB(self):
        """Create a new customer in the database (generates username and temp password)"""
        if not self.firstName or not self.lastName or not self.email or not self.address or not self.phoneNumber:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Check whether email already exists
            cursor.execute('''
                SELECT Customer_ID
                FROM customers
                WHERE email = ?
            ''', (self.email,))
            existing_email = cursor.fetchone()

            if existing_email is not None:
                conn.close()
                return False

            # Generate a base username from first initial + last name
            base_username = (self.firstName[0] + self.lastName).lower().replace(" ", "")
            username = base_username
            counter = 1

            # Make sure username is unique
            while True:
                cursor.execute('''
                    SELECT Customer_ID
                    FROM customers
                    WHERE username = ?
                ''', (username,))
                existing_username = cursor.fetchone()

                if existing_username is None:
                    break

                username = f"{base_username}{counter}"
                counter += 1

            # Generate temporary password and hash it
            temp_password = "temp123"
            self.passwordHash, self.salt = HashUtilities.hash_password(temp_password)
            self.userName = username
            self.mustChangePassword = True

            # Insert new customer record into database
            cursor.execute('''
                INSERT INTO customers
                (first_name, last_name, email, number, address, username, passwordHash, salt, mustChangePassword)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.firstName,
                self.lastName,
                self.email,
                self.phoneNumber,
                self.address,
                self.userName,
                self.passwordHash,
                self.salt,
                1
            ))

            conn.commit()
            self.customerID = cursor.lastrowid
            conn.close()
            return True

        except:
            conn.close()
            return False

    def updateCustomerInDB(self):
        """Update existing customer information in the database"""
        if self.customerID == -1:
            return False

        if not self.firstName or not self.lastName or not self.email or not self.address or not self.phoneNumber:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Check for duplicate email (excluding current customer)
            cursor.execute('''
                SELECT Customer_ID
                FROM customers
                WHERE email = ? AND Customer_ID != ?
            ''', (self.email, self.customerID))

            existing_email = cursor.fetchone()
            if existing_email is not None:
                conn.close()
                return False

            # Update with or without username depending on whether it exists
            if self.userName:
                cursor.execute('''
                    UPDATE customers
                    SET first_name = ?, last_name = ?, email = ?, number = ?, address = ?, username = ?
                    WHERE Customer_ID = ?
                ''', (
                    self.firstName,
                    self.lastName,
                    self.email,
                    self.phoneNumber,
                    self.address,
                    self.userName,
                    self.customerID
                ))
            else:
                cursor.execute('''
                    UPDATE customers
                    SET first_name = ?, last_name = ?, email = ?, number = ?, address = ?
                    WHERE Customer_ID = ?
                ''', (
                    self.firstName,
                    self.lastName,
                    self.email,
                    self.phoneNumber,
                    self.address,
                    self.customerID
                ))

            conn.commit()

            if cursor.rowcount == 0:
                conn.close()
                return False

            conn.close()
            return True

        except:
            conn.close()
            return False

    @staticmethod
    def findCustomerIDBySearch(searchText):
        """Find a customer ID using email, phone, full name, or username.
            Returns: ID, -1 (not found), or -2 (multiple matches)"""
        if not searchText:
            return -1

        searchText = searchText.strip()
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Try matching by email first
            if "@" in searchText:
                cursor.execute('''
                    SELECT Customer_ID
                    FROM customers
                    WHERE LOWER(email) = LOWER(?)
                ''', (searchText,))
                row = cursor.fetchone()
                conn.close()
                return row["Customer_ID"] if row else -1

            # Normalize input to digits and compare phone numbers
            digits_only = "".join(char for char in searchText if char.isdigit())
            if len(digits_only) >= 7:
                cursor.execute('''
                    SELECT Customer_ID, number
                    FROM customers
                ''')
                rows = cursor.fetchall()

                for row in rows:
                    db_digits = "".join(char for char in row["number"] if char.isdigit()) if row["number"] else ""
                    if db_digits == digits_only:
                        conn.close()
                        return row["Customer_ID"]

                conn.close()
                return -1

            # Attempt match using first and last name
            if " " in searchText:
                parts = searchText.split()
                if len(parts) >= 2:
                    first_name = parts[0]
                    last_name = " ".join(parts[1:])

                    cursor.execute('''
                        SELECT Customer_ID
                        FROM customers
                        WHERE LOWER(first_name) = LOWER(?) AND LOWER(last_name) = LOWER(?)
                    ''', (first_name, last_name))

                    rows = cursor.fetchall()

                    if len(rows) == 1:
                        conn.close()
                        return rows[0]["Customer_ID"]

                    if len(rows) > 1:
                        conn.close()
                        return -2

            # Fallback: try matching by username
            cursor.execute('''
                SELECT Customer_ID
                FROM customers
                WHERE LOWER(username) = LOWER(?)
            ''', (searchText,))
            row = cursor.fetchone()
            conn.close()

            return row["Customer_ID"] if row else -1

        except:
            conn.close()
            return -1

    def deleteCustomerInDB(self):
        """Delete customer from the database using their ID"""
        if self.customerID == -1:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Remove customer record from database
            cursor.execute('''
                DELETE FROM customers
                WHERE Customer_ID = ?
            ''', (self.customerID,))

            conn.commit()

            if cursor.rowcount == 0:
                conn.close()
                return False

            self.customerID = -1
            conn.close()
            return True

        except:
            conn.close()
            return False

    @staticmethod
    def getCustomerInfoByID(customerID):
        """Retrieve customer profile information by ID for display purposes"""
        if customerID == -1:
            return None

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Query database for customer details
            cursor.execute('''
                SELECT Customer_ID, first_name, last_name, email, number, address, username
                FROM customers
                WHERE Customer_ID = ?
            ''', (customerID,))

            row = cursor.fetchone()
            conn.close()

            if row is None:
                return None

            # Convert database row into dictionary for frontend use
            return {
                "customerID": row["Customer_ID"],
                "firstName": row["first_name"],
                "lastName": row["last_name"],
                "email": row["email"],
                "phoneNumber": row["number"],
                "address": row["address"],
                "username": row["username"]
            }

        except:
            conn.close()
            return None