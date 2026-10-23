class Country:
    def __init__(self,name: str,continent: str,population: int):
        self.__name,self.__continent,self.__population=name,continent,population
    def GetName(self) -> str:
        return self.__name
    def GetContinent(self) -> str:
        return self.__continent
    def GetPopulation(self) -> int:
        return self.__population
def PopulationByContinent(countries: list[Country], continent: str) -> int:
    return sum(
        map(
            lambda country: country.GetPopulation(),
            filter(lambda country: country.GetContinent() == continent, countries),
        )
    )
