document.addEventListener('DOMContentLoaded', function() {
    console.log('Document fully loaded');

    // Select the password input field
    const passwordInput = document.getElementById('password');
    const new_password = document.getElementById('new_password');
    const confirm_password = document.getElementById('confirm_password');
    let error_message_length = document.getElementById('message_p');
    let error_message_match = document.getElementById('not_match');

    // Check for the existence of the password input and its corresponding error message element
    if (passwordInput && error_message_length) {
        passwordInput.addEventListener('input', function() {
            // Check if the password is longer than 72 characters
            if (passwordInput.value.length > 72) {
                // Display a warning message
                error_message_length.textContent = 'Password must be less than 72 characters.';
            } else {
                // Clear the message if the password length is valid
                error_message_length.textContent = '';
            }
        });
    }

    // Check for the existence of the new and confirm password inputs and their corresponding error message element
    if (new_password && confirm_password && error_message_match) {
        confirm_password.addEventListener('input', function() {
            if (new_password.value.length > 72 || confirm_password.value.length > 72) { 
                // Display a warning message for length
                error_message_match.textContent = 'Password must be less than 72 characters.';
            } else if (new_password.value !== confirm_password.value) {
                // Display a warning message for mismatch
                error_message_match.textContent = 'Passwords do not match.';
            } else {
                // Clear the message if the passwords match and are of valid length
                error_message_match.textContent = '';
            }
        });
    }
});

function showPassword() {
    var x = document.getElementById("password");
    var y = document.getElementById("eye");
    if (x.type === "password") {
        x.type = "text";
        y.src = y.getAttribute('data-closed-eye');
    } else {
        x.type = "password";
        y.src = y.getAttribute('data-open-eye');
    }
}