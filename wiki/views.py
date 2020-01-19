# Stdlib imports
import requests
import os

# Core Django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files import File

# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pdfkit

# Imports from my apps
from .decorators import check_post_keys, check_get_params
from .wiki_logger import log_wiki

# Constants
WIKI_URL = "https://en.wikipedia.org/w/api.php"
WIKI_PAGE_URL = "https://en.wikipedia.org/wiki/"
WK_HTML_TO_PDF_PATH = "/usr/bin/wkhtmltopdf"


class OpenSearch(APIView):

    def get(self, request):
        """
        Display the form to search.
        """
        return render(request, 'wiki/index.html', {'search_item': ''})

    @check_post_keys(required_keys=('search_item', ))
    def post(self, request):
        """
        Takes input from end user , return suggestions based on input.
        """
        try:
            params = {
                "action": "opensearch",
                "format": "json",
                "namespace": 0,
                "limit": 10,
                "search": request.data['search_item']
            }
            res = requests.get(WIKI_URL, params=params)
            return render(request, 'wiki/index.html', {'suggestions': res.json()[1],
                                                       'search_item': request.data['search_item']})
        except Exception as e:
            log_wiki.error(str(e))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WikiSearch(APIView):

    @check_get_params(required_keys=('item',))
    def get(self, request):
        """
        Takes input Search Item from end user and return Search Results, with download as pdf option.
        """
        try:
            params = {
                "action": "query",
                "list": "search",
                "format": "json",
                "srsearch": request.query_params['item']
            }
            res = requests.get(WIKI_URL, params=params)
            return render(request, 'wiki/search_results.html', {'search_results': res.json()['query']['search']})
        except Exception as e:
            log_wiki.error(str(e))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DownloadPDF(APIView):

    @check_get_params(required_keys=('item',))
    def get(self, request):
        """
        create a pdf format of wiki page and send in response as attachment so that end user can download.
        """
        try:
            page_url = WIKI_PAGE_URL+request.query_params['item']
            filename = request.query_params['item'].replace(" ", "")+'.pdf'
            config = pdfkit.configuration(wkhtmltopdf=WK_HTML_TO_PDF_PATH)
            res = pdfkit.from_url(page_url, 'static/'+filename, configuration=config)
            with open('static/'+filename, 'rb') as wiki_pdf:
                response = HttpResponse(File(wiki_pdf), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment;filename='+filename
                if os.path.exists('static/'+filename):
                    os.remove('static/'+filename)
                else:
                    print("Pdf doesn't exist")
                return response
        except Exception as e:
            log_wiki.error(str(e))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


