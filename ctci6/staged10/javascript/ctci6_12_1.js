'use strict';
function LastKLines(filePath, k) {
  const tailFs = require("node:fs");
  const descriptor = tailFs.openSync(filePath, "r");
  const chunk = Buffer.alloc(4096),
    ring = new Array(k);
  let used = 0,
    next = 0,
    current = "";
  try {
    for (;;) {
      const count = tailFs.readSync(descriptor, chunk, 0, chunk.length, null);
      if (count === 0) break;
      for (let i = 0; i < count; ++i) {
        if (chunk[i] === 10) {
          ring[next] = current;
          next = (next + 1) % k;
          used = Math.min(used + 1, k);
          current = "";
        } else current += String.fromCharCode(chunk[i]);
      }
    }
  } finally {
    tailFs.closeSync(descriptor);
  }
  const result = [];
  for (let i = 0; i < used; ++i) result.push(ring[(next - used + k + i) % k]);
  return result;
}
