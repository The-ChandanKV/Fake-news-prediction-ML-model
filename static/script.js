// ===== PARTICLE ANIMATION =====
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 1}px;
            height: ${Math.random() * 4 + 1}px;
            background: rgba(102, 126, 234, ${Math.random() * 0.5 + 0.2});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: float ${Math.random() * 10 + 10}s linear infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        particlesContainer.appendChild(particle);
    }

    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0%, 100% { transform: translate(0, 0); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translate(${Math.random() * 200 - 100}px, ${Math.random() * 200 - 100}px); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}

// ===== COUNTER ANIMATION =====
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current).toLocaleString();
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toLocaleString();
            }
        };
        updateCounter();
    });
}

// ===== CHARACTER COUNTER =====
function setupCharCounter() {
    const textarea = document.getElementById('news_text');
    const charCount = document.getElementById('charCount');
    if (textarea && charCount) {
        textarea.addEventListener('input', () => {
            charCount.textContent = textarea.value.length.toLocaleString();
        });
    }
}

// ===== FORM SUBMISSION WITH SCROLL POSITION =====
function setupFormSubmission() {
    const form = document.getElementById('predictionForm');
    const loadingContainer = document.getElementById('loadingContainer');
    const submitBtn = document.getElementById('submitBtn');

    if (form) {
        form.addEventListener('submit', (e) => {
            // Save scroll position
            const scrollPos = window.pageYOffset || document.documentElement.scrollTop;
            sessionStorage.setItem('scrollPosition', scrollPos);

            // Show loading
            if (loadingContainer) loadingContainer.style.display = 'block';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.6';
            }
        });
    }
}

// ===== RESTORE SCROLL POSITION =====
function restoreScrollPosition() {
    const scrollPos = sessionStorage.getItem('scrollPosition');
    if (scrollPos) {
        setTimeout(() => {
            window.scrollTo({ top: parseInt(scrollPos), behavior: 'instant' });
            sessionStorage.removeItem('scrollPosition');
        }, 100);
    }
}

// ===== RESET FORM =====
function resetForm() {
    const textarea = document.getElementById('news_text');
    const resultContainer = document.getElementById('resultContainer');
    const charCount = document.getElementById('charCount');

    if (textarea) {
        textarea.value = '';
        textarea.focus();
    }
    if (charCount) charCount.textContent = '0';
    if (resultContainer) {
        resultContainer.style.animation = 'slideOutDown 0.5s ease-out';
        setTimeout(() => resultContainer.remove(), 500);
    }
}

// ===== SCROLL ANIMATIONS =====
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, observerOptions);

    // Add scroll-reveal class
    document.querySelectorAll('.fade-in, .slide-up').forEach(el => {
        el.classList.add('scroll-reveal');
    });

    // Observe elements
    document.querySelectorAll('.scroll-reveal').forEach(el => {
        observer.observe(el);

        // Activate elements already in viewport
        const rect = el.getBoundingClientRect();
        const isInViewport = (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );

        if (isInViewport) {
            setTimeout(() => el.classList.add('active'), 100);
        }
    });
}

// ===== SMOOTH SCROLL =====
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// ===== PARALLAX EFFECT =====
function setupParallax() {
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;
                document.querySelectorAll('.hero-content').forEach(el => {
                    el.style.transform = `translateY(${scrolled * 0.5}px)`;
                });
                ticking = false;
            });
            ticking = true;
        }
    });
}

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', () => {
    // Restore scroll position first
    restoreScrollPosition();

    // Create particles
    createParticles();

    // Animate counters when visible
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const statsContainer = document.querySelector('.stats-container');
    if (statsContainer) statsObserver.observe(statsContainer);

    // Setup features
    setupCharCounter();
    setupFormSubmission();
    setupScrollAnimations();
    setupSmoothScroll();
    setupParallax();

    // Hero animation
    setTimeout(() => {
        document.querySelector('.hero-content')?.classList.add('fade-in');
    }, 100);
});

// ===== EXPORT FUNCTIONS =====
window.resetForm = resetForm;

// ===== SLIDEOUT ANIMATION =====
const slideOutStyle = document.createElement('style');
slideOutStyle.textContent = `
    @keyframes slideOutDown {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(30px); }
    }
`;
document.head.appendChild(slideOutStyle);
