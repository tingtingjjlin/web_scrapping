"""function to summerize spend for grocery."""

import pandas as pd
import numpy as np
import argparse

print(' ==== current keywords ======')
kws = ['TRADER JOE', 'WHOLEFDS', 'SAFEWAY', 'MARKET']
print(kws)

parser = argparse.ArgumentParser(description='Process some transactions')
parser.add_argument('--filename', default=None,
                    help='full path of the transaction file')
parser.add_argument('--start_date', default=None,
                    help='start date of transactions')
parser.add_argument('--end_date', default=None,
                    help='end date of transactions')

args = parser.parse_args()

# get arguements from commend line
filename = args.filename
start_date = args.start_date
end_date = args.end_date


def spend_calculator(filename, kewwords, start_date, end_date):
    """Function to summerize transactions."""
    # read Amex transaction csv and subset to useful columns
    dat = pd.read_csv(filename, header=None)[[0, 2, 7]]
    # rename columns and convert format
    dat.columns = ["event_day", "merchant", "value"]
    dat["event_day"] = pd.to_datetime(dat["event_day"])

    # subset transaction data to required date range
    if start_date is not None:
        dat_sub = dat.loc[dat["event_day"] >= start_date]
    if end_date is not None:
        dat_sub = dat_sub.loc[dat_sub["event_day"] <= end_date]

    total_details = pd.DataFrame()

    for k in kws:
        print("======= " + k + " ==========")

        # select transaction based on keyword
        values = dat_sub[[k in x for x in dat_sub['merchant']]]
        if values.shape[0] != 0:
            print(values)

        # save selected transaction to a data frame
        total_details = total_details.append(values)

        print('--------------------------')
        print(k + ':' + str(np.sum(values['value'])))

    print('=========== Total Transactions ===========')
    print(total_details)

    # calculate the total amount of transactions that match the keywards
    total_amount = np.sum(total_details['value']).round(0)
    amount_per_person = total_amount/2

    pd.DataFrame.to_csv(total_details,
                        """/home/tingtingl/grocery/transaction_{}_to_{}.csv""".format(start_date, end_date))
    print("""The total amount from {} to {} is {};
            The amount per person is {}""".format(start_date,
                                                  end_date,
                                                  total_amount,
                                                  amount_per_person))

if __name__ == "__main__":
    spend_calculator(filename=filename, kewwords = kws, start_date = start_date, end_date= end_date)
