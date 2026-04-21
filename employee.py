from hash_utilities import HashUtilities
from database import get_connection

# Employee class handles employee authentication and database operations
class Employee:
    def __init__(self, fN="", lN="", email="", uName="", passwordHash="", salt="", empID=-1,
                 mustChangePassword=False, expenses=0.0):
        """Initialize an Employee object with profile and login information"""
        self.firstName = fN
        self.lastName = lN
        self.email = email
        self.userName = uName
        self.passwordHash = passwordHash
        self.salt = salt
        self.employeeID = empID
        self.mustChangePassword = mustChangePassword
        self.expenses = expenses

    def setTemporaryPassword(self, tempPassword):
        """Set a temporary password and require change on first login"""
        if not tempPassword:
            return False

        # Hash temporary password and flag for reset
        self.passwordHash, self.salt = HashUtilities.hash_password(tempPassword)
        self.mustChangePassword = True
        return True

    def changePassword(self, newPassword):
        """Update employee password (hash + salt) and clear must-change flag"""
        if not newPassword or self.employeeID == -1:
            return False

        # Hash new password and update flags
        self.passwordHash, self.salt = HashUtilities.hash_password(newPassword)
        self.mustChangePassword = False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Save updated credentials to database
            cursor.execute('''
                UPDATE employees
                SET passwordHash = ?, salt = ?, mustChangePassword = ?
                WHERE Employee_ID = ?
            ''', (self.passwordHash, self.salt, 0, self.employeeID))

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
    def findEmployeeIDBySearch(searchText):
        """Find an employee ID using full name, email, or username.
           Returns: ID, -1 (not found), or -2 (multiple matches)"""
        if not searchText:
            return -1

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Try exact match on unique fields first
            cursor.execute('''
                SELECT Employee_ID FROM employees
                WHERE email = ? OR username = ?
            ''', (searchText, searchText))

            rows = cursor.fetchall()

            if len(rows) == 1:
                conn.close()
                return rows[0]["Employee_ID"]

            # Try full name match ("First Last")
            parts = searchText.strip().split()
            if len(parts) == 2:
                cursor.execute('''
                    SELECT Employee_ID FROM employees
                    WHERE LOWER(first_name) = LOWER(?) AND LOWER(last_name) = LOWER(?)
                ''', (parts[0], parts[1]))

                rows = cursor.fetchall()

                if len(rows) == 1:
                    conn.close()
                    return rows[0]["Employee_ID"]
                elif len(rows) > 1:
                    conn.close()
                    return -2

            conn.close()
            return -1

        except:
            conn.close()
            return -1

    @staticmethod
    def getEmployeeInfoByID(employeeID):
        """Retrieve employee profile information by ID for display purposes"""
        if employeeID == -1:
            return None

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Query database for employee details
            cursor.execute('''
                SELECT Employee_ID, first_name, last_name, email, username, expenses, mustChangePassword
                FROM employees
                WHERE Employee_ID = ?
            ''', (employeeID,))

            row = cursor.fetchone()
            conn.close()

            if row is None:
                return None

            # Convert database row into dictionary for frontend use
            return {
                "employeeID": row["Employee_ID"],
                "firstName": row["first_name"],
                "lastName": row["last_name"],
                "email": row["email"],
                "username": row["username"],
                "expenses": row["expenses"],
                "mustChangePassword": bool(row["mustChangePassword"])
            }

        except:
            conn.close()
            return None

    @staticmethod
    def authenticateEmployee(userName, plainPassword):
        """Verify employee login credentials and return Employee object if valid"""
        if not userName or not plainPassword:
            return None

        conn = get_connection()
        cursor = conn.cursor()

        # Fetch stored credentials for username
        cursor.execute('''
            SELECT Employee_ID, first_name, last_name, email, username, passwordHash, salt, mustChangePassword, expenses
            FROM employees
            WHERE username = ?
        ''', (userName,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        # Compare hashed password with stored hash
        entered_hash = HashUtilities.hash_with_salt(plainPassword, row["salt"])

        if entered_hash == row["passwordHash"]:
            # Return fully populated Employee object on successful login
            return Employee(
                fN=row["first_name"],
                lN=row["last_name"],
                email=row["email"],
                uName=row["username"],
                passwordHash=row["passwordHash"],
                salt=row["salt"],
                empID=row["Employee_ID"],
                mustChangePassword=bool(row["mustChangePassword"]),
                expenses=row["expenses"]
            )

        return None

    def createEmployeeInDB(self):
        """Create a new employee in the database"""
        if not self.firstName or not self.lastName or not self.email or not self.userName or not self.passwordHash:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Insert new employee record into database
            cursor.execute('''
                INSERT INTO employees (first_name, last_name, email, username, passwordHash, salt, expenses, mustChangePassword)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.firstName, self.lastName, self.email, self.userName,
                  self.passwordHash, self.salt, 0.0, 1 if self.mustChangePassword else 0))

            conn.commit()
            self.employeeID = cursor.lastrowid
            conn.close()
            return True

        except Exception:
            conn.close()
            return False

    def updateEmployeeInDB(self):
        """Update existing employee information in the database"""
        if self.employeeID == -1:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Save updated employee profile fields
            cursor.execute('''
                UPDATE employees
                SET first_name = ?, last_name = ?, email = ?, username = ?
                WHERE Employee_ID = ?
            ''', (self.firstName, self.lastName, self.email, self.userName, self.employeeID))

            conn.commit()

            if cursor.rowcount == 0:
                conn.close()
                return False

            conn.close()
            return True

        except Exception:
            conn.close()
            return False

    def deleteEmployeeInDB(self):
        """Delete employee from the database using their ID"""
        if self.employeeID == -1:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Remove employee record from database
            cursor.execute('''
                DELETE FROM employees WHERE Employee_ID = ?
            ''', (self.employeeID,))

            conn.commit()

            if cursor.rowcount == 0:
                conn.close()
                return False

            conn.close()
            return True

        except Exception:
            conn.close()
            return False

    def addExpenseToDB(self, amount, date, description):
        """Add an expense record and update the employee's running expense total"""
        if amount <= 0 or self.employeeID == -1 or not date or not description:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Insert individual expense record
            cursor.execute('''
                INSERT INTO expenses (Employee_ID, amount, date, description)
                VALUES (?, ?, ?, ?)
            ''', (self.employeeID, amount, date, description))

            # Update running total on the employee record
            cursor.execute('''
                UPDATE employees
                SET expenses = expenses + ?
                WHERE Employee_ID = ?
            ''', (amount, self.employeeID))

            conn.commit()
            self.expenses += amount
            conn.close()
            return True

        except Exception:
            conn.close()
            return False