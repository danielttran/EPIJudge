'use strict';
class Country {#name;#continent;#population;constructor(name,continent,population){this.#name=name;this.#continent=continent;this.#population=population;}GetName(){return this.#name;}GetContinent(){return this.#continent;}GetPopulation(){return this.#population;}}
function PopulationByContinent(countries, continent) {
  return countries
    .filter((country) => country.GetContinent() === continent)
    .reduce((total, country) => total + country.GetPopulation(), 0);
}
