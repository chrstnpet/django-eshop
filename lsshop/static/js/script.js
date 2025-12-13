document.addEventListener("DOMContentLoaded", function () {
    const imageElement = document.getElementById("main-product-image");
    const colors = document.querySelectorAll("input[name='color']");

    colors.forEach(input => {
        input.addEventListener("change", function () {
            const front = this.dataset.image;
            const back = this.dataset.back;

            if (front) {
                imageElement.src = front;
                imageElement.dataset.front = front;
            }

            if (back) {
                imageElement.dataset.back = back;
            } else {
                imageElement.dataset.back = ""; // no back image exists
            }

            document.querySelectorAll(".color-option").forEach(btn =>
                btn.classList.remove("active")
            );
            this.closest(".color-option").classList.add("active");
        });
    });

    imageElement.addEventListener("mouseenter", function () {
        const backImg = imageElement.dataset.back;
        if (backImg) {
            imageElement.src = backImg;
        }
    });

    imageElement.addEventListener("mouseleave", function () {
        const frontImg = imageElement.dataset.front;
        if (frontImg) {
            imageElement.src = frontImg;
        }
    });
});