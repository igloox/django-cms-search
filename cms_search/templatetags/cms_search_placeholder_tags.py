from django import template
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from django.template.defaultfilters import safe
from cms_search.search_indexes import _strip_tags
from cms.middleware.page import LazyPage
from cms.templatetags.placeholder_tags import RenderPlaceholder

register = template.Library()


class SearchPlaceHolder(RenderPlaceholder):
    """
    Use this in search index templates instead of cms.templatetags.placeholder_tags
    render placeholder, because the indexer can't render those without
    a slightly more realistic request object in the context - which is
    what this provides.
    """
    name = 'render_placeholder'
    
    def render_tag(self, context, placeholder, width, language=None):
        rf = RequestFactory()
        request = rf.get("/")
        request.session = {}
        request.LANGUAGE_CODE = settings.LANGUAGES[0][0]
        request.__class__.current_page = LazyPage()
        request.user = AnonymousUser()
        context['request'] = request
        if not placeholder:
            return ''
        return _strip_tags(
            safe(placeholder.render(context, width, lang=language))
        )
register.tag(SearchPlaceHolder)
