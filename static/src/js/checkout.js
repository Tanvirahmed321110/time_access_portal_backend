// =========== Confirm Order ==============
let confirmBtn = document.querySelector('.btn-confirm-order');

if (confirmBtn) {
    confirmBtn.addEventListener('click', function () {

        let productId = this.getAttribute('data-product-id');
        let qty = this.getAttribute('data-qty');

        let companyName = document.querySelector('[name="company_name"]')?.value || '';
        let mobile = document.querySelector('[name="mobile"]')?.value || '';
        let email = document.querySelector('[name="email"]')?.value || '';
        let street = document.querySelector('[name="street"]')?.value || '';

        fetch('/cart/confirm', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'call',
                params: {
                    product_id: productId,
                    qty: qty,
                    company_name: companyName,
                    mobile: mobile,
                    email: email,
                    street: street,
                }
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.result && data.result.success) {
                window.location.href = '/orders/' + data.result.order_id;
            } else {
                alert(data.result?.error || 'Something went wrong.');
            }
        })
        .catch(err => {
            console.error(err);
            alert('Order confirmation failed.');
        });
    });
}