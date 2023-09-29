# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    
    for date_str in old_dates:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        new_date = date.strftime('%d %b %Y')
        new_dates.append(new_date)
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError()
    if not isinstance(n, int):
        raise TypeError()
    try:
        start = datetime.strptime(start, "%Y-%m-%d")
    except ValueError:
        raise ValueError("start date format should be yyyy-mm-dd")
    date_sequence = [start + timedelta(days=i) for i in range(n)]
    return date_sequence


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    if not isinstance(values, list):
        raise TypeError()
    if not isinstance(start_date, str):
        raise TypeError()
    date_sequence = date_range(start_date, len(values))
    return list(zip(date_sequence, values))

def hp4_util(infile):
    
    header = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    with open(infile, 'r') as file:
        
        a = DictReader(file, fieldnames=header)
        
        data = [row for row in a]

        data.pop(0)
    
    return data
    
def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    dict_for_output = hp4_util(infile)
    late_fees_dict = defaultdict(float)

    for entry in dict_for_output:
       
        patron = entry['patron_id']
        due_as_per = datetime.strptime(entry['date_due'], '%m/%d/%Y')
        returned_as_per = datetime.strptime(entry['date_returned'], '%m/%d/%Y')
        days_late_fees = (returned_as_per - due_as_per).days
        late_fees_dict[patron]+= 0.25 * days_late_fees if days_late_fees > 0 else 0.0
    
    res_line = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in late_fees_dict.items()
    ]
    with open(outfile, 'w') as file_fee:
        rd = DictWriter(file_fee, ['patron_id', 'late_fees'])
        rd.writeheader()
        rd.writerows(res_line)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
