function findSalaryCap(target_payroll, current_salaries) {
  const salaries = current_salaries.slice().sort((a, b) => a - b);
  let paid = 0;
  for (let i = 0; i < salaries.length; i++) {
    const cap = (target_payroll - paid) / (salaries.length - i);
    if (cap <= salaries[i]) return cap;
    paid += salaries[i];
  }
  return paid === target_payroll && salaries.length ? salaries.at(-1) : -1;
}

module.exports = { findSalaryCap };
