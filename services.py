from database import get_connection

# Service class handles service database operations
class Service:
    def __init__(self, name="", description="", cost=0.0, serviceID=-1):
        """Initialize a Service object with service details"""
        self.name        = name
        self.description = description
        self.cost        = cost
        self.serviceID   = serviceID

    @staticmethod
    def getAllServices():
        """
        Returns a list of all services as dicts, ordered by name.
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Query all service records
            cursor.execute('''
                SELECT Service_ID, name, description, cost
                FROM services
                ORDER BY name ASC
            ''')

            rows = cursor.fetchall()
            conn.close()

            # Convert rows into dictionaries for frontend use
            return [
                {
                    "serviceID":   row["Service_ID"],
                    "name":        row["name"],
                    "description": row["description"],
                    "cost":        row["cost"]
                }
                for row in rows
            ]

        except:
            conn.close()
            return []

    @staticmethod
    def getServiceByID(serviceID):
        """
        Returns a single service as a dict, or None if not found.
        """
        if serviceID == -1:
            return None

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Query database for matching service
            cursor.execute('''
                SELECT Service_ID, name, description, cost
                FROM services
                WHERE Service_ID = ?
            ''', (serviceID,))

            row = cursor.fetchone()
            conn.close()

            if row is None:
                return None

            # Convert row into dictionary for frontend use
            return {
                "serviceID":   row["Service_ID"],
                "name":        row["name"],
                "description": row["description"],
                "cost":        row["cost"]
            }

        except:
            conn.close()
            return None


    @staticmethod
    def findServiceIDByName(searchText):
        """
        Searches services by name (case-insensitive, partial match).
        - Returns Service_ID if exactly one match is found.
        - Returns -2 if multiple matches are found.
        - Returns -1 if no match is found.
        """
        if not searchText:
            return -1

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Search service names using partial match
            cursor.execute('''
                SELECT Service_ID FROM services
                WHERE LOWER(name) LIKE LOWER(?)
            ''', (f"%{searchText}%",))

            rows = cursor.fetchall()
            conn.close()

            if len(rows) == 1:
                return rows[0]["Service_ID"]
            elif len(rows) > 1:
                return -2

            return -1

        except:
            conn.close()
            return -1

    def updateServiceInDB(self):
        """Update an existing service in the database"""
        if self.serviceID == -1:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Save updated service fields
            cursor.execute('''
                UPDATE services
                SET name = ?, description = ?, cost = ?
                WHERE Service_ID = ?
            ''', (self.name, self.description, self.cost, self.serviceID))

            conn.commit()

            if cursor.rowcount == 0:
                conn.close()
                return False

            conn.close()
            return True

        except Exception:
            conn.close()
            return False

    def deleteServiceInDB(self):
        """Delete a service from the database using its ID"""
        if self.serviceID == -1:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Remove service record from database
            cursor.execute('''
                DELETE FROM services WHERE Service_ID = ?
            ''', (self.serviceID,))

            conn.commit()

            if cursor.rowcount == 0:
                conn.close()
                return False

            conn.close()
            return True

        except Exception:
            conn.close()
            return False