
//================  add to cart  ==============
document.querySelectorAll('.add_to_cart').forEach(function(btn) {
    btn.addEventListener('click', function() {

        // 500ms debounce
        if (btn._processing) return;
        btn._processing = true;
        setTimeout(function() { btn._processing = false; }, 500);

        let productId = parseInt(this.getAttribute('data-product-id'));
        let qtyInput = document.querySelector('#qty-' + productId);
        let quantity = qtyInput ? parseInt(qtyInput.value) : 1;

        fetch('/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'call',
                params: {
                    product_id: productId,
                    quantity: quantity,
                }
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.result && data.result.success) {
                btn.disabled = true;
                btn.textContent = 'Added to Cart';
                btn.classList.add('disabled');
                btn.parentElement.setAttribute('title', 'Already added to cart');

                 // Cart count +1
                let cartCount = document.getElementById('cartCount');
                if (cartCount) {
                    cartCount.textContent = parseInt(cartCount.textContent || 0) + 1;
                }
            }
        });
    });
});






// =========== Remove from Cart ==========
deletebtns = document.querySelectorAll('.delete-line-btn')
if(deletebtns){
    deletebtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
        let lineId = parseInt(this.getAttribute('data-line-id'));
        fetch('/cart/remove', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                jsonrpc: '2.0', method: 'call',
                params: {line_id: lineId}
            })
        })
        .then(res => res.json())
       .then(data => {
            if (data.result && data.result.success) {
                btn.closest('tr').remove();
                checkEmptyCart();

                // Cart count -1
                let cartCount = document.getElementById('cartCount');
                if (cartCount) {
                    let count = parseInt(cartCount.textContent || 0) - 1;
                    cartCount.textContent = count < 0 ? 0 : count;
                }

                // Order summary update
                let result = data.result;
                let subtotal = document.getElementById('summarySubtotal');
                let total = document.getElementById('summaryTotal');
                if (subtotal && result.amount_untaxed !== undefined) {
                    subtotal.textContent = 'TK ' + parseFloat(result.amount_untaxed).toFixed(2);
                }
                if (total && result.amount_total !== undefined) {
                    total.textContent = 'TK ' + parseFloat(result.amount_total).toFixed(2);
                }
            }
        });
    });
});
}



//=========  check empty cart  =============
function checkEmptyCart() {
    let remainingRows = document.querySelectorAll('#cartTable tbody tr');
    let tableWrap = document.querySelector('.table-wrap');
    let emptyCart = document.querySelector('.empty-cart-wrapper');
    let checkoutBtn = document.querySelector('.btn-checkout');


    if (remainingRows.length === 0) {
        if (tableWrap) tableWrap.style.display = 'none';
        if (emptyCart) emptyCart.style.display = 'block';

        if (checkoutBtn) {
            checkoutBtn.removeAttribute('href');
            checkoutBtn.classList.add('disabled');
        }
    } else {
        if (tableWrap) tableWrap.style.display = 'block';
        if (emptyCart) emptyCart.style.display = 'none';
    }
}





// =========== Quantity Update ==============
let qtyInputs = document.querySelectorAll('.qty-update-input');
if (qtyInputs.length > 0) {
    qtyInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            let lineId = parseInt(this.getAttribute('data-line-id'));
            let quantity = parseFloat(this.value);

            if (quantity < 1) {
                this.value = 1;
                quantity = 1;
            }

            fetch('/cart/update_qty', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    jsonrpc: '2.0', method: 'call',
                    params: {
                        line_id: lineId,
                        quantity: quantity,
                    }
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.result && data.result.success) {
                    // Subtotal update
                    let row = this.closest('tr');
                    let subtotalCell = row.querySelector('td:nth-child(4)');
                    if (subtotalCell) {
                        subtotalCell.textContent = 'TK ' + parseFloat(data.result.price_subtotal).toFixed(2);
                    }

                    // Order summary update
                    let subtotal = document.getElementById('summarySubtotal');
                    let total = document.getElementById('summaryTotal');
                    if (subtotal) subtotal.textContent = 'TK ' + parseFloat(data.result.amount_untaxed).toFixed(2);
                    if (total) total.textContent = 'TK ' + parseFloat(data.result.amount_total).toFixed(2);
                }
            });
        });
    });
}





// =========== Buy Now ==============
let buyNowBtns = document.querySelectorAll('.btn-buy-now');
if (buyNowBtns.length > 0) {
    buyNowBtns.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();

            let productId = parseInt(this.getAttribute('data-product-id'));
            let qtyInput = document.querySelector('#qty-' + productId);
            let quantity = qtyInput ? parseInt(qtyInput.value) : 1;

            if (!quantity || quantity < 1) {
                quantity = 1;
            }

            fetch('/cart/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        product_id: productId,
                        quantity: quantity,

                        // IMPORTANT:
                        // Buy Now hole old qty er sathe add korbe na.
                        // Selected qty diye replace korbe.
                        replace_qty: true,
                    }
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.result && data.result.success) {
                    window.location.href = '/checkout';
                }
            });
        });
    });
}




