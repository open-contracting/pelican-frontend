

def terms_enumeration(it):
    return ', '.join(
        ('\'%s\'' % el)
        for el in it
    )
