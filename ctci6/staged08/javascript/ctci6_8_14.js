'use strict';
function CountBooleanParenthesizations(expression, desired) {
  if (expression.length === 0) return 0;
  const count = (expression.length + 1) / 2,
    truth = Array.from({ length: count }, () => Array(count).fill(0)),
    falsity = Array.from({ length: count }, () => Array(count).fill(0));
  for (let i = 0; i < count; ++i) {
    truth[i][i] = expression[2 * i] === "1" ? 1 : 0;
    falsity[i][i] = 1 - truth[i][i];
  }
  for (let length = 2; length <= count; ++length) {
    for (let low = 0; low + length <= count; ++low) {
      const high = low + length - 1;
      for (let split = low; split < high; ++split) {
        const lt = truth[low][split],
          lf = falsity[low][split],
          rt = truth[split + 1][high],
          rf = falsity[split + 1][high],
          total = (lt + lf) * (rt + rf),
          operation = expression[2 * split + 1],
          trueCount =
            operation === "&" ? lt * rt : operation === "|" ? total - lf * rf : lt * rf + lf * rt;
        truth[low][high] += trueCount;
        falsity[low][high] += total - trueCount;
      }
    }
  }
  return desired ? truth[0][count - 1] : falsity[0][count - 1];
}
