/**
 * Initializes user search functionality with dynamic dropdown.
 * Listens to input events on search_user field, fetches matching users via API,
 * and displays results in a dynamically created dropdown div.
 * 
 * Features:
 * - Debounces requests by requiring min 2 characters
 * - Self-contained DOM injection
 * - Tailwind-compatible visibility toggling
 */
function searchFollowers() {
    const searchInput = document.getElementById('search_user');
    const resultsDiv = document.createElement('div');
    resultsDiv.id = 'search-results';
    searchInput.parentNode.insertBefore(resultsDiv, searchInput.nextSibling);

    searchInput.addEventListener('input', async (e) => {
        if (e.target.value.length < 2) {
            resultsDiv.innerHTML = '';
            resultsDiv.classList.add('hidden')
            return;
        }
        
        const response = await fetch(`/follow/api/search_user/?q=${e.target.value}`);
        const data = await response.json();
        
        resultsDiv.innerHTML = data.results.map(u => `
            <div>
                ${u.username}
            </div>
        `).join('');
        resultsDiv.classList.remove('hidden');
        resultsDiv.classList.add('search-block')
    });
    hideOnClickOutside(searchInput, resultsDiv)
};


/**
 * Hides target element when clicking outside it or its child elements.
 * @param {HTMLElement} searchInput - Element triggering the dropdown
 * @param {HTMLElement} resultsDiv - Dropdown element to hide
 */
function hideOnClickOutside(searchInput, resultsDiv) {
  document.addEventListener('click', (e) => {
    const clickInside = searchInput.contains(e.target) || resultsDiv.contains(e.target);
    
    if (!clickInside) {
      resultsDiv.classList.add('hidden');
    }
  });
}

document.addEventListener('DOMContentLoaded', searchFollowers);