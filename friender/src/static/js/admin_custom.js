document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.action-checkbox input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            const closestTr = this.closest('tr');
            if (this.checked) {
                closestTr.classList.add('highlighted');
            } else {
                closestTr.classList.remove('highlighted');
            }
        });
    });
});