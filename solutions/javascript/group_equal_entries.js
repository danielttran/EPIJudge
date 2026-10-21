function groupByAge(people) {
  const groups = new Map();
  for (const person of people) {
    if (!groups.has(person[0])) groups.set(person[0], []);
    groups.get(person[0]).push(person);
  }
  let index = 0;
  for (const group of groups.values())
    for (const person of group) people[index++] = person;
}

module.exports = { groupByAge };
