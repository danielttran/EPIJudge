import java.util.*;
final class Country {private final String name,continent;private final int population;public Country(String name,String continent,int population){this.name=name;this.continent=continent;this.population=population;}public String GetName(){return name;}public String GetContinent(){return continent;}public int GetPopulation(){return population;}}
class Solution {
  public int PopulationByContinent(Country[] countries, String continent) {
    return Arrays.stream(countries)
        .filter(country -> country.GetContinent().equals(continent))
        .mapToInt(country -> country.GetPopulation())
        .sum();
  }
}
