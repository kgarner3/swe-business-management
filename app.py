from flask import Flask, render_template, request, jsonify
from employee import Employee

app = Flask(__name__)

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -----------------------------
# EMPLOYEE LOGIN PAGE
# -----------------------------
@app.route('/employee')
def employee_page():
    return render_template('employee_login.html')


# -----------------------------
# EMPLOYEE LOGIN
# -----------------------------
@app.route('/employee-login', methods=['POST'])
def employee_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    employee_id = Employee.authenticateEmployee(username, password)

    if employee_id != -1:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


# -----------------------------
# DASHBOARD PLACEHOLDER
# -----------------------------
@app.route('/dashboard')
def dashboard():
    return "<h1>Dashboard Placeholder</h1>"


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)