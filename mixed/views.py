from django.shortcuts import render
from django.http import JsonResponse

from mixed.models import Document


def document_list(requests):
    """
    Get document list with json format.
    """

    all_document = [{'name': d.name, 'slug': d.slug, 'context': d.context} for d in Document.objects.all()]
    return JsonResponse({'document': all_document})


def document(request, slug):
    """
    Get context of document.
    """

    document = Document.objects.get(slug=slug)

    return JsonResponse({'document': document.context})