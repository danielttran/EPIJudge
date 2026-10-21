#include <cstdint>
#include <stdexcept>
#include <string>
#include <vector>

#include "test_framework/generic_test.h"

// Original EPI Practice decoder: native strings arrive as UTF-8, while the
// published C# index contract counts UTF-16 code units, including surrogate
// pairs.
namespace {
std::u16string Utf16Units(const std::string& bytes) {
  std::u16string result;
  for (std::size_t index = 0; index < bytes.size();) {
    std::uint32_t first = static_cast<unsigned char>(bytes[index++]);
    std::uint32_t value = first, minimum = 0;
    unsigned continuations = 0;
    if (first < 0x80) {
    } else if ((first & 0xe0) == 0xc0) {
      value = first & 0x1f;
      continuations = 1;
      minimum = 0x80;
    } else if ((first & 0xf0) == 0xe0) {
      value = first & 0x0f;
      continuations = 2;
      minimum = 0x800;
    } else if ((first & 0xf8) == 0xf0) {
      value = first & 0x07;
      continuations = 3;
      minimum = 0x10000;
    } else
      throw std::invalid_argument("Invalid UTF-8 leading byte");
    for (unsigned next = 0; next < continuations; ++next) {
      if (index == bytes.size())
        throw std::invalid_argument("Truncated UTF-8 sequence");
      auto byte = static_cast<unsigned char>(bytes[index++]);
      if ((byte & 0xc0) != 0x80)
        throw std::invalid_argument("Invalid UTF-8 continuation");
      value = (value << 6) | (byte & 0x3f);
    }
    if (value < minimum || value > 0x10ffff ||
        (value >= 0xd800 && value <= 0xdfff))
      throw std::invalid_argument("Invalid Unicode scalar value");
    if (value < 0x10000)
      result.push_back(static_cast<char16_t>(value));
    else {
      value -= 0x10000;
      result.push_back(static_cast<char16_t>(0xd800 + (value >> 10)));
      result.push_back(static_cast<char16_t>(0xdc00 + (value & 0x3ff)));
    }
  }
  return result;
}
}  // namespace
// Keep the published method name; use an independently authored KMP search.
int RabinKarp(const std::string& t, const std::string& s) {
  auto text = Utf16Units(t), pattern = Utf16Units(s);
  if (pattern.empty()) return 0;
  std::vector<std::size_t> prefix(pattern.size());
  for (std::size_t i = 1, matched = 0; i < pattern.size(); ++i) {
    while (matched && pattern[i] != pattern[matched])
      matched = prefix[matched - 1];
    if (pattern[i] == pattern[matched]) ++matched;
    prefix[i] = matched;
  }
  for (std::size_t i = 0, matched = 0; i < text.size(); ++i) {
    while (matched && text[i] != pattern[matched])
      matched = prefix[matched - 1];
    if (text[i] == pattern[matched]) ++matched;
    if (matched == pattern.size())
      return static_cast<int>(i + 1 - pattern.size());
  }
  return -1;
}
int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"t", "s"};
  return GenericTestMain(arguments, "substring_match.cc", "substring_match.tsv",
                         &RabinKarp, DefaultComparator{}, parameters);
}
