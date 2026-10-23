'use strict';
function DivingBoardLengths(planks, shorter, longer) {
  if (shorter === longer) return [planks * shorter];
  return Array.from(
    { length: planks + 1 },
    (_, count) => planks * shorter + count * (longer - shorter),
  );
}
