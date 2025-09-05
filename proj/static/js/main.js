// main.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('videoForm');
    const submitBtn = document.getElementById('submitBtn');
    const loadingSection = document.getElementById('loadingSection');
    const mainContent = document.querySelector('.main-content');
    const progressFill = document.getElementById('progressFill');
    const loadingText = document.getElementById('loadingText');

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const videoUrl = document.getElementById('videoUrl').value;
            
            if (!videoUrl) {
                showNotification('Please enter a valid YouTube URL', 'error');
                return;
            }

            // Show loading state
            showLoading();
            
            // Submit the form
            form.submit();
        });
    }

    function showLoading() {
        if (mainContent) {
            mainContent.style.display = 'none';
        }
        if (loadingSection) {
            loadingSection.style.display = 'flex';
        }
        
        // Simulate progress updates
        simulateProgress();
    }

    function simulateProgress() {
        const steps = [
            { progress: 20, text: 'Downloading video...' },
            { progress: 40, text: 'Extracting audio...' },
            { progress: 60, text: 'Transcribing content...' },
            { progress: 80, text: 'Generating summary...' },
            { progress: 90, text: 'Creating quiz questions...' },
            { progress: 100, text: 'Finalizing results...' }
        ];

        let currentStep = 0;
        
        function updateProgress() {
            if (currentStep < steps.length && progressFill && loadingText) {
                const step = steps[currentStep];
                progressFill.style.width = step.progress + '%';
                loadingText.textContent = step.text;
                currentStep++;
                setTimeout(updateProgress, 2000);
            }
        }
        
        updateProgress();
    }

    // Quiz functionality
    window.revealAnswer = function(questionIndex, correctAnswer) {
        const answerDiv = document.getElementById('answer' + questionIndex);
        const revealBtn = event.target;
        
        if (answerDiv.style.display === 'none') {
            answerDiv.style.display = 'block';
            revealBtn.textContent = 'Hide Answer';
            revealBtn.style.background = '#dc3545';
        } else {
            answerDiv.style.display = 'none';
            revealBtn.textContent = 'Show Answer';
            revealBtn.style.background = '#667eea';
        }
    };

    window.checkAllAnswers = function() {
        const questions = document.querySelectorAll('.question-item');
        let correctCount = 0;
        let totalQuestions = questions.length;

        questions.forEach((question, index) => {
            const selectedOption = question.querySelector('input[type="radio"]:checked');
            const correctAnswer = question.querySelector('.answer-reveal');
            
            if (correctAnswer) {
                const correctText = correctAnswer.textContent;
                const correctIndex = parseInt(correctText.match(/Correct Answer: (.+)/)[1]);
                
                if (selectedOption) {
                    const selectedIndex = parseInt(selectedOption.value);
                    if (selectedIndex === correctIndex) {
                        correctCount++;
                        selectedOption.parentElement.style.background = '#d4edda';
                        selectedOption.parentElement.style.border = '2px solid #28a745';
                    } else {
                        selectedOption.parentElement.style.background = '#f8d7da';
                        selectedOption.parentElement.style.border = '2px solid #dc3545';
                    }
                }
                
                // Show correct answer
                const correctOption = question.querySelector(`input[value="${correctIndex}"]`);
                if (correctOption) {
                    correctOption.parentElement.style.background = '#d4edda';
                    correctOption.parentElement.style.border = '2px solid #28a745';
                }
            }
        });

        // Show results
        const score = Math.round((correctCount / totalQuestions) * 100);
        showNotification(`Quiz Complete! Score: ${correctCount}/${totalQuestions} (${score}%)`, 'success');
    };

    // Copy to clipboard functionality
    window.copyToClipboard = function(elementId) {
        const element = document.getElementById(elementId);
        if (!element) return;

        let textToCopy = '';
        
        if (elementId === 'quiz') {
            // Extract quiz text
            const questions = element.querySelectorAll('.question-item');
            questions.forEach((question, index) => {
                const questionText = question.querySelector('.question-text').textContent;
                const options = question.querySelectorAll('.option label');
                textToCopy += `Question ${index + 1}: ${questionText}\n`;
                options.forEach((option, optIndex) => {
                    textToCopy += `${String.fromCharCode(65 + optIndex)}. ${option.textContent.trim()}\n`;
                });
                textToCopy += '\n';
            });
        } else {
            textToCopy = element.textContent || element.innerText;
        }

        navigator.clipboard.writeText(textToCopy).then(function() {
            showNotification('Copied to clipboard!', 'success');
        }).catch(function(err) {
            console.error('Could not copy text: ', err);
            showNotification('Failed to copy to clipboard', 'error');
        });
    };

    // Notification system
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.copy-notification');
        existingNotifications.forEach(notification => notification.remove());

        const notification = document.createElement('div');
        notification.className = 'copy-notification';
        notification.textContent = message;
        
        if (type === 'error') {
            notification.style.background = '#dc3545';
        } else if (type === 'success') {
            notification.style.background = '#28a745';
        }

        document.body.appendChild(notification);

        // Show notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Hide notification after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // URL validation
    const urlInput = document.getElementById('videoUrl');
    if (urlInput) {
        urlInput.addEventListener('input', function() {
            const url = this.value;
            const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]+/;
            
            if (url && !youtubeRegex.test(url)) {
                this.style.borderColor = '#dc3545';
                showNotification('Please enter a valid YouTube URL', 'error');
            } else {
                this.style.borderColor = '#e1e5e9';
            }
        });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (form && !submitBtn.disabled) {
                form.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to go back
        if (e.key === 'Escape') {
            const backBtn = document.querySelector('.back-btn');
            if (backBtn) {
                backBtn.click();
            }
        }
    });

    // Auto-focus on URL input
    if (urlInput) {
        urlInput.focus();
    }
});
