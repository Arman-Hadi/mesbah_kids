from io import StringIO

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Reset PostgreSQL sequences after loaddata (no psql required).'

    def add_arguments(self, parser):
        parser.add_argument('apps', nargs='+', help='App labels, e.g. auth core')

    def handle(self, *args, **options):
        if connection.vendor != 'postgresql':
            self.stderr.write('This command only applies to PostgreSQL.')
            return

        out = StringIO()
        call_command('sqlsequencereset', *options['apps'], stdout=out)
        sql = out.getvalue().strip()
        if not sql:
            self.stdout.write('No sequences found.')
            return

        with connection.cursor() as cursor:
            for statement in sql.split(';'):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)

        self.stdout.write(self.style.SUCCESS('Sequences reset.'))
