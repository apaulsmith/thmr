from builtins import isinstance, list


def coerce_to_list(l):
    if isinstance(l, list):
        return l
    else:
        return [l]

def append_dicts(base, d):
    for k, v in d.items():
        base[k] = coerce_to_list(base[k]) + [v]

    return base