///////////////////////////////////////////////////////////////////////////////
// Author: Katie Garner
// Description: This is the specification file for the Customer class for the
//				COSC412 Project.
///////////////////////////////////////////////////////////////////////////////
#ifndef CUSTOMER_H
#define CUSTOMER_H

#include <string>				// Needed for strings
#include <vector>				// Needed for vectors of strings

using namespace std;			// Indicates standard naming convention

class Customer {
private:
	string firstName;
	string lastName;
	string phoneNumber;
	string address;
	string email;
	int customerID;				// Set by DB
public:
	// Description: Virtual form to be filled out to search for Customer in database
	struct SearchCriteria {
		int customerID = -1;
		string firstName = "";
		string lastName = "";
		string email = "";
		string address = "";
		string phoneNumber = "";
	};
	
	// Description: Default constructor creates a Customer with initial values.
	//				We choose to set customerID to -1 and let strings be empty.
	Customer();

	// Description: Constructor to instantiate a new Customer object with given data
	Customer(string fN, string lN, string pN, string add, string email, int custID);

	// Getters
	string getFirstName() const;
	string getLastName() const;
	string getPhoneNumber() const;
	string getAddress() const;
	string getEmail() const;
	int getCustomerID() const;

	// Setters
	void setFirstName(const string& firstName);
	void setLastName(const string& lastName);
	void setPhoneNumber(const string& phoneNumber);
	void setAddress(const string& address);
	void setEmail(const string& email);

	// Description: This method searches for a customer matching the given criteria
	//              and returns the customerID if found, or -1 if no match exists.
	static int findCustomerID(const SearchCriteria& criteria);

	// Description: This method updates the customer information in the database
	bool updateCustomerInDB() const;

	// Description: This method deletes a customer from the database
	bool deleteCustomerByID(int customerID)
};

#endif
