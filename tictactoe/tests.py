"""Test the tictactoe views.

"""

from django.test import TestCase
from django.test.client import Client
import re


class TestSimpleHtmlGame(TestCase):
    '''Tests to ensure requests to various urls return sane responses for the
    simple HTML view.
    
    '''
    urls = 'tictactoe.urls'

    def setUp(self):
        self.client = Client()

    def test_root(self):
        '''A request to the root returns the Simple HTML view.'''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Simple HTML version')
        self.assertContains(response, 'make the computer move first')

    def test_computerfirst(self):
        '''A request containing empty state causes the computer to make the first move.'''
        response = self.client.get('/---------')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'x.png')

    def test_humanfirst(self):
        '''A request in which we move first is equally valid.'''
        response = self.client.get('/----x----')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'o.png')
        self.assertContains(response, 'x.png')

    def test_anystate(self):
        '''The simple HTML game is stateless, so we can jump to any valid game
        state we wish.

        '''
        for state in [
            'xox--o---',
            'xxooxx--o',
            'x-ooxx-xo',
            'o-ox-xx--',
        ]:
            self.assertEqual(self.client.get('/%s' % state).status_code, 200)

    def test_badurls(self):
        '''However, invalid states indicate URL tampering and throw exceptions.'''
        import tictac
        for state in [
            'xxxxxxxxx',
            'oooxxxxxo',
        ]:
            self.assertRaises(tictac.TTTStateError, self.client.get, '/%s' % state)
