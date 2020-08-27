import pandas as pd
import operator


files = [r"C:\Users\keith_bailey\Documents\MarketData2\ABTTO_dataMarketData2020-06-03_14.47.41.csv", r"C:\Users\keith_bailey\Documents\MarketData2\APPN_dataMarketData2020-08-11_20.55.41.csv"]
print(files)

consol_df = None

for file in files:

    data = pd.read_csv(file)
    # properly timestamp data to allow for proper aggregation of multiple files

    def clean_table(df):

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

            #clean_up
            cols = [s.replace(leading_column_string, '') for s in cols]
            cols = [s.replace("(", '') for s in cols]
            cols = [s.replace(")", '') for s in cols]

            return leading_column_string, cols;
        co_name, clean_cols = clean_leading_columns(df.columns[1:])
        clean_cols = [df.columns[0]] + clean_cols
        # add new column to df
        df.columns = clean_cols
        df['co_name'] = co_name

        return df
        #print(co_name)
        #print(clean_cols)

    clean_df = clean_table(data)

    cols_to_rows = list(clean_df.columns)
    cols_to_rows.remove("Period")
    cols_to_rows.remove("co_name")

    tidy_df = pd.melt(clean_df, id_vars=["Period", "co_name"], value_vars=cols_to_rows)
    tidy_df.dropna(subset = ["value"], inplace=True)

    if not isinstance(consol_df, pd.DataFrame):
        consol_df = tidy_df
    else:
        frames = [consol_df, tidy_df]
        consol_df = pd.concat(frames, ignore_index=True)



print(consol_df)



