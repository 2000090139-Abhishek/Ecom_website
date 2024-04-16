var updateBtns = document.getElementsByClassName('Add-to-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

async function updateUserOrder(productId, action) {
    
        var url = '/update_item/'; // Ensure this is the correct URL for the POST request
        var response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                productId: productId,
                action: action
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        var data = await response.json();
        console.log('data:', data);
        location.reload(); // Refresh the page after updating the quantity
    
}
