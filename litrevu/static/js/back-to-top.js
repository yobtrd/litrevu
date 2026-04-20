/**
 * Initializes back-to-top button behavior:
 * - Shows/hides button based on scroll position (1000px threshold)
 * - Smooth scrolls to top on click
 * - Sets tooltip title
 */
function BackToTopButton() {
    const btn = document.getElementById('back-to-top');
    btn.setAttribute('title', 'Revenir en haut');
    if (!btn) return;
    
    // Force l'état initial immédiatement
    btn.classList.add('hidden');
    
    // Puis la logique normale
    window.addEventListener('scroll', () => {
        btn.classList.toggle('hidden', window.scrollY <= 1000);
    });

    btn.addEventListener('click', () => {
        window.scrollTo({
        top: 0,
        behavior: 'smooth'
        });
    });
    }

document.addEventListener('DOMContentLoaded', BackToTopButton);