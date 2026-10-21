function isLetterConstructibleFromMagazine(letter_text, magazine_text) {
  const needed = new Map();
  for (let i = 0; i < letter_text.length; i++) {
    const c = letter_text[i];
    needed.set(c, (needed.get(c) || 0) + 1);
  }
  let remaining = letter_text.length;
  for (let i = 0; i < magazine_text.length; i++) {
    const c = magazine_text[i],
      count = needed.get(c) || 0;
    if (count > 0) {
      needed.set(c, count - 1);
      remaining--;
    }
  }
  return remaining === 0;
}

module.exports = { isLetterConstructibleFromMagazine };
