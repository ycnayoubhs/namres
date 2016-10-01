from six.moves.urllib.parse import urlencode

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404

from .models import Document
from .forms import DocumentForm
from .server_list_converter import convert_server_list
from .custom_converter import convert_customizable


def document_create(request):
    if request.method == 'GET':
        content = {
            'form': DocumentForm(),
            'title': 'Create',
        }
        content.update(csrf(request))
        return render_to_response('doc_editor.html', content)

    elif request.method == 'POST':
        form = DocumentForm(request.POST)

        if not form.is_valid():
            content = {
                'form': form,
                'title': 'Create',
            }
            content.update(csrf(request))
            return render_to_response('doc_editor.html', content)

        form.save()

        return redirect(reverse('list'))


def document_edit(request, slug=None):
    if request.method == 'GET':
        try:
            document = Document.objects.get(slug=slug, is_deleted=False)
            form = DocumentForm(instance=document)
        except Document.DoesNotExist:
            message = 'Document %s not exists or maybe deleted.' % slug
            return redirect('%s?%s' % (reverse('list'), urlencode({'message': message})))

        content = {'form': form, 'title': document.name}
        content.update(csrf(request))

        return render_to_response('doc_editor.html', content)

    elif request.method == 'POST':
        document = get_object_or_404(Document, slug=slug)
        form = DocumentForm(request.POST, instance=document)

        if not form.is_valid():
            content = {
                'form': form,
                'title': document.name,
            }
            content.update(csrf(request))
            return render_to_response('doc_editor.html', content)

        form.save()

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


def document_view(request, slug):
    try:
        document = Document.objects.get(slug=slug, is_deleted=False)
    except Document.DoesNotExist:
        return redirect('%s?%s' % (reverse('list'), urlencode({'required': slug})))

    doc_context = document.context
    server_list = None
    customized_context = None

    if document.converter == 'N':
        pass  # normal context, output directly.
    elif document.converter == 'S':
        server_list, doc_context = convert_server_list(doc_context)
    elif document.custom_converter:
        customized_context, doc_context = convert_customizable(doc_context, document.custom_converter)

    content = {
        'title': document.name,
        'slug': document.slug,
        'server_list': server_list,
        'customized': customized_context,
        'paragraphs': [p2 for p2 in [p for p in doc_context.split('\n')] if p2.strip() != ''],
    }

    return render_to_response('doc.html', content)
