#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <numeric>
class Country {std::string name,continent;int population;public:Country(std::string name,std::string continent,int population):name(std::move(name)),continent(std::move(continent)),population(population){}const std::string& GetName()const{return name;}const std::string& GetContinent()const{return continent;}int GetPopulation()const{return population;}};
class Solution {
 public:
  int PopulationByContinent(const std::vector<Country>& countries, const std::string& continent) {
    return std::accumulate(
        countries.begin(), countries.end(), 0, [&continent](int total, const Country& country) {
          return total + (country.GetContinent() == continent ? country.GetPopulation() : 0);
        });
  }
};
