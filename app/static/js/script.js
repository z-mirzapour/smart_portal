/*admin.template.course*/
document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggleFormBtn');
    const cancelBtn = document.getElementById('cancelFormBtn');
    const formSection = document.getElementById('addCourseSection');
    const icon = toggleBtn.querySelector('i.fas');
    
    toggleBtn.addEventListener('click', function() {
        const isVisible = formSection.style.display === 'block';
        formSection.style.display = isVisible ? 'none' : 'block';
        
        if (isVisible) {
            toggleBtn.innerHTML = '<i class="fas fa-plus"></i> Add New Course';
        } else {
            toggleBtn.innerHTML = '<i class="fas fa-book"></i> New Course';
        }
    });
    
    cancelBtn.addEventListener('click', function() {
        formSection.style.display = 'none';
        toggleBtn.innerHTML = '<i class="fas fa-plus"></i> Add New Course';
    });
});