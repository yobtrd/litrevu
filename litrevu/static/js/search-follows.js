const searchInput = document.getElementById('search_user');
const resultsDiv = document.createElement('div');
resultsDiv.id = 'search-results';
searchInput.parentNode.insertBefore(resultsDiv, searchInput.nextSibling);

searchInput.addEventListener('input', async (e) => {
    if (e.target.value.length < 2) {
        resultsDiv.innerHTML = '';
        resultsDiv.style.display = 'none';
        return;
    }
    
    const response = await fetch(`/follow/api/search_user/?q=${e.target.value}`);
    const data = await response.json();
    
    resultsDiv.innerHTML = data.results.map(u => `
        <div>
            ${u.username}
        </div>
    `).join('');
    resultsDiv.style.display = 'block';

});