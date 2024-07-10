import { normalizeNumbers } from './normalizeNumber.js';

export function filterCards(search_input_id, card_class_name) {
    const input = document.getElementById(search_input_id)
    const filter = normalizeNumbers(input.value.toLowerCase(), true);
    const cards = document.getElementsByClassName(card_class_name)

    Array.from(cards).forEach(card => {
        const text = card.getAttribute('data-search').toLowerCase();
        card.style.display = text.includes(filter) ? '' : 'none';
    });
}

export function clearSearch(search_input_id, card_class_name) {
    const input = document.getElementById(search_input_id)
    input.value = '';
    filterCards(search_input_id, card_class_name);
}