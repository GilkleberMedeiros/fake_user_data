import random
import re

names_registry: set = set()


def generate_fake_names(n_names: int, unique: bool = True) -> list[str]:
    # Getting lists from files
    f1 = open("./app/fake_first_names.txt", encoding="utf-8")
    f2 = open("./app/fake_last_names.txt", encoding="utf-8")

    first_names = [ name.strip() for name in f1.readlines() ]
    last_names = [ name.strip() for name in f2.readlines() ]

    f1.close()
    f2.close()

    MAX_UNIQUE_NAMES = len(first_names) * len(last_names)

    generated_names = []
    for i in range(n_names):
        # break if can't generate more unique names
        if unique and len(names_registry) >= MAX_UNIQUE_NAMES:
            break

        name = random.choice(first_names) +" "+ random.choice(last_names)

        while unique and name in names_registry:
            name = random.choice(first_names) +" "+ random.choice(last_names)

        generated_names.append(name)

    return generated_names

def generate_fake_email(name: str) -> str:
    email_makers = [
        lambda f, l: l[0] +"."+ f +"@gmail.com",
        lambda f, l: f + str(random.randint(0, 500)).zfill(3) + "@gmail.com",
        lambda f, l: l + str(random.randint(0, 500)).zfill(3) + "@gmail.com",
        lambda f, l: f +"."+ l +"@gmail.com"
    ]

    if not re.match(r'^\w+ \w+$', name):
        raise ValueError('Name must be in the format "first_name last_name"')

    choice = random.randint(0, len(email_makers) - 1)

    first_name, last_name = name.split(" ")
    
    return email_makers[choice](first_name, last_name)