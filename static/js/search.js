/**
 * search.js — Fuse.js full-text search for AI Learning
 * Loads search-index.json, initializes Fuse, handles input/results.
 */
(function () {
  var fuse = null;
  var searchInput = document.getElementById('search-input');
  var searchResults = document.getElementById('search-results');

  if (!searchInput || !searchResults) return;

  // Determine root path from data attribute or default
  var root = document.body.getAttribute('data-root') || '';

  // Load search index
  fetch(root + 'search-index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      fuse = new Fuse(data, {
        keys: [
          { name: 'title', weight: 0.4 },
          { name: 'excerpt', weight: 0.3 },
          { name: 'tags', weight: 0.2 },
          { name: 'author', weight: 0.1 }
        ],
        threshold: 0.3,
        includeScore: true,
        minMatchCharLength: 2
      });
    })
    .catch(function () {});

  // Handle input
  searchInput.addEventListener('input', function () {
    var query = this.value.trim();
    if (!query || !fuse) {
      searchResults.classList.remove('active');
      return;
    }

    var results = fuse.search(query, { limit: 8 });
    if (results.length === 0) {
      searchResults.innerHTML = '<div class="search-no-result">找不到相關文章</div>';
      searchResults.classList.add('active');
      return;
    }

    var html = '';
    for (var i = 0; i < results.length; i++) {
      var item = results[i].item;
      html += '<a class="search-result-item" href="' + root + 'articles/' + item.slug + '.html">' +
        '<div class="search-result-title">' + escapeHtml(item.title) + '</div>' +
        '<div class="search-result-excerpt">' + escapeHtml(item.excerpt || '') + '</div>' +
        '</a>';
    }
    searchResults.innerHTML = html;
    searchResults.classList.add('active');
  });

  // Close on click outside
  document.addEventListener('click', function (e) {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.classList.remove('active');
    }
  });

  // Close on Escape
  searchInput.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      searchResults.classList.remove('active');
      searchInput.blur();
    }
  });

  function escapeHtml(text) {
    var d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
  }
})();
