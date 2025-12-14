document.addEventListener("DOMContentLoaded", function () {
    const imageElement = document.getElementById("main-product-image");
    const colors = document.querySelectorAll("input[name='color']");
    const sizeGroups = document.querySelectorAll(".size-group");

    colors.forEach(input => {
        input.addEventListener("change", function () {
            const colorId = this.value;

            sizeGroups.forEach(group => {
                group.classList.toggle(
                    "d-none",
                    group.dataset.colorId !== colorId
                );
            });
        });
    });


    // ----------------------------
    // Color Change
    colors.forEach(input => {
        input.addEventListener("change", function () {
            const front = this.dataset.image;
            const back = this.dataset.back;
            const colorId = this.value;

            // Update image
            if (front) {
                imageElement.src = front;
                imageElement.dataset.front = front;
            }
            imageElement.dataset.back = back || "";

            // Active state
            document.querySelectorAll(".color-option").forEach(btn =>
                btn.classList.remove("active")
            );
            this.closest(".color-option").classList.add("active");
        });
    });

    // ----------------------------
    // Image Hover
    imageElement.addEventListener("mouseenter", function () {
        if (imageElement.dataset.back) {
            imageElement.src = imageElement.dataset.back;
        }
    });

    imageElement.addEventListener("mouseleave", function () {
        imageElement.src = imageElement.dataset.front;
    });

    // ----------------------------
    // Add to Cart form
    const addToCartForm = document.getElementById("add-to-cart-form");
    const selectedSizeInput = document.getElementById("selected-size-variant");

    if (addToCartForm) {
        addToCartForm.addEventListener("submit", function (e) {
            e.preventDefault(); // prevent default to validate selection

            // get selected size radio
            const selectedSize = document.querySelector("input[name='size']:checked");

            if (!selectedSize) {
                alert("Please select a size");
                return;
            }

            // set hidden input value
            selectedSizeInput.value = selectedSize.value;

            // update form action dynamically
            addToCartForm.action = `/cart/add/${selectedSize.value}/`;

            // submit the form
            addToCartForm.submit();
        });
    }
});
