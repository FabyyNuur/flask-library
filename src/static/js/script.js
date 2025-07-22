document.querySelectorAll('.remove-btn').forEach(button => {
    button.addEventListener('click', function() {
        this.closest('.cart-item').remove();
        // Update subtotal here if necessary
    });
});