'use strict';
class NumberFile {ReadNext(){throw new Error("Provided by the judge");}Reset(){throw new Error("Provided by the judge");}}
function FindMissingInt(file, smallMemory) {
  let block = 0;
  if (smallMemory) {
    const counts = new Uint32Array(2048);
    for (let value; (value = file.ReadNext()) !== -1; ) ++counts[value >>> 20];
    while (counts[block] === 1 << 20) ++block;
    file.Reset();
  }
  const bitmap = new Uint8Array(smallMemory ? 1 << 17 : 1 << 28);
  for (let value; (value = file.ReadNext()) !== -1; )
    if (!smallMemory || value >>> 20 === block) {
      const offset = smallMemory ? value & ((1 << 20) - 1) : value;
      bitmap[offset >>> 3] |= 1 << (offset & 7);
    }
  for (let index = 0; index < bitmap.length; ++index)
    if (bitmap[index] !== 255)
      for (let bit = 0; bit < 8; ++bit)
        if ((bitmap[index] & (1 << bit)) === 0) return block * 1048576 + index * 8 + bit;
  return -1;
}
