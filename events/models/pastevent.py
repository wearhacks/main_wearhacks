from django.db import models
from event import Event
from project import Project
from bs4 import BeautifulSoup as BS
import urllib2
from django.conf import settings
import flickrapi
import os
import re
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urlparse import urlparse

class PastEvent(models.Model):
    SOURCETYPES = (
        ('0', 'Other'), # later we can add more sources
        ('1', 'flickr')
    )
    dev_post_default_image = u'thumbnail-placeholder'

    source_albumlink = models.URLField(max_length=100, blank=True,
        help_text="format: https://www.flickr.com/photos/77348536@N03/sets/72157660996201832/")
    source_type = models.CharField(max_length=1, choices=SOURCETYPES)

    source_projects = models.URLField(max_length=100, blank=True,
        help_text="format: http://wearhacksla.devpost.com/submissions")

    participants = models.IntegerField(default=100)
    event = models.OneToOneField(Event, primary_key=True)
    album = None
    photos = None

    def save(self, *args, **kwargs):
        super(PastEvent, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Past event data for %s" % (self.event.event_name)

    def fetch_album(self, username, album):
        if not self.album:
            if self.source_type == '1': # if from flickr
                flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET, format='parsed-json')
                
                sets = flickr.photosets.getPhotos(
                        user_id=username,
                        photoset_id=album)
                self.album = sets
            # handle other cases
        return self.album

    def fetch_photos(self):
        if not self.photos:
            if not self.album:
                self.fetch_album()
            if self.source_type == '1': # if from flickr
                self.photos = self.album['photoset']['photo']
            # handle other cases
        return self.photos

    def get_stats(self):
        source_username = re.search('(?<=photos/)([^/]*)', self.source_albumlink).group(0)
        source_albumname = re.search('(?<=sets/)([^/]*)', self.source_albumlink).group(0)

        if not self.album:
            self.fetch_album(source_username,source_albumname)
        if self.source_type == '1':
            return {
               'total': self.album['photoset']['total'],
               'userId': source_username,
               'albumId': source_albumname,
               'participants': self.participants
            }
        return None


    def add_arguments(self, parser):
        parser.add_argument('event', type=str)
        parser.add_argument('url', type=str)

    def retrieve_projects(self):
        url = self.source_projects
        counter = 0
        page = 1
        # assume url is something like this
        # http://wearhacksmontreal.devpost.com/submissions
        while(True):
            page_url = "%s?page=%d" % (url, page)
            soup = BS(urllib2.urlopen(page_url).read(), 'html.parser')
            print 'scraping %s' % url
            newProjects, scrapped = self.scrape_it(soup)
            if not scrapped:
                print('Added %d new projects.' % counter)
                print('WAHHOOO DONE!')
                return
            counter += newProjects
            page += 1

    def strip_text(self, text):
        return text.replace('\n', '').strip()

    def scrape_it(self, soup):
        entries = soup.find_all('div', {'class':'gallery-item'})
        if len(entries) == 0:
            return (0,False)

        counter = 0
        for entry in entries:
            name = self.strip_text(entry.h5.string)

            args = {
                'name':name,
                'desc':self.strip_text(entry.p.string),
                'url':entry.a['href'],
                'image':entry.img['src'],
                'type':'2' if entry.aside else '1' # 2 = winner
            }
            if self.dev_post_default_image in args['image']:
                args['image'] = ''
                # maybe we can have a placeholder too
            if self.saveProject(args):
                print('Created new project %s.' % name)
                counter += 1
            else:
                print('Project %s already exists in DB.' % name)


        return (counter, True)

    def saveProject(self, args):
        print u'%s' % args
        try:
            obj = Project.objects.get(project_name = args['name'],url = args['url'])
            return None
        except Project.DoesNotExist:
            obj = Project(
                submitted_event = self.event,
                project_name = args['name'],
                short_description = args['desc'],
                url = args['url'],
                project_type = args['type']
            )
            img_temp = NamedTemporaryFile(delete=True)

            if args['image']:
                img_temp.write(urllib2.urlopen(args['image']).read())
                img_temp.flush()
                img_temp.seek(0)
                img_filepath = os.path.join('projects', urlparse(args['image']).path.split('/')[-1])
                obj.image.save(img_filepath, File(img_temp))
                obj.save()
            else :
                obj.save()
            return obj



    class Meta:
        app_label = 'events'

