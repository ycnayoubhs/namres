from django import template

register = template.Library()

@register.filter
def svrinfo(server):
    paragraphs = [
        server['title'],
        '<a target="_blanket" href="%s">%s</a>' % (server['url'], server['url']),
        'Database: %s' % server['db'],
        'Path: %s' % server['path'],
        'Deploy: %s' % server['deploy'],
    ]

    return ''.join(['<p>%s</p>' % p for p in paragraphs])