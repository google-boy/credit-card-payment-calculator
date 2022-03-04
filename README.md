# Credit Card Payment Calculator

A script for calculating credit payments (Not actuall). It can only be run from the command-line.

## Running the script

The script takes 3 mandatory arguments and two optional arguments.

### Arguments

- balance_amount: Mandatory. The balance on the credit account to be paid.

- apr: Mandatory. The annual APR, a value between 1 and 100.

- credit_line: Mandatory. the maximum amount of balance allowed on the credit line.

- payment: Optional. The amount a user would like to make per payment.

- fees: Optional. Fees applicable to the credit card.

Run the script on the command-line, passing the mandatory payments and optionally the optional arguments, for example

    python credit_card.py 15000 10 17000 --payment 400 --fees 35

### Future Improvements
