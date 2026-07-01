const gridBtn = document.getElementById('gridBtn');
const listBtn = document.getElementById('listBtn');
const contentsWrapper = document.getElementById('grid-list-contents');


//list btn
listBtn.addEventListener('click', () => {
    gridBtn.classList.remove('active');
    listBtn.classList.add('active');
    contentsWrapper.classList.add('list-contents');
});


//grid btn
gridBtn.addEventListener('click', () => {
    listBtn.classList.remove('active');
    gridBtn.classList.add('active');
    contentsWrapper.classList.remove('list-contents');
});








// ==========  For Popup  ===========
document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (ev) {
        const button = ev.target.closest(".add_to_cart");

        if (!button) {
            return;
        }

        ev.preventDefault();
        const productId = button.dataset.productId;

        showB2BCartPopup(
            "Added to Cart",
            "Product added to draft order successfully."
        );
    });
});

function showB2BCartPopup(title, message) {
    const popup = document.getElementById("b2bCartPopup");
    const titleEl = document.getElementById("b2bCartPopupTitle");
    const messageEl = document.getElementById("b2bCartPopupMessage");

    if (!popup || !titleEl || !messageEl) {
        return;
    }

    titleEl.innerText = title;
    messageEl.innerText = message;

    popup.classList.add("show");

    setTimeout(function () {
        popup.classList.remove("show");
    }, 3500);
}






// For Product Search
function searchProducts() {
    const searchInput = document.getElementById('searchInput');
    const searchValue = (searchInput.value || '').toLowerCase().trim();

    const productCards = document.querySelectorAll('.product-card');
    const noResultsBox = document.getElementById('noResultsBox');
    const pagination = document.querySelector('.pagination');

    let matchedCount = 0;

    productCards.forEach(function(card) {
        const productName = (card.getAttribute('data-name') || '').toLowerCase();
        const itemId = (card.getAttribute('data-item-id') || '').toLowerCase();

        const isMatched =
            productName.includes(searchValue) ||
            itemId.includes(searchValue);

        if (!searchValue || isMatched) {
            card.style.display = '';
            matchedCount++;
        } else {
            card.style.display = 'none';
        }
    });

    if (noResultsBox) {
        noResultsBox.style.display = matchedCount === 0 ? 'block' : 'none';
    }

    // Search korar somoy pagination hide korbe
    if (pagination) {
        pagination.style.display = searchValue ? 'none' : '';
    }
}

// for clear input
function clearProductSearch() {
    const searchInput = document.getElementById('searchInput');

    if (searchInput) {
        searchInput.value = '';
    }
    searchProducts();
}


// for sort dropdown
// document.getElementById('sortSelect').addEventListener('change', function() {
//     const sortValue = this.value;
//     const container = document.getElementById('grid-list-contents');
//     const cards = Array.from(container.querySelectorAll('.product-card'));
//
//     cards.sort((a, b) => {
//         const priceA = parseFloat(a.querySelector('.new-price span').textContent);
//         const priceB = parseFloat(b.querySelector('.new-price span').textContent);
//
//         if (sortValue === 'low-high') return priceA - priceB;
//         if (sortValue === 'high-low') return priceB - priceA;
//         return 0;
//     });
//
//     cards.forEach(card => container.appendChild(card));
// });


// for sort dropdown
document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('grid-list-contents');
    const sortSelect = document.getElementById('sortSelect');

    // ===== Original order save kora (page load somoy) =====
    const originalCards = Array.from(container.querySelectorAll('.product-card'));

    sortSelect.addEventListener('change', function() {
        const sortValue = this.value;

        if (sortValue === 'default') {
            // ===== Original order restore kora =====
            originalCards.forEach(card => container.appendChild(card));
            return;
        }

        const cards = Array.from(container.querySelectorAll('.product-card'));

        cards.sort((a, b) => {
            const priceA = parseFloat(a.querySelector('.new-price span').textContent);
            const priceB = parseFloat(b.querySelector('.new-price span').textContent);

            if (sortValue === 'low-high') return priceA - priceB;
            if (sortValue === 'high-low') return priceB - priceA;
            return 0;
        });

        cards.forEach(card => container.appendChild(card));
    });
});