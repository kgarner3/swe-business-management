from datetime import datetime, timedelta
from database import get_connection

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
        startDate, endDate = Accounting.getLastMonthDateRange()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT SUM(serviceCost)
            FROM invoices
            WHERE date BETWEEN ? AND ?
        ''', (startDate, endDate))

        row = cursor.fetchone()

        if row and row[0]:
            total_revenue = row[0]
        else:
            total_revenue = 0.0

        conn.close()

        return {
            "reportType": "Revenue",
            "startDate": startDate,
            "endDate": endDate,
            "totalRevenue": total_revenue
        }


    @staticmethod
    def getExpReportLastMonth():
        startDate, endDate = Accounting.getLastMonthDateRange()

        conn = get_connection() 
        cursor = conn.cursor()

        cursor.execute('''
            SELECT SUM(amount)
            FROM expenses
            WHERE date BETWEEN ? AND ?
        ''', (startDate, endDate))

        row = cursor.fetchone()
        if row and row[0]:
            total_expenses = row[0]
        else:
            total_expenses = 0.0

        conn.close()

        return {
            "reportType": "Expenses",
            "startDate": startDate,
            "endDate": endDate,
            "totalExpenses": total_expenses
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