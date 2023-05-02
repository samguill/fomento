import pandas as pd
import os
#from .parser import ReadPlatformFormats, ParserFileAlreadyExists
#from ..core.clients.merlin_ftp import MerlinFtpDirectoryNotExists


from .models import Fomento, FomentoFile, FomentoTmp
from sqlalchemy import create_engine



class Loader:
    FIELDS = ['fomento', 'year', 'month', 'day']
    merlin = None

    @classmethod
    def validated_files(cls, files, ext):
        list_files = [f for f in files if ext in f]
        files_processed = FomentoFile.objects.filter(filename__in=list_files).values_list('filename')
        return list(set(list_files)-set(files_processed))

    @classmethod
    def validate_file(cls, file, year, month):
        f = FomentoFile.objects.filter(filename=file, year=year, month=month, processed=True)
        if f.count() == 1:
            raise ParserFileAlreadyExists
        return True

    @classmethod
    def get_month(cls, month):
        months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        index = months.index(month)
        return str(index+1).rjust(2, '0')

    @classmethod
    def create_sales_files(cls, filename, year, month):
        sf = FomentoFile.objects.create(filename=filename, year=year, month=month)
        sf.save()
        return sf

    @classmethod
    def append_rows_to_fomento(cls, filename, year, month):
        sf = cls.create_sales_files(filename, year, month)

        objects = FomentoTmp.objects.values_list(*cls.FIELDS)
        destination_objects = [dict(zip(cls.FIELDS, list(obj))) for obj in objects]

        model_instances = [Fomento(**my_dict) for my_dict in destination_objects]
        Fomento.objects.bulk_create(model_instances)

        Fomento.objects.filter(file__isnull=True).update(file=sf.id)
        FomentoFile.objects.filter(id=sf.id).update(processed=True)

    @classmethod
    def get_engine(cls):
        return create_engine("postgresql://fomento:dbpass@db:5432/fomentodb")

    @classmethod
    def append_rows_to_tmp(cls, df):
        df['day'] = df['day'].apply(str)
        df['day'] = df['day'].str.rjust(2, '0')
        df['fomento'] = df['fomento'].fillna('0,00')
        df['fomento'] = df['fomento'].str.replace('.', '').str.replace(',', '.').astype(float)
        engine = cls.get_engine()
        df.to_sql(FomentoTmp._meta.db_table, if_exists="replace", con=engine, index=False)
        FomentoTmp.objects.filter(fomento__isnull=True).update(fomento=0.00)


class ParserFileAlreadyExists(Exception):
    pass



class LoaderSIIFomento(Loader):
    EXTENSION = 'csv'
    PLATFORM = 'sii'
    FIELDS_FILTER = ['Día']
    TO_FIELDS_FORMAT = ['day', 'fomento']
    MAIN_DIRECTORY = 'csv-files'

    @classmethod
    def execute(cls, working_directory, year):
        path = f"{cls.MAIN_DIRECTORY}{working_directory}/"

        list_files = []
        try:
            list_files = os.listdir(path)
        except Exception:
            print(f"Directory {path} doesn't exists")
            return None

        months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        for file in list_files:
            try:
                df = pd.read_csv(f"{path}/{file}", sep=";")
                for m in months:
                    filter = ['Día']
                    filter.append(m)
                    month = cls.get_month(m)
                    temp_df = df.filter(filter, axis=1)
                    temp_df.columns = cls.TO_FIELDS_FORMAT
                    temp_df['year'] = year
                    temp_df['month'] = month

                    cls.append_rows_to_tmp(temp_df)
                    cls.append_rows_to_fomento(file, year, month)

            except pd.errors.EmptyDataError:
                continue
            # except ParserFileAlreadyExists:
            #     print(f"File {file} for year {year} and month {month} already processed!")
            #     continue
