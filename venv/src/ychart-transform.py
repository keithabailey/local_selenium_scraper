import pandas as pd
import numpy as np
import operator
import glob
import datetime

csv_list = [f for f in glob.glob("./report_output/*.csv")]

# construct dataframe of the files
csv_series= pd.Series(csv_list)
file_list = csv_series[csv_series.str.match("(.*_dataQtrYoYGrowth.*|.*_dataMarketData.*)")]
print(file_list)

time_stamp = file_list.str.extract("([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9])", expand=False)
time_stamp = [datetime.datetime.strptime(x,"%Y-%m-%d_%H.%M.%S") for x in time_stamp]


files_df = pd.DataFrame(list(zip(file_list, time_stamp)),
                columns = ["file_name","time_stamp"])


def clean_table(df, timest):
    def allsame(seq):
        "Determines whether all the elements in a sequence are the same."

        # Compare all the elements to the first in the sequence,
        # then do a logical and (min) to see if they all matched.
        return min([elem == seq[0] for elem in seq] + [True])

    def getcommonstart(seqlist):
        """Returns the common prefix of a list of sequences.

        Raises an exception if the list is empty.
        """
        # if not seqlist: return None
        m = [allsame(seq) for seq in zip(*seqlist)]  # Map the matching elements
        m.append(False)  # Guard in case all the sequences match
        return seqlist[0][0:m.index(False)]  # Truncate before first mismatch

    def clean_leading_columns(cols):
        leading_column_string = getcommonstart(cols)

        # clean_up columns
        cols = [s.replace(leading_column_string, '') for s in cols]
        cols = [s.replace("(", '') for s in cols]
        cols = [s.replace(")", '') for s in cols]

        return leading_column_string, cols;

    co_name, clean_cols = clean_leading_columns(df.columns[1:])
    clean_cols = [df.columns[0]] + clean_cols
    # add new columns to df
    df.columns = clean_cols
    df['co_name'] = co_name
    df['created_time'] = timest

    return df

consol_df = None

for index, row in files_df.iterrows():

    data = pd.read_csv(row["file_name"])
    # properly timestamp data to allow for proper aggregation of multiple files


    clean_df = clean_table(data, row["time_stamp"])

    cols_to_rows = list(clean_df.columns)
    cols_to_rows.remove("Period")
    cols_to_rows.remove("co_name")
    cols_to_rows.remove("created_time")

    tidy_df = pd.melt(clean_df, id_vars=["Period", "co_name","created_time"], value_vars=cols_to_rows)
    tidy_df.dropna(subset = ["value"], inplace=True)

    if not isinstance(consol_df, pd.DataFrame):
        consol_df = tidy_df
    else:
        frames = [consol_df, tidy_df]
        consol_df = pd.concat(frames, ignore_index=True)


consol_df.to_csv("full_historical_data.csv")

consol_df_gb = consol_df.groupby(['Period','co_name','variable'])\
    .apply(lambda x: x.sort_values(['created_time'], ascending = False)).\
    reset_index(drop=True)

print(consol_df_gb)

final = consol_df_gb.groupby(['Period','co_name','variable']).head(1)

final.to_csv("top_records.csv")

print(final)

# from instruction file, translate those that are asbolute $ numbers into USD at todays exchange rate
# if not a match, raise a warning and make NA in the resulting data