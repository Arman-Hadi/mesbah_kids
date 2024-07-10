import { normalizeNumbers } from './normalizeNumber.js';

export function filterCards(search_input_id, cards) {
    const input = document.getElementById(search_input_id)
    const filter = normalizeNumbers(input.value.toLowerCase(), true);
    console.log(filter)

    Array.from(cards).forEach(card => {
        const text = card.getAttribute('data-search').toLowerCase();
        card.style.display = text.includes(filter) ? '' : 'none';
    });
}

export function clearSearch(search_input_id, cards) {
    const input = document.getElementById(search_input_id)
    input.value = '';
    filterCards(search_input_id, cards);
}