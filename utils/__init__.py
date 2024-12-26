from settings import setting

def get_url() -> str:
    url = ''
    if setting.SSL:
        url = 'https://'
    else:
        url = 'http://'
    url += setting.DOMAIN
    return url