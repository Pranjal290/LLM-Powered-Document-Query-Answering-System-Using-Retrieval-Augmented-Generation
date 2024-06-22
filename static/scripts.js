// scripts.js

// Function to show loader
function showLoader() {
    document.getElementById('loader').classList.remove('d-none');
}

// Function to hide loader
function hideLoader() {
    document.getElementById('loader').classList.add('d-none');
}

// Show "Upload PDF" form and hide "Ask a Question" form
function showUploadPdfForm() {
    document.getElementById('uploadFormContainer').style.display = 'block';
    document.getElementById('questionFormContainer').style.display = 'none';
}

// Show "Ask a Question" form and hide "Upload PDF" form
function showAskQuestionForm() {
    document.getElementById('questionFormContainer').style.display = 'block';
    document.getElementById('uploadFormContainer').style.display = 'none';
}

// Handle form submission for asking a question
document.getElementById('questionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    try {
        showLoader(); // Show loader while processing

        const response = await fetch('/ask', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to fetch response');
        }

        const result = await response.text();
        document.getElementById('response').innerHTML = '<div class="alert alert-success" role="alert">' + result + '</div>';
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response').innerHTML = '<div class="alert alert-danger" role="alert">An error occurred. Please try again.</div>';
    } finally {
        hideLoader(); // Hide loader after processing
    }
});

// Handle form submission for processing PDF files
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    try {
        showLoader(); // Show loader while processing

        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to process PDF files');
        }

        const result = await response.text();
        document.getElementById('response').innerHTML = '<div class="alert alert-success" role="alert">' + result + '</div>';
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response').innerHTML = '<div class="alert alert-danger" role="alert">An error occurred. Please try again.</div>';
    } finally {
        hideLoader(); // Hide loader after processing
    }
});

// Show "Upload PDF" form by default on page load
showUploadPdfForm(); // Or use showAskQuestionForm() to show "Ask a Question" form by default
