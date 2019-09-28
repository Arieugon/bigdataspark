import pandas as pd
import datetime as dt

# split file
def split_file(input_file, file_len = 100000):

    dest_files = list()
    dest_filenames = list()

    file_num = 1

    with open(input_file, 'r') as source_f:
        for l, line in enumerate(source_f):
            if not l % file_len:
                dest_filename = 'sales_data_part_' + str(file_num) + '.csv'

                dest_files.append((dest_filename, open(dest_filename, 'w')))

                file_num += 1
                print('Writing file ' + dest_files[-1][0], end = '\r')

            dest_files[-1][1].write(line)

    for name, dest_file in dest_files:
        dest_file.close()
        dest_filenames.append(name)
        print('Closing file ' + name, end = '\r')

    print('\nFinished!')
    return dest_filenames

# read data
def read_sales_data(file, nrows = None):

    # read file
    df = pd.read_csv(file, sep = '|', header = None, nrows = nrows)

    df.columns = ['product_id', 'store_id', 'date', 'quantity', 'price']

    cols = ['date', 'quantity', 'price']

    for col in cols:
        df[col] = df[col].str[1:-1].str.split(',')

    df.quantity = df.quantity.apply(lambda x:[int(i) for i in x])
    df.price = df.price.apply(lambda x:[float(i) for i in x])
    
    return df

# map function
def my_map(df_in, my_fun):
    df_out = df_in.apply(my_fun, axis = 1)
    return df_out

# reduce function
def my_reduce(df_01, df_02, my_fun):
    df_out = pd.concat([df_01, df_02])
    
    return my_fun(df_out)