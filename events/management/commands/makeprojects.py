from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from events.models import Project, Event

from loremipsum import get_sentence, get_paragraph
from random import randint
from geoposition import Geoposition
from django.utils import timezone

class Command(BaseCommand):
    args = 'numProjects [--reset]'
    help = 'Create project using lorem ipsum generator'

    option_list = BaseCommand.option_list + (
        make_option('--reset',
            action='store_true',
            dest='reset',
            default=False,
            help='Delete all projects before generating new ones.'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Usage: {0}'.format(self.args))

        if options['reset']:
            Project.objects.all().delete()

        numProjects = args[0]

        try:
            Command.make_projects(int(numProjects))
        except ValueError, e:
            raise CommandError('Usage: you must pass a valid number.')
        except Exception, e:
            raise CommandError('An error occured while making projects')

        self.stdout.write('Successfully generated {0} projects'.format(numProjects))

    @staticmethod
    def get_random_event():
        if Event.objects.exists():
            event = Event.objects.order_by('?')[:1].first()
        else:
            # make a random event
            event_name = get_sentence()[:50]
            address = get_sentence()[:100]
            event_data = {
                'event_name': event_name,
                'slug': event_name.replace(' ', '-'),
                'start_date': timezone.now(),
                'end_date': timezone.now(),
                'address': address,
                'city': address.split()[-1],
                'location': Geoposition(randint(-90,90), randint(-90, 90))
            }
            event = Event.objects.create(**event_data)
        return event

    @staticmethod
    def make_projects(n, **kwargs):
        for i in range(n):
            Project.objects.create(**Command.generate_project_data(**kwargs))

    @staticmethod
    def generate_project_data():
        pt = Project.PROJECTTYPE
        data =  {
            'submitted_event': Command.get_random_event(),
            'project_name':  get_sentence()[:50], 
            'short_description': get_sentence()[:300],
            'project_type': pt[randint(0,len(pt)-1)][0] # pt = Project.PROJECTTYPE
        }
        return data