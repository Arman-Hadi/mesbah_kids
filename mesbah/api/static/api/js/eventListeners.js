import { filterCards } from "./searchCards.js";
import { clearSearch } from "./searchCards.js";


document.addEventListener('DOMContentLoaded', function () {
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function () {
            const cards = document.getElementsByClassName("card")
            filterCards("search_input", cards);
        });
    });

    const clearButtons = document.querySelectorAll('.clear-btn');
    clearButtons.forEach(button => {
        button.addEventListener('click', function () {
            const cards = document.getElementsByClassName("card")
            clearSearch("search_input", cards);
        });
    });
});
