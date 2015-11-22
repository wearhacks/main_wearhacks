from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup as BS
import urllib2
import sys

from events.models import Event, Project


class Command(BaseCommand):
    help = 'Scrapper to scrape whatever there is to scrape on imput devpost url.'

    eventObject = None
    eventName = None

    def add_arguments(self, parser):
        parser.add_argument('event', type=str)
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        counter = 0
        page = 1
        self.eventObject = Event.objects.get(short_name = options['event'])
        # assume url is something like this
        # http://wearhacksmontreal.devpost.com/submissions
        while(True):
            url = "%s?page=%d" % (options['url'],page)
            soup = BS(urllib2.urlopen(url).read(), 'html.parser')

            newProjects = self.scrapeIt(soup)
            if not newProjects:
                self.stdout.write('Added %d new projects.' % counter)
                self.stdout.write('WAHHOOO DONE!')
                sys.exit()

            counter += newProjects
            self.stdout.write('Scapped page %s' % url)
            page += 1

    def stripText(self, text):
        return text.replace('\n', '').strip()

    def scrapeIt(self, soup):
        entries = soup.find_all('div', {'class':'gallery-item'})
        if len(entries) == 0:
            return False

        counter = 0
        for entry in entries:
            name = self.stripText(entry.h5.string)
            args = {
                'name':name,
                'desc':self.stripText(entry.p.string),
                'url':entry.a['href'],
                'image':entry.img['src'],
                'type':'2' if entry.aside else '1' # 2 = winner

            }
            if self.saveProject(args):
                self.stdout.write('Created new project %s.' % name)
                counter += 1
            else:
                self.stdout.write('Project %s already exists in DB.' % name)

        return counter

    def saveProject(self, args):
        obj, created = self.eventObject.project_set.get_or_create(
            project_name = args['name'],
            short_description = args['desc'],
            url = args['url'],
            image = args['image'],
            project_type = args['type']
        )
        return created
