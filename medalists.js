document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search');
    const yearGroups = document.querySelectorAll('.year-group');
    const resultCount = document.getElementById('result-count');

    function updateResults() {
        const query = searchInput.value.trim().toLowerCase();
        let totalMatches = 0;
        
        // Reset all items to visible state first
        yearGroups.forEach(group => {
            group.style.display = 'block';
            const items = group.querySelectorAll('li');
            items.forEach(item => {
                item.style.display = 'list-item';
            });
        });

        // Handle empty query case
        if (query === '') {
            totalMatches = 0;
            yearGroups.forEach(group => {
                const items = group.querySelectorAll('li');
                items.forEach(item => {
                    totalMatches++;
                });
            });
            resultCount.textContent = `${totalMatches} result${totalMatches !== 1 ? 's' : ''}`;
            resultCount.style.display = 'block';
            return;
        }

        // Handle year query case (4-digit number)
        if (!isNaN(query) && query.length === 4) {
            const yearMatch = parseInt(query);
            let yearGroupFound = false;

            yearGroups.forEach(group => {
                const year = group.getAttribute('data-year');
                
                if (year === query) {
                    // Show all items in this year's group
                    const items = group.querySelectorAll('li');
                    items.forEach(item => {
                        totalMatches++;
                    });
                    yearGroupFound = true;
                } else {
                    // Hide other year groups
                    group.style.display = 'none';
                }
            });

            if (!yearGroupFound) {
                resultCount.textContent = 'No results found.';
            } else {
                resultCount.textContent = `${totalMatches} result${totalMatches !== 1 ? 's' : ''}`;
            }
            resultCount.style.display = 'block';
            return;
        }

        // Handle name query case (partial match)
        let hasMatches = false;
        yearGroups.forEach(group => {
            const items = group.querySelectorAll('li');
            
            // Count matches in this group
            let groupMatchCount = 0;
            items.forEach(item => {
                const text = item.textContent.trim().toLowerCase();
                if (text.includes(query)) {
                    groupMatchCount++;
                    hasMatches = true;
                } else {
                    // Hide non-matching items
                    item.style.display = 'none';
                }
            });
            
            // Hide groups with no matches
            if (groupMatchCount === 0) {
                group.style.display = 'none';
            }
            
            totalMatches += groupMatchCount;
        });

        if (hasMatches) {
            resultCount.textContent = `${totalMatches} result${totalMatches !== 1 ? 's' : ''}`;
        } else {
            resultCount.textContent = 'No results found.';
        }
        
        resultCount.style.display = 'block';
    }

    searchInput.addEventListener('input', updateResults);
});