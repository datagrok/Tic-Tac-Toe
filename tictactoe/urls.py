from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('')

if settings.DEBUG:
    from os.path import abspath, dirname, join
    urlpatterns = patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': join(dirname(abspath(__file__)), 'static')}),
    )

urlpatterns += patterns('tictactoe.views',
    (r'^(?P<state>[xo-]*$)', 'index'),
)
