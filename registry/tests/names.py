import random

girls_names = [
    'Amelia',
    'Olivia',
    'Isla',
    'Emily',
    'Poppy',
    'Ava',
    'Isabella',
    'Jessica',
    'Lily',
    'Sophie'
]

boys_names = [
    'Oliver',
    'Jack',
    'Jack',
    'Jacob',
    'Charlie',
    'Thomas',
    'George',
    'Oscar',
    'James',
    'William'
]

surnames = [
    'Smith',
    'Jones',
    'Williams',
    'Taylor',
    'Davies',
    'Evans',
    'Thomas',
    'Johnson',
    'Roberts',
    'Walker',
    'Wright',
    'Robinson',
    'Thompson'
]

domains = [
    'yahoo.com',
    'gmail.com',
    'fastmail.com',
    'telco.com'
]

streetnames = [
    'High Street',
    'Church Lane',
    'Station Road',
    'Church Street',
    'Mill Lane',
    'Church Road',
    'Green Lane',
    'Main Street',
    'School Lane',
    'New Road',
    'Back Lane',
    'Chapel Lane',
    'Park Road',
    'The Green',
    'The Street',
    'Orchard Close',
    'The Crescent',
    'Manor Road',
    'The Avenue',
    'Park Lane'
]

cities = [
    'London',
    'Birmingham',
    'Liverpool',
    'Nottingham',
    'Sheffield',
    'Bristol',
    'Glasgow',
    'Leicester',
    'Edinburgh',
    'Leeds',
    'Cardiff',
    'Manchester',
    'Stoke-on-Trent',
    'Coventry',
    'Sunderland',
    'Birkenhead',
    'Islington',
    'Reading',
    'Kingston upon Hull'
]

operations = [
    'hernia repair',
    'hip replacement',
    'knee replacement',
    'gall bladder removal',
    'tonsillectomy'
]


def name(gender: str) -> str:
    if gender == 'M':
        return random.choice(surnames) + ', ' + random.choice(boys_names)
    elif gender == 'F':
        return random.choice(surnames) + ', ' + random.choice(girls_names)
    else:
        raise ValueError('Unrecognised gender {}'.format(gender))


def email(name: str) -> str:
    surname, first_name = name.split(',')
    surname = surname.lower().strip()
    first_name = first_name.lower().strip()

    return '{}.{}@{}'.format(first_name, surname, random.choice(domains))


def address() -> str:
    return '{} {}\n{}'.format(
        random.randint(1, 150),
        random.choice(streetnames),
        random.choice(cities)
    )


def hospital(city: str) -> str:
    return '{} Hospital'.format(city)
