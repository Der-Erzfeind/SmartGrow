document.addEventListener('DOMContentLoaded', function () {
    const toggleButtons = document.querySelectorAll('.toggle-info');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function () {
            const plantInfo = button.nextElementSibling;

            if (plantInfo.classList.contains('collapsed')) {
                plantInfo.classList.remove('collapsed');
                plantInfo.classList.add('expanded');
                button.textContent = 'Plant Information';
            } else {
                plantInfo.classList.remove('expanded');
                plantInfo.classList.add('collapsed');
                button.textContent = 'Plant Information';
            }
        });
    });
});
