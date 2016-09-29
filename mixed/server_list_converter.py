def convert_server_list(context):
    try:
        server_list = _convert_server_list(context)
        if server_list:
            return server_list, ''
        else:
            return server_list, 'You have no server list configuration in current document.'
    except:
        return server_list, 'There is some thing wrong in your configuration document. Please check and try again.'


def _convert_server_list(context):
    converted_list = []
    info_list = _generate_info_list(context)
    
    for info in info_list:
        path = _get_server_setting(info, 'path')
        status_dict = _query_server_info(path)

        if not status_dict:
            continue

        data_source = status_dict['data_source']
        if data_source == '.':
            data_source = '(local)'

        converted_list.append({
            'title': _get_server_setting(info, 'title'),
            'url': _get_server_setting(info, 'url'),
            'db': '%s, %s' % (data_source, status_dict['initial_catalog']),
            'path': path,
            'deploy': status_dict['deploy_time'],
        })

    return converted_list


def _query_server_info(path):
    import json
    from six.moves.urllib.parse import urlencode, urljoin
    from django.conf import settings
    import requests

    status_dict = None

    if not hasattr(settings, 'DEPLOY_POLLING_SERVER_LIST'):
        return {}

    for server in settings.DEPLOY_POLLING_SERVER_LIST:
        query_string = urlencode({'folder': path})
        url = 'http://%s/RISMOEITWeb/VAT/Modules/Handlers/SvrStat.ashx?%s' % (server, query_string)
        try:
            status_dict = json.loads(requests.get(url).text)
            if status_dict[path]['status'] == 'OK':
                break
        except:
            pass
    
    if not status_dict and status_dict[path]['status'] != 'OK':
        return {}
    return status_dict[path]


def _generate_info_list(context):
    return [c.split('\r') for c in context.replace('\r\n', '\r').split('\r\r')]


def _get_server_setting(info, name):
    prefix = '%s:' % name
    # line = list(filter(lambda x: x.startswith(prefix), info))
    line = [l for l in info if l.startswith(prefix)]
    if len(line) != 1:
        return ''
    return line[0].lstrip(prefix).strip()
