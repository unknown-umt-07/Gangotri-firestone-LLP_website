// ==========================================================================
// GANGOTRI FIRESTONE (HEXOCHEMS) MAIN CLIENT-SIDE SCRIPT
// Features: Canvas Particle Background, Smooth Scroll, Category Tabs, Forms
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Header Scroll Effect ---
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            if (header && !header.classList.contains('always-scrolled')) {
                header.classList.remove('scrolled');
            }
        }
    });

    // --- Mobile Responsive Nav Toggle ---
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
        navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
            });
        });
    }

    // --- Hero Canvas Particle System ---
    initHeroParticles();

    // --- Product Tabs Filter ---
    initProductFilters();

    // --- Contact Inquiry Form Handler ---
    initInquiryForm();
    
    // --- Realtime updates (Socket.IO) ---
    initRealtime();
});

/**
 * Technical Particle Background for Hero Section / Global Background
 */
function initHeroParticles() {
    const canvas = document.getElementById('live-canvas') || document.getElementById('hero-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = canvas.width = canvas.offsetWidth;
    let height = canvas.height = canvas.offsetHeight;

    // Handle resizing
    window.addEventListener('resize', () => {
        width = canvas.width = canvas.offsetWidth;
        height = canvas.height = canvas.offsetHeight;
    });

    const particles = [];
    const maxParticles = 60;
    const connectionDist = 120;
    const speed = 0.5;

    // Initialize particles
    for (let i = 0; i < maxParticles; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * speed,
            vy: (Math.random() - 0.5) * speed,
            radius: Math.random() * 2 + 1
        });
    }

    // Animation Loop
    function animate() {
        ctx.clearRect(0, 0, width, height);

        // Update & Draw particles
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            
            p.x += p.vx;
            p.y += p.vy;

            // Boundary collision
            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;

            // Draw dot
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(249, 115, 22, 0.4)'; // Orange/Amber dots
            ctx.fill();

            // Connections
            for (let j = i + 1; j < particles.length; j++) {
                const p2 = particles[j];
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < connectionDist) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    // Fade lines out based on distance
                    const alpha = (1 - dist / connectionDist) * 0.15;
                    ctx.strokeStyle = `rgba(249, 115, 22, ${alpha})`;
                    ctx.lineWidth = 0.8;
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(animate);
    }

    animate();
}

/**
 * Initialize realtime Socket.IO connection and handlers
 */
function initRealtime() {
    // Only run if Socket.IO client is available
    if (typeof io === 'undefined') return;

    try {
        const socket = io();

        socket.on('connect', () => {
            console.log('Realtime: connected', socket.id);
        });

        socket.on('products_updated', (data) => {
            console.log('Realtime: products_updated', data);
            // Fetch latest products and update grid
            fetch('/api/products')
                .then(r => r.json())
                .then(resp => {
                    if (resp && resp.success && Array.isArray(resp.products)) {
                        renderProductsGrid(resp.products);
                    } else {
                        // fallback: reload page
                        console.warn('Realtime: failed to refresh products, reloading page');
                        window.location.reload();
                    }
                }).catch(err => {
                    console.error('Realtime fetch error', err);
                });
        });

    } catch (err) {
        console.error('Realtime init error', err);
    }
}

/**
 * Render products array into the grid (replaces existing .products-grid content)
 */
function renderProductsGrid(products) {
    const grid = document.querySelector('.products-grid');
    if (!grid) return;

    // Build HTML for each product (keeps same structure used by server templates)
    const html = products.map(product => {
        const categoryClass = (product.category === 'Liquid Base') ? 'liquid' : 'powder';
        const imgSrc = (product.category === 'Liquid Base') ? '/static/images/carbo.png' : '/static/images/powder_bag.webp';
        const badge = `<span class="product-category-badge">${escapeHtml(product.category || '')}</span>`;

        return `<div class="product-card glass-panel ${categoryClass}">
                    <div class="product-img-container">
                        <img src="${imgSrc}" alt="Product Image" style="max-height: 100%; object-fit: contain;" onerror="this.onerror=null; this.src='/static/images/hexochems_logo.png'">
                        ${badge}
                    </div>
                    <div class="product-info">
                        <span class="product-code">Code: ${escapeHtml(product.code || '')}</span>
                        <h4 class="product-card-title">${escapeHtml(product.name || '')}</h4>
                        <p class="product-card-desc">${escapeHtml(product.description || '')}</p>
                        <div class="product-card-footer">
                            <a href="/product/${encodeURIComponent(product.id)}" class="product-more-link">Technical Specs <i class="fas fa-chevron-right"></i></a>
                        </div>
                    </div>
                </div>`;
    }).join('\n');

    grid.innerHTML = html;

    // Re-bind filters so tabs keep working after replacing grid
    initProductFilters();
}

// Simple HTML escape helper
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/**
 * Product Categories Filtration via Tabs
 */
function initProductFilters() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const productCards = document.querySelectorAll('.product-card');

    if (tabButtons.length === 0 || productCards.length === 0) return;

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from other buttons
            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;

            // Filter cards
            productCards.forEach(card => {
                // If filter is all or matches class
                if (filter === 'all' || card.classList.contains(filter)) {
                    card.style.display = 'flex';
                    // Trigger simple entrance animation
                    card.style.animation = 'none';
                    setTimeout(() => {
                        card.style.animation = 'fadeInUp 0.5s ease forwards';
                    }, 10);
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

/**
 * Handle Contact Inquiry Form Ajax submission
 */
function initInquiryForm() {
    const form = document.getElementById('inquiry-form');
    const statusDiv = document.getElementById('form-status-msg');
    
    if (!form) return;

    // Pre-select product from URL query parameter (e.g. /contact?product=HEXA%20SNF%20200)
    const urlParams = new URLSearchParams(window.location.search);
    const productParam = urlParams.get('product');
    if (productParam) {
        const checkbox = Array.from(form.querySelectorAll('input[name="products"]'))
            .find(cb => cb.value.toLowerCase() === productParam.toLowerCase() || cb.value === productParam);
        if (checkbox) {
            checkbox.checked = true;
            // Scroll to the product selection grid smoothly after page load
            setTimeout(() => {
                const selectionGrid = form.querySelector('.product-selection-grid');
                if (selectionGrid) {
                    selectionGrid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }, 100);
        }
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Disable button while sending
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Sending Inquiry...';

        // Reset status message
        statusDiv.className = 'form-status';
        statusDiv.style.display = 'none';

        // Gather details
        const name = document.getElementById('form-name').value;
        const email = document.getElementById('form-email').value;
        const phone = document.getElementById('form-phone').value;
        const company = document.getElementById('form-company').value;
        const message = document.getElementById('form-message').value;

        // Get selected product IDs
        const selectedProducts = [];
        const checkboxes = form.querySelectorAll('input[name="products"]:checked');
        checkboxes.forEach(cb => {
            selectedProducts.push(cb.value);
        });

        const formData = {
            name: name,
            email: email,
            phone: phone,
            company: company,
            message: message,
            products: selectedProducts
        };

        try {
            const response = await fetch('/api/inquiry', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok && result.success) {
                statusDiv.classList.add('success');
                statusDiv.innerHTML = 'Thank you! Your inquiry has been submitted successfully. Our team will contact you shortly.';
                statusDiv.style.display = 'block';
                form.reset();
            } else {
                statusDiv.classList.add('error');
                statusDiv.innerHTML = `Error: ${result.error || 'Failed to submit inquiry. Please try again.'}`;
                statusDiv.style.display = 'block';
            }
        } catch (err) {
            statusDiv.classList.add('error');
            statusDiv.innerHTML = 'Unable to connect to the server. Please check your internet connection and try again.';
            statusDiv.style.display = 'block';
            console.error('Submission error:', err);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}
