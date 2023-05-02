from django.core.management import BaseCommand

from fomento.tasks import run_get_fomento_csv
from fomento.utils import get_from_dict


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--month', nargs='?', help='Month to be processed')
        parser.add_argument('--year', nargs='?', help='Year in process')

    def handle(self, *args, **options):
        month = get_from_dict(
            dictionary=options, key='month',
            default_if_empty=None, default_if_not_exist=None,
            cast_function=str
        )

        year = get_from_dict(
            dictionary=options, key='year',
            default_if_empty=None, default_if_not_exist=None,
            cast_function=str
        )

        run_get_fomento_csv(month, year)
        print('DONE')
