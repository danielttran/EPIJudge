#include <cmath>
#include <cstdint>
#include <random>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

#include "test_framework/generic_test.h"
#include "test_framework/random_sequence_checker.h"
#include "test_framework/timed_executor.h"

// Original EPI Practice sampler: rejection over independent fair-bit codes.
int ZeroOneRandom() {
  static thread_local std::mt19937_64 engine(std::random_device{}());
  return std::uniform_int_distribution<int>(0, 1)(engine);
}
std::uint64_t UniformOutcomeCount(int lower, int upper) {
  if (lower > upper)
    throw std::invalid_argument("Lower bound exceeds upper bound");
  return static_cast<std::uint64_t>(static_cast<std::int64_t>(upper) - lower) +
         1;
}
int UniformRandom(int lower_bound, int upper_bound) {
  std::uint64_t outcomes = UniformOutcomeCount(lower_bound, upper_bound);
  unsigned bits = 0;
  for (std::uint64_t remaining = outcomes - 1; remaining; remaining >>= 1)
    ++bits;
  std::uint64_t candidate;
  do {
    candidate = 0;
    for (unsigned bit = 0; bit < bits; ++bit)
      candidate = (candidate << 1) | static_cast<unsigned>(ZeroOneRandom());
  } while (candidate >= outcomes);
  return static_cast<int>(static_cast<std::int64_t>(lower_bound) +
                          static_cast<std::int64_t>(candidate));
}

// Count repeated windows in expected linear time. As in the original predicate,
// starts are 0..N-width-1: the final possible window is deliberately excluded.
std::size_t CountRepeatedUniformWindows(
    const std::vector<std::uint64_t>& sequence, std::size_t width) {
  if (width == 0 || width >= sequence.size()) return 0;
  std::unordered_map<std::uint64_t, std::size_t> frequencies;
  frequencies.reserve(width);
  std::size_t duplicate_keys = 0;
  auto add = [&](std::uint64_t value) {
    auto& count = frequencies[value];
    if (count == 1) ++duplicate_keys;
    ++count;
  };
  for (std::size_t i = 0; i < width; ++i) add(sequence[i]);
  const std::size_t checked_windows = sequence.size() - width;
  std::size_t repeated = 0;
  for (std::size_t start = 0; start < checked_windows; ++start) {
    if (duplicate_keys != 0) ++repeated;
    if (start + 1 == checked_windows) break;
    auto outgoing = frequencies.find(sequence[start]);
    if (outgoing->second == 2) --duplicate_keys;
    if (--outgoing->second == 0) frequencies.erase(outgoing);
    add(sequence[start + width]);
  }
  return repeated;
}
bool CheckUniformBirthdaySpacings(const std::vector<std::uint64_t>& sequence,
                                  std::uint64_t outcomes) {
  if (outcomes == 0 || outcomes > (std::uint64_t{1} << 32)) return false;
  std::size_t width = static_cast<std::size_t>(std::ceil(
      std::sqrt(std::log(2.0) * 2.0 * static_cast<double>(outcomes))));
  if (width > sequence.size()) return true;
  std::size_t possible_windows = sequence.size() - width + 1;
  if (possible_windows < 1000) return true;
  return 0.4 * static_cast<double>(possible_windows) <=
         static_cast<double>(CountRepeatedUniformWindows(sequence, width));
}
bool UniformBinsAreInformative(double bins, std::size_t count) {
  double probability = 1.0 / bins;
  return count * probability >= 50 && count * (1.0 - probability) >= 50;
}
bool CheckUniformSequence(const std::vector<std::uint64_t>& sequence,
                          std::uint64_t outcomes) {
  if (outcomes == 0 || outcomes > (std::uint64_t{1} << 32)) return false;
  for (std::uint64_t value : sequence)
    if (value >= outcomes) return false;
  // Each production trial has exactly 100000 samples. Apply the unchanged
  // expected-count/complement threshold before narrowing or encoding bins;
  // every informative marginal, pair or triple then has at most 2000 bins.
  if (UniformBinsAreInformative(static_cast<double>(outcomes),
                                sequence.size())) {
    std::vector<int> narrow;
    narrow.reserve(sequence.size());
    for (std::uint64_t value : sequence)
      narrow.push_back(static_cast<int>(value));
    int alphabet = static_cast<int>(outcomes);
    using namespace test_framework::random_sequence_checker;
    if (!CheckFrequencies(narrow, alphabet, 0.01)) return false;
    double pair_bins = static_cast<double>(outcomes) * outcomes;
    if (sequence.size() > 0 &&
        UniformBinsAreInformative(pair_bins, sequence.size() - 1) &&
        !CheckPairsFrequencies(narrow, alphabet, 0.01))
      return false;
    double triple_bins = pair_bins * outcomes;
    if (sequence.size() > 1 &&
        UniformBinsAreInformative(triple_bins, sequence.size() - 2) &&
        !CheckTriplesFrequencies(narrow, alphabet, 0.01))
      return false;
  }
  return CheckUniformBirthdaySpacings(sequence, outcomes);
}

template <typename Draw>
bool CollectUniformTrial(TimedExecutor& executor, int lower, int upper,
                         Draw draw) {
  std::uint64_t outcomes = UniformOutcomeCount(lower, upper);
  std::vector<std::uint64_t> offsets;
  offsets.reserve(100000);
  bool in_range = true;
  executor.Run([&] {
    for (int sample = 0; sample < 100000; ++sample) {
      int value = draw();
      if (value < lower || value > upper) in_range = false;
      offsets.push_back(
          static_cast<std::uint64_t>(static_cast<std::int64_t>(value) - lower));
    }
  });
  return in_range && CheckUniformSequence(offsets, outcomes);
}
void VerifyUniformDraw(TimedExecutor& executor, int lower_bound,
                       int upper_bound) {
  UniformOutcomeCount(lower_bound, upper_bound);
  auto trial = [&] {
    return CollectUniformTrial(executor, lower_bound, upper_bound, [&] {
      return UniformRandom(lower_bound, upper_bound);
    });
  };
  test_framework::RunFuncWithRetries(
      trial);  // Unchanged five complete attempts.
}
int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"executor", "lower_bound", "upper_bound"};
  return GenericTestMain(arguments, "uniform_random_number.cc",
                         "uniform_random_number.tsv", &VerifyUniformDraw,
                         DefaultComparator{}, parameters);
}
