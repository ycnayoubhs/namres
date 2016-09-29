import json

from six.moves.urllib.parse import urlencode

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render, render_to_response, redirect

from mixed.models import Document
from mixed.forms import DocumentForm

def document_edit(request, slug=None):
    if slug == None:
        form = DocumentForm()
        title = 'Create'
    else:
        try:
            document = Document.objects.get(slug=slug, is_deleted=False)
            form = DocumentForm(instance=document)
            title = document.name
        except Document.DoesNotExist:
            return redirect(reverse('create'))

    content = {'form': form, 'title': title}
    content.update(csrf(request))

    return render_to_response('doc_editor.html', content)


def document_save(request):
    name = request.POST.get('name') or request.GET.get('name')
    context = request.POST.get('context') or request.GET.get('context')

    saved = False
    try:
        document = Document.objects.get(name=name)
        if document.context != context:
            document.context = context
            saved = True
    except Document.DoesNotExist:
        document = Document(name=name, context=context)
        saved = True
    
    if saved:
        document.save()

    return redirect(reverse('list'))


def document_delete(request, slug):
    message = None
    try:
        document = Document.objects.get(slug=slug, is_deleted=False)
        if document.converter != 'S':
            document.is_deleted = True
            document.save()
        else:
            message = 'Server list cannot be deleted.'
            return redirect('%s?%s' % (reverse('list'), urlencode({'message': message})))
    except Document.DoesNotExist:
        pass

    return redirect(reverse('list'))


def document_list(request):
    doc_list = Document.objects.filter(is_deleted=False)

    content = {
        'doc_list': [
            {
                'name': doc.name,
                'slug': doc.slug,
            }
            for doc in doc_list
        ],
        'required': request.GET.get('required'),
        'message': request.GET.get('message'),
    }

    return render_to_response('doc_list.html', content)


def document(request, slug):
    try:
        document = Document.objects.get(slug=slug, is_deleted=False)
    except Document.DoesNotExist:
        return redirect('%s?%s' % (reverse('list'), urlencode({'required': slug})))

    doc_context = document.context
    server_list = None
    if document.converter == 'S':
        try:
            server_list = convert_server_list(doc_context)
            if server_list:
                doc_context = ''
            else:
                doc_context = 'You have no server list configuration in current document.'
        except:
            doc_context = 'There is some thing wrong in your configuration document. Please check and try again.'

    content = {
        'title': document.name,
        'paragraphs': list(filter(lambda x: x.strip() != '', [p for p in doc_context.split('\n')])),
        'server_list': server_list,
    }

    return render_to_response('doc.html', content)


def convert_server_list(context):
    converted_list = []
    info_list = _generate_info_list(context)

    server_offline_message = 'Server is under maintenance or you mis-configed.'
    
    for info in info_list:
        path = _get_server_setting(info, 'path')
        status_dict = _query_server_info(path)

        if not status_dict:
            converted_list.append({
                'title': _get_server_setting(info, 'title'),
                'url': _get_server_setting(info, 'url'),
                'db': server_offline_message,
                'path': path,
                'deploy': server_offline_message,
            })
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
    
    if not status_dict or status_dict[path]['status'] != 'OK':
        return {}
    return status_dict[path]


def _generate_info_list(context):
    return [c.split('\r') for c in context.replace('\r\n', '\r').split('\r\r')]


def _get_server_setting(info, name):
    prefix = '%s:' % name
    line = list(filter(lambda x: x.startswith(prefix), info))
    if len(line) != 1:
        return ''
    return line[0].lstrip(prefix).strip()