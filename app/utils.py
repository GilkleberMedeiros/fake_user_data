import random
import re


names_vars: dict[str, any] = {"limit": 0, "cache": []}


# Requisitos generate_fake_names:
#   1. Gerar nomes através de duas listas (l1:primeiros nomes e l2:sobrenomes).
#   2. Gerar os nomes de maneira eficiente.
#   3. Gerar somente nomes únicos se requisitado.
#   4. Gerar todos os nomes requisitados, caso isso não quebre a regra de unicicidade.
def generate_fake_names(n_names: int, unique: bool = True) -> list[str]:
    # Getting lists from files
    f1 = open("./app/fake_first_names.txt", encoding="utf-8")
    f2 = open("./app/fake_last_names.txt", encoding="utf-8")

    first_names = [ name.strip() for name in f1.readlines() ]
    last_names = [ name.strip() for name in f2.readlines() ]
    len_first_names = len(first_names)
    len_last_names = len(last_names)

    f1.close()
    f2.close()

    # return names when unique == False
    if names_vars["cache"] and not unique:
        return [ random.choice(names_vars["cache"]) for _ in range(n_names) ]

    # return names if names already generated and generated names still updated
    # and unique == True and generated names not exausted.
    if names_vars["cache"] and len(names_vars["cache"]) == len_first_names * len_last_names:
        if unique and names_vars["limit"] != 0:
            new_names_limit = names_vars["limit"] - n_names if names_vars["limit"] - n_names > 0 else -1

            result = []
            for i in range(names_vars["limit"], new_names_limit, -1):
                result.append(names_vars["cache"][i])

            names_vars["limit"] = new_names_limit if new_names_limit > 0 else -1

            return result
        
        return []

    # Generate all names at once
    MAX_UNIQUE_NAMES = len_first_names * len_last_names
    for i in range(len_first_names):
        for j in range(len_last_names):
            names_vars["cache"].append(first_names[i] +" "+ last_names[j])
        
    names_vars["limit"] = MAX_UNIQUE_NAMES - 1
    random.shuffle(names_vars["cache"]) # shuffle the cache list in place

    return generate_fake_names(n_names=n_names, unique=unique)


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