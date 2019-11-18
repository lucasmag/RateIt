import api.utils.constants as c


def put_bar(string):
    return '/{}'.format(string) if string is not '' else ''
    

def make(base_url, resource, first_id='', path='', final_path='', last_id='', language='pt-BR', page='1'):
    return base_url + put_bar(resource) + put_bar(first_id) + put_bar(path) + put_bar(final_path) + \
           put_bar(last_id) + "?api_key=" + c.API_KEY + "&language=" + "{}".format(language) + "&page=" + page



