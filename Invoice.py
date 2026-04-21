from datetime import datetime


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

    # =========================
    # Invoice logic methods
    # =========================
    @staticmethod
    def isValidInvoiceDate(invoiceDate):
        try:
            datetime.strptime(invoiceDate, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def findInvoiceID(criteria):
        # TODO: Replace with SQLite query.
        #
        # Planned DB behavior:
        # 1. Search the invoices table
        # 2. Match fields based on non-empty / non-default criteria
        # 3. Return the matching invoiceID if found
        # 4. Return false if no match exists

        return False

    @staticmethod
    def getInvoicesForCustomer(customerID):
        if customerID == -1:
            return []

        # TODO: Replace with SQLite query.
        #
        # Planned DB behavior:
        # 1. Search the invoices table using customerID
        # 2. Return all matching invoices
        # 3. Sort by invoiceDate
        # 4. Return the results as a list

        return []

    @staticmethod
    def getInvoiceByAppointmentID(appointmentID):
        if appointmentID == -1:
            return None

        # TODO: Replace with SQLite query.
        #
        # Planned DB behavior:
        # 1. Search the invoices table using appointmentID
        # 2. Return the matching invoice record if found
        # 3. Return None otherwise

        return None

    def generateInvoice(self):
        if self.customerID == -1 or self.appointmentID == -1 or self.serviceID == -1:
            return False

        if not self.serviceName or self.serviceCost < 0:
            return False

        if not self.invoiceDate:
            self.invoiceDate = datetime.now().strftime("%Y-%m-%d")

        if not self.isValidInvoiceDate(self.invoiceDate):
            return False

        # TODO: Replace with SQLite insertion query.
        #
        # Planned DB behavior:
        # 1. Insert a new invoice record into the invoices table
        # 2. Store customerID, appointmentID, serviceID, serviceName,
        #    serviceCost, and invoiceDate
        # 3. Let the database generate the invoiceID / invoice number
        # 4. Assign the generated invoiceID back to this object
        # 5. Return True if insertion succeeds

        return True

    def updateInvoiceInDB(self):
        if self.invoiceID == -1:
            return False

        if not self.isValidInvoiceDate(self.invoiceDate):
            return False

        # TODO: Replace with SQLite update query.
        #
        # Planned DB behavior:
        # 1. Use invoiceID to locate the invoice record
        # 2. Update editable invoice fields
        # 3. Return True if update succeeds

        return True