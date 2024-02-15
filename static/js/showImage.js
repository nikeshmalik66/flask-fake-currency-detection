document.addEventListener("DOMContentLoaded", function() {
    var fileInput = document.querySelector('input[type="file"]');
    var imagePreviewContainer = document.getElementById('imagePreviewContainer');
    var imagePreview = document.getElementById('imagePreview');

    fileInput.addEventListener('change', function(event) {
        var file = event.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imagePreviewContainer.style.display = 'block';
            }
            reader.readAsDataURL(file);
        }
    });
});
