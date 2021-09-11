import math
from config import CONSUMER_ID, REDIRECT_URI, JSON_PATH
from account import TD_ACCOUNT
from td.client import TDClient

def mean(list = [], string = ""): # calculates mean of candles using string
    result = 0
    counter = 0
    for x in list:
        result = result + x[string]
        counter = counter + 1
    return result / counter

def highest_steep(list = [], string = ""): #finds steepest part of two candles right next to eachother
    best = {0: {}, 1: {}, "diff": 0 }
    previous = {}
    for x in list: # x = current
        if previous != {}: #first case skipped cuz no previous yet
            difference = math.floor(abs(x[string] - previous[string]) * 100) / 100 # the difference between previous and current candle

            # print(string, "1: ", previous[string])                          #
            # print(string, "2: :", x[string])                                #
            # print("difference:", difference)                                #
            # print("full decimal:", (x[string] - previous[string]), "\n")    # uncomment if u want to see candle comparsion

            if best["diff"] == 0: # second case
                best[0] = previous
                best[1] = x
                best["diff"] = difference
            elif difference > best["diff"]: # bigger difference case
                best[0] = previous
                best[1] = x
                best["diff"] = difference
        previous = x

    return best

def call(data = [], string = ""):
    if string == 'all':
        all_options = ['close', 'high', 'low', 'open', 'volume']
        for x in all_options:
                print("\nDATA FOR", x,":")
                print("The mean for", x,"on this data is", math.floor(mean(data, x)*100)/100 , "\n")
                inc_dec_result = inc_dec_counter(data, x)
                print("The candles for", x,"increased", inc_dec_result["increase"],"times")
                print("The candles for", x,"decreased", inc_dec_result["decrease"],"times\n")
                steep_result = highest_steep(data, x)
                print("The biggest steep or slope in the data for", x, "were these two candles")
                print(steep_result[0])
                print(steep_result[1], "\nThe difference for", x, "between these two candles were", steep_result["diff"])
    else:
        print("\nDATA FOR", string,":")
        print("The mean for", string,"on this data is", math.floor(mean(data, string)*100)/100 , "\n")
        inc_dec_result = inc_dec_counter(data, string)
        print("The candles for", string,"increased", inc_dec_result["increase"],"times")
        print("The candles for", string,"decreased", inc_dec_result["decrease"],"times\n")
        steep_result = highest_steep(data, string)
        print("The biggest steep or slope in the data for", string, "were these two candles")
        print(steep_result[0])
        print(steep_result[1], "\nThe difference for", string, "between these two candles were", steep_result["diff"])

def split_data(only_live = [], live_and_extended = []): #splits the data to only extended hours
    result = []
    index = 0
    for current in live_and_extended:
        if current["datetime"] != only_live[index]["datetime"]:
            result.append(current)
        elif index < len(only_live) - 1:
            index = index + 1
    return result
    
def inc_dec_counter(list = [], string = ""): #counts amount how many times candles increased/decreased
    result = {"increase": 0, "decrease": 0}
    previous = {}
    # pprint.pprint(list)
    for current in list:
        if previous != {}:# first case (no previous yet)
            # print(previous[string], " > ", current[string],previous[string] > current[string]) # test, true = decrease, false = increase
            if previous[string] > current[string]: # decrease case
                result["decrease"] = result["decrease"] + 1
            elif previous[string] != {}: #increase case
                result["increase"] = result["increase"] + 1
        previous = current
    return result



def main():
    td_client = TDClient(client_id=CONSUMER_ID, redirect_uri=REDIRECT_URI, credentials_path=JSON_PATH)
    td_session = td_client.login()
    print("LIVE MARKET HOURS VS EXTENDED MARKET HOURS")
    print("Due to the limitation of the api, we can only gain extended market hours if the period is days ONLY (td ameritrade api will combine all the data of 1 day into 1 candle)")
    print("I also combined the extended market hours of before live market hours and after live market hours")
    # get user input
    user_input = input("\nTicker: ")
    print("\nThe period is what time frame do you want the data analyzed (ex. 5 days -> 5)")
    period_input = input("How many day(s) (1, 2, 3, 4, 5, 10 days are valid): ")
    print("\nThe frequency is how you want the period to be divided (this is like candles, dividing up 5 number of days into 30 minute candles)  ")
    freq_input = input("How many minute(s) (1, 5, 10, 15, 30 minutes are valid): ")
    test_input = input("\nWhat variable do you want to analyze or all (close, high, low, open, volume, all): ")
    # get user's requested data from api
    regular_only = td_client.get_price_history(symbol=user_input, period_type="day", period=period_input, frequency_type="minute", frequency=freq_input, extended_hours=False)
    regular_extended = td_client.get_price_history(symbol=user_input, period_type="day", period=period_input, frequency_type="minute", frequency=freq_input, extended_hours=True)
    extended_only = split_data(only_live=regular_only["candles"], live_and_extended=regular_extended["candles"]) #list only not dictionary
    # print analyzed data
    print("-----------------------------------------------------------------------------------") 
    print("LIVE MARKET HOURS:")
    call(regular_only["candles"], test_input)
    print("-----------------------------------------------------------------------------------")
    print("EXTENDED MARKET HOURS:")
    call(extended_only, test_input)



if __name__ == "__main__":
    main()
