"""
Creator: Mickey Gordon
No usage limitations with appropriate citations.
Initial upload: 06/17/2020

Last updated: 08/19/2020
Recent update: added module 5 (A/R turnover calculator)
"""

import babel.numbers as bn
import pandas as pd
import decimal as de
import sys
from pandas import DataFrame
import matplotlib.pyplot as plt

calcMode = input("""
Please choose calculator mode:
(1) Depreciation calculator
(2) Investment growth calculator
(3) Loan amortization calculator
(4) Present/future value calculator
(5) A/R turnover calculator
> """)

if "1" in calcMode:
    """DEPRECIATION CALCULATOR"""
    
    # Step 1- Type of depreciation
    depre_type = input("""> Method of depreciation:
    [s] Straight Line 
    [d] Declining Balance 
    [u] Units of Production 
        > """)
        
    # Control for invalid inputs
    control = ['s', 'd', 'u']
    if depre_type in control: 
    
        # Declining balance multiple and UOP units
        if "d" in depre_type:
            db_mult = float(input("> What multiple of the Straight Line rate? "))
            Use_life = float(input("> What is the estimated life of the asset? "))
        elif "s" in depre_type:
            Use_life = float(input("> What is the estimated life of the asset? "))
        elif "u" in depre_type:
           units_UOP = float(input("> How many units will be produced over the life of the asset? "))
           est_years = int(input("> How many years will the asset be in service? "))
           amts = []
           ctrl_amts = 0
           for year in range(1, est_years + 1):
               amt = float(input(f"Year {year} usage: "))
               amts.append(amt)
               ctrl_amts += amt
           if ctrl_amts != units_UOP:
                print("Error: Annual amounts entered don't add up to total number of units previously entered. Program will reset.")
                sys.exit()
                
        # Step 2- Financial information
        cost = float(input("> What is the cost of the asset? "))
        SV_yesno = input("> Is there a salvage value (yes or no)? ")
        if "y" in SV_yesno:
            Salvage = float(input("> What is the salvage value? "))
        else:
            Salvage = 0
            
        
    # Straight Line Output
        if 's' in depre_type:
            # Design DataFrame
            def dFrame (Use_life, listBal):
                listYears = []
                Use_life = int(Use_life)
                for year in range(1, Use_life + 1):
                    listYears.append(year)

                d = {'Year': listYears, 'Book Value': listBal}
                df = DataFrame(d, columns=['Year','Book Value'])
                df.plot(x='Year', y='Book Value', kind='line')
                plt.show()
                
            SL_Output = round((float(cost) - float(Salvage)) / float(Use_life),5)
            print("=" * 48)
            print("%29s" % "**Summary**\n")
            print("%7s%18s" % ("Method:","Straight-Line"))
            print("%11s%14s" % ("Cost basis:", bn.format_currency(de.Decimal(cost),"USD")))
            if Salvage > 0:
                print("%14s%11s" % ("Salvage value:", bn.format_currency(de.Decimal(Salvage),"USD")))
            print("%12s%6d%7s" % ("Useful life:", Use_life, "years"))
            print("-" * 48)
            print("%36s" % "**Depreciation Schedule**\n")
            print("%6s%15s%13s%12s" % ("Year", "Depreciation", "Cumulative", "Book Value"))
            print("-" * 48)
            listBal = []
            for num in range(1, int(Use_life) + 1):
                annual = float(SL_Output * num)
                bv = float(cost) - annual
                listBal.append(bv)
                print("%6s%15s%13s%12s" % (num, bn.format_currency(de.Decimal(SL_Output),"USD"), bn.format_currency(de.Decimal(annual),"USD"), bn.format_currency(de.Decimal(bv),"USD")))
            print("=" * 48)
            dFrame(Use_life, listBal)
        
    # Declining Balance Output
        if 'd' in depre_type:
            # Design DataFrame
            def dFrame (Use_life, listBal):
                listYears = []
                Use_life = int(Use_life)
                for year in range(1, Use_life + 1):
                    listYears.append(year)
                print(listBal)
                d = {'Year': listYears, 'Book Value': listBal}
                df = DataFrame(d, columns=['Year','Book Value'])
                df.plot(x='Year', y='Book Value', kind='line')
                plt.show()
                
            depRate = float((1 / Use_life) * db_mult)
            costBasis = float(cost - Salvage)
            print("=" * 48)
            print("%29s" % "**Summary**\n")
            print("%7s%18s" % ("Method:","Declining balance"))
            print("%11s%14s" % ("Cost basis:", bn.format_currency(de.Decimal(cost),"USD")))
            if Salvage > 0:
                print("%14s%11s" % ("Salvage value:", bn.format_currency(de.Decimal(Salvage),"USD")))
            print("%12s%7d%6s" % ("Useful life:", Use_life, "years"))
            print("%14s%11.1f" % ("Multiple used:", db_mult))
            print("-" * 48)
            print("%36s" % "**Depreciation Schedule**\n")
            print("%6s%15s%13s%12s" % ("Year", "Depreciation", "Cumulative", "Book Value"))
            print("-" * 48)
            accDep = 0.0
            listBal = []
            for num in range(1, int(Use_life) + 1):
                depExp = depRate * (costBasis - accDep)
                accDep += depExp
                bv = costBasis - accDep
                listBal.append(bv)
                print("%6d%15s%13s%12s" % (num, bn.format_currency(de.Decimal(depExp),"USD"), bn.format_currency(de.Decimal(accDep),"USD"), bn.format_currency(de.Decimal(bv),"USD")))
            print("- " * 24)
            print("Remaining balance to be depreciated:",bn.format_currency(de.Decimal(bv),"USD"))
            print("=" * 48)
            dFrame(Use_life, listBal)
        
    # UOP Output
        if 'u' in depre_type:
            # Design DataFrame
            def dFrame (est_years, listBal):
                listYears = []
                est_years = int(est_years)
                for year in range(1, est_years + 1):
                    listYears.append(year)
                
                d = {'Year': listYears, 'Book Value': listBal}
                df = DataFrame(d, columns=['Year','Book Value'])
                df.plot(x='Year', y='Book Value', kind='line')
                plt.show()
                
            unitDep = (float(cost) - float(Salvage)) / float(units_UOP)
            netCost = float(cost - Salvage)
            print("=" * 48)
            print("%29s" % "**Summary**\n")
            print("%7s%20s" % ("Method:","Units of production"))
            print("%11s%16s" % ("Cost basis:", bn.format_currency(de.Decimal(cost),"USD")))
            if Salvage > 0:
                print("%14s%13s" % ("Salvage value:", bn.format_currency(de.Decimal(Salvage),"USD")))
            print("%12s%9d%6s" % ("Useful life:", est_years, "years"))
            print("%14s%11s" % ("Estimated units:", bn.format_number(units_UOP)))
            print("%14s%13s" % ("Cost per unit:", bn.format_currency(de.Decimal(unitDep),"USD")))
            print("-" * 48)
            print("%36s" % "**Depreciation Schedule**\n")
            print("%6s%15s%13s%12s" % ("Year", "Depreciation", "Cumulative", "Book Value"))
            print("-" * 48)
            year = 1
            accDep = 0.0
            listBal = []
            for amt in amts:
                depExp = amt * unitDep
                accDep += depExp
                bv = netCost - accDep
                listBal.append(bv)
                print("%6d%15s%13s%12s" % (year, bn.format_currency(de.Decimal(depExp),"USD"), bn.format_currency(de.Decimal(accDep),"USD"), bn.format_currency(de.Decimal(bv),"USD")))
                year += 1
            print("=" * 48)
            dFrame(est_years, listBal)
    else:
        print("Error! Invalid input.\nPlease enter s, d, or u.\nProgram will reset.")

elif "2" in calcMode:
    """INVESTMENT CALCULATOR"""
    # Define function to display output
    def intCalc(rate, totalInterest, startBalance, years):
        # Display table header
        print("=" * 48)
        print("%4s%18s%10s%16s" % \
              ("Year", "Starting Balance",
               "Interest", "Ending Balance"))
        print("%4s%18s%10s%16s" % ("-" * 4, "-" * 16, "-" * 8, "-" * 14,))
        listBal = []
        # Compute and display the results for each year
        for year in range (1, years + 1):
            interest = startBalance * rate
            endBalance = startBalance + interest
            listBal.append(endBalance)
            print("%4s%18s%10s%16s" % \
                  (year, bn.format_currency(de.Decimal(startBalance),"USD"), bn.format_currency(de.Decimal(interest),"USD"), bn.format_currency(de.Decimal(endBalance),"USD")))
            startBalance = endBalance
            totalInterest += interest
            
        # Display the totals for the period
        print("-" * 48)
        print("Ending balance: %11s" % bn.format_currency(de.Decimal(endBalance),"USD"), "\nTotal interest: %11s" % bn.format_currency(de.Decimal(totalInterest),"USD"))
        print("=" * 48)
    
    # Accept inputs
    startBalance = float(input("Enter the investment amount: "))
    years = int(input("Enter the number of years: "))
    rate = float(input("Enter the rate as a %: "))
    
    # Convert rate to decimal number
    rate = rate / 100
    
    # Initialize the interest accumulation
    totalInterest = 0.0
    
    # Call function with variables
    intCalc(rate, totalInterest, startBalance, years)
    
    # Design DataFrame
    listYears = []
    for year in range(1, years + 1):
        listYears.append(year)
    
    listBal = []
    for year in range (1, years + 1):
        interest = startBalance * rate
        endBalance = startBalance + interest
        listBal.append(endBalance)
        startBalance = endBalance
        
    d = {'Year': listYears, 'Balance': listBal}
    df = DataFrame(d, columns=['Year','Balance'])
    df.plot(x='Year', y='Balance', kind='line')
    plt.show()

elif "3" in calcMode:
    """LOAN AMORTIZATION CALCULATOR"""
    
    # Declare DataFrame function
    def dFrame (loan, years, interest, apr, pymt):
        listYears = []
        for year in range(1, years + 1):
            listYears.append(year)
        
        listBal = []
        loan = loan
        for year in range (1, years + 1):
            interest = apr * loan
            principal = pymt - interest
            listBal.append(loan)
            loan -= principal

        d = {'Year': listYears, 'Carry Value': listBal}
        df = DataFrame(d, columns=['Year','Carry Value'])
        df.plot(x='Year', y='Carry Value', kind='line')
        plt.show()
        
    # Accept loan amount
    loan = float(input("Enter the loan amount: "))
    
    # Accept loan interest rate and convert to decimal
    apr = float(input("Enter the annual interest rate as a %: "))
    apr /= 100
    
    # Accept loan duration
    years = int(input("Enter the number of years of the loan: "))
    
    # Accept loan start date and convert to python-readable date
    start = str(input("Enter start date in format mm/dd/yyyy: "))
    startYear = int(start[6:10])
    startMonth = int(start[0:2])
    startDay = int(start[3:5])
    startDate = bn.date_(startYear, startMonth, startDay)
    print(startDate)
    
    print("=" * 60)
    print("%43s" % "**Amortization Schedule**\n")
    print("%4s%18s%12s%12s%14s" % ("Date", "Payment", "Interest", "Principal",
    "Carry Value"))
    print("-" * 60)
    print("%10s%50s" % (startDate, bn.format_currency(de.Decimal(loan), "USD")))
    
    # Calculate annuity factor for loan
    annuityFactor = float((apr * ((1 + apr) ** years)) / (((1 + apr) ** years) - 1))
    
    loan1 = loan
    startYear += 1
    startDate = bn.date_(startYear, startMonth, startDay)
    pymt = annuityFactor * loan
    totalInterest = 0.0
    for year in range(1, years + 1):
        interest = apr * loan1
        principal = pymt - interest
        loan1 -= principal
        print("%10s%12s%12s%12s%14s" % (startDate, bn.format_currency(de.Decimal(pymt), "USD"), bn.format_currency(de.Decimal(interest), "USD"),bn.format_currency(de.Decimal(principal), "USD"), bn.format_currency(de.Decimal(loan1), "USD")))
        startYear += 1
        startDate = bn.date_(startYear, startMonth, startDay)
        totalInterest += interest
    print("-" * 60)
    print("%20s%11s" % ("Total Interest Paid:", bn.format_currency(de.Decimal(totalInterest), "USD")))
    print("=" * 60)
    
    # Call DataFrame function
    dFrame(loan, years, interest, apr, pymt)

elif "4" in calcMode:
    """PRESENT/FUTURE VALUE CALCULATOR"""
    method = input("Present value calculation (PV) or future value calculation (FV)? ")
    PV_control = ['PV', 'pv']
    FV_control = ['FV', 'fv']
    control = PV_control + FV_control
    
    if method not in control:
        print("Error: invalid input./nProgram will reset.")
        sys.exit()
    periods = int(input("Enter the number of years: "))
    pds = str(periods)
    rate = float(input("Enter the discount rate as a %: "))
    rt = str(rate)
    rate /= 100
    
    if method in PV_control:
        amount = float(input("Enter the amount to be discounted: "))
        amt1 = bn.format_currency(de.Decimal(amount),"USD")
        denominator = (1 + rate) ** periods
        discounted = amount / denominator
        disc = bn.format_currency(de.Decimal(discounted),"USD")
        result = f"{amt1} discounted at {rt}% for {pds} years is worth {disc}."
        print("-" * len(result))
        print(result)
        print("-" * len(result))
    else:
        amount = float(input("Enter the present amount: "))
        amt1 = bn.format_currency(de.Decimal(amount),"USD")
        calc = (1 + rate) ** periods
        discounted = amount * calc
        amt2 = bn.format_currency(de.Decimal(discounted),"USD")
        result = f"In {pds} years, {amt1} growing at {rt}% annually will be worth {amt2}."
        print("-" * len(result))
        print(result)
        print("-" * len(result))
        
elif "5" in calcMode:
    """A/R TURNOVER CALCULATOR"""
    print("""\n\nEnsure that the list is formatted as a CSV file in the same folder as this Python file. It must be in the format:
        ___________________________________
        Date      AR_Sale     AR_Collection
        1/1/20    8480          8393
        ...       ...           ...
        ___________________________________
    """)
    
    filename = input("What is the file name (i.e., AR_Sales.csv)? ")
    # Import csv file with A/R data
    file = pd.read_csv(filename, usecols=['Date', 'AR_Sale', 'AR_Collection'])
    
    # Convert A/R sales data to iterable list
    df = pd.DataFrame(file, columns= ['AR_Sale'])
    sales = df['AR_Sale'].values.tolist()
    
    # Calculate average A/R balance for the period
    beg_ar = sales[0]
    end_ar = sales[-1]
    avg_ar = (beg_ar + end_ar)/2
    
    # Calculate total credit sales
    net_sales = sum(sales)
    
    # Convert A/R collections data to iterable list
    df = pd.DataFrame(file, columns= ['AR_Collection'])
    collections = df['AR_Collection'].values.tolist()
    total_coll = sum(collections)
    percent = total_coll / net_sales
    percent *= 100
    
    # Calculate A/R turnover ratio
    turnover_ratio = net_sales / avg_ar
    
    # Format inputs
    beg_ar = bn.format_currency(de.Decimal(beg_ar), "USD")
    end_ar = bn.format_currency(de.Decimal(end_ar), "USD")
    avg_ar = bn.format_currency(de.Decimal(avg_ar), "USD")
    total_sales = bn.format_currency(de.Decimal(net_sales), "USD")
    turnover_ratio = round(turnover_ratio,1)
    percent = round(percent)
    
    # Print summary
    print("=" * 36)
    print("%23s" % "**Summary**\n")
    print("%11s%14s" % ("Beginning A/R Balance:", beg_ar))
    print("%11s%17s" % ("Ending A/R Balance:", end_ar))
    print("%11s%16s" % ("Average A/R Balance:", avg_ar))
    print("%11s%24s" % ("Total Sales:", total_sales))
    print("%11s%17s\n" % ("A/R Turnover Ratio:", turnover_ratio))
    print("%11s%13s%0s" % ("Percent A/R Collected:", percent, "%"))
    print("=" * 36)
    
    # Construct collection % pie chart
    collected = int(percent)
    uncollected = 100 - collected
    coll_label = f"Collected: {collected}%"
    uncoll_label = f"Uncollected: {uncollected}%"
    df = pd.DataFrame({'A/R Collections': [collected, uncollected]}, index=[coll_label, uncoll_label])
    plot = df.plot.pie(y='A/R Collections', figsize=(5, 5))
    
else:
    print("Invalid entry. Please choose 1, 2, 3, 4, or 5.\nProgram restarting.")
