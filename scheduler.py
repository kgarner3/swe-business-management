from datetime import datetime, timedelta
from google import genai
import smtplib
from email.mime.text import MIMEText
from database import get_connection

# Scheduler handles appointment logic, availability checks, and automated email workflows
client = genai.Client(api_key="This is where the key goes")

# Email information for win-back & reminder emails
SENDER_EMAIL = "team1.scheduler@gmail.com"
SENDER_PASSWORD = "email password goes here"

# Set email for testing. Set to None to send to actual customer emails.
TEST_EMAIL = "student email goes here"

# Demo safety limits
MAX_REMINDER_SENDS = 3
MAX_WINBACK_SENDS = 3

class Scheduler:
    # Constructor
    def __init__(self):
        pass

    @staticmethod
    def checkServiceExists(serviceID):
        """Check if a service exists in the database"""
        if serviceID == -1:
            return False

        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Query service existence
            cursor.execute('SELECT 1 FROM services WHERE Service_ID = ?', (serviceID,))
            exists = cursor.fetchone() is not None
            conn.close()
            return exists
        except:
            conn.close()
            return False

    @staticmethod
    def isEmployeeAvailable(employeeID, appointmentDate):
        """Check if an employee is available on a given date"""
        if employeeID == -1:
            return False

        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Count non-cancelled appointments for employee on that date
            cursor.execute('''
                SELECT COUNT(*) FROM appointments
                WHERE Employee_ID = ? AND date = ? AND status != 'Cancelled'
            ''', (employeeID, appointmentDate))
            count = cursor.fetchone()[0]
            conn.close()
            return count == 0
        except:
            conn.close()
            return False

    @staticmethod
    def isCustomerAvailable(customerID, appointmentDate):
        """Check if a customer is available on a given date"""
        if customerID == -1:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Count non-cancelled appointments for customer on that date
            cursor.execute('''
                SELECT COUNT(*) FROM appointments
                WHERE Customer_ID = ? AND date = ? AND status != 'Cancelled'
            ''', (customerID, appointmentDate))
            count = cursor.fetchone()[0]
            conn.close()
            return count == 0
        except:
            conn.close()
            return False

    def createAppointment(self, customerID, employeeID, serviceID, appointmentDate,
                          description="", additionalExpenses=0.0):
        """Create a new appointment after validating inputs and availability"""
        if customerID == -1 or employeeID == -1 or serviceID == -1:
            return False

        # Validate date format
        try:
            datetime.strptime(appointmentDate, "%Y-%m-%d")
        except ValueError:
            return False

        # Validate service and scheduling conflicts
        if not self.checkServiceExists(serviceID):
            return False
        if not self.isEmployeeAvailable(employeeID, appointmentDate):
            return False
        if not self.isCustomerAvailable(customerID, appointmentDate):
            return False

        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Pull cost from the service
            cursor.execute('SELECT cost FROM services WHERE Service_ID = ?', (serviceID,))
            row = cursor.fetchone()
            cost = row["cost"] if row else 0.0

            # Insert appointment record
            cursor.execute('''
                INSERT INTO appointments
                    (Customer_ID, Employee_ID, Service_ID, date, description,
                     cost, additional_expenses, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (customerID, employeeID, serviceID, appointmentDate,
                  description, cost, additionalExpenses, "Scheduled"))

            conn.commit()
            conn.close()
            return True

        except Exception:
            conn.close()
            return False

    def searchAppointments(self, appointmentID=-1, customerID=-1, employeeID=-1,
                           serviceID=-1, appointmentDate=""):
        """Search for appointments using optional filters"""

        # Prevent empty search
        if (appointmentID == -1 and customerID == -1 and employeeID == -1 and
                serviceID == -1 and not appointmentDate):
            return []

        # Validate date if provided
        if appointmentDate:
            try:
                datetime.strptime(appointmentDate, "%Y-%m-%d")
            except ValueError:
                return []

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Build query based on provided parameters
            query  = "SELECT * FROM appointments WHERE 1=1"
            params = []

            if appointmentID != -1:
                query += " AND Appointment_ID = ?"
                params.append(appointmentID)
            if customerID != -1:
                query += " AND Customer_ID = ?"
                params.append(customerID)
            if employeeID != -1:
                query += " AND Employee_ID = ?"
                params.append(employeeID)
            if serviceID != -1:
                query += " AND Service_ID = ?"
                params.append(serviceID)
            if appointmentDate:
                query += " AND date = ?"
                params.append(appointmentDate)

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]

        except:
            conn.close()
            return []

    def deleteAppointment(self, appointmentID):
        """Cancel an appointment (soft delete by updating status)"""
        if appointmentID == -1:
            return False

        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Mark appointment as cancelled instead of removing it
            cursor.execute('''
                UPDATE appointments SET status = 'Cancelled'
                WHERE Appointment_ID = ?
            ''', (appointmentID,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except:
            conn.close()
            return False

    def updateAppointmentStatus(self, appointmentID, newStatus):
        """Update the status of an appointment (Scheduled, Completed, Cancelled)"""
        if appointmentID == -1 or newStatus not in ("Scheduled", "Completed", "Cancelled"):
            return False

        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Save new status
            cursor.execute('''
                UPDATE appointments SET status = ? WHERE Appointment_ID = ?
            ''', (newStatus, appointmentID))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except:
            conn.close()
            return False
        
    @staticmethod
    def getAllAppointments():
        """Retrieve all appointments with joined customer, employee, and service data"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT
                    a.Appointment_ID,
                    a.date,
                    a.description,
                    a.cost,
                    a.additional_expenses,
                    a.status,
                    c.first_name || ' ' || c.last_name AS customer_name,
                    c.Customer_ID,
                    e.first_name || ' ' || e.last_name AS employee_name,
                    e.Employee_ID,
                    s.name AS service_name,
                    s.Service_ID
                FROM appointments a
                JOIN customers c ON a.Customer_ID = c.Customer_ID
                JOIN employees e ON a.Employee_ID = e.Employee_ID
                JOIN services s ON a.Service_ID = s.Service_ID
                ORDER BY a.date ASC
            ''')
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except:
            conn.close()
            return []

    @staticmethod
    def getAppointmentsByCustomer(customerID):
        """Retrieve all appointments for a specific customer"""
        if customerID == -1:
            return []

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT
                    a.Appointment_ID,
                    a.date,
                    a.description,
                    a.cost,
                    a.additional_expenses,
                    a.status,
                    e.first_name || ' ' || e.last_name AS employee_name,
                    e.Employee_ID,
                    s.name AS service_name,
                    s.Service_ID
                FROM appointments a
                JOIN employees e ON a.Employee_ID = e.Employee_ID
                JOIN services s ON a.Service_ID = s.Service_ID
                WHERE a.Customer_ID = ?
                ORDER BY a.date ASC
            ''', (customerID,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except:
            conn.close()
            return []

    @staticmethod
    def getLastAppointmentForCustomer(customerID):
        """Get the most recent appointment for a customer"""
        if customerID == -1:
            return None

        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Order by date descending to get latest appointment
            cursor.execute('''
                SELECT * FROM appointments
                WHERE Customer_ID = ?
                ORDER BY date DESC
                LIMIT 1
            ''', (customerID,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except:
            conn.close()
            return None

    @staticmethod
    def checkWinBackOpportunity(customerID):
        """Determine if a customer qualifies for a win-back email"""
        if customerID == -1:
            return False

        lastAppointment = Scheduler.getLastAppointmentForCustomer(customerID)

        if lastAppointment is None:
            return False

        lastDateString = lastAppointment.get("date")
        if not lastDateString:
            return False

        try:
            lastDate = datetime.strptime(lastDateString, "%Y-%m-%d")
        except ValueError:
            return False

        # Compare last appointment date to 30-day cutoff
        oneMonthAgo = datetime.now() - timedelta(days=30)
        return lastDate < oneMonthAgo
