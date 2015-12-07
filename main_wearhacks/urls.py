from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Examples:
     url(r'^$', 'events.views.home', name='home'),
     url(r'^aboutus/', 'events.views.about_us', name='aboutus'),
     url(r'^events/(?:(?P<event_slug>[\w-]+)/)?$', 'events.views.events', name='events'),
     # url(r'^events/', 'events.views.events', name='events'),
     url(r'^partnerships/', 'events.views.partnerships', name='partnerships'),
     url(r'^ambassador/', 'events.views.ambassador', name='ambassador'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    #apis
    url(r'^api/signup', 'events.views.mailchimp_signup'),
    url(r'^api/posts', 'events.views.get_sticky_post')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
