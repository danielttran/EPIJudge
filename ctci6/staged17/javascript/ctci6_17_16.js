'use strict';
function MaximumMassageMinutes(appointments) {
  let oneBack = 0,
    twoBack = 0;
  for (const duration of appointments) {
    const current = Math.max(oneBack, duration + twoBack);
    twoBack = oneBack;
    oneBack = current;
  }
  return oneBack;
}
