from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('')

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': 'tictactoe/static'}),
    )

urlpatterns += patterns('tictactoe.views',
    (r'^(?P<state>[xo-]*$)', 'index'),
)
