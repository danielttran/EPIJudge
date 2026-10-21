function generatePowerSet(input_set) {
  const result = [[]];
  for (const value of input_set) {
    const count = result.length;
    for (let i = 0; i < count; i++) result.push([...result[i], value]);
  }
  return result;
}

module.exports = { generatePowerSet };
