import apiai
import json
import requests
from datetime import datetime, timedelta
from DatRet import *
from NewsSentiment import *

CLIENT_ACCESS_TOKEN='ee339c04a181469aba3549870dfeca5e'
DR = DatRet()
NS = NewsSentiment()

def main(query):
    if query=='':
        return

    ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request=ai.text_request()
    request.lang='en'
    request.session_id="1"
    request.query=query
    res=request.getresponse()

    jsonres=json.loads(res.read())

    company=""
    try:
        company=jsonres['result']['parameters']['companies'].strip(".")
    except KeyError:
        pass

    date=""
    try:
        date=jsonres['result']['parameters']['date']
        print(date)
        if datetime.strptime(date, "%Y-%m-%d")>datetime.now():
            print("At this point, I am unable to predict the future.")
            return ("At this point, I am unable to predict the future.")
    except KeyError:
        pass
    except ValueError:
        pass

    time=""
    try:
        time=jsonres['result']['parameters']['time']
        print(time)
        if datetime.strptime(time, "%H:%M:%S")>datetime.now():
            print("At this point, I am unable to predict the future.")
            return ("At this point, I am unable to predict the future.")
    except KeyError:
        pass
    except ValueError:
        pass
        
    if company=="":
        default=jsonres['result']['fulfillment']['speech']
        print(default)
        return default
    else:
        print("company:"+company)
            
    intent=jsonres['result']['metadata']['intentName']
    if intent=="Default Fallback Intent" or intent=="Default Welcome Intent":
        default=jsonres['result']['fulfillment']['speech']
        print(default)
        return default
    else:
        print("intent:"+intent)

    #If we've reached this point, we have a company and intent (and myb date)
    #Wrap all of this in a try catch and excuse ourselves for not having the data?
    if intent=="Spot Price":
        if date=="" and time=="":
            print(DR.stock_price(company))
            return DR.stock_price(company)
        elif date=="":
            print(DR.stock_price(company, time=time))
            return DR.stock_price(company, time=time)
        elif time=="":
            print(DR.stock_price(company, date))
            return DR.stock_price(company, date)
        else:
            print(DR.stock_price(company, date, time))
            return DR.stock_price(company, date, time)
    elif intent=="Market Capitalisation":
        print(DR.current_marketcap(company))
        return DR.current_marketcap(company)
    elif intent=="retrieve-news-company":
        returnarray=[]
        for article in DR.get_news(company):
            print("URL:"+article['u'])
            print("Snippit:"+article['sp'])
            polarity=NS.getPolarity(article['u'])
            print(polarity)
            returnarray.append((article['u'], article['sp'], polarity))
        return returnarray
    elif intent=="Open":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[0])
            return DR.price_data(company, date)[0]
        else:
            print(DR.price_data_today(company)[0])
            return DR.price_data_today(company)[0]
    elif intent=="Close":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(date)
            print(DR.price_data(company, date)[1])
            return DR.price_data(company, date)[1]
        else:
            print(DR.price_data_today(company)[1])
            return DR.price_data_today(company)[1]
    elif intent=="High":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[2])
            return DR.price_data(company, date)[2]
        else:
            print(DR.price_data_today(company)[2])
            return DR.price_data_today(company)[2]
        return
    elif intent=="Low":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[3])
            return DR.price_data(company, date)[3]
        else:
            print(DR.price_data_today(company)[3])
            return DR.price_data_today(company)[3]
    elif intent=="Volume":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[4])
            return DR.price_data(company, date)[4]
        else:
            print(DR.price_data_today(company)[4])
            return DR.price_data_today(company)[4]
    elif intent=="Percentage Change":
        listinput=list(jsonres['result']['parameters']['date-time'])
        startenddates=extract_diff_dates(listinput)
        print(startenddates)
        startdt=startenddates[0]
        enddt=startenddates[1]
        
        if enddt=="":
            print(DR.diff(company, start=startdt))
            return DR.diff(company, start=startdt)
        else:
            print(DR.diff(company, start=startdt, end=enddt))
            return DR.diff(company, start=startdt, end=enddt)
    return ("This is the catch-all return at the end of the main function")

#Function for determining start/end dates of difference function
def extract_diff_dates(listinput):
    startdt=listinput[0]
    try:
        enddt=listinput[1]
    except IndexError:
        enddt=""
    if "/" in startdt:
        enddt=startdt.split("/")[1]
        startdt=startdt.split("/")[0]
    return (startdt, enddt)
    
    
#while True:
#    main(input("\n"))
