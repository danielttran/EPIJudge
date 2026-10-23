'use strict';
class ForkContext {Take(fork){throw new Error('Provided fork lock');}Drop(fork){throw new Error('Provided fork lock');}Eat(){throw new Error('Provided eating callback');}}
function Dine(role, philosophers, bites, context) {
  const left = role,
    right = (role + 1) % philosophers,
    lower = Math.min(left, right),
    higher = Math.max(left, right);
  for (let bite = 0; bite < bites; ++bite) {
    context.Take(lower);
    context.Take(higher);
    context.Eat();
    context.Drop(higher);
    context.Drop(lower);
  }
}
