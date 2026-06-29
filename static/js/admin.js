// ==========================================================================
// GANGOTRI FIRESTONE (HEXOCHEMS) ADMIN PANEL CONTROL
// Features: Login Authentication, Tabs, Inquiry Accordions, CRUD Forms
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Login Form Handler ---
    const loginForm = document.getElementById('admin-login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const passcode = document.getElementById('admin-passcode').value;
            const errorDiv = document.getElementById('login-error-msg');
            
            errorDiv.style.display = 'none';

            try {
                const response = await fetch('/admin/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: `passcode=${encodeURIComponent(passcode)}`
                });

                const result = await response.json();
                if (response.ok && result.success) {
                    window.location.reload();
                } else {
                    errorDiv.innerText = result.error || 'Invalid Passcode';
                    errorDiv.style.display = 'block';
                }
            } catch (err) {
                errorDiv.innerText = 'Server connection error.';
                errorDiv.style.display = 'block';
            }
        });
    }

    // --- Dashboard Tabs Control ---
    const adminTabs = document.querySelectorAll('.admin-tab-btn');
    const adminSections = document.querySelectorAll('.admin-panel-section');
    if (adminTabs.length > 0) {
        adminTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                adminTabs.forEach(t => t.classList.remove('active'));
                adminSections.forEach(s => s.classList.remove('active'));

                tab.classList.add('active');
                const targetSection = document.getElementById(`admin-sec-${tab.dataset.tab}`);
                if (targetSection) targetSection.classList.add('active');
            });
        });
    }

    // --- Inquiries Accordion Toggle ---
    const inquiryHeaders = document.querySelectorAll('.inquiry-header');
    if (inquiryHeaders.length > 0) {
        inquiryHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const drawer = header.nextElementSibling;
                if (drawer && drawer.classList.contains('inquiry-details-drawer')) {
                    const isVisible = window.getComputedStyle(drawer).display !== 'none';
                    drawer.style.display = isVisible ? 'none' : 'block';
                    header.classList.toggle('drawer-open', !isVisible);
                }
            });
        });
    }

    // --- Delete Inquiry handler (Real-time Optimistic UI) ---
    const deleteInquiryBtns = document.querySelectorAll('.btn-delete-inquiry');
    deleteInquiryBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation(); // Prevent accordion toggling
            
            const inquiryId = btn.dataset.id;
            const clientName = btn.dataset.name;
            const inquiryCard = btn.closest('.inquiry-card');
            
            if (!inquiryCard) return;

            // 1. Optimistic UI update: Fade out & collapse the card immediately
            inquiryCard.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            inquiryCard.style.opacity = '0';
            inquiryCard.style.transform = 'scale(0.95) translateY(-10px)';
            inquiryCard.style.maxHeight = inquiryCard.offsetHeight + 'px'; // Set height explicitly for transition
            
            // Force browser layout reflow
            inquiryCard.offsetHeight;
            
            inquiryCard.style.maxHeight = '0';
            inquiryCard.style.paddingTop = '0';
            inquiryCard.style.paddingBottom = '0';
            inquiryCard.style.marginTop = '0';
            inquiryCard.style.marginBottom = '0';
            inquiryCard.style.overflow = 'hidden';
            inquiryCard.style.border = 'none';

            // 2. Update count instantly in the tab
            const countSpan = document.getElementById('inquiry-count');
            if (countSpan) {
                const currentCount = parseInt(countSpan.textContent) || 0;
                const newCount = Math.max(0, currentCount - 1);
                countSpan.textContent = newCount;
                
                // If count becomes 0, show the empty state after animation
                if (newCount === 0) {
                    setTimeout(() => {
                        const inquiriesSection = document.getElementById('admin-sec-inquiries');
                        if (inquiriesSection) {
                            inquiriesSection.innerHTML = `
                                <div class="glass-panel text-center" style="padding: 4rem; opacity: 0; transform: translateY(10px); transition: all 0.4s ease;">
                                    <i class="fas fa-inbox" style="font-size: 3rem; color: var(--text-muted); margin-bottom: 1rem;"></i>
                                    <p style="color: var(--text-secondary);">No customer inquiries found.</p>
                                </div>
                            `;
                            // Trigger fade in for empty state
                            const emptyPanel = inquiriesSection.querySelector('.glass-panel');
                            if (emptyPanel) {
                                setTimeout(() => {
                                    emptyPanel.style.opacity = '1';
                                    emptyPanel.style.transform = 'translateY(0)';
                                }, 50);
                            }
                        }
                    }, 400);
                }
            }

            // Remove element from DOM after transition finishes
            setTimeout(() => {
                inquiryCard.remove();
            }, 400);

            // 3. Make background API request to delete from database
            try {
                const response = await fetch(`/api/inquiry/${inquiryId}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                if (!response.ok || !result.success) {
                    throw new Error(result.error || 'Failed to delete');
                }
                console.log(`Inquiry from ${clientName} deleted successfully in database.`);
            } catch (err) {
                alert(`Error deleting inquiry: ${err.message || err}. Restoring item.`);
                // If deletion fails, reload the page to restore state
                window.location.reload();
            }
        });
    });


    // --- Product Actions (Add, Edit, Delete) ---
    initProductAdmin();
});

/**
 * Handle CRUD operations for Products inside Admin Dashboard
 */
function initProductAdmin() {
    const modal = document.getElementById('product-modal');
    const openModalBtn = document.getElementById('btn-open-prod-modal');
    const closeModalBtn = document.getElementById('btn-close-prod-modal');
    const productForm = document.getElementById('product-form');

    if (!modal) return;

    // Open Modal
    if (openModalBtn) {
        openModalBtn.addEventListener('click', () => {
            productForm.reset();
            document.getElementById('modal-title').innerText = 'Add New Product';
            document.getElementById('prod-form-id').value = '';
            document.getElementById('prod-form-id').readOnly = false;
            modal.classList.add('active');
        });
    }

    // Close Modal
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            modal.classList.remove('active');
        });
    }

    // Close Modal on clicking outside the modal content (on the overlay)
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });

    // Submit Product Form (multipart/form-data)
    productForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = productForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerText = 'Saving...';

        const formData = new FormData(productForm);

        try {
            const response = await fetch('/api/products', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            if (response.ok && result.success) {
                alert('Product saved successfully!');
                window.location.reload();
            } else {
                alert(`Error: ${result.error || 'Failed to save product'}`);
            }
        } catch (err) {
            alert('Failed to connect to server.');
            console.error(err);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerText = 'Save Product';
        }
    });

    // Delete Product handler
    const deleteButtons = document.querySelectorAll('.btn-delete-product');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const productId = btn.dataset.id;
            const productName = btn.dataset.name;
            
            if (confirm(`Are you sure you want to delete the product: ${productName}?`)) {
                try {
                    const response = await fetch(`/api/products/${productId}`, {
                        method: 'DELETE'
                    });
                    
                    const result = await response.json();
                    if (response.ok && result.success) {
                        alert('Product deleted successfully.');
                        window.location.reload();
                    } else {
                        alert(`Error: ${result.error || 'Failed to delete product.'}`);
                    }
                } catch (err) {
                    alert('Server error while deleting product.');
                    console.error(err);
                }
            }
        });
    });

    // Edit Product handler (Prefills form)
    const editButtons = document.querySelectorAll('.btn-edit-product');
    editButtons.forEach(btn => {
        btn.addEventListener('click', async () => {
            const productId = btn.dataset.id;
            try {
                const response = await fetch('/api/products');
                const result = await response.json();
                
                if (response.ok && result.success) {
                    const product = result.products.find(p => p.id === productId);
                    if (product) {
                        // Prefill form fields
                        document.getElementById('prod-form-id').value = product.id;
                        document.getElementById('prod-form-id').readOnly = true;
                        document.getElementById('prod-form-name').value = product.name || '';
                        document.getElementById('prod-form-code').value = product.code || '';
                        document.getElementById('prod-form-category').value = product.category || 'Liquid Base';
                        document.getElementById('prod-form-tagline').value = product.tagline || '';
                        document.getElementById('prod-form-desc').value = product.description || '';
                        document.getElementById('prod-form-dosage').value = product.dosage || '';
                        document.getElementById('prod-form-compliance').value = product.compliance || '';
                        document.getElementById('prod-form-packaging').value = product.packaging || '';
                        document.getElementById('prod-form-image-url').value = product.image || '';
                        
                        // Prefill arrays / lists as textareas
                        const benefits = product.key_benefits || [];
                        document.getElementById('prod-form-benefits').value = benefits.join('\n');
                        
                        const guides = product.application_guide || [];
                        document.getElementById('prod-form-guides').value = guides.join('\n');
                        
                        // Prefill specs
                        const specs = product.technical_features || {};
                        let specsStr = '';
                        for (const [k, v] of Object.entries(specs)) {
                            specsStr += `${k}:${v}\n`;
                        }
                        document.getElementById('prod-form-features').value = specsStr.trim();
                        
                        // Set title & open modal
                        document.getElementById('modal-title').innerText = 'Edit Product';
                        modal.classList.add('active');
                    }
                }
            } catch (err) {
                alert('Failed to retrieve product details.');
                console.error(err);
            }
        });
    });
}
