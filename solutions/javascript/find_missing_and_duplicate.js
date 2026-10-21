function findDuplicateMissing(A) {
  const seen = Array(A.length).fill(false);
  let duplicate = -1;
  for (const value of A) {
    if (seen[value]) duplicate = value;
    seen[value] = true;
  }
  for (let value = 0; value < seen.length; value++)
    if (!seen[value]) return [duplicate, value];
  throw new RangeError("One duplicate and missing value required");
}

module.exports = { findDuplicateMissing };
