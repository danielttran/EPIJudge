'use strict';
function EnglishInteger(value) {
  if (value === 0) return "Zero";
  const small = [
      "Zero",
      "One",
      "Two",
      "Three",
      "Four",
      "Five",
      "Six",
      "Seven",
      "Eight",
      "Nine",
      "Ten",
      "Eleven",
      "Twelve",
      "Thirteen",
      "Fourteen",
      "Fifteen",
      "Sixteen",
      "Seventeen",
      "Eighteen",
      "Nineteen",
    ],
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"],
    scales = ["", "Thousand", "Million", "Billion"],
    groups = [];
  let magnitude = Math.abs(value),
    scale = 0;
  while (magnitude > 0) {
    let chunk = magnitude % 1000;
    if (chunk !== 0) {
      const words = [];
      if (chunk >= 100) {
        words.push(small[Math.floor(chunk / 100)], "Hundred");
        chunk %= 100;
      }
      if (chunk >= 20) {
        words.push(tens[Math.floor(chunk / 10)]);
        chunk %= 10;
      }
      if (chunk !== 0) words.push(small[chunk]);
      if (scale !== 0) words.push(scales[scale]);
      groups.push(words.join(" "));
    }
    magnitude = Math.floor(magnitude / 1000);
    ++scale;
  }
  return (value < 0 ? "Negative " : "") + groups.reverse().join(" ");
}
