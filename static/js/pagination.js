document.addEventListener("DOMContentLoaded", function () {
    const cardsWrapper = document.querySelector(".volunteer-cards-wrapper");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    let currentIndex = 0;
    const cardsPerPage = 3;
    const totalCards = document.querySelectorAll(".volunteer-cards-wrapper .custom-block-wrap").length;

    function updateView() {
        const cards = document.querySelectorAll(".volunteer-cards-wrapper .custom-block-wrap");
        cards.forEach((card, index) => {
            card.style.display = index >= currentIndex && index < currentIndex + cardsPerPage ? "block" : "none";
        });
        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex + cardsPerPage >= totalCards;
    }

    prevBtn.addEventListener("click", function () {
        if (currentIndex > 0) {
            currentIndex -= cardsPerPage;
            updateView();
        }
    });

    nextBtn.addEventListener("click", function () {
        if (currentIndex + cardsPerPage < totalCards) {
            currentIndex += cardsPerPage;
            updateView();
        }
    });

    updateView();
});
