'use strict';
function IsRotation(first, second) {
  if (first.length === 0 || first.length !== second.length) return false;
  return (first + first).includes(second);
}
