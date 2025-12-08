// ===== FAKE NEWS DETECTOR - ENHANCED SCRIPT =====

// ===== PARTICLE ANIMATION =====
function createParticles() {
    const container = document.getElementById('particles');
    if (!container) return;

    const particleCount = 60;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        const size = Math.random() * 4 + 1;
        const opacity = Math.random() * 0.4 + 0.1;
        const duration = Math.random() * 20 + 15;
        const delay = Math.random() * 10;
        const xStart = Math.random() * 100;
        const yStart = Math.random() * 100;

        particle.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: radial-gradient(circle, rgba(120, 100, 255, ${opacity}) 0%, transparent 70%);
            border-radius: 50%;
            left: ${xStart}%;
            top: ${yStart}%;
            animation: floatParticle ${duration}s ease-in-out infinite;
            animation-delay: ${delay}s;
            pointer-events: none;
        `;
        container.appendChild(particle);
    }

    // Add particle animation styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatParticle {
            0%, 100% { 
                transform: translate(0, 0) scale(1);
                opacity: 0.3;
            }
            25% { 
                transform: translate(${Math.random() * 50 - 25}px, ${Math.random() * 50 - 25}px) scale(1.2);
                opacity: 0.6;
            }
            50% { 
                transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) scale(1);
                opacity: 0.4;
            }
            75% { 
                transform: translate(${Math.random() * 50 - 25}px, ${Math.random() * 50 - 25}px) scale(0.8);
                opacity: 0.5;
            }
        }
    `;
    document.head.appendChild(style);
}

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    const elements = document.querySelectorAll('[data-scroll]');

    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.getAttribute('data-scroll-delay') || 0;
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, parseInt(delay));
            }
        });
    }, observerOptions);

    elements.forEach(el => {
        // Skip hero section elements - they have their own animation
        if (!el.closest('.hero-section')) {
            observer.observe(el);
        } else {
            el.classList.add('visible');
        }
    });
}

// ===== NAVBAR SCROLL EFFECT =====
function initNavbarScroll() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    }, { passive: true });
}

// ===== SMOOTH SCROLL FOR NAV LINKS =====
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                // Update active nav link
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });
}

// ===== COUNTER ANIMATION =====
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');

    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000;
        const startTime = Date.now();

        const updateCounter = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(target * easeOut);

            counter.textContent = current.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toLocaleString();
            }
        };

        updateCounter();
    });
}

// ===== OBSERVE STATS FOR COUNTER ANIMATION =====
function initCounterObserver() {
    const statsContainer = document.querySelector('.stats-container');
    if (!statsContainer) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    observer.observe(statsContainer);
}

// ===== CHARACTER COUNTER =====
function initCharCounter() {
    const textarea = document.getElementById('news_text');
    const charCount = document.getElementById('charCount');

    if (textarea && charCount) {
        textarea.addEventListener('input', () => {
            charCount.textContent = textarea.value.length.toLocaleString();
        });
    }
}

// ===== AJAX FORM SUBMISSION =====
function initFormSubmission() {
    const form = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultContainer = document.getElementById('resultContainer');

    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const textarea = document.getElementById('news_text');
        const text = textarea.value.trim();

        if (text.length < 10) {
            showNotification('Please enter at least 10 characters', 'error');
            return;
        }

        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            if (response.ok) {
                displayResult(data);
            } else {
                showNotification(data.error || 'An error occurred', 'error');
            }
        } catch (error) {
            console.error('Prediction error:', error);
            showNotification('Failed to connect to the server', 'error');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });
}

// ===== DISPLAY RESULT =====
function displayResult(data) {
    const resultContainer = document.getElementById('resultContainer');
    const resultCard = document.getElementById('resultCard');
    const resultIcon = document.getElementById('resultIcon');
    const resultPrediction = document.getElementById('resultPrediction');
    const confidenceValue = document.getElementById('confidenceValue');
    const confidenceFill = document.getElementById('confidenceFill');
    const detailText = document.getElementById('detailText');

    // Determine if fake or real
    const isFake = data.prediction.toLowerCase().includes('fake');

    // Update card class
    resultCard.className = 'result-card ' + (isFake ? 'fake-result' : 'real-result');

    // Update icon
    if (isFake) {
        resultIcon.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M15 9L9 15M9 9L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
        `;
    } else {
        resultIcon.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
    }

    // Update prediction text
    resultPrediction.textContent = data.prediction;

    // Update confidence with animation
    const confidence = data.confidence || (isFake ? 85 : 92);
    confidenceValue.textContent = '0%';
    confidenceFill.style.width = '0%';

    // Animate confidence
    setTimeout(() => {
        confidenceValue.textContent = confidence.toFixed(1) + '%';
        confidenceFill.style.width = confidence + '%';
    }, 100);

    // Update detail text
    detailText.textContent = isFake
        ? 'This article shows patterns commonly found in misleading content'
        : 'This article appears to be from a credible source';

    // Show result container
    resultContainer.style.display = 'block';

    // Scroll to result
    setTimeout(() => {
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 200);
}

// ===== RESET FORM =====
function resetForm() {
    const textarea = document.getElementById('news_text');
    const charCount = document.getElementById('charCount');
    const resultContainer = document.getElementById('resultContainer');

    if (textarea) {
        textarea.value = '';
        textarea.focus();
    }

    if (charCount) {
        charCount.textContent = '0';
    }

    if (resultContainer) {
        resultContainer.style.animation = 'slideDown 0.4s ease-out forwards';
        setTimeout(() => {
            resultContainer.style.display = 'none';
            resultContainer.style.animation = '';
        }, 400);
    }
}

// ===== NOTIFICATION SYSTEM =====
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${type === 'error' ? '⚠️' : 'ℹ️'}</span>
        <span class="notification-message">${message}</span>
    `;

    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => notification.classList.add('show'), 10);

    // Remove after delay
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Add notification styles
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%) translateY(100px);
        padding: 1rem 1.5rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: white;
        font-size: 0.95rem;
        z-index: 10000;
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .notification.show {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
    
    .notification-error {
        border-color: rgba(239, 68, 68, 0.3);
        background: rgba(239, 68, 68, 0.15);
    }
    
    .notification-icon {
        font-size: 1.1rem;
    }
    
    @keyframes slideDown {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(notificationStyles);

// ===== ACTIVE NAV LINK ON SCROLL =====
function initNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;

            if (window.pageYOffset >= sectionTop &&
                window.pageYOffset < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }, { passive: true });
}

// ===== PARALLAX EFFECT =====
function initParallax() {
    const video = document.querySelector('.video-background video');
    if (!video) return;

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * 0.3;
        video.style.transform = `translate(-50%, calc(-50% + ${rate}px))`;
    }, { passive: true });
}

// ===== VIDEO LOADING =====
function initVideoBackground() {
    const video = document.getElementById('bgVideo');
    if (!video) return;

    video.playbackRate = 0.8; // Slow down video slightly

    video.addEventListener('loadeddata', () => {
        video.style.opacity = '1';
    });

    // Fallback if video doesn't load
    video.addEventListener('error', () => {
        console.warn('Video failed to load, using fallback background');
        const videoContainer = document.querySelector('.video-background');
        if (videoContainer) {
            videoContainer.style.background = 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%)';
        }
    });
}

// ===== TEXTAREA AUTO-RESIZE =====
function initTextareaResize() {
    const textarea = document.getElementById('news_text');
    if (!textarea) return;

    textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 400) + 'px';
    });
}

// ===== INITIALIZE EVERYTHING =====
document.addEventListener('DOMContentLoaded', () => {
    // Video background
    initVideoBackground();

    // Create particle effects
    createParticles();

    // Navbar effects
    initNavbarScroll();
    initNavHighlight();

    // Scroll effects
    initScrollAnimations();
    initSmoothScroll();
    initParallax();

    // Counter animation
    initCounterObserver();

    // Form functionality
    initCharCounter();
    initFormSubmission();
    initTextareaResize();

    console.log('🚀 Fake News Detector initialized successfully!');
});

// Export functions for global access
window.resetForm = resetForm;
window.showNotification = showNotification;
