from django.test import TestCase
import requests
BASE_URL = 'http://127.0.0.1:8000/wiki/'


class TestOpenSearch:
    def test_one(self):
        """
        pass valid keys and data
        """
        data = {'search_item': 'Hampi'}
        res = requests.post(BASE_URL+'index/', data=data)
        assert res.status_code == 200

    def test_two(self):
        """
        pass invalid keys and valid data
        """
        data = {'xyz': 'Hampi'}
        res = requests.post(BASE_URL+'index/', data=data)
        assert res.status_code == 400
        assert 'KeyError' in res.json()

    def test_three(self):
        """
        pass None
        """
        data = None
        res = requests.post(BASE_URL+'index/', data=data)
        assert res.status_code == 400
        assert 'KeyError' in res.json()


class TestWikiSearch:
    def test_one(self):
        """
        pass valid keys and data
        """
        params = {'item': 'Hampi Express'}
        res = requests.get(BASE_URL+'search/', params=params)
        assert res.status_code == 200

    def test_two(self):
        """
        pass invalid keys and valid data
        """
        params = {'xyz': 'Hampi Express'}
        res = requests.get(BASE_URL + 'search/', params=params)
        assert res.status_code == 400
        assert 'KeyError' in res.json()

    def test_three(self):
        """
        pass None
        """
        params = None
        res = requests.get(BASE_URL + 'search/', params=params)
        assert res.status_code == 400
        assert 'KeyError' in res.json()


class TestDownloadPDF:
    def test_one(self):
        """
        pass valid keys and data
        """
        params = {'item': 'Hampi Express'}
        res = requests.get(BASE_URL+'download/', params=params)
        assert res.status_code == 200

    def test_two(self):
        """
        pass invalid keys and valid data
        """
        params = {'xyz': 'Hampi Express'}
        res = requests.get(BASE_URL + 'download/', params=params)
        assert res.status_code == 400
        assert 'KeyError' in res.json()

    def test_three(self):
        """
        pass None
        """
        params = None
        res = requests.get(BASE_URL + 'download/', params=params)
        assert res.status_code == 400
        assert 'KeyError' in res.json()

