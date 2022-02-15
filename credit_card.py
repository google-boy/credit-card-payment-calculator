"""Perform credit card calculations"""
from argparse import ArgumentParser
from json.tool import main
import sys

def get_min_payment(balance, fees=0):
    '''
    Compute the minimum credit card payment
    balance = balance left to pay
    fees = 
    '''
    min_payement = (balance * (0.02)) + fees

    if min_payement < 25:
        min_payement = 25
    
    return min_payement

def interest_charged(balance, apr):
    '''Compute the interest accrued in the next payment'''
    i = ((apr/100)/365)*balance*30
    return i

def remaining_payments(balance, apr, targetamount, credit_line=5000, fees=0):
    '''Compute the number of payements required to pay off the credit card balance'''
    count = 0
    count75 = 0
    count50 = 0
    count25 = 0
    payment = targetamount
    while balance > 0:
        if targetamount is None:
            payment = get_min_payment(balance, fees)

        paymentamount = payment - interest_charged(balance,apr)

        if paymentamount < 0:
            sys.exit("The card balance cannot be paid off")
        balance -= paymentamount
        count += 1
        if balance > 75/100 * credit_line:
            count75 += 1
        if balance > 50/100 * credit_line:
            count50 += 1
        if balance > 25/100 * credit_line:
            count25 += 1
        
    return count,count75,count50,count25

def main(balance_amount, apr, targetamount, credit_line=5000, fees=0):
    pays_minimum = False
    min_payment = get_min_payment(balance_amount, fees)
    print(f"Your recommended starting minimum payement is ${min_payment}")

    if targetamount is None:
        pays_minimum = True
    elif targetamount < min_payment:
        print("Your target payment is less than the minimum payment for this credit card\n")
        sys.exit()
    
    counter = remaining_payments(balance_amount, apr, targetamount, credit_line, fees)
    if pays_minimum:
        print(f"If you pay the minimum payments each month, you will pay off the balance in {counter[0]} payments", end='\n')
    else:
        print(
            f"If you make payments of ${targetamount}, you will pay off the balance in {counter[0]} payments",
            end='\n'
        )
    
    return f"You will spend a total of {counter[3]} months over 25% of the credit line \
    \nYou will spend a total of {counter[2]} months over 50% of the credit line \
    \nYou will spend a total of {counter[1]} months over 75% of the credit line"
    

def parse_args(args_list):
    """
    Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list): the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = ArgumentParser()

    parser.add_argument(
        'balance_amount',
        type=float,
        help='The total amount of balance left on the credit acount'
    )
    parser.add_argument(
        'apr',
        type=int,
        help='The annual APR, should be an int between 1 and 100'
    )
    parser.add_argument(
        'credit_line',
        type=int,
        help='The maximum amount balance allowed on the credit card'
    )
    parser.add_argument(
        '--payment',
        type=int,
        default=None,
        help='The amount the user wants to pay per payment, should be a positive number'
    )
    parser.add_argument(
        '--fees',
        type=float,
        default=0,
        help='The fees that are applied monthly.'
    )

    # parse and validate arguments
    args = parser.parse_args(args_list)

    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    
    return args

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))

    print(main(
        arguments.balance_amount,
        arguments.apr,
        credit_line=arguments.credit_line,
        targetamount=arguments.payment,
        fees=arguments.fees
    ))