from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.db import connection


class Command(BaseCommand):
    help = 'Reset PostgreSQL sequences after loaddata (no psql required).'

    def add_arguments(self, parser):
        parser.add_argument('apps', nargs='+', help='App labels, e.g. auth core')

    def handle(self, *args, **options):
        if connection.vendor != 'postgresql':
            self.stderr.write('This command only applies to PostgreSQL.')
            return

        style = no_style()
        statements = []
        for app_label in options['apps']:
            try:
                app_config = apps.get_app_config(app_label)
            except LookupError as e:
                raise CommandError(str(e)) from e
            if app_config.models_module is None:
                continue
            models = app_config.get_models(include_auto_created=True)
            statements.extend(connection.ops.sequence_reset_sql(style, models))

        if not statements:
            self.stdout.write('No sequences found.')
            return

        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)

        self.stdout.write(self.style.SUCCESS(f'Sequences reset ({len(statements)}).'))
