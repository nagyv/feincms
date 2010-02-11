from feincms.module.page.models import Page
from django.http import HttpResponseRedirect, Http404
from django.conf import settings

class LanguageLookupMiddleware(object):
    '''
    Redirect to a language specific page if it exists. First look up the request's 
    language, then the default language.
    '''
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.
            
        try:
            language = [short for short, long in settings.LANGUAGES if short==request.LANGUAGE_CODE][0]
        except KeyError:
            pass
        else:
            response = self.get_page(language, request.path) and \
                HttpResponseRedirect('/%s%s' % (language, request.path)) or response

        if response.status_code == 404:
            response = self.get_page(settings.LANGUAGES[0][0], request.path) and \
                HttpResponseRedirect('/%s%s' % (settings.LANGUAGES[0][0], request.path)) or \
                response
        return response

    def get_page(self, language, path):
        try:
            return Page.objects.page_for_path_or_404('/%s%s' % (language, path))
        except Http404:
            return False

