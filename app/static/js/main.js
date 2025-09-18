// Main JavaScript functionality for Task Manager

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add priority classes to task cards
    document.querySelectorAll('.task-card').forEach(function(card) {
        var priorityBadge = card.querySelector('.badge');
        if (priorityBadge) {
            var priority = priorityBadge.textContent.toLowerCase().trim();
            card.classList.add('priority-' + priority);
        }
    });
});

// Toggle task completion status
function toggleTask(taskId) {
    var checkbox = document.querySelector(`[data-task-id="${taskId}"] .task-checkbox`);
    var card = document.querySelector(`[data-task-id="${taskId}"]`);
    
    // Show loading state
    checkbox.disabled = true;
    
    fetch(`/main/toggle_task/${taskId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update UI based on completion status
            var title = card.querySelector('.card-title');
            var description = card.querySelector('.card-text');
            
            if (data.completed) {
                title.classList.add('text-decoration-line-through', 'text-muted');
                if (description) {
                    description.classList.add('text-muted');
                }
                card.classList.add('completed');
                card.classList.add('task-completed');
            } else {
                title.classList.remove('text-decoration-line-through', 'text-muted');
                if (description) {
                    description.classList.remove('text-muted');
                }
                card.classList.remove('completed');
                card.classList.remove('task-completed');
            }
            
            // Show success message
            showNotification('Task updated successfully!', 'success');
        } else {
            // Revert checkbox state on error
            checkbox.checked = !checkbox.checked;
            showNotification('Error updating task. Please try again.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Revert checkbox state on error
        checkbox.checked = !checkbox.checked;
        showNotification('Error updating task. Please try again.', 'error');
    })
    .finally(() => {
        checkbox.disabled = false;
    });
}

// Show notification
function showNotification(message, type) {
    var alertClass = type === 'error' ? 'alert-danger' : 'alert-success';
    var alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    var container = document.querySelector('main .container');
    container.insertAdjacentHTML('afterbegin', alertHtml);
    
    // Auto-hide after 3 seconds
    setTimeout(function() {
        var alert = container.querySelector('.alert');
        if (alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 3000);
}

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Form validation helpers
function validateForm(formId) {
    var form = document.getElementById(formId);
    var isValid = true;
    
    // Check required fields
    var requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Search functionality (if needed)
function filterTasks(searchTerm) {
    var tasks = document.querySelectorAll('.task-card');
    
    tasks.forEach(function(task) {
        var title = task.querySelector('.card-title').textContent.toLowerCase();
        var description = task.querySelector('.card-text');
        var descText = description ? description.textContent.toLowerCase() : '';
        
        if (title.includes(searchTerm.toLowerCase()) || descText.includes(searchTerm.toLowerCase())) {
            task.style.display = 'block';
        } else {
            task.style.display = 'none';
        }
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + N for new task
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        var addTaskLink = document.querySelector('a[href*="add_task"]');
        if (addTaskLink) {
            window.location.href = addTaskLink.href;
        }
    }
    
    // Escape to close modals or go back
    if (e.key === 'Escape') {
        var modals = document.querySelectorAll('.modal.show');
        if (modals.length === 0) {
            // No modals open, go back if on form page
            var cancelBtn = document.querySelector('a.btn-secondary');
            if (cancelBtn && cancelBtn.textContent.trim() === 'Cancel') {
                window.location.href = cancelBtn.href;
            }
        }
    }
});