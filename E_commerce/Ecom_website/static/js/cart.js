var updateBtns = document.getElementsByClassName('Add-to-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        // console.log('productId:', productId, 'action:', action);

        // Debugging: Check if event listener is triggered
        // console.log('Clicked on arrow:', this);

        // console.log('USER:', user);
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
}


function updateUserOrder(productId, action) {
    var url = '/update_item/'; // Ensure this is the correct URL for the POST request
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            productId: productId,
            action: action
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('data:', data);
        location.reload(); // Refresh the page after updating the quantity
    })
    .catch(error => {
        console.error('Error:', error.message);
        alert('An error occurred while updating the item. Please try again later.');
    });
}
