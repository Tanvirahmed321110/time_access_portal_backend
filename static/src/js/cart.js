
//================  add to cart  ==============
document.querySelectorAll('.add_to_cart').forEach(function(btn) {
    btn.addEventListener('click', function() {
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
                btn.setAttribute('title', 'Already added to cart');

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
            }

             // Cart count -1
            let cartCount = document.getElementById('cartCount');
            if (cartCount) {
                let count = parseInt(cartCount.textContent || 0) - 1;
                cartCount.textContent = count < 0 ? 0 : count;
            }
        });
    });
});
}


