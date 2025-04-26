const loginForm = document.getElementById("login-form");
const twoFaForm = document.getElementById("2fa-form");
const targetForm = document.getElementById("target-form");
const messageForm = document.getElementById("message-form");
const startButton = document.getElementById("start-button");
const logsDiv = document.getElementById("logs");

loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(loginForm);
    fetch("/login", {
        method: "POST",
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        if (data["2FA"]) {
            loginForm.style.display = "none";
            twoFaForm.style.display = "block";
        } else if (data.success) {
            loginForm.style.display = "none";
            targetForm.style.display = "block";
        } else {
            alert("Invalid credentials");
        }
    });
});

twoFaForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(twoFaForm);
    fetch("/2fa", {
        method: "POST",
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            twoFaForm.style.display = "none";
            targetForm.style.display = "block";
        } else {
            alert("Invalid 2FA code");
        }
    });
});

targetForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(targetForm);
    fetch("/target", {
        method: "POST",
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            targetForm.style.display = "none";
            messageForm.style.display = "block";
        } else {
            alert("Error");
        }
    });
});

messageForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(messageForm);
    fetch("/message", {
        method: "POST",
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            messageForm.style.display = "none";
            startButton.style.display = "block";
        } else {
            alert("Error");
        }
    });
});

startButton.addEventListener("click", () => {
    fetch("/start", {
        method: "POST"
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            startButton.style.display = "none";
            logsDiv.innerHTML = "Bot started!";
        } else {
            alert("Error");
        }
    });
});
