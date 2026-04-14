// ===== FAKEDETECT AI — ENHANCED SCRIPT v3.0 =====

// Global state
let lastAnalysisResult = null;

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

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }, { passive: true });
}

// ===== SMOOTH SCROLL FOR NAV LINKS =====
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
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


// ===== NEURAL NETWORK ANIMATION =====
function drawNeuralNetwork(canvas, active = false) {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width;
    const H = canvas.height;
    
    const layers = [3, 5, 7, 5, 7, 5, 3]; // 7 layers
    const layerLabels = ['Input', 'Lang', 'ML', 'Sent.', 'Manip.', 'Source', 'Output'];
    const layerGap = W / (layers.length + 1);
    
    let animFrame = 0;
    
    function draw() {
        ctx.clearRect(0, 0, W, H);
        
        // Draw connections
        for (let l = 0; l < layers.length - 1; l++) {
            const x1 = (l + 1) * layerGap;
            const x2 = (l + 2) * layerGap;
            
            for (let i = 0; i < layers[l]; i++) {
                const y1 = (H / (layers[l] + 1)) * (i + 1);
                for (let j = 0; j < layers[l + 1]; j++) {
                    const y2 = (H / (layers[l + 1] + 1)) * (j + 1);
                    
                    ctx.beginPath();
                    ctx.moveTo(x1, y1);
                    ctx.lineTo(x2, y2);
                    
                    if (active) {
                        const pulse = Math.sin(animFrame * 0.05 + l * 0.5 + i * 0.3) * 0.5 + 0.5;
                        ctx.strokeStyle = `rgba(129, 140, 248, ${0.1 + pulse * 0.3})`;
                        ctx.lineWidth = 0.5 + pulse;
                    } else {
                        ctx.strokeStyle = 'rgba(129, 140, 248, 0.15)';
                        ctx.lineWidth = 0.5;
                    }
                    ctx.stroke();
                }
            }
        }
        
        // Draw nodes
        for (let l = 0; l < layers.length; l++) {
            const x = (l + 1) * layerGap;
            for (let i = 0; i < layers[l]; i++) {
                const y = (H / (layers[l] + 1)) * (i + 1);
                
                if (active) {
                    const pulse = Math.sin(animFrame * 0.08 + l * 0.7) * 0.5 + 0.5;
                    const glow = ctx.createRadialGradient(x, y, 0, x, y, 12 + pulse * 5);
                    glow.addColorStop(0, `rgba(129, 140, 248, ${0.6 + pulse * 0.4})`);
                    glow.addColorStop(1, 'rgba(129, 140, 248, 0)');
                    ctx.fillStyle = glow;
                    ctx.beginPath();
                    ctx.arc(x, y, 12 + pulse * 5, 0, Math.PI * 2);
                    ctx.fill();
                }
                
                ctx.beginPath();
                ctx.arc(x, y, 5, 0, Math.PI * 2);
                ctx.fillStyle = active 
                    ? `rgba(129, 140, 248, ${0.7 + Math.sin(animFrame * 0.08 + l) * 0.3})`
                    : 'rgba(129, 140, 248, 0.5)';
                ctx.fill();
            }
            
            // Layer label
            ctx.fillStyle = 'rgba(148, 163, 184, 0.8)';
            ctx.font = '10px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(layerLabels[l] || '', x, H - 5);
        }
        
        animFrame++;
        if (active) {
            requestAnimationFrame(draw);
        }
    }
    
    draw();
    return draw;
}


// ===== TRUST SCORE RING =====
function drawTrustScoreRing(score, color) {
    const canvas = document.getElementById('trustScoreCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const size = canvas.width;
    const center = size / 2;
    const radius = center - 10;
    const lineWidth = 8;
    
    ctx.clearRect(0, 0, size, size);
    
    // Background ring
    ctx.beginPath();
    ctx.arc(center, center, radius, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = lineWidth;
    ctx.stroke();
    
    // Score ring (animated)
    const endAngle = (score / 100) * Math.PI * 2 - Math.PI / 2;
    const startAngle = -Math.PI / 2;
    
    const gradient = ctx.createLinearGradient(0, 0, size, size);
    gradient.addColorStop(0, color);
    gradient.addColorStop(1, shiftHue(color, 30));
    
    ctx.beginPath();
    ctx.arc(center, center, radius, startAngle, endAngle);
    ctx.strokeStyle = gradient;
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';
    ctx.stroke();
    
    // Glow effect
    ctx.beginPath();
    ctx.arc(center, center, radius, startAngle, endAngle);
    ctx.strokeStyle = color;
    ctx.lineWidth = lineWidth + 4;
    ctx.globalAlpha = 0.15;
    ctx.stroke();
    ctx.globalAlpha = 1;
    
    // Update text
    const textEl = document.getElementById('trustScoreText');
    if (textEl) {
        textEl.querySelector('span:first-child').textContent = Math.round(score);
        textEl.querySelector('span:first-child').style.color = color;
    }
}

function shiftHue(hex, amount) {
    // Simple hue shift for gradient effect
    return hex; // Simplified - returns same color
}


// ===== DISPLAY RESULT (Enhanced with all new analysis) =====
function displayResult(data) {
    const resultContainer = document.getElementById('resultContainer');
    const resultCard = document.getElementById('resultCard');
    const resultIcon = document.getElementById('resultIcon');
    const resultPrediction = document.getElementById('resultPrediction');
    const confidenceValue = document.getElementById('confidenceValue');
    const confidenceFill = document.getElementById('confidenceFill');
    const detailText = document.getElementById('detailText');

    // Hide neural network animation
    const nnContainer = document.getElementById('neuralNetContainer');
    if (nnContainer) nnContainer.style.display = 'none';
    
    // Store for report/feedback
    lastAnalysisResult = data;

    const isFake = data.prediction.toLowerCase().includes('fake');
    const isUncertain = data.label === 2;
    
    window.currentPrediction = {
        text: document.getElementById('news_text').value.trim(),
        label: data.label
    };
    
    // Reset feedback
    const feedbackButtons = document.getElementById('feedbackButtons');
    const feedbackThanks = document.getElementById('feedbackThanks');
    if(feedbackButtons) feedbackButtons.style.display = 'flex';
    if(feedbackThanks) feedbackThanks.style.display = 'none';

    // 3-tier color: red = fake, green = real, amber = uncertain
    if (isUncertain) {
        resultCard.className = 'result-card uncertain-result';
    } else {
        resultCard.className = 'result-card ' + (isFake ? 'fake-result' : 'real-result');
    }

    // Icon
    if (isUncertain) {
        resultIcon.innerHTML = `<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/><path d="M12 8V12M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`;
    } else if (isFake) {
        resultIcon.innerHTML = `<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/><path d="M15 9L9 15M9 9L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`;
    } else {
        resultIcon.innerHTML = `<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/><path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
    }

    resultPrediction.textContent = data.prediction;

    // Confidence animation
    const confidence = data.confidence || 50;
    confidenceValue.textContent = '0%';
    confidenceFill.style.width = '0%';
    setTimeout(() => {
        confidenceValue.textContent = confidence.toFixed(1) + '%';
        confidenceFill.style.width = confidence + '%';
    }, 100);

    if (isUncertain) {
        detailText.textContent = 'The model could not determine this article reliably. It may be outside the training domain.';
    } else {
        detailText.textContent = isFake
            ? 'This article shows patterns commonly found in misleading content'
            : 'This article appears to be from a credible source';
    }

    // Warning message for uncertain predictions
    let warningEl = document.getElementById('uncertainWarning');
    if (!warningEl) {
        warningEl = document.createElement('div');
        warningEl.id = 'uncertainWarning';
        warningEl.style.cssText = 'display:none; background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.3); border-radius: 10px; padding: 0.75rem 1rem; margin-top: 0.75rem; color: #fbbf24; font-size: 0.9rem; text-align: center;';
        detailText.parentElement.after(warningEl);
    }
    if (data.warning) {
        warningEl.textContent = '⚠️ ' + data.warning;
        warningEl.style.display = 'block';
    } else {
        warningEl.style.display = 'none';
    }

    // Trust Score Ring
    const trustScore = data.overall_trust_score || (isFake ? 25 : isUncertain ? 50 : 82);
    const trustColor = trustScore >= 70 ? '#22c55e' : trustScore >= 40 ? '#f59e0b' : '#ef4444';
    setTimeout(() => drawTrustScoreRing(trustScore, trustColor), 200);

    // Language Notice
    const langDetail = document.getElementById('langDetail');
    const langText = document.getElementById('langText');
    if (data.language && data.language.translated) {
        langText.innerHTML = `<strong>Auto-translated</strong> from ${data.language.name} for analysis`;
        langDetail.style.display = 'flex';
    } else {
        langDetail.style.display = 'none';
    }

    // ====== NEW: Sentiment Analysis ======
    const sentimentDetail = document.getElementById('sentimentDetail');
    const sentimentContent = document.getElementById('sentimentContent');
    if (data.content_analysis && data.content_analysis.sentiment) {
        const s = data.content_analysis.sentiment;
        const polarityColor = s.polarity > 0.1 ? '#22c55e' : s.polarity < -0.1 ? '#ef4444' : '#94a3b8';
        const subjectivityColor = s.subjectivity > 0.6 ? '#f59e0b' : '#3b82f6';
        
        sentimentContent.innerHTML = `
            <div style="background: rgba(255,255,255,0.03); padding: 0.6rem 0.8rem; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 4px;">Tone</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: ${polarityColor};">${s.label}</div>
                <div style="font-size: 0.8rem; color: #64748b;">${s.polarity > 0 ? '+' : ''}${s.polarity}</div>
            </div>
            <div style="background: rgba(255,255,255,0.03); padding: 0.6rem 0.8rem; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 4px;">Subjectivity</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: ${subjectivityColor};">${s.subjectivity_pct}%</div>
                <div style="font-size: 0.8rem; color: #64748b;">${s.subjectivity > 0.6 ? 'Opinion-heavy' : s.subjectivity > 0.3 ? 'Balanced' : 'Factual'}</div>
            </div>
        `;
        sentimentDetail.style.display = 'flex';
    } else {
        sentimentDetail.style.display = 'none';
    }

    // ====== NEW: Manipulation Detection ======
    const manipulationDetail = document.getElementById('manipulationDetail');
    const manipulationBadge = document.getElementById('manipulationBadge');
    const manipulationContent = document.getElementById('manipulationContent');
    if (data.content_analysis && data.content_analysis.manipulation) {
        const m = data.content_analysis.manipulation;
        
        manipulationBadge.textContent = m.verdict;
        manipulationBadge.style.background = m.verdict_color + '22';
        manipulationBadge.style.color = m.verdict_color;
        manipulationBadge.style.border = `1px solid ${m.verdict_color}44`;
        
        if (m.findings && m.findings.length > 0) {
            manipulationContent.innerHTML = m.findings.map(f => `
                <div style="background: rgba(255,255,255,0.03); padding: 0.5rem 0.75rem; border-radius: 6px; margin-top: 0.5rem; font-size: 0.85rem;">
                    <span style="color: ${f.severity === 'high' ? '#ef4444' : f.severity === 'medium' ? '#f59e0b' : '#3b82f6'}; font-weight: 600;">${f.severity.toUpperCase()}</span>
                    <span style="color: #cbd5e1;"> — ${f.description}</span>
                    ${f.examples ? `<div style="margin-top: 4px; display: flex; gap: 4px; flex-wrap: wrap;">${f.examples.slice(0, 4).map(e => `<span style="background: rgba(239,68,68,0.15); color: #fca5a5; padding: 1px 6px; border-radius: 4px; font-size: 0.75rem;">${e}</span>`).join('')}</div>` : ''}
                </div>
            `).join('');
        } else {
            manipulationContent.innerHTML = `<p style="color: #4ade80; font-size: 0.85rem; margin-top: 0.5rem;">✓ No manipulation patterns detected</p>`;
        }
        
        manipulationDetail.style.display = 'flex';
    } else {
        manipulationDetail.style.display = 'none';
    }

    // ====== NEW: Writing Quality ======
    const writingDetail = document.getElementById('writingDetail');
    const writingContent = document.getElementById('writingContent');
    if (data.content_analysis && data.content_analysis.writing_quality) {
        const w = data.content_analysis.writing_quality;
        writingContent.innerHTML = `
            <div style="display: flex; align-items: center; gap: 1rem; margin-top: 0.5rem;">
                <div style="flex: 1; background: rgba(255,255,255,0.05); border-radius: 8px; height: 8px; overflow: hidden;">
                    <div style="width: ${w.score}%; height: 100%; background: ${w.color}; border-radius: 8px; transition: width 1s;"></div>
                </div>
                <span style="font-weight: 700; color: ${w.color}; font-size: 0.95rem; min-width: 60px;">${w.label}</span>
            </div>
            <div style="display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 0.75rem; font-size: 0.8rem; color: #94a3b8;">
                <span>📝 ${w.metrics.word_count} words</span>
                <span>📃 ${w.metrics.sentence_count} sentences</span>
                <span>📏 Avg ${w.metrics.avg_sentence_length} words/sentence</span>
                <span>📚 ${w.metrics.vocabulary_richness}% vocab richness</span>
            </div>
        `;
        writingDetail.style.display = 'flex';
    } else {
        writingDetail.style.display = 'none';
    }

    // ====== NEW: URL Analysis ======
    const urlDetail = document.getElementById('urlDetail');
    const urlContent = document.getElementById('urlContent');
    if (data.url_analysis) {
        const u = data.url_analysis;
        urlContent.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem;">
                <span style="font-size: 0.85rem; color: #64748b;">Domain:</span>
                <span style="font-weight: 600; color: #e2e8f0;">${u.domain || 'Unknown'}</span>
                <span style="font-size: 0.75rem; padding: 2px 8px; border-radius: 10px; background: ${u.verdict_color}22; color: ${u.verdict_color}; font-weight: 600; border: 1px solid ${u.verdict_color}44;">${u.verdict}</span>
            </div>
            ${u.trust_factors && u.trust_factors.length > 0 ? `<div style="margin-top: 0.5rem;">${u.trust_factors.map(f => `<div style="color: #4ade80; font-size: 0.8rem;">✓ ${f}</div>`).join('')}</div>` : ''}
            ${u.risk_factors && u.risk_factors.length > 0 ? `<div style="margin-top: 0.5rem;">${u.risk_factors.map(f => `<div style="color: #f87171; font-size: 0.8rem;">⚠ ${f}</div>`).join('')}</div>` : ''}
            <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #94a3b8;">${u.analysis_summary || ''}</div>
        `;
        urlDetail.style.display = 'flex';
    } else {
        urlDetail.style.display = 'none';
    }

    // Source Credibility
    const sourceDetail = document.getElementById('sourceDetail');
    const sourceText = document.getElementById('sourceText');
    if (data.sources && data.sources.length > 0) {
        const topSource = data.sources[0];
        let color = '#4ade80';
        if (topSource.score < 50) color = '#ef4444';
        else if (topSource.score < 80) color = '#facc15';
        
        sourceText.innerHTML = `Source matched: <strong>${topSource.name}</strong> • Trust Score: <span style="color: ${color}; font-weight: bold;">${topSource.score}/100</span> (${topSource.tier})`;
        sourceDetail.style.display = 'flex';
    } else {
        sourceDetail.style.display = 'none';
    }

    // Fact Checks
    const factCheckDetail = document.getElementById('factCheckDetail');
    const factCheckList = document.getElementById('factCheckList');
    if (data.fact_checks && data.fact_checks.length > 0) {
        factCheckList.innerHTML = data.fact_checks.map(fc => `
            <div style="background: rgba(255,255,255,0.05); padding: 8px 12px; border-radius: 6px; font-size: 0.9rem;">
                <span style="color: #94a3b8; font-size: 0.8rem; display: block; margin-bottom: 2px;">Fact Check by ${fc.publisher}</span>
                <a href="${fc.url}" target="_blank" style="color: #60a5fa; text-decoration: none;">${fc.title || fc.claim}</a>
                <span style="display: inline-block; margin-left: 8px; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; background: rgba(255,255,255,0.1);">${fc.rating}</span>
            </div>
        `).join('');
        factCheckDetail.style.display = 'flex';
    } else {
        factCheckDetail.style.display = 'none';
    }

    // Explainability / Heatmap (LIME-style)
    const heatmapDetail = document.getElementById('heatmapDetail');
    const heatmapContent = document.getElementById('heatmapContent');
    const textToAnalyze = window.currentPrediction.text;
    
    if (textToAnalyze && textToAnalyze.length > 50) {
        heatmapDetail.style.display = 'flex';
        heatmapContent.innerHTML = '<span style="color:#64748b; font-style:italic;">Generating neural perception map...</span>';
        
        fetch('/api/heatmap', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textToAnalyze })
        }).then(r => r.json()).then(heatmapData => {
            if (heatmapData.success && heatmapData.annotated) {
                heatmapContent.innerHTML = heatmapData.annotated.map(wordObj => {
                    if (wordObj.score === 0) return `<span>${wordObj.token}</span>`;
                    
                    let bg = '';
                    let color = '#fff';
                    // Red for fake (> 0), Green for real (< 0)
                    if (wordObj.score > 0) {
                        const intensity = Math.min(1, wordObj.score * 1.5);
                        bg = `rgba(239, 68, 68, ${intensity})`;
                    } else {
                        const intensity = Math.min(1, Math.abs(wordObj.score) * 1.5);
                        bg = `rgba(34, 197, 94, ${intensity})`;
                    }
                    return `<span style="background: ${bg}; color: ${color}; border-radius: 3px; padding: 0 2px;">${wordObj.token}</span>`;
                }).join('');
            }
        }).catch(e => console.error(e));
    } else {
        heatmapDetail.style.display = 'none';
    }

    // IPR Content Originality Score
    const iprDetail = document.getElementById('iprDetail');
    const iprScore = document.getElementById('iprScore');
    const iprText = document.getElementById('iprText');
    const iprContent = document.getElementById('iprContent');
    
    if (textToAnalyze && textToAnalyze.length > 50) {
        iprDetail.style.display = 'flex';
        iprScore.innerHTML = `<span style="font-size: 0.8rem; color: #94a3b8;">Scanning...</span>`;
        iprText.innerHTML = '';
        iprContent.innerHTML = '';
        
        // Fire async request to IPR endpoint
        fetch('/api/ipr-check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textToAnalyze })
        }).then(r => r.json()).then(iprData => {
            if (iprData.success && iprData.ipr) {
                const iprType = iprData.ipr;
                
                let colorHex = '#eab308';
                if (iprType.ipr_color === 'red') colorHex = '#ef4444';
                if (iprType.ipr_color === 'green') colorHex = '#22c55e';
                if (iprType.ipr_color === 'orange') colorHex = '#f97316';
                if (iprType.ipr_color === 'yellow') colorHex = '#eab308';
                
                iprDetail.style.borderLeftColor = colorHex;
                iprScore.style.color = colorHex;
                iprScore.textContent = `${iprType.originality_score}/100`;
                
                iprText.style.color = colorHex;
                iprText.textContent = iprType.ipr_risk;
                
                // Content summary details
                let detailsHTML = `<div style="display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 0.5rem; font-size: 0.8rem; color: #94a3b8;">`;
                detailsHTML += `<span>📚 ${iprType.vocab_diversity}% vocab diversity</span>`;
                if(iprType.ipr_summary.pattern_flags.length > 0) {
                    detailsHTML += `<span style="color:#fb923c;">⚠️ ${iprType.ipr_summary.pattern_flags.length} stylistic flags</span>`;
                }
                detailsHTML += `</div>`;
                
                // Key phrases pill list
                if (iprType.key_phrases && iprType.key_phrases.length > 0) {
                    detailsHTML += `<div style="margin-top: 0.75rem;"><div style="font-size:0.75rem; color:#64748b; margin-bottom:0.25rem; text-transform:uppercase;">Extracted Key Sequences:</div><div style="display: flex; flex-wrap: wrap; gap: 4px;">`;
                    detailsHTML += iprType.key_phrases.map(p => `<span style="background: rgba(255,255,255,0.05); padding: 2px 8px; border-radius: 8px; font-size: 0.75rem; color: #cbd5e1; border: 1px solid rgba(255,255,255,0.1);">${p}</span>`).join('');
                    detailsHTML += `</div></div>`;
                }
                iprContent.innerHTML = detailsHTML;
            }
        }).catch(e => {
            console.error(e);
            iprDetail.style.display = 'none';
        });
    } else {
        iprDetail.style.display = 'none';
    }

    // Trust Score Components Breakdown
    const trustBreakdown = document.getElementById('trustBreakdown');
    const trustBars = document.getElementById('trustBars');
    if (data.trust_components) {
        const components = [
            { label: 'ML Prediction', value: data.trust_components.ml_prediction, color: '#818cf8' },
            { label: 'Content Credibility', value: data.trust_components.content_analysis, color: '#a855f7' },
            { label: 'Manipulation Safety', value: data.trust_components.manipulation_inverse, color: '#22c55e' },
            { label: 'Writing Quality', value: data.trust_components.writing_quality, color: '#3b82f6' }
        ];
        
        trustBars.innerHTML = components.map(c => `
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 0.8rem; color: #94a3b8; min-width: 140px; text-align: right;">${c.label}</span>
                <div style="flex: 1; background: rgba(255,255,255,0.05); border-radius: 6px; height: 6px; overflow: hidden;">
                    <div style="width: ${c.value}%; height: 100%; background: ${c.color}; border-radius: 6px; transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);"></div>
                </div>
                <span style="font-size: 0.8rem; font-weight: 700; color: ${c.color}; min-width: 40px;">${Math.round(c.value)}%</span>
            </div>
        `).join('');
        
        trustBreakdown.style.display = 'block';
    } else {
        trustBreakdown.style.display = 'none';
    }

    // Show result
    resultContainer.style.display = 'block';
    setTimeout(() => {
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 200);
}


// ===== FORM SUBMISSION =====
function initFormSubmission() {
    const form = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');

    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const textarea = document.getElementById('news_text');
        const text = textarea.value.trim();

        if (text.length < 10) {
            showNotification('Please enter at least 10 characters', 'error');
            return;
        }

        // Show loading + neural network animation
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        const nnContainer = document.getElementById('neuralNetContainer');
        const resultContainer = document.getElementById('resultContainer');
        if (resultContainer) resultContainer.style.display = 'none';
        if (nnContainer) {
            nnContainer.style.display = 'block';
            const canvas = document.getElementById('neuralNetCanvas');
            drawNeuralNetwork(canvas, true);
        }

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            if (response.ok) {
                displayResult(data);
            } else {
                showNotification(data.error || 'An error occurred', 'error');
                if (nnContainer) nnContainer.style.display = 'none';
            }
        } catch (error) {
            console.error('Prediction error:', error);
            showNotification('Failed to connect to the server', 'error');
            if (nnContainer) nnContainer.style.display = 'none';
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });
}


// ===== SHARE REPORT / WHATSAPP =====
async function shareReport() {
    if (!lastAnalysisResult) return;
    const btn = document.getElementById('shareReportBtn');
    const ogText = btn.innerHTML;
    btn.innerHTML = '⏳ Generating...';
    btn.disabled = true;

    try {
        const response = await fetch('/api/share-card', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(lastAnalysisResult)
        });
        const data = await response.json();
        
        if (data.success && data.whatsapp_url) {
            window.open(data.whatsapp_url, '_blank');
        } else {
            showNotification('Failed to generate share link', 'error');
        }
    } catch (e) {
        console.error(e);
        showNotification('Connection error', 'error');
    } finally {
        btn.innerHTML = ogText;
        btn.disabled = false;
    }
}

// ===== GENERATE REPORT (PDF/HTML) =====
function generateReport() {
    if (!lastAnalysisResult) {
        showNotification('No analysis data available', 'error');
        return;
    }
    
    const data = lastAnalysisResult;
    const isFake = data.prediction.toLowerCase().includes('fake');
    
    const reportHTML = `
<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>FakeDetect AI Report — ${new Date().toLocaleDateString()}</title>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', Arial, sans-serif; background: #0f172a; color: #e2e8f0; padding: 2rem; }
    .report { max-width: 800px; margin: 0 auto; background: #1e293b; border-radius: 16px; padding: 2.5rem; border: 1px solid rgba(255,255,255,0.1); }
    .header { text-align: center; margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .header h1 { font-size: 1.5rem; color: #818cf8; margin-bottom: 0.5rem; }
    .header p { color: #94a3b8; font-size: 0.9rem; }
    .verdict { text-align: center; padding: 1.5rem; margin: 1.5rem 0; border-radius: 12px; background: ${isFake ? 'rgba(239,68,68,0.1)' : 'rgba(34,197,94,0.1)'}; border: 1px solid ${isFake ? 'rgba(239,68,68,0.3)' : 'rgba(34,197,94,0.3)'}; }
    .verdict h2 { font-size: 2rem; color: ${isFake ? '#ef4444' : '#22c55e'}; margin-bottom: 0.5rem; }
    .verdict .score { font-size: 1.2rem; color: #94a3b8; }
    .section { margin: 1.5rem 0; padding: 1rem 1.25rem; background: rgba(255,255,255,0.03); border-radius: 10px; border-left: 3px solid #818cf8; }
    .section h3 { font-size: 1rem; color: #818cf8; margin-bottom: 0.75rem; }
    .metric { display: flex; justify-content: space-between; padding: 0.4rem 0; font-size: 0.9rem; }
    .metric .label { color: #94a3b8; }
    .metric .value { font-weight: 600; }
    .footer { text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1); color: #64748b; font-size: 0.8rem; }
    @media print { body { background: white; color: #1e293b; } .report { border: 1px solid #e5e7eb; } }
</style></head>
<body>
<div class="report">
    <div class="header">
        <h1>🛡️ FakeDetect AI — Analysis Report</h1>
        <p>Generated on ${new Date().toLocaleString()} • Report ID: FD-${Date.now().toString(36).toUpperCase()}</p>
    </div>
    
    <div class="verdict">
        <h2>${isFake ? '❌ FAKE NEWS' : '✅ REAL NEWS'}</h2>
        <div class="score">ML Confidence: ${data.confidence?.toFixed(1) || 'N/A'}% | Overall Trust Score: ${data.overall_trust_score?.toFixed(1) || 'N/A'}%</div>
    </div>

    <div class="section">
        <h3>📝 Analyzed Content</h3>
        <p style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;">${data.text_preview || 'N/A'}</p>
    </div>

    ${data.content_analysis?.sentiment ? `
    <div class="section" style="border-left-color: #8b5cf6;">
        <h3>💭 Sentiment Analysis</h3>
        <div class="metric"><span class="label">Tone</span><span class="value">${data.content_analysis.sentiment.label} (${data.content_analysis.sentiment.polarity})</span></div>
        <div class="metric"><span class="label">Subjectivity</span><span class="value">${data.content_analysis.sentiment.subjectivity_pct}%</span></div>
    </div>` : ''}

    ${data.content_analysis?.manipulation ? `
    <div class="section" style="border-left-color: #ef4444;">
        <h3>🚨 Manipulation Detection</h3>
        <div class="metric"><span class="label">Verdict</span><span class="value" style="color: ${data.content_analysis.manipulation.verdict_color};">${data.content_analysis.manipulation.verdict}</span></div>
        <div class="metric"><span class="label">Score</span><span class="value">${data.content_analysis.manipulation.score}/100</span></div>
        <div class="metric"><span class="label">Patterns Found</span><span class="value">${data.content_analysis.manipulation.total_patterns_found}</span></div>
    </div>` : ''}

    ${data.content_analysis?.writing_quality ? `
    <div class="section" style="border-left-color: #22c55e;">
        <h3>✍️ Writing Quality</h3>
        <div class="metric"><span class="label">Quality</span><span class="value" style="color: ${data.content_analysis.writing_quality.color};">${data.content_analysis.writing_quality.label}</span></div>
        <div class="metric"><span class="label">Word Count</span><span class="value">${data.content_analysis.writing_quality.metrics.word_count}</span></div>
        <div class="metric"><span class="label">Vocabulary Richness</span><span class="value">${data.content_analysis.writing_quality.metrics.vocabulary_richness}%</span></div>
    </div>` : ''}

    ${data.trust_components ? `
    <div class="section" style="border-left-color: #f59e0b;">
        <h3>📊 Trust Score Breakdown</h3>
        <div class="metric"><span class="label">ML Prediction</span><span class="value">${Math.round(data.trust_components.ml_prediction)}%</span></div>
        <div class="metric"><span class="label">Content Credibility</span><span class="value">${Math.round(data.trust_components.content_analysis)}%</span></div>
        <div class="metric"><span class="label">Manipulation Safety</span><span class="value">${Math.round(data.trust_components.manipulation_inverse)}%</span></div>
        <div class="metric"><span class="label">Writing Quality</span><span class="value">${Math.round(data.trust_components.writing_quality)}%</span></div>
    </div>` : ''}

    <div class="footer">
        <p>© 2026 FakeDetect AI • Fake News Detection Platform</p>
        <p style="margin-top: 4px;">Presented at AIKYAM 2026 — RVITM Bengaluru</p>
    </div>
</div>
</body></html>`;

    const blob = new Blob([reportHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `FakeDetect_Report_${new Date().toISOString().slice(0,10)}.html`;
    a.click();
    URL.revokeObjectURL(url);
    
    showNotification('📄 Report downloaded successfully!', 'info');
}


// ===== RESET FORM =====
function resetForm() {
    const textarea = document.getElementById('news_text');
    const charCount = document.getElementById('charCount');
    const resultContainer = document.getElementById('resultContainer');
    const nnContainer = document.getElementById('neuralNetContainer');

    if (textarea) { textarea.value = ''; textarea.focus(); }
    if (charCount) charCount.textContent = '0';
    if (nnContainer) nnContainer.style.display = 'none';

    if (resultContainer) {
        resultContainer.style.animation = 'slideDown 0.4s ease-out forwards';
        setTimeout(() => {
            resultContainer.style.display = 'none';
            resultContainer.style.animation = '';
        }, 400);
    }
    
    lastAnalysisResult = null;
}


// ===== SUBMIT FEEDBACK =====
async function submitFeedback(isCorrect) {
    if (!window.currentPrediction) return;
    
    const feedbackButtons = document.getElementById('feedbackButtons');
    const feedbackThanks = document.getElementById('feedbackThanks');
    
    if (feedbackButtons) feedbackButtons.style.display = 'none';
    if (feedbackThanks) {
        feedbackThanks.style.display = 'block';
        feedbackThanks.textContent = 'Submitting feedback...';
    }
    
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: window.currentPrediction.text,
                label: window.currentPrediction.label,
                correct: isCorrect
            })
        });

        const data = await response.json();

        if (response.ok) {
            if (feedbackThanks) {
                feedbackThanks.innerHTML = '✨ Thank you! Your feedback makes FakeDetect AI smarter.';
            }
            showNotification('Feedback saved! Your input makes the AI smarter.', 'info');
            window.currentPrediction = null;
        } else {
            throw new Error(data.error || 'Failed to save feedback');
        }
    } catch (error) {
        console.error('Feedback error:', error);
        if (feedbackButtons) feedbackButtons.style.display = 'flex';
        if (feedbackThanks) feedbackThanks.style.display = 'none';
        showNotification('An error occurred while saving your feedback.', 'error');
    }
}


// ===== NOTIFICATION SYSTEM =====
function showNotification(message, type = 'info') {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${type === 'error' ? '⚠️' : 'ℹ️'}</span>
        <span class="notification-message">${message}</span>
    `;

    document.body.appendChild(notification);
    setTimeout(() => notification.classList.add('show'), 10);
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Notification styles
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
    .notification-icon { font-size: 1.1rem; }
    @keyframes slideDown {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-20px); }
    }
`;
document.head.appendChild(notificationStyles);


// ===== ACTIVE NAV LINK =====
function initNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            if (window.pageYOffset >= sectionTop && window.pageYOffset < sectionTop + section.offsetHeight) {
                current = section.getAttribute('id');
            }
        });
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) link.classList.add('active');
        });
    }, { passive: true });
}


// ===== PARALLAX =====
function initParallax() {
    const video = document.querySelector('.video-background video');
    if (!video) return;
    window.addEventListener('scroll', () => {
        const rate = window.pageYOffset * 0.3;
        video.style.transform = `translate(-50%, calc(-50% + ${rate}px))`;
    }, { passive: true });
}


// ===== VIDEO BACKGROUND =====
function initVideoBackground() {
    const video = document.getElementById('bgVideo');
    if (!video) return;
    video.playbackRate = 0.8;
    video.addEventListener('loadeddata', () => { video.style.opacity = '1'; });
    video.addEventListener('error', () => {
        const vc = document.querySelector('.video-background');
        if (vc) vc.style.background = 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%)';
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


// ===== FETCH LATEST NEWS =====
async function fetchLatestNews() {
    const btn = document.getElementById('fetchNewsBtn');
    const resultText = document.getElementById('fetchResult');
    if (!btn) return;
    
    btn.classList.add('loading');
    btn.disabled = true;
    if (resultText) resultText.textContent = '';

    try {
        const response = await fetch('/api/fetch-news', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();

        if (response.ok && data.success) {
            if (resultText) {
                resultText.style.color = '#4ade80';
                resultText.textContent = `✓ ${data.new_articles} new articles added! Total: ${data.total_articles}`;
            }
            showNotification(`Fetched ${data.new_articles} new articles!`, 'info');
            loadFetchStatus();
        } else {
            throw new Error(data.error || 'Failed to fetch news');
        }
    } catch (error) {
        if (resultText) {
            resultText.style.color = '#f87171';
            resultText.textContent = '✗ ' + error.message;
        }
    } finally {
        btn.classList.remove('loading');
        btn.disabled = false;
    }
}


// ===== LOAD FETCH STATUS =====
async function loadFetchStatus() {
    try {
        const response = await fetch('/api/fetch-status');
        if (!response.ok) return;
        const data = await response.json();

        const fetchedEl = document.getElementById('fetchedCount');
        const feedbackEl = document.getElementById('feedbackCount');
        const lastFetchEl = document.getElementById('lastFetchTime');

        if (fetchedEl) fetchedEl.textContent = data.total_fetched || 0;
        if (feedbackEl) feedbackEl.textContent = data.total_feedback || 0;
        if (lastFetchEl) {
            if (data.last_fetch) {
                const d = new Date(data.last_fetch);
                lastFetchEl.textContent = d.toLocaleDateString('en-US', {
                    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                });
            } else {
                lastFetchEl.textContent = 'Never';
            }
        }
    } catch (error) {
        console.log('Could not load fetch status:', error);
    }
}


// ===== LOAD GLOBAL STATS =====
async function loadGlobalStats() {
    try {
        const response = await fetch('/api/stats');
        if (!response.ok) return;
        const data = await response.json();

        animateNumber('globalAnalyses', data.total_analyses || 0);
        animateNumber('globalFake', data.fake_detected || 0);
        animateNumber('globalReal', data.real_detected || 0);
        animateNumber('globalLangs', data.languages_count || 1);
    } catch (error) {
        console.log('Could not load global stats');
    }
}

function animateNumber(elementId, target) {
    const el = document.getElementById(elementId);
    if (!el) return;
    
    const duration = 1500;
    const start = Date.now();
    
    const update = () => {
        const elapsed = Date.now() - start;
        const progress = Math.min(elapsed / duration, 1);
        const easeOut = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.floor(target * easeOut).toLocaleString();
        
        if (progress < 1) requestAnimationFrame(update);
        else el.textContent = target.toLocaleString();
    };
    
    update();
}


// ===== TRENDING TOPICS =====
async function loadTrendingTopics() {
    const container = document.getElementById('trendingTopicsContainer');
    const btn = document.getElementById('refreshTrendingBtn');
    if (!container) return;
    
    if (btn) { btn.classList.add('loading'); btn.disabled = true; }
    container.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: #64748b;">Loading live topics...</div>`;

    try {
        const response = await fetch('/api/trending');
        const data = await response.json();

        if (response.ok && data.success && data.topics.length > 0) {
            container.innerHTML = data.topics.map(topic => {
                let riskColor, riskBg;
                if (topic.risk_level === 'Low') {
                    riskColor = '#4ade80'; riskBg = 'rgba(34, 197, 94, 0.1)';
                } else if (topic.risk_level === 'Medium') {
                    riskColor = '#facc15'; riskBg = 'rgba(250, 204, 21, 0.1)';
                } else {
                    riskColor = '#ef4444'; riskBg = 'rgba(239, 68, 68, 0.1)';
                }

                return `
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 1.2rem; border-radius: 12px; display: flex; flex-direction: column; gap: 0.5rem; transition: transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem;">
                            <span style="font-size: 0.75rem; padding: 2px 8px; border-radius: 10px; background: rgba(59,130,246,0.1); color: #60a5fa; white-space: nowrap;">${topic.category}</span>
                            <span style="font-size: 0.75rem; padding: 2px 8px; border-radius: 10px; background: ${riskBg}; color: ${riskColor}; white-space: nowrap;">${topic.fake_probability}% Fake Risk</span>
                        </div>
                        <h4 style="font-size: 1rem; line-height: 1.4; margin: 0.25rem 0; color: #f8fafc;">
                            <a href="${topic.link}" target="_blank" style="color: inherit; text-decoration: none;">${topic.title}</a>
                        </h4>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.05);">
                            <span style="font-size: 0.8rem; color: #64748b;">${topic.source}</span>
                            <button onclick="document.getElementById('news_text').value='${topic.title.replace(/'/g, "\\'")}'; document.getElementById('predictionForm').scrollIntoView();" style="background: none; border: none; color: #818cf8; font-size: 0.8rem; cursor: pointer; padding: 0;">Analyze ➔</button>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            container.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: #64748b;">No trending topics available right now.</div>`;
        }
    } catch (error) {
        container.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: #ef4444;">Failed to load trending topics.</div>`;
    } finally {
        if (btn) { btn.classList.remove('loading'); btn.disabled = false; }
    }
}


// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', () => {
    initVideoBackground();
    createParticles();
    initNavbarScroll();
    initNavHighlight();
    initScrollAnimations();
    initSmoothScroll();
    initParallax();
    initCounterObserver();
    initCharCounter();
    initFormSubmission();
    initTextareaResize();
    loadFetchStatus();
    loadTrendingTopics();
    loadGlobalStats();

    // Draw static neural network
    const nnCanvas = document.getElementById('neuralNetCanvas');
    if (nnCanvas) drawNeuralNetwork(nnCanvas, false);

    console.log('🛡️ FakeDetect AI v3.0 initialized!');
});

// Global exports
window.resetForm = resetForm;
window.showNotification = showNotification;
window.submitFeedback = submitFeedback;
window.fetchLatestNews = fetchLatestNews;
window.loadTrendingTopics = loadTrendingTopics;
window.generateReport = generateReport;
