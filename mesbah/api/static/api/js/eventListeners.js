import { filterCards } from "./searchCards.js";
import { clearSearch } from "./searchCards.js";


document.addEventListener('DOMContentLoaded', function () {
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function () {
            filterCards("search_input", "card");
        });
    });

    const clearButtons = document.querySelectorAll('.clear-btn');
    clearButtons.forEach(button => {
        button.addEventListener('click', function () {
            clearSearch("search_input", "card");
        });
    });
});
