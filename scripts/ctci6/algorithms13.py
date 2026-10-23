"""Independently authored functional aggregation in each supported language."""
def body(ref,language):
    if ref!='13.7':raise ValueError(ref)
    return {
'csharp':'return countries.Where(country => country.GetContinent() == continent).Sum(country => country.GetPopulation());',
'java':'return Arrays.stream(countries).filter(country -> country.GetContinent().equals(continent)).mapToInt(country -> country.GetPopulation()).sum();',
'cpp':'return std::accumulate(countries.begin(),countries.end(),0,[&continent](int total,const Country& country){return total+(country.GetContinent()==continent?country.GetPopulation():0);});',
'python':'return sum(map(lambda country: country.GetPopulation(), filter(lambda country: country.GetContinent() == continent, countries)))',
'javascript':'return countries.filter(country => country.GetContinent() === continent).reduce((total,country) => total + country.GetPopulation(),0);'}[language]

_previous_body=body
def body(ref,language):
    if ref!='13.8':return _previous_body(ref,language)
    return {
'csharp':'return values.Where(value => coins.Next()).ToArray();',
'java':'return Arrays.stream(values).filter(value -> coins.Next()).toArray();',
'cpp':'std::vector<int> selected;std::copy_if(values.begin(),values.end(),std::back_inserter(selected),[&coins](int value){return coins.Next();});return selected;',
'python':'return list(filter(lambda value: coins.Next(), values))',
'javascript':'return values.filter(value => coins.Next());'}[language]
