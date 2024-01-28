from enum import Enum
from itertools import combinations
import re
from datetime import datetime, timedelta
import logging
import functools

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)


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

    


class OddEven(Enum):
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

class DagUge(Enum):

    MANDAG = 0
    TIRSDAG = 1
    ONSDAG = 2
    TORSDAG = 3
    FREDAG = 4
    LØRDAG = 5
    SØNDAG = 6
    UGE = 7
    @classmethod
    def from_string(cls, string):
        try:
            return getattr(cls, string.upper()).value
        except AttributeError:
            #return None
            raise AttributeError(f'AttributeError "{string}" is not a valid DagUge')
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

def get_dag_uge(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dag_uge = return_dag_uge(args[0])
        return func(dag_uge, *args[1:], **kwargs)

#def find_dag_uge(tur: str):
    # dag_uge_list = Skema.components()
    # dag_uge_pattern = re.compile(rf'{"|".join(dag_uge_list)}', re.IGNORECASE)

    # if dag_uge_pattern.findall(tur):
    #     dag_uge_str = '_'.join(dag_uge_pattern.findall(tur))

        
    #     if Skema.is_member(dag_uge_str):
    #         #return Skema.from_string(nyskema)
    #         return dag_uge_str

def return_dag_uge(tur: str):
    dag_uge_list = Skema.components()
    dag_uge_pattern = re.compile(rf'{"|".join(dag_uge_list)}', re.IGNORECASE)

    #return tuple(dag_uge_pattern.findall(tur)) if dag_uge_pattern.findall(tur) else None
    if dag_uge_pattern.findall(tur):
        return dag_uge_pattern.findall(tur)
    else:
        raise ValueError('dag_uge_pattern.findall(tur) must not be empty')


def return_skema(tur: str):
    dag_uge = return_dag_uge(tur)
    dag_uge = '_'.join(dag_uge)
    if Skema.is_member(dag_uge):
        return Skema.from_string(dag_uge)
    else:
        raise ValueError('dag_uge must be a member of Skema')

    


def get_next_weekday(weekday, week_odd_even = None):

    '''
    Find next weekday

    Args:
        weekday (str): weekday as string, e.g. 'thursday'
        week_odd_even (int, optional): 1 for odd weeks, 0 for even weeks.
        Defaults to none.
    '''
    weekday_number = weekday_to_int(weekday)
    current_date = datetime.now()
    days_until_next_weekday = (weekday_number - current_date.weekday() + 7) % 7
    next_weekday = current_date + timedelta(days=days_until_next_weekday)
    while next_weekday.isocalendar()[1] % 2 == week_odd_even:
        next_weekday += timedelta(weeks=1)
    return next_weekday.date()

def get_next_weekday2(weekday: list, week_odd_even = None):

    '''
    Find next weekday

    Args:
        weekday (str): weekday as string, e.g. 'thursday'
        week_odd_even (int, optional): 1 for odd weeks, 0 for even weeks.
        Defaults to none.
    '''
    #weekday_number = weekday_to_int(weekday)
    current_date = datetime.now()
    days_until_next_weekday = (weekday- current_date.weekday() + 7) % 7
    next_weekday = current_date + timedelta(days=days_until_next_weekday)
    while next_weekday.isocalendar()[1] % 2 == week_odd_even:
        next_weekday += timedelta(weeks=1)
    return next_weekday.date()

def get_next_weekday3(weekdays: list, week_odd_even = None):
    '''test if list is empty'''
    if not weekdays:
        return()
    
    else:
        weekday = weekday_to_int(weekdays[0])
        current_date = datetime.now()
        days_until_next_weekday = (weekday- current_date.weekday() + 7) % 7
        next_weekday = current_date + timedelta(days=days_until_next_weekday)
        while next_weekday.isocalendar()[1] % 2 == week_odd_even:
            next_weekday += timedelta(weeks=1)
        return (next_weekday.date(),) + (get_next_weekday3(weekdays[1:], week_odd_even))
    
def mandag_torsdag(dag_uge: list):
    '''return True if mandag_torsdag is in dag_uge'''
    if 'mandag' in dag_uge and 'torsdag' in dag_uge:
        return True
    else:
        return False

def format_date(date:list):

        førstkommende = min(date)
        førstkommende_weekday_number = førstkommende.weekday()
        førstkommende_weekday_name = Weekday.get_name_from_value(førstkommende_weekday_number).title()
        return (førstkommende_weekday_name, førstkommende.strftime("%d-%m"))

def naste_tomning(tur: str):
    
    resultat = return_dag_uge(tur)
    weekday = resultat[0]
    frequency = resultat[1]
    if OddEven.is_member(frequency):
        resultat.pop(1)
        #frequency_value = OddEven.from_string(frequency)
    
    
    try:
        weekday_value = Weekday.from_string(weekday)

    except AttributeError as e:
        print(f'AttributeError {e}')

    try:
        frequency_value = OddEven.from_string(frequency)

    except AttributeError as e:
        print(f'AttributeError {e}')
    
    

    q2 = get_next_weekday3(resultat, frequency_value)
    #print(format_date(q2))
    return format_date(q2)
    
    


if __name__ == '__main__':



    #Example usage
    print(f'Næste Torsdag {get_next_weekday("torsdag")}')
    print(f'Næste lige Torsdag {get_next_weekday("torsdag", 1)}')
    print(f'Næste ulige Torsdag {get_next_weekday("torsdag", 0)}')

    # Test section
    # frequency should be renamed to week
    weekday, frequency = return_dag_uge('mandag, torsdag')

    # construct arguments for get_next_weekday3

    resultat = return_dag_uge('mandag, torsdag')
    frequency = resultat[1]
    if OddEven.is_member(frequency):
        resultat.pop(1)
        #frequency_value = OddEven.from_string(frequency)
    
    
    try:
        weekday_value = Weekday.from_string(weekday)

    except AttributeError as e:
        print(f'AttributeError {e}')

    try:
        frequency_value = OddEven.from_string(frequency)

    except AttributeError as e:
        print(f'AttributeError {e}')
    
    

    q2 = get_next_weekday3(resultat, frequency_value)
    print(format_date(q2))
    # print(q2)
    # length_q2 = len(q2)
    # if length_q2 == 1:
    #     print(f'Næste {weekday} {frequency} {q2[0]}')
    # elif length_q2 == 2:

    #     for  q in q2:
    #         # from q get weekday_number

    #         weekday_number = q.weekday()
    #         weekday_name = Weekday.get_name_from_value(weekday_number).title()
    #         print(f'Næste {weekday_name} {q.strftime("%d-%m")}')

    #     # print(f'Næste {weekday} {frequency} {q2[0]} og {q2[1]}')
    #     firstcomming = min(q2)
    #     firstcomming_weekday_number = firstcomming.weekday()
    #     firstcomming_weekday_name = Weekday.get_name_from_value(firstcomming_weekday_number).title()
    #     print(f'Næste {firstcomming_weekday_name} {firstcomming.strftime("%d-%m")}')

    
    if OddEven.is_member(frequency) and Weekday.is_member(weekday):
            '''get the next weekday'''
            next_weekday = get_next_weekday2(weekday_value, frequency_value)

            print(f'Næste {weekday} {frequency} {next_weekday}')



    # Test for tilfælde hvor der er angivet to dage, men ikke uge
    if not OddEven.is_member(frequency):
        if Weekday.is_member(frequency) and Weekday.is_member(weekday):
            weekdays = [weekday, frequency]

            today = datetime.today().weekday()
            next_weekdays = []
            for weekday in weekdays:
                weekday = Weekday.from_string(weekday)
                next_weekdays.append(get_next_weekday2(weekday))
            for x in next_weekdays:

                print(x.strftime('%d-%m'), x.strftime('%A'))
            
            print(min(next_weekdays))
        #test for tilfælde hvor der kun er angivet en dag
        
        elif Weekday.is_member(weekday):
            '''get the next weekday'''
            next_weekday = get_next_weekday2(weekday_value)

            print(f'Bæste {weekday} {frequency} {next_weekday}')
        else:
            print('Invalid input')












