function findAmpleCity(gallons, distances) {
  let start = 0,
    tank = 0;
  for (let city = 0; city < gallons.length; city++) {
    tank += 20 * gallons[city] - distances[city];
    if (tank < 0) {
      start = city + 1;
      tank = 0;
    }
  }
  return start % gallons.length;
}

module.exports = { findAmpleCity };
