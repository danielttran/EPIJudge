'use strict';
function MergeSortedIntoFirst(first, realCount, second) {
  let a = realCount - 1,
    b = second.length - 1,
    write = first.length - 1;
  while (b >= 0) {
    if (a >= 0 && first[a] > second[b]) first[write--] = first[a--];
    else first[write--] = second[b--];
  }
  return first;
}
