// static/js/inactivity.js

let timeout;

function resetTimer() {
    console.log("Resetting timer.");  // Log statement to confirm function is called
    clearTimeout(timeout);
    timeout = setTimeout(logout, 1800000);  // 1800000 ms = 30 minutes
}

function logout() {
    console.log("Logging out due to inactivity.");  // Log statement to confirm function is called
    window.location.href = "/logout/";
}

window.onload = resetTimer;
document.onmousemove = resetTimer;
document.onkeydown = resetTimer;
document.onmousedown = resetTimer;  // To detect mouse clicks