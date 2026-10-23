'use strict';
class SyncContext {Wait(gate){throw new Error('Provided synchronization primitive');}Signal(gate){throw new Error('Provided synchronization primitive');}Work(){throw new Error('Provided worker callback');}}
function RunOrdered(role, context) {
  if (role > 0) context.Wait(role - 1);
  context.Work();
  if (role < 2) context.Signal(role);
}

module.exports = {SyncContext,RunOrdered};
