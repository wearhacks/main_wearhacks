from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
     url(r'^$', 'events.views.home', name='home'),
     url(r'^aboutus/', 'events.views.about_us', name='aboutus'),
     url(r'^events/', 'events.views.events', name='events'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
]
