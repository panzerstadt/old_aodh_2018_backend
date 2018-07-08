import datetime
import time


def str_2_datetime(str_in, input_format='%Y-%m-%d', timezone='JST'):
    #separator = find_sep(input_format)
    #struct_time = str_2_struct_time(str_in, input_format=input_format)
    response = datetime.datetime.strptime(str_in, input_format)
    # # todo
    # if timezone == 'JST':
    #     response_with_timezone = response.replace(tzinfo=pytz.timezone('Japan'))
    # else:
    #     # todo not implemented
    #     response_with_timezone = response.replace(tzinfo=pytz.timezone('Japan'))

    return response


def datetime_2_str(datetime_in, output_format='%Y-%m-%d'):
    return time.strftime(output_format, datetime_in.timetuple())