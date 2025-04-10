// Main JavaScript for StudyTrack application

// Enable tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize date pickers
    if (document.querySelector('.datepicker')) {
        flatpickr('.datepicker', {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
        });
    }

    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDarkMode);
            
            // Update icon
            const icon = darkModeToggle.querySelector('i');
            if (isDarkMode) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        });

        // Check for saved dark mode preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
            const icon = darkModeToggle.querySelector('i');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }

    // Task status update
    const statusButtons = document.querySelectorAll('.status-update-btn');
    statusButtons.forEach(button => {
        button.addEventListener('click', function() {
            const taskId = this.getAttribute('data-task-id');
            const newStatus = this.getAttribute('data-status');
            const form = document.getElementById('status-form-' + taskId);
            const statusInput = form.querySelector('input[name="status"]');
            statusInput.value = newStatus;
            form.submit();
        });
    });

    // Charts for statistics page
    if (document.getElementById('courseCompletionChart')) {
        renderCourseCompletionChart();
    }
    
    if (document.getElementById('taskStatusChart')) {
        renderTaskStatusChart();
    }
    
    if (document.getElementById('taskPriorityChart')) {
        renderTaskPriorityChart();
    }
});

// Function to render course completion chart
function renderCourseCompletionChart() {
    const ctx = document.getElementById('courseCompletionChart').getContext('2d');
    const courseNames = JSON.parse(document.getElementById('courseCompletionChart').getAttribute('data-labels'));
    const completionRates = JSON.parse(document.getElementById('courseCompletionChart').getAttribute('data-values'));
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: courseNames,
            datasets: [{
                label: 'نسبة إكمال المهام (%)',
                data: completionRates,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Function to render task status chart
function renderTaskStatusChart() {
    const ctx = document.getElementById('taskStatusChart').getContext('2d');
    const statusCounts = JSON.parse(document.getElementById('taskStatusChart').getAttribute('data-values'));
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['قيد الانتظار', 'قيد التنفيذ', 'مكتملة'],
            datasets: [{
                data: [statusCounts.pending, statusCounts.in_progress, statusCounts.completed],
                backgroundColor: [
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(23, 162, 184, 0.8)',
                    'rgba(40, 167, 69, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 193, 7, 1)',
                    'rgba(23, 162, 184, 1)',
                    'rgba(40, 167, 69, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
}

// Function to render task priority chart
function renderTaskPriorityChart() {
    const ctx = document.getElementById('taskPriorityChart').getContext('2d');
    const priorityCounts = JSON.parse(document.getElementById('taskPriorityChart').getAttribute('data-values'));
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['منخفضة', 'متوسطة', 'عالية'],
            datasets: [{
                data: [priorityCounts.low, priorityCounts.medium, priorityCounts.high],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(220, 53, 69, 0.8)'
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(255, 193, 7, 1)',
                    'rgba(220, 53, 69, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
}
