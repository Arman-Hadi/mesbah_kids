from django.core.management.base import BaseCommand, CommandError

from core.models import Kid

import pandas


def dataframe_to_database(df : pandas.DataFrame, set_id=True):
    cols = df.columns.to_list()
    df.drop_duplicates(subset=[cols[1], cols[2], cols[3], cols[4], cols[5],], inplace=True)
    if set_id:
        for c, i in df.iterrows():
            kid = Kid()
            kid.id = c
            kid.porsline_id = i[0]
            kid.first_name = i[1]
            kid.last_name = i[2]
            kid.birth_date = i[3]
            kid.caretaker = i[4]
            kid.caretaker_name = i[5]
            kid.caretaker_phone_number = i[6]
            kid.emergancy_calls = i[7]
            kid.wc = i[8] != 'خیر'
            kid.caretaker_home_number = i[9]
            kid.save()
    else:
        for c, i in df.iterrows():
            kid = Kid()
            kid.porsline_id = i[0]
            kid.first_name = i[1]
            kid.last_name = i[2]
            kid.birth_date = i[3]
            kid.caretaker = i[4]
            kid.caretaker_name = i[5]
            kid.caretaker_phone_number = i[6]
            kid.emergancy_calls = i[7]
            kid.wc = i[8] != 'خیر'
            kid.caretaker_home_number = i[9]
            kid.save()


class Command(BaseCommand):
    help = 'Imports csv file into database.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='csv file path')
        parser.add_argument('set_id', type=int, help='set id for entry')

    def handle(self, *args, **options):
        try:
            df = pandas.read_csv(options['file_path'])
            set_id = bool(options['set_id'])
            dataframe_to_database(df, set_id=set_id)
        except Exception as e:
            raise CommandError(str(e))

        self.stdout.write(self.style.SUCCESS('imported successfuly!'))
