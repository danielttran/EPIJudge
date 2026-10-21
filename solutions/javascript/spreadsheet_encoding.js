function ssDecodeColId(col) {
  let value = 0;
  for (let i = 0; i < col.length; i++)
    value = value * 26 + col.charCodeAt(i) - 64;
  return value;
}

module.exports = { ssDecodeColId };
