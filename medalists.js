document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search');
    const yearGroups = document.querySelectorAll('.year-group');
    const resultCount = document.getElementById('result-count');

    function updateResults() {
        const query = searchInput.value.trim().toLowerCase();
        let totalMatches = 0;
        let hasMatches = false;

        yearGroups.forEach(group => {
            const year = group.getAttribute('data-year');
            const items = group.querySelectorAll('li');
            let groupHasMatches = false;

            if (query === '') {
                group.style.display = 'block';
                totalMatches = 8;
                hasMatches = true;
            } else {
                // Check for exact year match
                if (!isNaN(query) && query.length === 4) {
                    const yearMatch = parseInt(query);
                    if (year === query) {
                        group.style.display = 'block';
                        totalMatches += items.length;
                        hasMatches = true;
                        groupHasMatches = true;
                    } else {
                        group.style.display = 'none';
                    }
                } else {
                    // Check for name matches
                    let matchCount = 0;
                    items.forEach(item => {
                        const text = item.textContent.trim().toLowerCase();
                        if (text.includes(query)) {
                            item.style.display = 'list-item';
                            matchCount++;
                            hasMatches = true;
                        } else {
                            item.style.display = 'none';
                        }
                    });

                    if (matchCount > 0) {
                        group.style.display = 'block';
                        totalMatches += matchCount;
                        groupHasMatches = true;
                    } else {
                        group.style.display = 'none';
                    }
                }
            }
        });

        if (hasMatches) {
            resultCount.textContent = `${totalMatches} result${totalMatches !== 1 ? 's' : ''}`;
            resultCount.style.display = 'block';
        } else {
            resultCount.textContent = 'No results found.';
            resultCount.style.display = 'block';
        }
    }

    searchInput.addEventListener('input', updateResults);
});