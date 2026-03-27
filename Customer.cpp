///////////////////////////////////////////////////////////////////////////////
// Author: Katie Garner
// Description: This is the implementation file for the Customer class for the
//				COSC412 Project.
///////////////////////////////////////////////////////////////////////////////
#include "Customer.h"

// Constructors
Customer::Customer() {
	firstName = "";
	lastName = "";
	phoneNumber = "";
	address = "";
	email = "";
	customerID = -1;
}
	
Customer::Customer(string fN, string lN, string pN, string add, string email, int custID) {
	this->firstName = fN;
	this->lastName = lN;
	this->phoneNumber = pN;
	this->address = add;
	this->email = email;
	this->customerID = custID;
}

//Getters
string Customer::getFirstName() const
{
    return firstName;
}

string Customer::getLastName() const
{
    return lastName;
}

string Customer::getPhoneNumber() const
{
    return phoneNumber;
}

string Customer::getAddress() const
{
    return address;
}

string Customer::getEmail() const
{
    return email;
}

int Customer::getCustomerID() const
{
    return customerID;
}

// Setters
void Customer::setFirstName(const string& fN) {
    firstName = fN;
}

void Customer::setLastName(const string& lN) {
    lastName = lN;
}

void Customer::setPhoneNumber(const string& pN) {
    phoneNumber = pN;
}

void Customer::setAddress(const string& addr) {
    address = addr;
}

void Customer::setEmail(const string& em) {
    email = em;
}


// Helper methods
int Customer::findCustomerID(const SearchCriteria& criteria) {
    // This section will be replaced with database functionality
    vector<Customer> storedCustomers = {
    {"Katie", "Garner", "4105551234", "123 Main St", "katie@gmail.com", 1},
    {"John", "Smith", "4432225678", "456 Oak Ave", "johnsmith@yahoo.com", 2},
    {"John", "Doe", "4105551234", "789 Pine Rd", "johndoe@email.com", 3}
    };

    // For loop to check for customer information and return customer ID using a 
    // boolean variable to flag when something doesn't match.
    for (const Customer& customer : storedCustomers) {
        bool match = true;

        if (criteria.customerID != -1 && customer.getCustomerID() != criteria.customerID)
            match = false;

        if (!criteria.firstName.empty() && customer.getFirstName() != criteria.firstName)
            match = false;

        if (!criteria.lastName.empty() && customer.getLastName() != criteria.lastName)
            match = false;

        if (!criteria.email.empty() && customer.getEmail() != criteria.email)
            match = false;

        if (!criteria.address.empty() && customer.getAddress() != criteria.address)
            match = false;

        if (!criteria.phoneNumber.empty() && customer.getPhoneNumber() != criteria.phoneNumber)
            match = false;

        if (match)
            return customer.getCustomerID();
    }

    return -1;
}

bool Customer::updateCustomerInDB() const {
    // Flag if customer ID is invalid
    if (customerID == -1) return false;

    // Database stuff

    return true;
}

bool Customer::deleteCustomerByID(int customerID) {
    // Flag if customer ID is invalid
    if (customerID == -1) return false;

    // Database stuff

    return true;
}
