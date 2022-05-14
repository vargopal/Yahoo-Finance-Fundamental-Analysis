from ssl import ALERT_DESCRIPTION_UNKNOWN_PSK_IDENTITY
import pandas as pd
import yahoo_fin.stock_info as yf

balance_sheet = []
income_statement = []
cash_flow_analysis = []
years = []

tickers = yf.tickers_sp500()


def get_data(ticker):
    global balance_sheet
    global income_statement
    global cash_flow_analysis
    global years
    balance_sheet = yf.get_balance_sheet(ticker)
    income_statement = yf.get_income_statement(ticker)
    cash_flow_analysis = yf.get_cash_flow(ticker)
    years = balance_sheet.columns

profitability_score = 0
def profitability():
    global profitability_score
    """ 
    ROA, Operating Cash Flow, Change in ROA, and Accruals
    """
    # Income
    net_income = income_statement[years[0]]['netIncome']
    if net_income > 0:
        ni_score = 1
    else:
        ni_score = 0
    net_income_diff = net_income - income_statement[years[1]]['netIncome']
    if net_income_diff > 0:
        ni_score_2 = 1
    else:
        ni_score_2 = 0
    # Operating Cash Flows
    cash_flow = cash_flow_analysis[years[0]]['totalCashFromOperatingActivities']
    if cash_flow > 0:
        op_cf_score = 1
    else:
        op_cf_score = 0
    
    # Change in ROA
    avg_assets_1 = (balance_sheet[years[0]]['totalAssets'] + balance_sheet[years[1]]['totalAssets'])/2   
    avg_assets_2 = (balance_sheet[years[1]]['totalAssets'] + balance_sheet[years[2]]['totalAssets'])/2   
    RoA = net_income/avg_assets_1
    RoA_prior = income_statement[years[1]]['netIncome']/avg_assets_2
    if RoA > RoA_prior:
        RoA_score = 1
    else:
        RoA_score = 0

    # Accruals
    total_assets = balance_sheet[years[0]]['totalAssets']
    accruals = cash_flow/total_assets - RoA
    if accruals > 0:
        ac_score = 1
    else:
        ac_score = 0

    profitability_score = ni_score + ni_score_2 + op_cf_score + RoA_score + ac_score
    print(profitability_score)

leverage_score = 0
def leverage():
    global leverage_score
    """
    Leverage, Liquidity, and Sources of Funds
    """

    # Leverage Exposure
    try:
        lt_debt = balance_sheet[years[0]]['longTermDebt']
        total_assets = balance_sheet[years[0]]['totalAssets']
        debt_ratio = lt_debt /total_assets

        if debt_ratio >= 0.4:
            debt_score = 0
        else:
            debt_score = 1
    except:
        debt_score = 1
    

    # Current Ratio
    current_assets = balance_sheet[years[0]]['totalCurrentAssets']
    current_liab = balance_sheet[years[0]]['totalCurrentLiabilities']
    current_ratio = current_assets / current_liab
    if current_ratio > 1:
        current_ratio_score = 1
    else:
        current_ratio_score = 0

    leverage_score = debt_score + current_ratio_score
    print(leverage_score)


operating_score = 0
def operating():
    global operating_score
    """
    Gross margin and asset turnover ratio
    """

    # Gross Margin
    gp = income_statement[years[0]]['grossProfit']
    gp_1 = income_statement[years[1]]['grossProfit']
    revenue = income_statement[years[0]]['totalRevenue']
    revenue_1 = income_statement[years[1]]['totalRevenue']
    gross_margin = gp/ revenue
    gross_margin_1 = gp_1/revenue_1

    if gross_margin > gross_margin_1:
        margin_score = 1
    else:
        margin_score = 0
    
    # Asset Turnover
    avg_assets_1 = (balance_sheet[years[0]]['totalAssets'] + balance_sheet[years[1]]['totalAssets'])/2   
    avg_assets_2 = (balance_sheet[years[1]]['totalAssets'] + balance_sheet[years[2]]['totalAssets'])/2   
    asset_turnover = revenue/ avg_assets_1
    asset_turnover_1 = revenue_1/ avg_assets_2

    if asset_turnover > asset_turnover_1:
        asset_turnover_score = 1
    else:
        asset_turnover_score = 0

    operating_score = margin_score + asset_turnover_score
    print(operating_score)



for ticker in tickers[40:41]:
    try:
        get_data(ticker)
        print(ticker)
        profitability()
        leverage()
        operating()
        f_score = profitability_score + leverage_score + operating_score
        print("Total Score: " + str(f_score))
    except:
        print(ticker + ": Something went wrong.")

print(income_statement)


