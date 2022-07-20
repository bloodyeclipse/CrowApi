from CrowApi.settings import SECRET_KEY
salt = SECRET_KEY

def mix(uid,forward=True):
    # The first half
    h1 = uid[:len(uid)//2]
    # The last Half
    h2 = uid[len(uid)//2:]