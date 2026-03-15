/**
 * filter.js — Tag/category filtering for article lists
 * Reads data-tags and data-category attributes from .article-card elements.
 */
(function () {
  var filterBar = document.querySelector('.filter-bar');
  if (!filterBar) return;

  var buttons = filterBar.querySelectorAll('.filter-btn');
  var cards = document.querySelectorAll('.article-card[data-tags]');

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var filterType = btn.getAttribute('data-filter-type') || 'tag';
      var filterValue = btn.getAttribute('data-filter');

      // Toggle active state
      if (btn.classList.contains('active')) {
        btn.classList.remove('active');
        filterValue = null;
      } else {
        buttons.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
      }

      // Filter cards
      cards.forEach(function (card) {
        if (!filterValue) {
          card.style.display = '';
          return;
        }

        var match = false;
        if (filterType === 'tag') {
          var tags = (card.getAttribute('data-tags') || '').split(',');
          match = tags.indexOf(filterValue) !== -1;
        } else if (filterType === 'category') {
          match = card.getAttribute('data-category') === filterValue;
        }

        card.style.display = match ? '' : 'none';
      });
    });
  });
})();
