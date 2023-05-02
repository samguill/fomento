import tempfile
from celery import shared_task
from fomento.loaders import LoaderSIIFomento

@shared_task
def run_get_fomento_csv(month, year):
    parser, path = LOADER_FORMAT_PARSER['load_csv']
    parser.execute(path, year)


LOADER_FORMAT_PARSER = {
    'load_csv': (LoaderSIIFomento, ''),
}
