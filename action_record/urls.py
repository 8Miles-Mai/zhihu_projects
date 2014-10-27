__author__ = 'miles'

from django.conf.urls import include, url
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

urlpatterns = [
    # Examples:
    # url(r'^$', 'zhihu_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'action_record.views.index', name='index'),
    url(r'^create_file', 'action_record.views.create_test_data_file', name='create_file'),
    url(r'^read_file', 'action_record.views.read_test_data_file', name='read_file'),
    url(r'^query_data', 'action_record.views.query_user_action_record', name='query_data'),
    url(r'^set_anonymity', 'action_record.views.set_item_anonymity', name='set_anonymity'),
    url(r'^unset_anonymity', 'action_record.views.unset_item_anonymity', name='unset_anonymity'),

    # url(r'^data', 'action_record.views.data', name='data'),
    # url(r'^time', 'action_record.views.current_datetime', name='time'),
    # url(r'^initTestData', 'action_record.views.init_test_data', name='init_test_data'),
    # (r'^js/(?P<path>.*)$', 'django.views.static.serve',
    #          { 'document_root': os.path.join(BASE_DIR,  'templates/action_record') }
    #  ),

]