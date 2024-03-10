from enum import Enum
from itertools import combinations
import re
from datetime import datetime, timedelta
import logging
import functools

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)


class Frekvens(Enum):
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
    
    


class Lige_Ulige(Enum):
    LIGE = 1
    ULIGE = 0

    '''return None if the string is not a valid OddEven'''
    @classmethod
    def from_string(cls, string):
        try:
            return getattr(cls, string.upper()).value
        except AttributeError:
            return None
            #raise AttributeError(f'Argument must be either {cls.options()}')
            raise AttributeError(f'AttributeError {string} is not a valid OddEven')

    
    def __str__(self):
        return self.name.lower()
   
    @classmethod
    def options(cls):
        return [ item.name.lower() for item in cls]
    
    '''is string a member of OddEven'''
    @classmethod
    def is_member(cls, string):
        return string.upper() in cls.__members__
    


class Weekday(Enum):
    MANDAG = 0
    TIRSDAG = 1
    ONSDAG = 2
    TORSDAG = 3
    FREDAG = 4
    LØRDAG = 5
    SØNDAG = 6
    
    @classmethod
    def from_string(cls, string):
        try:
            return getattr(cls, string.upper()).value
        except AttributeError:
            #return None
            raise AttributeError(f'AttributeError "{string}" is not a valid Weekday')
    
    @classmethod
    def is_member(cls, string):
        return string.upper() in cls.__members__
    
    @classmethod
    def get_name_from_value(cls, value):
        for name, member in cls.__members__.items():
            if member.value == value:
                return name.lower()
        return None

# Helper functions

def weekday_to_int(weekday):
    if weekday == 'mandag':
        return 0
    elif weekday == 'tirsdag':
        return 1
    elif weekday == 'onsdag':
        return 2
    elif weekday == 'torsdag':
        return 3
    elif weekday == 'fredag':
        return 4
    elif weekday == 'lørdag':
        return 5
    elif weekday == 'søndag':
        return 6
    else:
        return -1


def find_mønster(tur: str):
    mønster = 'mandag, torsdag, ugentlig, lige, ulige'.split(', ')
    mønster = re.compile(rf'{"|".join(mønster)}', re.IGNORECASE)

    if mønster.findall(tur):
        return mønster.findall(tur)
    else:
        raise ValueError(f"Illegal input {tur}. Must be one of {mønster}.")


def find_frekvens(tur: str):
    
    dag_uge = find_mønster(tur)
    dag_uge = '_'.join(dag_uge)
    if Frekvens.is_member(dag_uge):
        return Frekvens.from_string(dag_uge)
    else:
        raise ValueError(f"Illegal input {dag_uge}. Must be one of {Frekvens.options()}.")


def næste_ugedag(weekdays: list, week_odd_even = None):
    '''
    Find next weekday
    
    Args:
        weekdays (list): list of weekdays as strings, e.g. ['thursday', 'friday']
        week_odd_even (int, optional): 1 for odd weeks, 0 for even weeks.
        Defaults to none.

    Returns:
        tuple: tuple of next weekdays

    '''
    if not weekdays:
        return()
    
    else:
        weekday = weekday_to_int(weekdays[0])
        current_date = datetime.now()
        days_until_next_weekday = (weekday- current_date.weekday() + 7) % 7
        next_weekday = current_date + timedelta(days=days_until_next_weekday)
        while next_weekday.isocalendar()[1] % 2 == week_odd_even:
            next_weekday += timedelta(weeks=1)
        return (next_weekday.date(),) + (næste_ugedag(weekdays[1:], week_odd_even))
    


def format_date(date:list):

        førstkommende = min(date)
        førstkommende_weekday_number = førstkommende.weekday()
        førstkommende_weekday_name = Weekday.get_name_from_value(førstkommende_weekday_number).title()
        return (førstkommende_weekday_name, førstkommende.strftime("%d-%m"))


def næste_tømningsdag(tur: str):
    
    resultat = find_mønster(tur)
    weekday = resultat[0]
    frequency = resultat[1]
    if Lige_Ulige.is_member(frequency):
        resultat.pop(1)
    
    try:
        weekday_value = Weekday.from_string(weekday)

    except AttributeError as e:
        print(f'AttributeError {e}')

    try:
        frequency_value = Lige_Ulige.from_string(frequency)

    except AttributeError as e:
        print(f'AttributeError {e}')
    
    

    uge_dag = næste_ugedag(resultat, frequency_value)
    return format_date(uge_dag)
    
    






