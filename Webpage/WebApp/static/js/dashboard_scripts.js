document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard page loaded');
});

document.getElementById("status-button").addEventListener("click", function() {
    document.getElementById("service-status-popup").style.display = "block";
});

document.querySelector(".close-popup").addEventListener("click", function() {
    document.getElementById("service-status-popup").style.display = "none";
});

window.addEventListener("click", function(event) {
    if (event.target == document.getElementById("service-status-popup")) {
        document.getElementById("service-status-popup").style.display = "none";
    }
});
