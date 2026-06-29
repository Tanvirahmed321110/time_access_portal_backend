// =========== Confirm Order ==============
let confirmBtn = document.querySelector('.btn-confirm-order');
if (confirmBtn) {
    confirmBtn.addEventListener('click', function() {
        if (!confirm('Are you sure you want to place this order?')) return;

        let productId = this.getAttribute('data-product-id');
        let qty = this.getAttribute('data-qty');

        fetch('/cart/confirm', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                jsonrpc: '2.0', method: 'call',
                params: { product_id: productId, qty: qty }
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.result && data.result.success) {
                window.location.href = '/order_invoice/' + data.result.order_id;
            }
        });
    });
}