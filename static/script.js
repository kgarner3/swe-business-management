// Shows only the selected dashboard section and hides all others
function showDashboardSection(sectionId) {
    const sections = document.querySelectorAll(".dashboard-section");

    sections.forEach(section => {
        section.style.display = "none";
    });

    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = "block";
    }
}

// Redirects user to employee login page
function goToEmployeeLogin() {
    window.location.href = "/employee";
}

// Redirects user to customer login page
function goToCustomerLogin() {
    window.location.href = "/customer";
}

// Logs out user (clears session storage) and returns to home page
function goHome() {
    sessionStorage.clear();
    window.location.href = "/";
}

// Runs when page loads
// - Sets welcome message from sessionStorage
// - Fetches fresh name from server and updates sessionStorage
document.addEventListener("DOMContentLoaded", function () {
    const welcomeMessage = document.getElementById("welcomeMessage");
    if (welcomeMessage) {
        const storedName = sessionStorage.getItem("employeeFirstName");
        if (storedName) {
            welcomeMessage.textContent = "Hi there, " + storedName + "!";
        }
        fetch("/get-employee-name")
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    welcomeMessage.textContent = "Hi there, " + data.firstName + "!";
                    sessionStorage.setItem("employeeFirstName", data.firstName);
                }
            })
            .catch(() => {});
    }

    // Get references to all relevant form elements on the page
    const employeeLoginForm = document.getElementById("employeeLoginForm");
    const changePasswordForm = document.getElementById("changePasswordForm");
    const customerLoginForm = document.getElementById("customerLoginForm");
    const customerChangePasswordForm = document.getElementById("customerChangePasswordForm");
    const createCustomerForm = document.getElementById("createCustomerForm");
    const deleteCustomerForm = document.getElementById("deleteCustomerForm");
    const findCustomerToUpdateForm = document.getElementById("findCustomerToUpdateForm");
    const updateCustomerForm = document.getElementById("updateCustomerForm");
 
    // Handles employee login form submission
    // - Validates input
    // - Sends login request to backend
    // - Stores name in sessionStorage
    // - Redirects to dashboard or password change
    // - Displays error messages if login fails
    if (employeeLoginForm) {
        employeeLoginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value.trim();
            const loginMessage = document.getElementById("loginMessage");

            loginMessage.textContent = "";

            if (!username || !password) {
                loginMessage.textContent = "Please enter both username and password.";
                return;
            }

            try {
                const response = await fetch("/employee-login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                });

                const data = await response.json();

                if (data.success) {
                    if (data.firstName) {
                        sessionStorage.setItem("employeeFirstName", data.firstName);
                    }
                    if (data.mustChangePassword) {
                        window.location.href = "/change-password";
                    } else {
                        window.location.href = "/dashboard";
                    }
                } else {
                    loginMessage.textContent = data.message || "Invalid username or password.";
                }
            } catch (error) {
                loginMessage.textContent = "An error occurred while logging in.";
                console.error(error);
            }
        });
    }

    // Handles employee password change
    // - Validates matching passwords
    // - Sends update request to backend
    // - Redirects to dashboard on success
    // - Displays errors if failed
    if (changePasswordForm) {
        changePasswordForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const newPassword = document.getElementById("newPassword").value.trim();
            const confirmPassword = document.getElementById("confirmPassword").value.trim();
            const changePasswordMessage = document.getElementById("changePasswordMessage");

            changePasswordMessage.textContent = "";

            if (!newPassword || !confirmPassword) {
                changePasswordMessage.textContent = "Please fill in both password fields.";
                return;
            }

            if (newPassword !== confirmPassword) {
                changePasswordMessage.textContent = "Passwords do not match.";
                return;
            }

            try {
                const response = await fetch("/change-password", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        newPassword: newPassword
                    })
                });

                const data = await response.json();

                if (data.success) {
                    window.location.href = "/dashboard";
                } else {
                    changePasswordMessage.textContent = data.message || "Unable to change password.";
                }
            } catch (error) {
                changePasswordMessage.textContent = "An error occurred while changing the password.";
                console.error(error);
            }
        });
    }

    // Handles customer login form submission
    // - Validates input
    // - Sends login request to backend
    // - Redirects to dashboard or password change
    // - Displays error messages if login fails
    if (customerLoginForm) {
        customerLoginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const username = document.getElementById("customerUsername").value.trim();
            const password = document.getElementById("customerPassword").value.trim();
            const customerLoginMessage = document.getElementById("customerLoginMessage");

            customerLoginMessage.textContent = "";

            if (!username || !password) {
                customerLoginMessage.textContent = "Please enter both username and password.";
                return;
            }

            try {
                const response = await fetch("/customer-login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                });

                const data = await response.json();

                if (data.success) {
                    if (data.mustChangePassword) {
                        window.location.href = "/customer-change-password";
                    } else {
                        window.location.href = "/customer-dashboard";
                    }
                } else {
                    customerLoginMessage.textContent = data.message || "Invalid username or password.";
                }
            } catch (error) {
                customerLoginMessage.textContent = "An error occurred while logging in.";
                console.error(error);
            }
        });
    }

    // Handles customer password change
    // - Validates matching passwords
    // - Sends update request to backend
    // - Redirects to dashboard on success
    // - Displays errors if failed
    if (customerChangePasswordForm) {
        customerChangePasswordForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const newPassword = document.getElementById("customerNewPassword").value.trim();
            const confirmPassword = document.getElementById("customerConfirmPassword").value.trim();
            const customerChangePasswordMessage = document.getElementById("customerChangePasswordMessage");

            customerChangePasswordMessage.textContent = "";

            if (!newPassword || !confirmPassword) {
                customerChangePasswordMessage.textContent = "Please fill in both password fields.";
                return;
            }

            if (newPassword !== confirmPassword) {
                customerChangePasswordMessage.textContent = "Passwords do not match.";
                return;
            }

            try {
                const response = await fetch("/customer-change-password", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        newPassword: newPassword
                    })
                });

                const data = await response.json();

                if (data.success) {
                    window.location.href = "/customer-dashboard";
                } else {
                    customerChangePasswordMessage.textContent = data.message || "Unable to change password.";
                }
            } catch (error) {
                customerChangePasswordMessage.textContent = "An error occurred while changing the password.";
                console.error(error);
            }
        });
    }

    // Handles creating a new customer
    // - Validates all fields
    // - Sends data to backend
    // - Displays success or error message
    // - Resets form on success
    if (createCustomerForm) {
        createCustomerForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const firstName = document.getElementById("customerFirstName").value.trim();
            const lastName = document.getElementById("customerLastName").value.trim();
            const phoneNumber = document.getElementById("customerPhoneNumber").value.trim();
            const address = document.getElementById("customerAddress").value.trim();
            const email = document.getElementById("customerEmail").value.trim();
            const createCustomerMessage = document.getElementById("createCustomerMessage");

            createCustomerMessage.textContent = "";

            if (!firstName || !lastName || !phoneNumber || !address || !email) {
                createCustomerMessage.textContent = "Please fill in all fields.";
                return;
            }

            try {
                const response = await fetch("/create-customer", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        firstName: firstName,
                        lastName: lastName,
                        phoneNumber: phoneNumber,
                        address: address,
                        email: email
                    })
                });

                const data = await response.json();

                if (data.success) {
                    createCustomerMessage.style.color = "green";
                    createCustomerMessage.textContent = data.message;
                    createCustomerForm.reset();
                } else {
                    createCustomerMessage.style.color = "#cc0000";
                    createCustomerMessage.textContent = data.message || "Unable to create customer.";
                }
            } catch (error) {
                createCustomerMessage.style.color = "#cc0000";
                createCustomerMessage.textContent = "An error occurred while creating the customer.";
                console.error(error);
            }
        });
    }

    // Handles customer deletion workflow
    // - Searches for customer first
    // - Displays confirmation modal with details
    // - Stores selected customer ID for deletion
    if (deleteCustomerForm) {
        const deleteCustomerModal = document.getElementById("deleteCustomerModal");
        const deleteCustomerDetails = document.getElementById("deleteCustomerDetails");
        const confirmDeleteCustomerButton = document.getElementById("confirmDeleteCustomerButton");
        const cancelDeleteCustomerButton = document.getElementById("cancelDeleteCustomerButton");

        let pendingDeleteCustomerID = null;

        deleteCustomerForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const searchText = document.getElementById("deleteCustomerSearch").value.trim();
            const deleteCustomerMessage = document.getElementById("deleteCustomerMessage");

            deleteCustomerMessage.textContent = "";

            if (!searchText) {
                deleteCustomerMessage.style.color = "#cc0000";
                deleteCustomerMessage.textContent = "Please enter customer information.";
                return;
            }

            try {
                const previewResponse = await fetch("/find-customer-for-delete", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        searchText: searchText
                    })
                });

                const previewData = await previewResponse.json();

                if (!previewData.success) {
                    deleteCustomerMessage.style.color = "#cc0000";
                    deleteCustomerMessage.textContent = previewData.message || "Customer not found.";
                    return;
                }

                const customer = previewData.customer;
                pendingDeleteCustomerID = customer.customerID;

                deleteCustomerDetails.innerHTML = `
                    <strong>ID:</strong> ${customer.customerID}<br>
                    <strong>Name:</strong> ${customer.firstName} ${customer.lastName}<br>
                    <strong>Email:</strong> ${customer.email}<br>
                    <strong>Phone:</strong> ${customer.phoneNumber}<br>
                    <strong>Address:</strong> ${customer.address}<br>
                    <strong>Username:</strong> ${customer.username}
                `;

                deleteCustomerModal.style.display = "flex";

            } catch (error) {
                deleteCustomerMessage.style.color = "#cc0000";
                deleteCustomerMessage.textContent = "An error occurred while searching for the customer.";
                console.error(error);
            }
        });

        // Confirms and executes customer deletion
        // - Sends delete request to backend
        // - Displays success/error message
        // - Resets form and closes modal
        if (confirmDeleteCustomerButton) {
            confirmDeleteCustomerButton.addEventListener("click", async function () {
                const deleteCustomerMessage = document.getElementById("deleteCustomerMessage");

                if (!pendingDeleteCustomerID) {
                    deleteCustomerModal.style.display = "none";
                    return;
                }

                try {
                    const deleteResponse = await fetch("/delete-customer", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            customerID: pendingDeleteCustomerID
                        })
                    });

                    const deleteData = await deleteResponse.json();

                    if (deleteData.success) {
                        deleteCustomerMessage.style.color = "green";
                        deleteCustomerMessage.textContent = deleteData.message;
                        deleteCustomerForm.reset();
                    } else {
                        deleteCustomerMessage.style.color = "#cc0000";
                        deleteCustomerMessage.textContent = deleteData.message || "Unable to delete customer.";
                    }
                } catch (error) {
                    deleteCustomerMessage.style.color = "#cc0000";
                    deleteCustomerMessage.textContent = "An error occurred while deleting the customer.";
                    console.error(error);
                }

                pendingDeleteCustomerID = null;
                deleteCustomerModal.style.display = "none";
            });
        }

        // Cancels customer deletion and closes modal
        if (cancelDeleteCustomerButton) {
            cancelDeleteCustomerButton.addEventListener("click", function () {
                pendingDeleteCustomerID = null;
                deleteCustomerModal.style.display = "none";
            });
        }
    }

    // Searches for a customer to update
    // - Sends search request to backend
    // - Fills form with existing data
    // - Shows update form if found
    if (findCustomerToUpdateForm) {
        findCustomerToUpdateForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const searchText = document.getElementById("updateCustomerSearch").value.trim();
            const findMessage = document.getElementById("findCustomerToUpdateMessage");
            const updateForm = document.getElementById("updateCustomerForm");

            findMessage.textContent = "";
            updateForm.style.display = "none";

            if (!searchText) {
                findMessage.style.color = "#cc0000";
                findMessage.textContent = "Please enter customer information.";
                return;
            }

            try {
                const response = await fetch("/find-customer-for-update", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        searchText: searchText
                    })
                });

                const data = await response.json();

                if (!data.success) {
                    findMessage.style.color = "#cc0000";
                    findMessage.textContent = data.message || "Customer not found.";
                    return;
                }

                const customer = data.customer;

                document.getElementById("updateCustomerID").value = customer.customerID;
                document.getElementById("updateCustomerFirstName").value = customer.firstName;
                document.getElementById("updateCustomerLastName").value = customer.lastName;
                document.getElementById("updateCustomerPhoneNumber").value = customer.phoneNumber || "";
                document.getElementById("updateCustomerAddress").value = customer.address || "";
                document.getElementById("updateCustomerEmail").value = customer.email;
                document.getElementById("updateCustomerUsername").value = customer.username || "";

                findMessage.style.color = "green";
                findMessage.textContent = "Customer found. Review and update the information below.";
                updateForm.style.display = "block";

            } catch (error) {
                findMessage.style.color = "#cc0000";
                findMessage.textContent = "An error occurred while finding the customer.";
                console.error(error);
            }
        });
    }

    // Handles updating customer information
    // - Validates all required fields
    // - Sends update request to backend
    // - Displays success or error message
    if (updateCustomerForm) {
        updateCustomerForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const customerID = document.getElementById("updateCustomerID").value.trim();
            const firstName = document.getElementById("updateCustomerFirstName").value.trim();
            const lastName = document.getElementById("updateCustomerLastName").value.trim();
            const phoneNumber = document.getElementById("updateCustomerPhoneNumber").value.trim();
            const address = document.getElementById("updateCustomerAddress").value.trim();
            const email = document.getElementById("updateCustomerEmail").value.trim();
            const username = document.getElementById("updateCustomerUsername").value.trim();
            const updateMessage = document.getElementById("updateCustomerMessage");

            updateMessage.textContent = "";

            if (!customerID || !firstName || !lastName || !phoneNumber || !address || !email) {
                updateMessage.style.color = "#cc0000";
                updateMessage.textContent = "Please fill in all customer fields.";
                return;
            }

            try {
                const response = await fetch("/update-customer", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        customerID: customerID,
                        firstName: firstName,
                        lastName: lastName,
                        phoneNumber: phoneNumber,
                        address: address,
                        email: email,
                        username: username
                    })
                });

                const data = await response.json();

                if (data.success) {
                    updateMessage.style.color = "green";
                    updateMessage.textContent = data.message;
                } else {
                    updateMessage.style.color = "#cc0000";
                    updateMessage.textContent = data.message || "Unable to update customer.";
                }
            } catch (error) {
                updateMessage.style.color = "#cc0000";
                updateMessage.textContent = "An error occurred while updating the customer.";
                console.error(error);
            }
        });
    }
    
    // Handles creating a new employee
    // - Validates all fields
    // - Sends data to backend
    // - Displays success or error message
    // - Resets form on success
    const createEmployeeForm = document.getElementById("createEmployeeForm");

    if (createEmployeeForm) {
        createEmployeeForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const firstName = document.getElementById("employeeFirstName").value.trim();
            const lastName  = document.getElementById("employeeLastName").value.trim();
            const email     = document.getElementById("employeeEmail").value.trim();
            const username  = document.getElementById("employeeUsername").value.trim();
            const createEmployeeMessage = document.getElementById("createEmployeeMessage");

            createEmployeeMessage.textContent = "";

            if (!firstName || !lastName || !email || !username) {
                createEmployeeMessage.style.color = "#cc0000";
                createEmployeeMessage.textContent = "Please fill in all fields.";
                return;
            }

            try {
                const response = await fetch("/create-employee", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ firstName, lastName, email, username })
                });

                const data = await response.json();

                if (data.success) {
                    createEmployeeMessage.style.color = "green";
                    createEmployeeMessage.textContent = data.message;
                    createEmployeeForm.reset();
                } else {
                    createEmployeeMessage.style.color = "#cc0000";
                    createEmployeeMessage.textContent = data.message || "Unable to create employee.";
                }
            } catch (error) {
                createEmployeeMessage.style.color = "#cc0000";
                createEmployeeMessage.textContent = "An error occurred while creating the employee.";
                console.error(error);
            }
        });
    }

    // Handles employee deletion workflow
    // - Searches for employee
    // - Displays confirmation modal
    // - Stores employee ID for deletion
    const deleteEmployeeForm = document.getElementById("deleteEmployeeForm");

    if (deleteEmployeeForm) {
        const deleteEmployeeModal   = document.getElementById("deleteEmployeeModal");
        const deleteEmployeeDetails = document.getElementById("deleteEmployeeDetails");
        const confirmDeleteEmployeeButton = document.getElementById("confirmDeleteEmployeeButton");
        const cancelDeleteEmployeeButton  = document.getElementById("cancelDeleteEmployeeButton");

        let pendingDeleteEmployeeID = null;

        deleteEmployeeForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const searchText = document.getElementById("deleteEmployeeSearch").value.trim();
            const deleteEmployeeMessage = document.getElementById("deleteEmployeeMessage");

            deleteEmployeeMessage.textContent = "";

            if (!searchText) {
                deleteEmployeeMessage.style.color = "#cc0000";
                deleteEmployeeMessage.textContent = "Please enter employee information.";
                return;
            }

            try {
                const response = await fetch("/find-employee-for-delete", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ searchText })
                });

                const data = await response.json();

                if (!data.success) {
                    deleteEmployeeMessage.style.color = "#cc0000";
                    deleteEmployeeMessage.textContent = data.message || "Employee not found.";
                    return;
                }

                const employee = data.employee;
                pendingDeleteEmployeeID = employee.employeeID;

                deleteEmployeeDetails.innerHTML = `
                    <strong>ID:</strong> ${employee.employeeID}<br>
                    <strong>Name:</strong> ${employee.firstName} ${employee.lastName}<br>
                    <strong>Email:</strong> ${employee.email}<br>
                    <strong>Username:</strong> ${employee.username}
                `;

                deleteEmployeeModal.style.display = "flex";

            } catch (error) {
                deleteEmployeeMessage.style.color = "#cc0000";
                deleteEmployeeMessage.textContent = "An error occurred while searching for the employee.";
                console.error(error);
            }
        });

        // Confirms and executes employee deletion
        if (confirmDeleteEmployeeButton) {
            confirmDeleteEmployeeButton.addEventListener("click", async function () {
                const deleteEmployeeMessage = document.getElementById("deleteEmployeeMessage");

                if (!pendingDeleteEmployeeID) {
                    deleteEmployeeModal.style.display = "none";
                    return;
                }

                try {
                    const response = await fetch("/delete-employee", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ employeeID: pendingDeleteEmployeeID })
                    });

                    const data = await response.json();

                    if (data.success) {
                        deleteEmployeeMessage.style.color = "green";
                        deleteEmployeeMessage.textContent = data.message;
                        deleteEmployeeForm.reset();
                    } else {
                        deleteEmployeeMessage.style.color = "#cc0000";
                        deleteEmployeeMessage.textContent = data.message || "Unable to delete employee.";
                    }
                } catch (error) {
                    deleteEmployeeMessage.style.color = "#cc0000";
                    deleteEmployeeMessage.textContent = "An error occurred while deleting the employee.";
                    console.error(error);
                }

                pendingDeleteEmployeeID = null;
                deleteEmployeeModal.style.display = "none";
            });
        }

        // Cancels employee deletion
        if (cancelDeleteEmployeeButton) {
            cancelDeleteEmployeeButton.addEventListener("click", function () {
                pendingDeleteEmployeeID = null;
                deleteEmployeeModal.style.display = "none";
            });
        }
    }

    // Searches for employee to update
    // - Sends search request
    // - Populates update form
    // - Displays form if found
    const findEmployeeToUpdateForm = document.getElementById("findEmployeeToUpdateForm");

    if (findEmployeeToUpdateForm) {
        findEmployeeToUpdateForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const searchText  = document.getElementById("updateEmployeeSearch").value.trim();
            const findMessage = document.getElementById("findEmployeeToUpdateMessage");
            const updateForm  = document.getElementById("updateEmployeeForm");

            findMessage.textContent = "";
            updateForm.style.display = "none";

            if (!searchText) {
                findMessage.style.color = "#cc0000";
                findMessage.textContent = "Please enter employee information.";
                return;
            }

            try {
                const response = await fetch("/find-employee-for-update", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ searchText })
                });

                const data = await response.json();

                if (!data.success) {
                    findMessage.style.color = "#cc0000";
                    findMessage.textContent = data.message || "Employee not found.";
                    return;
                }

                const employee = data.employee;

                document.getElementById("updateEmployeeID").value        = employee.employeeID;
                document.getElementById("updateEmployeeFirstName").value = employee.firstName;
                document.getElementById("updateEmployeeLastName").value  = employee.lastName;
                document.getElementById("updateEmployeeEmail").value     = employee.email;
                document.getElementById("updateEmployeeUsername").value  = employee.username;

                findMessage.style.color = "green";
                findMessage.textContent = "Employee found. Review and update the information below.";
                updateForm.style.display = "block";

            } catch (error) {
                findMessage.style.color = "#cc0000";
                findMessage.textContent = "An error occurred while finding the employee.";
                console.error(error);
            }
        });
    }

    // Prepares employee update
    // - Validates fields
    // - Stores data temporarily
    // - Shows confirmation modal
    const updateEmployeeForm = document.getElementById("updateEmployeeForm");

    if (updateEmployeeForm) {
        const updateEmployeeModal   = document.getElementById("updateEmployeeModal");
        const updateEmployeeDetails = document.getElementById("updateEmployeeDetails");
        const confirmUpdateEmployeeButton = document.getElementById("confirmUpdateEmployeeButton");
        const cancelUpdateEmployeeButton  = document.getElementById("cancelUpdateEmployeeButton");

        let pendingUpdateEmployeeData = null;

        updateEmployeeForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const employeeID = document.getElementById("updateEmployeeID").value.trim();
            const firstName  = document.getElementById("updateEmployeeFirstName").value.trim();
            const lastName   = document.getElementById("updateEmployeeLastName").value.trim();
            const email      = document.getElementById("updateEmployeeEmail").value.trim();
            const username   = document.getElementById("updateEmployeeUsername").value.trim();
            const updateMessage = document.getElementById("updateEmployeeMessage");

            updateMessage.textContent = "";

            if (!employeeID || !firstName || !lastName || !email || !username) {
                updateMessage.style.color = "#cc0000";
                updateMessage.textContent = "Please fill in all employee fields.";
                return;
            }

            pendingUpdateEmployeeData = { employeeID, firstName, lastName, email, username };

            updateEmployeeDetails.innerHTML = `
                <strong>Name:</strong> ${firstName} ${lastName}<br>
                <strong>Email:</strong> ${email}<br>
                <strong>Username:</strong> ${username}
            `;

            updateEmployeeModal.style.display = "flex";
        });

        // Confirms and submits employee update
        if (confirmUpdateEmployeeButton) {
            confirmUpdateEmployeeButton.addEventListener("click", async function () {
                const updateMessage = document.getElementById("updateEmployeeMessage");

                if (!pendingUpdateEmployeeData) {
                    updateEmployeeModal.style.display = "none";
                    return;
                }

                try {
                    const response = await fetch("/update-employee", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(pendingUpdateEmployeeData)
                    });

                    const data = await response.json();

                    if (data.success) {
                        updateMessage.style.color = "green";
                        updateMessage.textContent = data.message;
                    } else {
                        updateMessage.style.color = "#cc0000";
                        updateMessage.textContent = data.message || "Unable to update employee.";
                    }
                } catch (error) {
                    updateMessage.style.color = "#cc0000";
                    updateMessage.textContent = "An error occurred while updating the employee.";
                    console.error(error);
                }

                pendingUpdateEmployeeData = null;
                updateEmployeeModal.style.display = "none";
            });
        }

        // Cancels employee update
        if (cancelUpdateEmployeeButton) {
            cancelUpdateEmployeeButton.addEventListener("click", function () {
                pendingUpdateEmployeeData = null;
                updateEmployeeModal.style.display = "none";
            });
        }
    }
});

// Shows section and optionally runs a loader function
function loadAndShow(sectionId, loaderFn) {
    showDashboardSection(sectionId);
    if (loaderFn) loaderFn();
}

// Converts YYYY-MM-DD into readable date format
function formatDate(dateStr) {
    // Converts "2026-04-15" to "April 15, 2026"
    const [year, month, day] = dateStr.split('-');
    const months = ["January","February","March","April","May","June",
                    "July","August","September","October","November","December"];
    return `${months[parseInt(month, 10) - 1]} ${parseInt(day, 10)}, ${year}`;
}

// Loads all appointments for employees
// - Fetches data from backend
// - Builds and displays table
// - Handles empty/error states
async function loadAllAppointments() {
    const container = document.getElementById("appointmentsTableContainer");
    if (!container) return;

    container.innerHTML = "<p>Loading...</p>";

    try {
        const response = await fetch("/get-all-appointments");
        const data = await response.json();

        if (!data.success || data.appointments.length === 0) {
            container.innerHTML = "<p>No appointments found.</p>";
            return;
        }

        let html = `
            <table style="width:100%; border-collapse:collapse; margin-top:10px;">
                <thead>
                    <tr>
                        <th style="text-align:left; padding:8px; border-bottom:2px solid #ccc;">Date</th>
                        <th style="text-align:left; padding:8px; border-bottom:2px solid #ccc;">Customer</th>
                        <th style="text-align:left; padding:8px; border-bottom:2px solid #ccc;">Employee</th>
                        <th style="text-align:left; padding:8px; border-bottom:2px solid #ccc;">Service</th>
                        <th style="text-align:right; padding:8px; border-bottom:2px solid #ccc;">Cost</th>
                        <th style="text-align:right; padding:8px; border-bottom:2px solid #ccc;">Add. Expenses</th>
                        <th style="text-align:center; padding:8px; border-bottom:2px solid #ccc;">Status</th>
                        <th style="text-align:center; padding:8px; border-bottom:2px solid #ccc;">Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;

        for (const appt of data.appointments) {
            const statusColor = appt.status === "Completed" ? "green"
                              : appt.status === "Cancelled" ? "#cc0000"
                              : "#b8860b";

            html += `
                <tr>
                    <td style="padding:8px; border-bottom:1px solid #eee;">${formatDate(appt.date)}</td>
                    <td style="padding:8px; border-bottom:1px solid #eee;">${appt.customer_name}</td>
                    <td style="padding:8px; border-bottom:1px solid #eee;">${appt.employee_name}</td>
                    <td style="padding:8px; border-bottom:1px solid #eee;">${appt.service_name}</td>
                    <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">$${appt.cost.toFixed(2)}</td>
                    <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">$${appt.additional_expenses.toFixed(2)}</td>
                    <td style="padding:8px; border-bottom:1px solid #eee; text-align:center; color:${statusColor}; font-weight:bold;">${appt.status}</td>
                    <td style="padding:8px; border-bottom:1px solid #eee; text-align:center;">
                        ${appt.status === "Scheduled"
                            ? `<button type="button" onclick="openStatusModal(${appt.Appointment_ID}, '${appt.customer_name}', '${appt.date}', ${appt.additional_expenses})">Update</button>`
                            : "—"}
                    </td>
                </tr>
            `;
        }

        html += `</tbody></table>`;
        container.innerHTML = html;

    } catch (error) {
        container.innerHTML = "<p style='color:#cc0000;'>An error occurred while loading appointments.</p>";
        console.error(error);
    }
}

// Opens modal to update appointment status
// - Stores appointment ID
// - Displays customer/date info
// - Allows editing additional expenses
let pendingStatusAppointmentID = null;

function openStatusModal(appointmentID, customerName, date, currentExpenses) {
    pendingStatusAppointmentID = appointmentID;

    const details = document.getElementById("updateAppointmentStatusDetails");
    if (details) {
        details.innerHTML = `
            <strong>Customer:</strong> ${customerName}<br>
            <strong>Date:</strong> ${formatDate(date)}<br><br>
            <label for="modalAdditionalExpenses" style="font-weight:bold;">Additional Expenses ($)</label><br>
            <input type="number" id="modalAdditionalExpenses" min="0" step="0.01"
                value="${parseFloat(currentExpenses).toFixed(2)}"
                style="width:100%; padding:6px; margin-top:4px; box-sizing:border-box;">
        `;
    }

    const modal = document.getElementById("updateAppointmentStatusModal");
    if (modal) modal.style.display = "flex";
}

// Submits status update (Completed/Cancelled)
// - Sends update to backend
// - Reloads appointments on success
async function submitStatusUpdate(newStatus) {
    if (!pendingStatusAppointmentID) return;

    const expensesInput = document.getElementById("modalAdditionalExpenses");
    const additionalExpenses = expensesInput !== null ? parseFloat(expensesInput.value) : 0;

    try {
        const response = await fetch("/update-appointment-status", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                appointmentID: pendingStatusAppointmentID,
                status: newStatus,
                additionalExpenses: additionalExpenses
            })
        });

        const data = await response.json();
        const modal = document.getElementById("updateAppointmentStatusModal");
        if (modal) modal.style.display = "none";
        pendingStatusAppointmentID = null;

        if (data.success) {
            loadAllAppointments();
        } else {
            alert(data.message || "Unable to update appointment.");
        }
    } catch (error) {
        console.error(error);
        alert("An error occurred while updating the appointment.");
    }
}

// Closes status modal without saving
function closeStatusModal() {
    pendingStatusAppointmentID = null;
    const modal = document.getElementById("updateAppointmentStatusModal");
    if (modal) modal.style.display = "none";
}

// Saves additional expenses without changing status
// - Updates backend
// - Refreshes table
// - Shows confirmation inside modal
async function saveExpensesOnly() {
    if (!pendingStatusAppointmentID) return;

    const expensesInput = document.getElementById("modalAdditionalExpenses");
    const additionalExpenses = expensesInput !== null ? parseFloat(expensesInput.value) : 0;

    try {
        const response = await fetch("/save-appointment-expenses", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                appointmentID: pendingStatusAppointmentID,
                additionalExpenses: additionalExpenses
            })
        });

        const data = await response.json();

        if (data.success) {
            // Update the displayed value in the table without closing the modal
            loadAllAppointments();
            // Show brief confirmation in the modal
            const details = document.getElementById("updateAppointmentStatusDetails");
            const savedMsg = document.createElement("p");
            savedMsg.textContent = "✓ Expenses saved.";
            savedMsg.style.color = "green";
            savedMsg.style.marginTop = "8px";
            savedMsg.style.fontWeight = "bold";
            // Remove any previous confirmation message
            const prev = details.querySelector(".save-confirm");
            if (prev) prev.remove();
            savedMsg.classList.add("save-confirm");
            details.appendChild(savedMsg);
        } else {
            alert(data.message || "Unable to save expenses.");
        }
    } catch (error) {
        console.error(error);
        alert("An error occurred while saving expenses.");
    }
}

// Loads dropdowns for scheduling
// - Fetches customers, employees, services
// - Populates select menus
// - Stores service costs for later use
async function loadScheduleDropdowns() {
    try {
        const [custRes, empRes, svcRes] = await Promise.all([
            fetch("/get-customers-list"),
            fetch("/get-employees-list"),
            fetch("/get-all-services")
        ]);

        const custData = await custRes.json();
        const empData  = await empRes.json();
        const svcData  = await svcRes.json();

        const custSelect = document.getElementById("apptCustomer");
        const empSelect  = document.getElementById("apptEmployee");
        const svcSelect  = document.getElementById("apptService");

        if (!custSelect || !empSelect || !svcSelect) return;

        // Reset
        custSelect.innerHTML = '<option value="">-- Select Customer --</option>';
        empSelect.innerHTML  = '<option value="">-- Select Employee --</option>';
        svcSelect.innerHTML  = '<option value="">-- Select Service --</option>';

        if (custData.success) {
            for (const c of custData.customers) {
                custSelect.innerHTML += `<option value="${c.Customer_ID}">${c.name}</option>`;
            }
        }

        if (empData.success) {
            for (const e of empData.employees) {
                empSelect.innerHTML += `<option value="${e.Employee_ID}">${e.name}</option>`;
            }
        }

        // Store service costs for auto-fill
        window._serviceCosts = {};
        if (svcData.success) {
            for (const s of svcData.services) {
                svcSelect.innerHTML += `<option value="${s.serviceID}">${s.name} — $${s.cost.toFixed(2)}</option>`;
                window._serviceCosts[s.serviceID] = s.cost;
            }
        }

    } catch (error) {
        console.error("Error loading dropdowns:", error);
    }
}

// Handles scheduling a new appointment
// - Validates inputs
// - Sends data to backend
// - Displays success/error message
// - Resets form on success
document.addEventListener("DOMContentLoaded", function () {
    const scheduleAppointmentForm = document.getElementById("scheduleAppointmentForm");
    if (scheduleAppointmentForm) {
        scheduleAppointmentForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const customerID          = document.getElementById("apptCustomer").value;
            const employeeID          = document.getElementById("apptEmployee").value;
            const serviceID           = document.getElementById("apptService").value;
            const date                = document.getElementById("apptDate").value;
            const additionalExpenses  = document.getElementById("apptAdditionalExpenses").value || 0;
            const msg                 = document.getElementById("scheduleAppointmentMessage");

            msg.textContent = "";

            if (!customerID || !employeeID || !serviceID || !date) {
                msg.style.color = "#cc0000";
                msg.textContent = "Please fill in all required fields.";
                return;
            }

            try {
                const response = await fetch("/schedule-appointment", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        customerID,
                        employeeID,
                        serviceID,
                        date,
                        description: "",
                        additionalExpenses: parseFloat(additionalExpenses)
                    })
                });

                const data = await response.json();

                if (data.success) {
                    msg.style.color = "green";
                    msg.textContent = data.message;
                    scheduleAppointmentForm.reset();
                } else {
                    msg.style.color = "#cc0000";
                    msg.textContent = data.message || "Unable to schedule appointment.";
                }
            } catch (error) {
                msg.style.color = "#cc0000";
                msg.textContent = "An error occurred while scheduling the appointment.";
                console.error(error);
            }
        });
    }
});

// Triggers reminder emails (appointments in 7 days)
// - Calls backend
// - Displays success/failure results
async function triggerReminders() {
    const resultsDiv = document.getElementById("reminderResults");
    resultsDiv.innerHTML = "<p style='color:#888;'>Sending reminder emails...</p>";

    try {
        const response = await fetch("/trigger-reminders", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });
        const data = await response.json();

        if (!data.success) {
            resultsDiv.innerHTML = `<p style='color:#cc0000;'>${data.message}</p>`;
            return;
        }

        if (data.sent.length === 0 && data.failed.length === 0) {
            resultsDiv.innerHTML = "<p style='color:#888;'>No appointments found 7 days from today.</p>";
            return;
        }

        let html = `<p style='color:green; font-weight:bold;'>${data.message}</p>`;
        if (data.sent.length > 0) {
            html += "<ul style='margin-top:8px;'>";
            for (const r of data.sent) {
                html += `<li>✓ <strong>${r.customer}</strong> (${r.email}) — ${r.service} on ${formatDate(r.date)}</li>`;
            }
            html += "</ul>";
        }
        if (data.failed.length > 0) {
            html += "<ul style='margin-top:8px; color:#cc0000;'>";
            for (const r of data.failed) {
                html += `<li>✗ <strong>${r.customer}</strong> (${r.email}) — ${r.error || "Unknown error"}</li>`;
            }
            html += "</ul>";
        }
        resultsDiv.innerHTML = html;

    } catch (error) {
        resultsDiv.innerHTML = "<p style='color:#cc0000;'>An error occurred while sending reminders.</p>";
        console.error(error);
    }
}

// Triggers win-back emails (inactive customers)
// - Calls backend
// - Displays success/failure results
async function triggerWinBack() {
    const resultsDiv = document.getElementById("winbackResults");
    resultsDiv.innerHTML = "<p style='color:#888;'>Sending win-back emails...</p>";

    try {
        const response = await fetch("/trigger-winback", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });
        const data = await response.json();

        if (!data.success) {
            resultsDiv.innerHTML = `<p style='color:#cc0000;'>${data.message}</p>`;
            return;
        }

        if (data.sent.length === 0 && data.failed.length === 0) {
            resultsDiv.innerHTML = "<p style='color:#888;'>No qualifying inactive customers found.</p>";
            return;
        }

        let html = `<p style='color:green; font-weight:bold;'>${data.message}</p>`;
        if (data.sent.length > 0) {
            html += "<ul style='margin-top:8px;'>";
            for (const r of data.sent) {
                html += `<li>✓ <strong>${r.customer}</strong> (${r.email}) — last appointment ${formatDate(r.last_appointment)}</li>`;
            }
            html += "</ul>";
        }
        if (data.failed.length > 0) {
            html += "<ul style='margin-top:8px; color:#cc0000;'>";
            for (const r of data.failed) {
                html += `<li>✗ <strong>${r.customer}</strong> (${r.email}) — ${r.error || "Unknown error"}</li>`;
            }
            html += "</ul>";
        }
        resultsDiv.innerHTML = html;

    } catch (error) {
        resultsDiv.innerHTML = "<p style='color:#cc0000;'>An error occurred while sending win-back emails.</p>";
        console.error(error);
    }
}

// Loads reports (revenue + expenses)
// - Calls backend 
// - Retrieves JSON report data
// - Displays results in the report container
async function loadReports() {
    const container = document.getElementById("reportContainer");

    if (!container) return;

    container.innerHTML = "<p>Loading...</p>";

    try {
        const response = await fetch("/report-Section");
        const data = await response.json();

        if (!data.success) {
            container.innerHTML = "<p style='color:red;'>Error loading report.</p>";
            return;
        }

        const rev = data.revenueReport;
        const exp = data.expenseReport;

        container.innerHTML = `
            <div style="margin-top:20px;">

                <h2 style="font-size:20px; margin-bottom:10px;">Revenue Report</h2>
                <p><strong>Start Date:</strong> ${rev.startDate}</p>
                <p><strong>End Date:</strong> ${rev.endDate}</p>
                <p><strong>Total Revenue:</strong> 
                    <span style="color:green;">$${rev.totalRevenue.toFixed(2)}</span>
                </p>

                <hr style="margin:15px 0; border:none; border-top:1px solid #ccc;">

                <h2 style="font-size:20px; margin-bottom:10px;">Expense Report</h2>
                <p><strong>Start Date:</strong> ${exp.startDate}</p>
                <p><strong>End Date:</strong> ${exp.endDate}</p>
                <p><strong>Total Expenses:</strong> 
                    <span style="color:#cc0000;">$${exp.totalExpenses.toFixed(2)}</span>
                </p>

            </div>
        `;
    } catch (err) {
        console.error(err);
        container.innerHTML = "<p style='color:red;'>Error loading report.</p>";
    }
}
