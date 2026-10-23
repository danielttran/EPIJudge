'use strict';
class FizzContext {Wait(gate){throw new Error('Provided synchronization primitive');}Signal(gate){throw new Error('Provided synchronization primitive');}Print(value){throw new Error('Provided role-bound print callback');}}
function RunFizzBuzz(role, limit, context) {
  const owner = (value) => (value % 15 === 0 ? 3 : value % 3 === 0 ? 1 : value % 5 === 0 ? 2 : 0);
  for (let value = 1; value <= limit; ++value) {
    if (owner(value) !== role) continue;
    context.Wait(role);
    context.Print(value);
    if (value < limit) context.Signal(owner(value + 1));
  }
}
