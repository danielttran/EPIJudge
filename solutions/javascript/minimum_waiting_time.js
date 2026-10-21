function minimumTotalWaitingTime(service_times) {
  let waiting = 0,
    elapsed = 0;
  for (const duration of service_times.slice().sort((a, b) => a - b)) {
    waiting += elapsed;
    elapsed += duration;
  }
  return waiting;
}

module.exports = { minimumTotalWaitingTime };
