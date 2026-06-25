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