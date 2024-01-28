from enum import Enum
from itertools import combinations
import re

class Skema(Enum):
    MANDAG_UGENTLIG = 'Mandag, ugentlig'
    MANDAG_LIGE = 'Mandag, lige uger'
    MANDAG_ULIGE = 'Mandag, ulige uger'
    TORSDAG_UGENTLIG = 'Torsdag, ugentlig'
    TORSDAG_LIGE = 'Torsdag, lige uger'
    TORSDAG_ULIGE = 'Torsdag, ulige uger'
    MANDAG_TORSDAG = 'Mandag og torsdag, ugentlig'

    @classmethod
    def from_string(cls, string):
        try:
            return getattr(cls, string.upper()).value
        except AttributeError:
            return None
    @classmethod
    def is_member(cls, string):
        return string.upper() in cls.__members__
    
    @classmethod
    def options(cls):
        return list(cls.__members__.keys())
    
    @classmethod
    def combinations(cls):
        return list(combinations(cls.__members__.keys(), 2))
    
    @classmethod
    def components(cls):
        '''split string on underscore'''
        '''return unique list of components'''
        components = [ option.split('_') for option in cls.options() ]
        components = [ item.lower() for sublist in components for item in sublist ]
        return list(dict.fromkeys(components))
    
    
    @classmethod
    def components2(cls, string):
        '''split string on underscore'''
        '''return unique list of components'''
        if not isinstance(string, str):
            raise TypeError('string must be of type str')
        '''if string does not contain underscore, raise ValueError'''
        if '_' not in string:
            raise ValueError('string must contain underscore')
        '''if string does not contain exactly one underscore, raise ValueError'''
        if string.count('_') != 1:
            raise ValueError('string must contain exactly one underscore')
        
        
        if cls.is_member(string):
            return string.split('_')
        else:
            return None

def find_dag_uge(tur: str):
    '''use members of Skema to create a list of strings'''

    #dag_uge_list = [str(x).lower() for x in Skema]
    #dag_uge_list = [x.split('_') for x in dag_uge_list]
    #dag_uge_list = [item for sublist in dag_uge_list for item in sublist]

    #dag_uge = 'mandag, torsdag, ugentlig, lige, ulige'.split(', ')
    ##dag_uge = [ str(x).lower() for y in Skema for x in y.name.split('_')]
    #myskemab = list(dict.fromkeys(myskema))

    # List of lists
    ##dag_uge = [ option.split('_') for option in Skema.options() ]
    # Flatten list
    ##dag_uge = [ item for sublist in dag_uge for item in sublist ]
    # Remove duplicates
    ##dag_uge_list = list(dict.fromkeys(dag_uge))

    dag_uge_list = Skema.components()
    # dag_uge = [x.name.lower() for x in Skema]
    # dag_uge = [x.split('_') for x in dag_uge]
    # dag_uge = [item for sublist in dag_uge for item in sublist]
    # dag_uge_list = list(dict.fromkeys(dag_uge))
    # '''use list dag_uge to create a regex pattern'''
    dag_uge_pattern = re.compile(rf'{"|".join(dag_uge_list)}', re.IGNORECASE)

    if dag_uge_pattern.findall(tur):
        #nyskema = '_'.join(dag_uge_pattern.findall(tur)).upper()
        nyskema = '_'.join(dag_uge_pattern.findall(tur))

        #return getattr(Skema, nyskema).value
        #return Skema.from_string(nyskema)

        if Skema.is_member(nyskema):
            #return Skema.from_string(nyskema)
            return nyskema

def extract_street_city_country3(df):
    """Extract the street, city and country from column 'adresse'

    Args:
        df (pd.DataFrame): The dataframe to extract from
    Returns:
        pd.DataFrame: The dataframe with the new columns
    """
    for index, row in df.iterrows():
        adresse = row['adresse'].split(',')

        df.loc[index, 'street'] = adresse[0]
        df.loc[index, 'city'] = adresse[1]
        df.loc[index, 'country'] = adresse[2]
    return df

def extract_house_number(df):
    '''split the street column on the first occurence of a space and a number'''
    df[['street_part', 'house_number', 'house_anyting']] = df['street'].str.split(r' (\d+)', n=1,expand=True)
    '''remove duplicates'''
    #df.drop_duplicates(inplace=True)
    '''sort the values in the street column'''
    df.sort_values(by=['street_part', 'house_number'], ascending=True, inplace=True)
    '''reset the index'''
    df.reset_index(drop=True, inplace=True)
    '''join the street and house_number columns'''
    #df['street'] = df['street'].str.cat(df['house_number'], sep=" ")
    '''drop the house_number column'''
    #df.drop(columns=['house_number'], inplace=True)
    '''return the dataframe'''
    return df

    
if __name__ == '__main__':
    '''iterate over items in class Skema'''
    #myskema = [ str(x).lower() for y in Skema for x in y.name.split('_')]
    '''in list myskema remove duplicates'''
    #myskemab = list(dict.fromkeys(myskema))
    #print(myskemab)

    #print(find_dag_uge('mandag, ulige'))

    print(Skema.options())
    tur = 'mandag, ugentlig'
    daguge = find_dag_uge(tur)
    print(Skema.from_string(daguge))
    print(Skema.from_string('mandag_ugentlig'))
    print(Skema.components2(daguge))
    

