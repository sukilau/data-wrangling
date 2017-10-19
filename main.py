# scripting language : Python 3.6
# module : Pandas 

import pandas as pd

# read logfile
filename = "logfile.tsv"
df = pd.read_csv(filename, sep='\t', header=0)

# rename column name
df.rename(columns={'# date':'date'}, inplace=True)

# convert 'date' to timestamp
df['date'] = pd.to_datetime(df['date'])

def total_data_transfer(df, start_date, end_date, filetype, showlog=0):
    """
    Compute total data transfer of filetype from start_date to end_date
    """
    # add file_check column to store boolean value for filetype
    suffix ='.'+filetype
    df['file_check']  = list(map(lambda x: x.endswith(suffix), df['url']))
   
    # add date_check column to store boolean value for date range
    start_date = pd.Timestamp(start_date) - pd.Timedelta('1D')
    end_date = pd.Timestamp(end_date) + pd.Timedelta('1D')
    df['date_check']  = list(map(lambda x: x>start_date and x<end_date , df['date']))
    
    short_df = df[df['file_check'] & df['date_check']]
    
    # print log file if showlog=1 
    if showlog:
        print(short_df)
        
    return sum(short_df['size'])
    
    
total = total_data_transfer(df, start_date='2017-08-24', end_date='2017-08-25', filetype='jpg', showlog=1)

print("Total data transfer: {} bytes ({} MB)".format(total, total/1000000))