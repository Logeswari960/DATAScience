document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const resultsSection = document.getElementById('resultsSection');
    const loading = document.getElementById('loading');

    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Upload button click
    uploadBtn.addEventListener('click', uploadFile);

    let selectedFile = null;

    function handleFile(file) {
        if (file && file.type.startsWith('image/')) {
            selectedFile = file;
            uploadArea.innerHTML = `<p>Selected: ${file.name}</p>`;
            uploadBtn.style.display = 'block';
        } else {
            alert('Please select a valid image file.');
        }
    }

    function uploadFile() {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);

        loading.style.display = 'block';
        resultsSection.style.display = 'none';

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            
            if (data.success) {
                displayResults(data);
            } else {
                alert(data.error || 'Upload failed');
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            alert('Upload failed: ' + error.message);
        });
    }

    function displayResults(data) {
        const previewImage = document.getElementById('previewImage');
        const qualityScore = document.getElementById('qualityScore');
        const temperature = document.getElementById('temperature');
        const humidity = document.getElementById('humidity');
        const freshness = document.getElementById('freshness');

        previewImage.src = `/static/uploads/${data.filename}`;
        qualityScore.textContent = data.analysis.quality_score;
        temperature.textContent = data.analysis.temperature;
        humidity.textContent = data.analysis.humidity;
        freshness.textContent = data.analysis.freshness;
        freshness.className = `freshness-badge ${data.analysis.freshness.toLowerCase()}`;

        resultsSection.style.display = 'block';
    }
});