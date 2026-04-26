from datetime import datetime
from database import get_connection

class Invoice:
    class SearchCriteria:
        def __init__(self, invoiceID=-1, customerID=-1, appointmentID=-1, invoiceDate=""):
            self.invoiceID = invoiceID
            self.customerID = customerID
            self.appointmentID = appointmentID
            self.invoiceDate = invoiceDate

    def __init__(self, customerID=-1, appointmentID=-1, serviceID=-1,
                 serviceName="", serviceCost=0.0, invoiceDate="", invoiceID=-1):
        self.invoiceID = invoiceID
        self.customerID = customerID
        self.appointmentID = appointmentID
        self.serviceID = serviceID
        self.serviceName = serviceName
        self.serviceCost = serviceCost
        self.invoiceDate = invoiceDate

    # Getters
    def getInvoiceID(self):
        return self.invoiceID

    def getCustomerID(self):
        return self.customerID

    def getAppointmentID(self):
        return self.appointmentID

    def getServiceID(self):
        return self.serviceID

    def getServiceName(self):
        return self.serviceName

    def getServiceCost(self):
        return self.serviceCost

    def getInvoiceDate(self):
        return self.invoiceDate

    @staticmethod
    def getInvoicesForCustomer(customerID):
        """Get invoices for customer dashboard"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM invoices
            WHERE Customer_ID = ?
            ORDER BY invoice_date DESC
        ''', (customerID,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(r) for r in rows]

    def isValidInvoiceDate(invoiceDate):
        """Check that the invoice date is valid and uses YYYY-MM-DD format."""
        try:
            datetime.strptime(invoiceDate, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def generateInvoice(self):
        """Create an invoice for this appointment if one does not already exist."""

        if self.customerID == -1 or self.appointmentID == -1 or self.serviceID == -1:
            return False

        if not self.serviceName or self.serviceCost < 0:
            return False

        if not self.invoiceDate:
            self.invoiceDate = datetime.now().strftime("%Y-%m-%d")

        if not self.isValidInvoiceDate(self.invoiceDate):
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Prevent duplicate invoices for the same appointment
            cursor.execute('''
                SELECT Invoice_ID
                FROM invoices
                WHERE Appointment_ID = ?
            ''', (self.appointmentID,))

            existing_invoice = cursor.fetchone()

            if existing_invoice:
                self.invoiceID = existing_invoice["Invoice_ID"]
                conn.close()
                return True

            # Create new invoice
            cursor.execute('''
                INSERT INTO invoices
                (Customer_ID, Appointment_ID, Service_ID, service_name, service_cost, invoice_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.customerID,
                self.appointmentID,
                self.serviceID,
                self.serviceName,
                self.serviceCost,
                self.invoiceDate
            ))

            self.invoiceID = cursor.lastrowid
            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print("Invoice insert error:", e)
            conn.close()
            return False
