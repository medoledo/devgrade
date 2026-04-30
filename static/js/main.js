// Main JS file for DevGrade

// Mobile menu toggle is handled inline in base.html

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// HTMX global handlers
document.body.addEventListener('htmx:afterSwap', function(evt) {
    // Re-initialize any JS needed after HTMX swaps
});

// Auto-hide alerts after 5 seconds
function autoHideAlerts() {
    const alerts = document.querySelectorAll('[class*="bg-green-100"], [class*="bg-red-100"], [class*="bg-blue-100"]');
    alerts.forEach(alert => {
        if (!alert.closest('form')) {
            setTimeout(() => {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.5s ease';
                setTimeout(() => alert.remove(), 500);
            }, 5000);
        }
    });
}

// Run on page load and after HTMX swaps
document.addEventListener('DOMContentLoaded', autoHideAlerts);
document.body.addEventListener('htmx:afterSwap', autoHideAlerts);
