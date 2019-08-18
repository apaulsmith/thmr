from sqlalchemy import and_


def like_all(d):
    filter = []
    for k, v in d.items():
        if len(v) > 0:
            filter.append(k.like('%' + str(v) + '%'))

    return and_(*filter)

