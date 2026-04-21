from flask import Flask, render_template, request, jsonify, session
from employee import Employee
from customer import Customer
from services import Service
from scheduler import Scheduler
from database import init_db, seed_customers, seed_employees, seed_services, seed_appointments, get_connection

# Main Flask app: manages routing, session handling, and communication between the frontend and database
app = Flask(__name__)
app.secret_key = "scheduler-secret-key"

# Home page ==============================================================
@app.route('/')
def home():
    return render_template('index.html')

# Employee login page ====================================================
@app.route('/employee')
def employee_page():
    return render_template('employee_login.html')

# Employee login logic =========================================================
@app.route('/employee-login', methods=['POST'])
def employee_login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    auth_result = Employee.authenticateEmployee(username, password)

    if auth_result:
        session["employeeID"] = auth_result.employeeID
        session["employeeFirstName"] = auth_result.firstName

        return jsonify({
            "success": True,
            "employeeID": auth_result.employeeID,
            "firstName": auth_result.firstName,
            "mustChangePassword": auth_result.mustChangePassword
        })

    return jsonify({
        "success": False,
        "message": "Invalid username or password."
    })

# Employee change password page ===========================================
@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        return render_template('employee_change_password.html')

    data = request.get_json()
    new_password = data.get('newPassword', '').strip()

    if not new_password:
        return jsonify({
            "success": False,
            "message": "Password cannot be empty."
        })

    employee_id = session.get("employeeID")
    if not employee_id:
        return jsonify({
            "success": False,
            "message": "No employee is currently logged in."
        })

    employee = Employee(empID=employee_id)
    changed = employee.changePassword(new_password)

    if changed:
        return jsonify({
            "success": True,
            "message": "Password updated successfully."
        })

    return jsonify({
        "success": False,
        "message": "Unable to change password."
    })

# Dashboard functionality ===================================================================
@app.route('/dashboard')
def dashboard():
    return render_template('employee_dashboard.html')


@app.route('/get-employee-name')
def get_employee_name():
    first_name = session.get("employeeFirstName")
    if first_name:
        return jsonify({"success": True, "firstName": first_name})

    employee_id = session.get("employeeID")
    if not employee_id:
        return jsonify({"success": False, "message": "Not logged in."})

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT first_name FROM employees WHERE Employee_ID = ?', (employee_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        session["employeeFirstName"] = row["first_name"]
        return jsonify({"success": True, "firstName": row["first_name"]})

    return jsonify({"success": False, "message": "Employee not found."})

# Create customer tab =========================================================================
@app.route('/create-customer', methods=['POST'])
def create_customer():
    data = request.get_json()

    first_name = data.get('firstName', '').strip()
    last_name = data.get('lastName', '').strip()
    phone_number = data.get('phoneNumber', '').strip()
    address = data.get('address', '').strip()
    email = data.get('email', '').strip()

    if not first_name or not last_name or not phone_number or not address or not email:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        })

    new_customer = Customer(first_name, last_name, phone_number, address, email)

    created = new_customer.createCustomerInDB()

    if created:
        return jsonify({
            "success": True,
            "message": f"Customer created. Username: {new_customer.userName} | Temporary Password: temp123",
            "username": new_customer.userName,
            "temporaryPassword": "temp123"
        })

    return jsonify({
        "success": False,
        "message": "Unable to create customer profile."
    })

# Find customer information for delete confirmation ==============================================================
@app.route('/find-customer-for-delete', methods=['POST'])
def find_customer_for_delete():
    data = request.get_json()
    search_text = data.get('searchText', '').strip()

    if not session.get("employeeID"):
        return jsonify({
            "success": False,
            "message": "You must be logged in as an employee."
        })

    if not search_text:
        return jsonify({
            "success": False,
            "message": "Customer search information is required."
        })

    customer_id = Customer.findCustomerIDBySearch(search_text)

    if customer_id == -2:
        return jsonify({
            "success": False,
            "message": "Multiple customers matched that name. Please use email, username, or phone number."
        })

    if customer_id == -1:
        return jsonify({
            "success": False,
            "message": "Customer not found."
        })

    customer_info = Customer.getCustomerInfoByID(customer_id)

    if customer_info is None:
        return jsonify({
            "success": False,
            "message": "Unable to load customer information."
        })

    return jsonify({
        "success": True,
        "customer": customer_info
    })

# Delete customer after confirmation ===============================================================
@app.route('/delete-customer', methods=['POST'])
def delete_customer():
    data = request.get_json()
    customer_id = data.get('customerID', -1)

    if not session.get("employeeID"):
        return jsonify({
            "success": False,
            "message": "You must be logged in as an employee."
        })

    try:
        customer_id = int(customer_id)
    except:
        return jsonify({
            "success": False,
            "message": "Invalid customer ID."
        })

    if customer_id == -1:
        return jsonify({
            "success": False,
            "message": "Customer ID is required."
        })

    customer = Customer(custID=customer_id)
    deleted = customer.deleteCustomerInDB()

    if deleted:
        return jsonify({
            "success": True,
            "message": "Customer deleted successfully."
        })

    return jsonify({
        "success": False,
        "message": "Unable to delete customer."
    })

# Find customer information for update confirmation ================================================
@app.route('/find-customer-for-update', methods=['POST'])
def find_customer_for_update():
    data = request.get_json()
    search_text = data.get('searchText', '').strip()

    if not session.get("employeeID"):
        return jsonify({
            "success": False,
            "message": "You must be logged in as an employee."
        })

    if not search_text:
        return jsonify({
            "success": False,
            "message": "Customer search information is required."
        })

    customer_id = Customer.findCustomerIDBySearch(search_text)

    if customer_id == -2:
        return jsonify({
            "success": False,
            "message": "Multiple customers matched that name. Please use email, username, or phone number."
        })

    if customer_id == -1:
        return jsonify({
            "success": False,
            "message": "Customer not found."
        })

    customer_info = Customer.getCustomerInfoByID(customer_id)

    if customer_info is None:
        return jsonify({
            "success": False,
            "message": "Unable to load customer information."
        })

    return jsonify({
        "success": True,
        "customer": customer_info
    })

# Update customer after confirmation ===============================================================
@app.route('/update-customer', methods=['POST'])
def update_customer():
    data = request.get_json()

    if not session.get("employeeID"):
        return jsonify({
            "success": False,
            "message": "You must be logged in as an employee."
        })

    customer_id = data.get('customerID', -1)
    first_name = data.get('firstName', '').strip()
    last_name = data.get('lastName', '').strip()
    phone_number = data.get('phoneNumber', '').strip()
    address = data.get('address', '').strip()
    email = data.get('email', '').strip()
    username = data.get('username', '').strip()

    try:
        customer_id = int(customer_id)
    except:
        return jsonify({
            "success": False,
            "message": "Invalid customer ID."
        })

    if customer_id == -1 or not first_name or not last_name or not phone_number or not address or not email:
        return jsonify({
            "success": False,
            "message": "All customer fields are required."
        })

    customer = Customer(
        fN=first_name,
        lN=last_name,
        pN=phone_number,
        addr=address,
        email=email,
        custID=customer_id,
        uName=username
    )

    updated = customer.updateCustomerInDB()

    if updated:
        return jsonify({
            "success": True,
            "message": "Customer profile updated successfully."
        })

    return jsonify({
        "success": False,
        "message": "Unable to update customer profile."
    })

# Create Employees ======================================================================================
@app.route('/create-employee', methods=['POST'])
def create_employee():
    data = request.get_json()

    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    first_name = data.get('firstName', '').strip()
    last_name  = data.get('lastName', '').strip()
    email      = data.get('email', '').strip()
    username   = data.get('username', '').strip()

    if not first_name or not last_name or not email or not username:
        return jsonify({"success": False, "message": "All fields are required."})

    new_employee = Employee(fN=first_name, lN=last_name, email=email, uName=username)
    new_employee.setTemporaryPassword("temp123")

    created = new_employee.createEmployeeInDB()

    if created:
        return jsonify({
            "success": True,
            "message": f"Employee created. Username: {new_employee.userName} | Temporary Password: temp123",
            "username": new_employee.userName,
            "temporaryPassword": "temp123"
        })

    return jsonify({"success": False, "message": "Unable to create employee. Username or email may already exist."})

# Find employee information for delete confirmation =============================================================
@app.route('/find-employee-for-delete', methods=['POST'])
def find_employee_for_delete():
    data = request.get_json()
    search_text = data.get('searchText', '').strip()

    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    if not search_text:
        return jsonify({"success": False, "message": "Employee search information is required."})

    employee_id = Employee.findEmployeeIDBySearch(search_text)

    if employee_id == -2:
        return jsonify({"success": False, "message": "Multiple employees matched that name. Please use email or username."})

    if employee_id == -1:
        return jsonify({"success": False, "message": "Employee not found."})

    if employee_id == session.get("employeeID"):
        return jsonify({"success": False, "message": "You cannot delete your own account."})

    employee_info = Employee.getEmployeeInfoByID(employee_id)

    if employee_info is None:
        return jsonify({"success": False, "message": "Unable to load employee information."})

    return jsonify({"success": True, "employee": employee_info})

# Delete employee after confirmation =================================================================================
@app.route('/delete-employee', methods=['POST'])
def delete_employee():
    data = request.get_json()
    employee_id = data.get('employeeID', -1)

    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    try:
        employee_id = int(employee_id)
    except:
        return jsonify({"success": False, "message": "Invalid employee ID."})

    if employee_id == -1:
        return jsonify({"success": False, "message": "Employee ID is required."})

    if employee_id == session.get("employeeID"):
        return jsonify({"success": False, "message": "You cannot delete your own account."})

    employee = Employee(empID=employee_id)
    deleted = employee.deleteEmployeeInDB()

    if deleted:
        return jsonify({"success": True, "message": "Employee deleted successfully."})

    return jsonify({"success": False, "message": "Unable to delete employee."})

# Find employee information for update confirmation ======================================================================
@app.route('/find-employee-for-update', methods=['POST'])
def find_employee_for_update():
    data = request.get_json()
    search_text = data.get('searchText', '').strip()

    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    if not search_text:
        return jsonify({"success": False, "message": "Employee search information is required."})

    employee_id = Employee.findEmployeeIDBySearch(search_text)

    if employee_id == -2:
        return jsonify({"success": False, "message": "Multiple employees matched that name. Please use email or username."})

    if employee_id == -1:
        return jsonify({"success": False, "message": "Employee not found."})

    employee_info = Employee.getEmployeeInfoByID(employee_id)

    if employee_info is None:
        return jsonify({"success": False, "message": "Unable to load employee information."})

    return jsonify({"success": True, "employee": employee_info})

# Delete employee after confirmation ========================================================================================
@app.route('/update-employee', methods=['POST'])
def update_employee():
    data = request.get_json()

    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    employee_id = data.get('employeeID', -1)
    first_name  = data.get('firstName', '').strip()
    last_name   = data.get('lastName', '').strip()
    email       = data.get('email', '').strip()
    username    = data.get('username', '').strip()

    try:
        employee_id = int(employee_id)
    except:
        return jsonify({"success": False, "message": "Invalid employee ID."})

    if employee_id == -1 or not first_name or not last_name or not email or not username:
        return jsonify({"success": False, "message": "All employee fields are required."})

    employee = Employee(fN=first_name, lN=last_name, email=email, uName=username, empID=employee_id)
    updated = employee.updateEmployeeInDB()

    if updated:
        return jsonify({"success": True, "message": "Employee profile updated successfully."})

    return jsonify({"success": False, "message": "Unable to update employee profile."})

# Show all services offered =================================================================================================
@app.route('/get-all-services')
def get_all_services():
    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    services = Service.getAllServices()
    return jsonify({"success": True, "services": services})

# Show all appointments =====================================================================================
@app.route('/get-all-appointments')
def get_all_appointments():
    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    appointments = Scheduler.getAllAppointments()
    return jsonify({"success": True, "appointments": appointments})

# Schedule an appointment ===================================================================================
@app.route('/schedule-appointment', methods=['POST'])
def schedule_appointment():
    data = request.get_json()

    # Employees only can schedule
    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    customer_id         = data.get('customerID', -1)
    employee_id         = data.get('employeeID', -1)
    service_id          = data.get('serviceID', -1)
    date                = data.get('date', '').strip()
    additional_expenses = data.get('additionalExpenses', 0.0)

    try:
        customer_id         = int(customer_id)
        employee_id         = int(employee_id)
        service_id          = int(service_id)
        additional_expenses = float(additional_expenses)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid appointment data."})

    if customer_id == -1 or employee_id == -1 or service_id == -1 or not date:
        return jsonify({"success": False, "message": "Customer, employee, service, and date are all required."})

    # Validate date is in 2026
    if not date.startswith("2026-"):
        return jsonify({"success": False, "message": "Appointments must be scheduled in 2026."})

    # Check availability
    if not Scheduler.isCustomerAvailable(customer_id, date):
        return jsonify({"success": False, "message": "That customer already has an appointment on this date."})

    if not Scheduler.isEmployeeAvailable(employee_id, date):
        return jsonify({"success": False, "message": "That employee is already booked on this date."})

    # Pull service cost
    service_info = Service.getServiceByID(service_id)
    if service_info is None:
        return jsonify({"success": False, "message": "Service not found."})

    scheduler = Scheduler()
    created = scheduler.createAppointment(
        customerID=customer_id,
        employeeID=employee_id,
        serviceID=service_id,
        appointmentDate=date,
        additionalExpenses=additional_expenses
    )

    if created:
        return jsonify({
            "success": True,
            "message": f"Appointment scheduled for {date}.",
        })

    return jsonify({"success": False, "message": "Unable to schedule appointment."})

# Update expenses if needed =====================================================================
@app.route('/save-appointment-expenses', methods=['POST'])
def save_appointment_expenses():
    data = request.get_json()

    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    appointment_id      = data.get('appointmentID', -1)
    additional_expenses = data.get('additionalExpenses', None)

    try:
        appointment_id = int(appointment_id)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid appointment ID."})

    if appointment_id == -1 or additional_expenses is None:
        return jsonify({"success": False, "message": "Appointment ID and expenses are required."})

    try:
        additional_expenses = float(additional_expenses)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid additional expenses value."})

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE appointments SET additional_expenses = ? WHERE Appointment_ID = ?
        ''', (additional_expenses, appointment_id))
        conn.commit()
    except Exception:
        conn.close()
        return jsonify({"success": False, "message": "Unable to save expenses."})
    conn.close()

    return jsonify({"success": True, "message": "Expenses saved."})

# Flag an appointment as cancelled or completed ====================================================
@app.route('/update-appointment-status', methods=['POST'])
def update_appointment_status():
    data = request.get_json()

    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    appointment_id      = data.get('appointmentID', -1)
    new_status          = data.get('status', '').strip()
    additional_expenses = data.get('additionalExpenses', None)

    try:
        appointment_id = int(appointment_id)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid appointment ID."})

    if appointment_id == -1 or new_status not in ("Scheduled", "Completed", "Cancelled"):
        return jsonify({"success": False, "message": "Valid appointment ID and status are required."})

    # Update expenses if provided
    if additional_expenses is not None:
        try:
            additional_expenses = float(additional_expenses)
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "Invalid additional expenses value."})

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE appointments SET additional_expenses = ? WHERE Appointment_ID = ?
            ''', (additional_expenses, appointment_id))
            conn.commit()
        except Exception as e:
            conn.close()
            return jsonify({"success": False, "message": "Unable to save additional expenses."})
        conn.close()

    scheduler = Scheduler()
    updated = scheduler.updateAppointmentStatus(appointment_id, new_status)

    if updated:
        return jsonify({"success": True, "message": f"Appointment marked as {new_status}."})

    return jsonify({"success": False, "message": "Unable to update appointment status."})

# Show employees in a dropdown menu =====================================================================
@app.route('/get-employees-list')
def get_employees_list():
    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Employee_ID, first_name || ' ' || last_name AS name
        FROM employees ORDER BY first_name ASC
    ''')
    rows = cursor.fetchall()
    conn.close()

    return jsonify({"success": True, "employees": [dict(r) for r in rows]})

# Show customers in a dropdown menu ======================================================================
@app.route('/get-customers-list')
def get_customers_list():
    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Customer_ID, first_name || ' ' || last_name AS name
        FROM customers ORDER BY first_name ASC
    ''')
    rows = cursor.fetchall()
    conn.close()

    return jsonify({"success": True, "customers": [dict(r) for r in rows]})

# AI reminder email integration =======================================================================================================
@app.route('/trigger-reminders', methods=['POST'])
def trigger_reminders():
    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    results = Scheduler.sendAppointmentReminders()
    sent = [r for r in results if r.get("sent")]
    failed = [r for r in results if not r.get("sent")]

    return jsonify({
        "success": True,
        "sent": sent,
        "failed": failed,
        "message": f"{len(sent)} reminder email(s) sent, {len(failed)} failed."
    })

# AI win-back email integration =======================================================================================================
@app.route('/trigger-winback', methods=['POST'])
def trigger_winback():
    if not session.get("employeeID"):
        return jsonify({"success": False, "message": "You must be logged in as an employee."})

    results = Scheduler.sendWinBackEmails()
    sent = [r for r in results if r.get("sent")]
    failed = [r for r in results if not r.get("sent")]

    return jsonify({
        "success": True,
        "sent": sent,
        "failed": failed,
        "message": f"{len(sent)} win-back email(s) sent, {len(failed)} failed."
    })

# Customer login page ====================================================
@app.route('/customer')
def customer_page():
    return render_template('customer_login.html')

# Customer login logic ==========================================================
@app.route('/customer-login', methods=['POST'])
def customer_login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    auth_result = Customer.authenticateCustomer(username, password)

    if auth_result:
        session["customerID"] = auth_result["customerID"]

        # Fetch first name for the welcome message
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT first_name FROM customers WHERE Customer_ID = ?', (auth_result["customerID"],))
        row = cursor.fetchone()
        conn.close()
        if row:
            session["customerFirstName"] = row["first_name"]

        return jsonify({
            "success": True,
            "customerID": auth_result["customerID"],
            "mustChangePassword": auth_result["mustChangePassword"]
        })

    return jsonify({
        "success": False,
        "message": "Invalid username or password."
    })

# Customer change password page================================================
@app.route('/customer-change-password', methods=['GET', 'POST'])
def customer_change_password():
    if request.method == 'GET':
        return render_template('customer_change_password.html')

    data = request.get_json()
    new_password = data.get('newPassword', '').strip()

    if not new_password:
        return jsonify({
            "success": False,
            "message": "Password cannot be empty."
        })

    customer_id = session.get("customerID")
    if not customer_id:
        return jsonify({
            "success": False,
            "message": "No customer is currently logged in."
        })

    customer = Customer(custID=customer_id)
    changed = customer.changePassword(new_password)

    if changed:
        return jsonify({
            "success": True,
            "message": "Password updated successfully."
        })

    return jsonify({
        "success": False,
        "message": "Unable to change password."
    })

# Get customer first name for dashboard display ================================================================
@app.route('/get-customer-name')
def get_customer_name():
    first_name = session.get("customerFirstName")
    if first_name:
        return jsonify({"success": True, "firstName": first_name})

    customer_id = session.get("customerID")
    if not customer_id:
        return jsonify({"success": False, "message": "Not logged in."})

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT first_name FROM customers WHERE Customer_ID = ?', (customer_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        session["customerFirstName"] = row["first_name"]
        return jsonify({"success": True, "firstName": row["first_name"]})

    return jsonify({"success": False, "message": "Customer not found."})

# Redirect to customer dashboard ==================================================================================
@app.route('/customer-dashboard')
def customer_dashboard():
    return render_template('customer_dashboard.html')

# Show customer appointments ======================================================================================
@app.route('/get-my-appointments')
def get_my_appointments():
    customer_id = session.get("customerID")
    if not customer_id:
        return jsonify({"success": False, "message": "You must be logged in as a customer."})

    appointments = Scheduler.getAppointmentsByCustomer(customer_id)
    return jsonify({"success": True, "appointments": appointments})

# Main ============================================================================================================
if __name__ == '__main__':
    init_db()
    seed_customers()
    seed_employees()
    seed_services()
    seed_appointments()

    app.run(debug=True)