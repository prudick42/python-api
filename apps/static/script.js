document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(event) {
            const serviceId = this.dataset.id;
            fetch(`/add_to_cart/${serviceId}`, {
                method: 'POST'
            }).then(response => response.json()).then(data => {
                showNotification(data.message);
                this.blur();
            });
        });
    });

    function showNotification(message) {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.opacity = 1;
            setTimeout(() => {
                notification.style.opacity = 0;
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 375);
            }, 750);
        }, 50);
    }

    document.getElementById('sortAsc').addEventListener('click', function() {
        sortServices(true);
        this.blur();
    });

    document.getElementById('sortDesc').addEventListener('click', function() {
        sortServices(false);
        this.blur();
    });

    function sortServices(isAscending) {
        const services = [...document.querySelectorAll('.card')];
        services.sort((a, b) => {
            const priceA = parseFloat(a.querySelector('.card-text').textContent.replace(' ₽', '').replace('от', '').replace(/\s/g, ''));
            const priceB = parseFloat(b.querySelector('.card-text').textContent.replace(' ₽', '').replace('от', '').replace(/\s/g, ''));
            return isAscending ? priceA - priceB : priceB - priceA;
        });

        const container = document.querySelector('.row');
        services.forEach(service => container.appendChild(service));
    }
});
