from datetime import datetime, timedelta

class Accounting:
    # Constructor
    def __init__(self):
        pass

    # Helper methods
    @staticmethod
    def getLastMonthDateRange():
        """Returns a simple 30-day date range ending today"""
        endDate = datetime.now()
        startDate = endDate - timedelta(days=30)
        return startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d")

    # Report methods
    @staticmethod
    def getRevReportLastMonth():
        # TODO: Replace with SQLite query.
        #
        # Planned DB behavior:
        # 1. Search the invoices table for invoices from the last 30 days
        # 2. Sum the serviceCost values for those invoices
        # 3. Return a revenue report object or dictionary
        #
        # Example return format:
        # {
        #     "reportType": "Revenue",
        #     "startDate": "YYYY-MM-DD",
        #     "endDate": "YYYY-MM-DD",
        #     "totalRevenue": 0.0
        # }

        startDate, endDate = Accounting.getLastMonthDateRange()

        # Temporary placeholder behavior
        return {
            "reportType": "Revenue",
            "startDate": startDate,
            "endDate": endDate,
            "totalRevenue": 0.0
        }

    @staticmethod
    def getExpReportLastMonth():
        # TODO: Replace with SQLite query.
        #
        # Planned DB behavior:
        # 1. Search the employee expenses data from the last 30 days
        # 2. Sum all recorded expenses in that time period
        # 3. Return an expense report object or dictionary
        #
        # Example return format:
        # {
        #     "reportType": "Expenses",
        #     "startDate": "YYYY-MM-DD",
        #     "endDate": "YYYY-MM-DD",
        #     "totalExpenses": 0.0
        # }

        startDate, endDate = Accounting.getLastMonthDateRange()

        # Temporary placeholder behavior
        return {
            "reportType": "Expenses",
            "startDate": startDate,
            "endDate": endDate,
            "totalExpenses": 0.0
        }

    @staticmethod
    def generateMasterReportLastMonth():
        # Combines revenue, expenses, and income into one report
        revenueReport = Accounting.getRevReportLastMonth()
        expenseReport = Accounting.getExpReportLastMonth()

        totalRevenue = revenueReport["totalRevenue"]
        totalExpenses = expenseReport["totalExpenses"]
        totalIncome = totalRevenue - totalExpenses

        return {
            "reportTitle": "Last Month Financial Summary",
            "startDate": revenueReport["startDate"],
            "endDate": revenueReport["endDate"],
            "revenue": revenueReport["totalRevenue"],
            "expenses": expenseReport["totalExpenses"],
            "income": totalIncome
        }