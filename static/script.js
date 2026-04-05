function goToEmployeeLogin() {
    window.location.href = "/employee";
}

function goHome() {
    window.location.href = "/";
}

document.addEventListener("DOMContentLoaded", function () {
    const employeeLoginForm = document.getElementById("employeeLoginForm");

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
                    // Redirect immediately (no message flash)
                    window.location.href = "/dashboard";
                } else {
                    loginMessage.textContent = "Invalid username or password.";
                }
            } catch (error) {
                loginMessage.textContent = "An error occurred while logging in.";
                console.error(error);
            }
        });
    }
});