using System;
using System.Collections.Generic;
using System.Text;
public sealed class Country {private readonly string name,continent;private readonly int population;public Country(string name,string continent,int population){this.name=name;this.continent=continent;this.population=population;}public string GetName()=>name;public string GetContinent()=>continent;public int GetPopulation()=>population;}
public class Solution
{
    public int PopulationByContinent(Country[] countries, string continent)
    {
        return countries.Where(country => country.GetContinent() == continent)
            .Sum(country => country.GetPopulation());
    }
}
