import glob
import os
import time
import pandas as pd

from pathlib import Path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from shutil import copyfile
import xlwings as xw
import json


def date(delta_days=None, delta_months=None, delta_years=None, date_format='%Y-%m-%d'):
    """
    date(delta_days=None, date_format=None,)
    Return a date for the date format in the parameters
        The default data format is '%Y-%m-%d', exemple:'2020-12-31' 

        delta_days, delta_months e delta_years will add days/months/years to the date
    """

    calculated_date = datetime.now()

    if delta_days:
        calculated_date = calculated_date + timedelta(delta_days)

    if delta_months:
        calculated_date = calculated_date + relativedelta(months=delta_months)

    if delta_years:
        calculated_date = calculated_date + relativedelta(years=delta_years)
        
    if date_format:
        calculated_date = calculated_date.strftime(date_format)


    return calculated_date


def convert_date_to_datetime(date, origin_format='%Y-%m-%d'):

    return datetime.strptime(date, origin_format)


def convert_datetime_to_format(date, origin_format='%Y-%m-%d', destination_format='%d/%m/%Y'):

    return convert_date_to_datetime(date=date, origin_format=origin_format).strftime(destination_format)


def export_dataframe_to_csv(dataframe, filepath, separator=';', header=True, index=False, encoding=None, date_format=None, decimal=',', quoting=None, float_format=None):

    dataframe.to_csv(path_or_buf=filepath,
                    index=index,
                    sep=separator,
                    header=header,
                    date_format=date_format,
                    decimal=decimal,
                    quoting=quoting,
                    float_format=float_format)


def export_dataframe_to_excel(dataframe, filepath, encoding=None,  header=True, index=False, 
    float_format=None, sheet_name='Sheet1', date_format='YYYY-MM-DD'):

    writer = pd.ExcelWriter(path=filepath, datetime_format=date_format)

    dataframe.to_excel(excel_writer=writer, header=header, index=index, sheet_name=sheet_name,
                        encoding=encoding, float_format=float_format)

    writer.close()


def read_csv_file(filepath, sep=';', encoding=None, engine='python'):

    return pd.read_csv(filepath_or_buffer=filepath, sep=sep, encoding=encoding, engine=engine)


def read_excel_file(filepath, converters=None, dtype=None):

    return pd.read_excel(io=filepath, converters=converters, dtype=dtype)


def read_html_file(filepath):
    return pd.read_html(io=filepath)


def copy_file(origin_file, destination_file):

    copyfile(origin_file, destination_file)


def move_file(origin_file, destination_file):

    copyfile(origin_file, destination_file)
    os.remove(origin_file)


def delete_file(filepath):

    os.remove(filepath)


def wait(seconds):

    time.sleep(seconds)


def wait_file_download(directory=None, prefix=None, suffix=None, timeout=600):


    # Set default Downloads Folder
    if directory == None:
        directory = get_downloads_path()

    files = list_dir(path=directory, prefix=prefix, suffix=suffix)

    seconds = 0
    while seconds < timeout:

        try:
            file_path = sorted(files, 
                key=lambda x: os.path.getmtime(os.path.join(directory, x)), 
                reverse=True)[0]
        except:
            pass

        if '.crdownload' in str(file_path):
            seconds += 1
            time.sleep(1)
        else:
            return True

    raise Exception('Timeout waitFileDownload Function')


def get_last_downloaded_file(file_name_prefix=None, file_name_suffix=None):
    file_list = list_dir(prefix=file_name_prefix, suffix=file_name_suffix)
    
    return sorted(file_list, key=os.path.getmtime, reverse=True)[0]


def file_is_updated(filepath, referenceDate):

    date = datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%d")

    if date >= referenceDate:
        return True
    else:
        return False


def file_to_dataframe(filepath, encoding=None, engine='python', converters=None, dtype=None):
    """
    Import file types: XLS, XLSX e CSV

    Its necessary to send a string with the path of the files without the 
        slash at the end of the directory
    """

    if filepath.endswith("xlsx") or filepath.endswith("xls"):
        dataFrame = read_excel_file(filepath=filepath, converters=converters, dtype=dtype)

    elif filepath.endswith('csv'):
        try:
            dataFrame = read_csv_file(filepath, sep=';', encoding=encoding, engine=engine)
        except:
            dataFrame = read_csv_file(filepath, sep=',', encoding=encoding, engine=engine)
    return dataFrame


def return_dataframe_from_restricted_excel(filepath, sheet, cells_range):
    """ 
    Open restricted files if the user on the machine have access
    """
    wb = xw.Book(filepath)
    sheet = wb.sheets[sheet]
    df = sheet[cells_range].options(pd.DataFrame, index=False, header=True).value

    return df


def data_frame_to_clipboard(dataFrame, sep=',', index=False, header=False):
    dataFrame.to_clipboard(sep=sep, index=index, header=header)


def get_json(file):
    parametros = json.loads(open (file).read())
    
    return parametros


def get_json_value(json, key):
    return json[key]


def is_nan(value):
    if value != value or value == '' or value == 'NULL' or value == 'null' or value == 'Null' or value == None:
        result = True
    else:
        result = False

    return result


def add_quotation_mark(value):
    
    if value != 'NULL':
        # remove all Single Quotation Marks
        value = str(value).replace("'","")
        
        # add HANA String Quotation Marks around the value
        value = "'{}'".format(value)
    
    return value


def convert_number_to_datetime(number):

    try:
        date = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(number) - 2)
        #hour, minute, second = floatHourToTime(date % 1)
        
        hour, rest = divmod((number % 1 * 24), 1)
        minut, rest = divmod(rest*60, 1)
        
        date = date.replace(hour=int(hour), minute=int(minut), second=int(rest*60))
    except:
        raise Exception('Convert Number to Datetime failed, update function "convert_number_to_datetime"\nDate: {}'.format(date))
    return date


def get_file_creation_date(filepath, dateFormat):
    
    if dateFormat == None:
    
        date = datetime.fromtimestamp(os.path.getctime(filepath))
    else:
        
        date = datetime.strptime(str(datetime.fromtimestamp(os.path.getctime(filepath)))[:10], '%Y-%m-%d').strftime(dateFormat)
    return date

def create_directory(directory):
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass


def is_nan(value):
    if value != value or value == '' or value == 'NULL' or value == 'null' or value == 'Null' or value == None:
        result = True
    else:
        result = False

    return result


def list_dir(path, suffix=None):

    if platform.system() == 'Windows':
        dir = '{}\\'.format(path)
    else:
        dir = path
    
    files = os.listdir(dir)
    
    if suffix:
        return [ filename for filename in files if filename.endswith( suffix ) ]
    else:
        return files


def get_downloads_path():
    return os.path.join(os.path.expanduser("~"), 'Downloads')


def get_file_name_from_path(path):
    return os.path.basename(path)
