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
    salt = "";
	customerID = -1;
}
	
Customer::Customer(string fN, string lN, string pN, string add, string email, string uName, string pHash, string s, int custID) {
	this->firstName = fN;
	this->lastName = lN;
	this->phoneNumber = pN;
	this->address = add;
	this->email = email;
	this->userName = uName;
	this->passwordHash = pHash;
	this->salt = s;
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

void Customer::setUsername(const string& uName) {
    userName = uName;
}

void Customer::setPassword(const string& plainPassword) {
    passwordHash = HashUtilities::hashPassword(plainPassword, salt);
}

// Helper methods
int Customer::findCustomerID(const SearchCriteria& criteria) {
    // TODO: Replace with database query

    // The database will:
    // 1. Search the customers table
    // 2. Match fields based on non-empty criteria
    // 3. Return the matching customerID if found
    // 4. Return -1 if no match exists

    return -1;
}

int Customer::authenticateCustomer(const string& userName, const string& password) {
    // TODO: Replace with database query.

    // This method will:
    // 1. Search the customers table for the given username
    // 2. Retrieve the stored password hash and salt for that customer
    // 3. Hash the entered plainPassword using the stored salt
    // 4. Compare the new hash to the stored password hash
    // 5. Return the customerID if they match
    // 6. Return -1 if no matching username exists or the password is incorrect

    return -1;
}

bool Customer::createCustomerInDB() {
    // Validate required fields are provided
    if (firstName.empty() || lastName.empty() || email.empty() || userName.empty() || passwordHash.empty()) {
        return false;
    }
    
    // TODO: Replace with database insertion query.

    // This method will:
    // 1. Check whether the username or email already exists in the database
    // 2. Insert the new customer record into the customers table
    // 3. Store the customer's passwordHash and salt in the database
    // 4. Assign the generated customerID from the database to this object
    // 5. Return true if the insertion is successful
    // 6. Return false if creation fails or required fields are missing

    return true;
}

bool Customer::updateCustomerInDB() const {
    // TODO: Replace with database update query.
    
    // This method will:
    // 1. Validate that customerID is not -1
    // 2. Use the current object's customerID to locate the record in the database
    // 3. Update the customer's fields (first name, last name, email, etc.)
    // 4. Return true if the update is successful
    // 5. Return false if the customerID is invalid or the update fails

    return true;
}

bool Customer::deleteCustomerByID(int customerID) {
    // TODO: Replace with database deletion query.
    
    // This method will:
    // 1. Validate that customerID is not -1
    // 2. Use the provided customerID to locate the record in the database
    // 3. Delete the customer from the database
    // 4. Return true if the deletion is successful
    // 5. Return false if the customerID is invalid or the deletion fails

    return true;
}
