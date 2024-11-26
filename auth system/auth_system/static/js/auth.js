const USER_TYPES = {
    ADMIN: "admin",
    EMPLOYEE: "employee",
};

async function handleFormSubmission(event, form) {
    event.preventDefault();

    const submitButton = form.querySelector("button[type='submit']");
    if (submitButton) submitButton.disabled = true; // Disable the button during submission

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value; // Optional chaining for safety
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    try {
        const actionUrl = form.dataset.action;
        const response = await fetch(actionUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}), // Include CSRF token if available
            },
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            const result = await response.json();
            console.log("API Response:", result);

            // Determine redirect URL safely
            const redirectUrl = result?.data?.user_type === USER_TYPES.ADMIN
                ? "/admin/dashboard/"
                : result?.data?.user_type === USER_TYPES.EMPLOYEE
                ? "/attendance"
                : "/auth/employee/login";
            console.log("Redirect URL:", redirectUrl);

            window.location.assign(redirectUrl); // Redirect to the appropriate page
        } else {
            const error = await response.json();
            alert(error.error || "Submission failed");
            const redirectUrl = "/auth/employee/login";
            window.location.assign(redirectUrl); 
        }
    } catch (error) {
        alert(error.message || "An unexpected error occurred");
        console.error("Submission Error:", error);
    } finally {
        if (submitButton) submitButton.disabled = false; // Re-enable the button after submission
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const forms = {
        adminLogin: document.querySelector("#adminLoginForm"),
        adminSignup: document.querySelector("#adminSignupForm"),
        employeeLogin: document.querySelector("#employeeLoginForm"),
        employeeSignup: document.querySelector("#employeeSignupForm"),
    };

    Object.entries(forms).forEach(([type, form]) => {
        if (form) {
            form.addEventListener("submit", (event) => handleFormSubmission(event, form));
        }
    });
});
