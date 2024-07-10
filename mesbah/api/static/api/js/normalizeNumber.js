// Normalizer Number
export function normalizeNumbers(str, toFarsi = false) {
    const persianNumbers = '۰۱۲۳۴۵۶۷۸۹';
    const englishNumbers = '0123456789'
    const arabicNumbers = '٠١٢٣٤٥٦٧٨٩';

    if (toFarsi) {
        return str.split('').map(char => {
            if (englishNumbers.indexOf(char) !== -1) {
                return persianNumbers[englishNumbers.indexOf(char)];
            } else if (arabicNumbers.indexOf(char) !== -1) {
                return persianNumbers[arabicNumbers.indexOf(char)];
            } else {
                return char;
            }
        }).join('');
    }

    return str.split('').map(char => {
        if (persianNumbers.indexOf(char) !== -1) {
            return persianNumbers.indexOf(char);
        } else if (arabicNumbers.indexOf(char) !== -1) {
            return arabicNumbers.indexOf(char);
        } else {
            return char;
        }
    }).join('');
}
