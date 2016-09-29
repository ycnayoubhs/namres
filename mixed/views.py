from six.moves.urllib.parse import urlencode

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect

from .models import Document
from .forms import DocumentForm
from .server_list_converter import convert_server_list
from .custom_converter import convert_customizable

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
    customized_context = None

    if document.converter == 'S':
        server_list, doc_context = convert_server_list(doc_context)
    elif document.custom_converter:
        customized_context, doc_context = convert_customizable(doc_context, document.custom_converter)

    content = {
        'title': document.name,
        'server_list': server_list,
        'customized': customized_context,
        'paragraphs': [p2 for p2 in [p for p in doc_context.split('\n')] if p2.strip() != ''],
    }

    return render_to_response('doc.html', content)
