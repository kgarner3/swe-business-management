///////////////////////////////////////////////////////////////////////////////
// Author: Katie Garner
// Description: This is the specification file for the Employee class for the
//				COSC412 Project.
///////////////////////////////////////////////////////////////////////////////
#ifndef EMPLOYEE_H
#define EMPLOYEE_H

#include <string>

using namespace std;

class Employee
{
private:
    string firstName;
    string lastName;
    string email;
    string userName;
    string passwordHash;
    string salt;
    int employeeID;
    double expenses;

public:
    // Default constructor
    Employee();

    // Constructor for new employee
    Employee(string fN, string lN, string email, string uName, int empID);

    // Constructor for loading employee from DB
    Employee(string fN, string lN, string email, string uName, string pHash, string s, int empID);

    string getFirstName() const;
    string getLastName() const;
    string getEmail() const;
    int getEmployeeID() const;
    double getExpenses() const;

    void setUserName(const string& uName);
    void setPassword(const string& plainPassword);
    bool verifyPassword(const string& plainPassword) const;
    bool addExpenseToDB(double exp);
};

#endif
