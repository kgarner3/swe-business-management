from datetime import datetime, timedelta
from google import genai
import smtplib
import os
from email.mime.text import MIMEText
from database import get_connection

# Scheduler handles appointment logic, availability checks, and automated email workflows
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")

TEST_EMAIL = "kgarner3@students.towson.edu"

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

    def updateAppointmentStatus(self, appointmentID, newStatus, additionalExpenses=0):
        """Update the status and additional expenses of an appointment."""
        if appointmentID == -1 or newStatus not in ("Scheduled", "Completed", "Cancelled"):
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE appointments
                SET status = ?,
                    additional_expenses = ?
                WHERE Appointment_ID = ?
            ''', (newStatus, additionalExpenses, appointmentID))

            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success

        except Exception as e:
            print("Update appointment status error:", e)
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
    
    @staticmethod
    def sendAppointmentReminders():
        """Sends AI-generated reminder emails for appointments 7 days from today."""
        conn = get_connection()
        cursor = conn.cursor()

        reminder_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        cursor.execute('''
            SELECT
                c.first_name,
                c.email,
                a.date,
                s.name AS service_name
            FROM appointments a
            JOIN customers c ON a.Customer_ID = c.Customer_ID
            JOIN services s ON a.Service_ID = s.Service_ID
            WHERE a.date = ?
            AND a.status = 'Scheduled'
            LIMIT ?
        ''', (reminder_date, MAX_REMINDER_SENDS))

        rows = cursor.fetchall()
        conn.close()

        results = []

        for row in rows:
            recipient = TEST_EMAIL if TEST_EMAIL else row["email"]

            prompt = f"""
            Create an email that reminds a customer about their upcoming appointment.

            Customer Name: {row["first_name"]}
            Service: {row["service_name"]}
            Appointment Date: {row["date"]}

            The email should:
            - Be friendly and professional
            - Be concise (3 to 5 sentences max)
            - Clearly remind them of the appointment details
            - Encourage them to reach out if they need to reschedule
            - Sign emails from "Maryland Contracting Company"

            Do not include a subject line.
            Do not insert brackets for potential address/phone number/hyperlink.

            This is meant to act as a demo to show off AI integration.
            """

            body = Scheduler.generateAIEmail(prompt)

            if not body:
                results.append({
                    "sent": False,
                    "customer": row["first_name"],
                    "email": recipient,
                    "error": "AI generation failed"
                })
                continue

            sent = Scheduler.sendEmail(
                recipient,
                "Appointment Reminder",
                body
            )

            results.append({
                "sent": sent,
                "customer": row["first_name"],
                "email": recipient,
                "service": row["service_name"],
                "date": row["date"],
                "error": "" if sent else "Email failed"
            })

        return results
    
    @staticmethod
    def sendWinBackEmails():
        """Sends AI-generated win-back emails to inactive customers."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                c.Customer_ID,
                c.first_name,
                c.email,
                MAX(a.date) AS last_appointment
            FROM customers c
            JOIN appointments a ON c.Customer_ID = a.Customer_ID
            GROUP BY c.Customer_ID
            HAVING MAX(a.date) < date('now', '-30 days')
            LIMIT ?
        ''', (MAX_WINBACK_SENDS,))

        rows = cursor.fetchall()
        conn.close()

        results = []

        for row in rows:
            recipient = TEST_EMAIL if TEST_EMAIL else row["email"]

            prompt = f"""
            Create a friendly win-back email for a customer who has not scheduled an appointment in a while.

            Customer Name: {row["first_name"]}
            Last Appointment Date: {row["last_appointment"]}

            The email should:
            - Be warm and inviting
            - Mention that it has been a while since their last service
            - Offer 20% off their next service
            - Encourage them to schedule another appointment, do not provide space for a hyperlink or a phone number to call
            - Keep it short and professional
            - Sign emails from "Maryland Contracting Company"

            Do not include a subject line.
            Do not insert brackets for potential address/phone number/hyperlink.
            This is meant to act as a demo to show off AI integration.
            """

            body = Scheduler.generateAIEmail(prompt)

            if not body:
                results.append({
                    "sent": False,
                    "customer": row["first_name"],
                    "email": recipient,
                    "error": "AI generation failed"
                })
                continue

            sent = Scheduler.sendEmail(
                recipient,
                "We Miss You!",
                body
            )

            results.append({
                "sent": sent,
                "customer": row["first_name"],
                "email": recipient,
                "last_appointment": row["last_appointment"],
                "error": "" if sent else "Email failed"
            })

        return results
    
    @staticmethod
    def generateAIEmail(prompt):
        """Uses Gemini AI to generate email body text."""
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print("AI generation error:", e)
            return None
        
    @staticmethod
    def sendEmail(toEmail, subject, body):
        """Sends an email using Gmail SMTP."""
        if not toEmail or not subject or not body:
            return False

        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = f"My Scheduler App <{SENDER_EMAIL}>"
            msg["To"] = toEmail

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)

            return True

        except Exception as e:
            print("Email error:", e)
            return False
