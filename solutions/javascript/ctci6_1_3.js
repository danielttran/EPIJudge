'use strict';
function Urlify(buffer, trueLength) {
  let write = buffer.length - 1;
  for (let read = trueLength - 1; read >= 0; --read) {
    const current = buffer[read];
    if (current === " ") {
      buffer[write--] = "0";
      buffer[write--] = "2";
      buffer[write--] = "%";
    } else {
      buffer[write--] = current;
    }
  }
}

module.exports = {Urlify};
