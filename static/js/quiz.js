// Quiz State
let questions = [];
let currentQuestionIndex = 0;
let score = 0;
let answeredQuestions = new Set();
let currentLanguage = localStorage.getItem('language') || 'en';

// Get news UID from URL
const newsUid = window.location.pathname.split('/')[2];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeLanguageToggle();
    loadQuestions();
});

// Language Toggle
function initializeLanguageToggle() {
    const toggleBtn = document.getElementById('lang-toggle');
    updateToggleText(toggleBtn);
    
    toggleBtn.addEventListener('click', function() {
        currentLanguage = currentLanguage === 'en' ? 'hi' : 'en';
        localStorage.setItem('language', currentLanguage);
        window.location.href = `/mcq/${newsUid}/?lang=${currentLanguage}`;
    });
}

function updateToggleText(toggleBtn) {
    toggleBtn.textContent = currentLanguage === 'en' ? 'हिंदी' : 'English';
}

// Load Questions from API
async function loadQuestions() {
    const container = document.getElementById('quiz-container');
    
    try {
        const response = await fetch(`/questions/${newsUid}/?lang=${currentLanguage}`);
        const data = await response.json();
        questions = data;
        
        if (questions.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    ${currentLanguage === 'en' ? 
                        'No questions available for this news article.' : 
                        'इस समाचार लेख के लिए कोई प्रश्न उपलब्ध नहीं है।'}
                </div>`;
            return;
        }
        
        displayQuestion();
    } catch (error) {
        console.error('Error fetching questions:', error);
        container.innerHTML = `
            <div class="no-results">
                ${currentLanguage === 'en' ? 
                    'Failed to load questions. Please try again.' : 
                    'प्रश्न लोड करने में विफल। कृपया पुन: प्रयास करें।'}
            </div>`;
    }
}

// Display Current Question
function displayQuestion() {
    const question = questions[currentQuestionIndex];
    const container = document.getElementById('quiz-container');
    
    // Update progress
    document.getElementById('current-question').textContent = currentQuestionIndex + 1;
    document.getElementById('total-questions').textContent = questions.length;
    document.getElementById('score-display').textContent = score;
    
    // Render question
    container.innerHTML = `
        <div class="question-card">
            <div class="question-number">
                ${currentLanguage === 'en' ? 'Question' : 'प्रश्न'} ${currentQuestionIndex + 1}/${questions.length}
            </div>
            <div class="question-text">${question.question}</div>
            <div class="options-container" id="options-container">
                ${question.options.map((option, index) => `
                    <div class="option" onclick="selectOption(${index})" id="option-${index}">
                        <span class="option-letter">${String.fromCharCode(65 + index)}.</span>
                        <span class="option-text">${option.option}</span>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div class="quiz-controls">
            <div id="feedback-message" class="feedback-message"></div>
            <button id="next-btn" class="btn-next" onclick="nextQuestion()" disabled>
                ${currentLanguage === 'en' ? 'Next Question' : 'अगला प्रश्न'}
            </button>
        </div>
    `;
}

// Select Option
function selectOption(optionIndex) {
    // Prevent re-answering
    if (answeredQuestions.has(currentQuestionIndex)) {
        return;
    }
    
    const question = questions[currentQuestionIndex];
    const selectedOption = question.options[optionIndex];
    const isCorrect = selectedOption.is_correct;
    
    // Mark as answered
    answeredQuestions.add(currentQuestionIndex);
    
    // Update score
    if (isCorrect) {
        score++;
        document.getElementById('score-display').textContent = score;
    }
    
    // Visual feedback
    const optionsContainer = document.getElementById('options-container');
    const allOptions = optionsContainer.querySelectorAll('.option');
    
    allOptions.forEach((opt, index) => {
        opt.classList.add('disabled');
        
        if (question.options[index].is_correct) {
            opt.classList.add('correct');
        } else if (index === optionIndex && !isCorrect) {
            opt.classList.add('incorrect');
        }
    });
    
    // Show feedback
    const feedbackDiv = document.getElementById('feedback-message');
    if (isCorrect) {
        feedbackDiv.textContent = currentLanguage === 'en' ? '✓ Correct!' : '✓ सही!';
        feedbackDiv.className = 'feedback-message correct';
    } else {
        feedbackDiv.textContent = currentLanguage === 'en' ? '✗ Incorrect' : '✗ गलत';
        feedbackDiv.className = 'feedback-message incorrect';
    }
    
    // Enable next button
    document.getElementById('next-btn').disabled = false;
}

// Next Question
function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    } else {
        showFinalScore();
    }
}

// Show Final Score
function showFinalScore() {
    const container = document.getElementById('quiz-container');
    const percentage = Math.round((score / questions.length) * 100);
    
    let message = '';
    if (currentLanguage === 'en') {
        if (percentage >= 80) message = 'Excellent! 🎉';
        else if (percentage >= 60) message = 'Good job! 👍';
        else if (percentage >= 40) message = 'Keep practicing! 📚';
        else message = 'Need more practice! 💪';
    } else {
        if (percentage >= 80) message = 'उत्कृष्ट! 🎉';
        else if (percentage >= 60) message = 'अच्छा काम! 👍';
        else if (percentage >= 40) message = 'अभ्यास जारी रखें! 📚';
        else message = 'और अभ्यास की जरूरत है! 💪';
    }
    
    container.innerHTML = `
        <div class="final-score">
            <h2>${currentLanguage === 'en' ? 'Quiz Completed!' : 'क्विज़ पूर्ण!'}</h2>
            <div class="score-display">${score} / ${questions.length}</div>
            <div class="score-message">${message}</div>
            <div class="score-message">${currentLanguage === 'en' ? 'Percentage:' : 'प्रतिशत:'} ${percentage}%</div>
            <div style="margin-top: 30px; display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
                <button onclick="window.location.reload()" class="btn btn-success">
                    ${currentLanguage === 'en' ? 'Retry Quiz' : 'फिर से प्रयास करें'}
                </button>
                <a href="/?lang=${currentLanguage}" class="btn btn-primary">
                    ${currentLanguage === 'en' ? 'Back to Home' : 'होम पर वापस जाएं'}
                </a>
            </div>
        </div>
    `;
    
    // Hide controls
    document.querySelector('.quiz-controls').style.display = 'none';
}
