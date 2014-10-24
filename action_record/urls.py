__author__ = 'miles'

from django.conf.urls import include, url

urlpatterns = [
    # Examples:
    # url(r'^$', 'zhihu_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),

	url(r'^$', 'action_record.views.index', name='index'),
    url(r'^data', 'action_record.views.data', name='data'),
    url(r'^time', 'action_record.views.current_datetime', name='time'),
    url(r'^initTestData', 'action_record.views.init_test_data', name='init_test_data')

]