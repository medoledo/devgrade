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
    autoHideAlerts();
    initFormValidation();
});

// HTMX error handling
document.body.addEventListener('htmx:responseError', function(evt) {
    const detail = evt.detail;
    let msg = 'حصلت مشكلة في الاتصال بالسيرفر. جرب تاني.';
    if (detail.xhr.status === 404) {
        msg = 'الصفحة أو البيانات اللي بتدور عليها مش موجودة.';
    } else if (detail.xhr.status === 403) {
        msg = 'مش مسموحلك تعمل العملية دي.';
    } else if (detail.xhr.status === 500) {
        msg = 'حصلت مشكلة فنية في السيرفر. جرب تاني بعد شوية.';
    }
    showAlert(msg, 'error');
});

document.body.addEventListener('htmx:sendError', function(evt) {
    showAlert('مش قادرين نوصل للسيرفر. اتأكد من اتصالك بالإنترنت.', 'error');
});

// Auto-hide alerts after 6 seconds
function autoHideAlerts() {
    const alerts = document.querySelectorAll('#messages-container > div[role="alert"]');
    alerts.forEach(alert => {
        if (!alert.dataset.hasTimer) {
            alert.dataset.hasTimer = 'true';
            setTimeout(() => {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-10px)';
                alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                setTimeout(() => alert.remove(), 400);
            }, 6000);
        }
    });
}

// Show a floating alert programmatically
function showAlert(message, type = 'info') {
    const container = document.getElementById('messages-container');
    if (!container) return;

    const colors = {
        success: 'bg-green-50 text-green-800 border-green-200',
        error: 'bg-red-50 text-red-800 border-red-200',
        warning: 'bg-yellow-50 text-yellow-800 border-yellow-200',
        info: 'bg-blue-50 text-blue-800 border-blue-200'
    };

    const icons = {
        success: '<svg class="w-5 h-5 mt-0.5 flex-shrink-0 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
        error: '<svg class="w-5 h-5 mt-0.5 flex-shrink-0 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
        warning: '<svg class="w-5 h-5 mt-0.5 flex-shrink-0 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>',
        info: '<svg class="w-5 h-5 mt-0.5 flex-shrink-0 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    };

    const div = document.createElement('div');
    div.className = `rounded-lg px-4 py-3 flex items-start gap-3 ${colors[type]} border`;
    div.setAttribute('role', 'alert');
    div.innerHTML = `
        ${icons[type]}
        <div class="flex-1 text-sm font-medium leading-relaxed">${message}</div>
        <button type="button" onclick="this.parentElement.remove()" class="hover:opacity-70 transition flex-shrink-0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
        </button>
    `;
    container.appendChild(div);
    autoHideAlerts();
}

// Highlight invalid form fields
function initFormValidation() {
    document.querySelectorAll('input[required], textarea[required], select[required]').forEach(field => {
        field.addEventListener('invalid', function(e) {
            e.preventDefault();
            this.classList.add('border-red-500', 'ring-1', 'ring-red-200');
        });
        field.addEventListener('input', function() {
            this.classList.remove('border-red-500', 'ring-1', 'ring-red-200');
        });
    });
}

// Run on page load
document.addEventListener('DOMContentLoaded', function() {
    autoHideAlerts();
    initFormValidation();
});
