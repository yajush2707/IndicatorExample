from base64 import b64decode
import pandas as pd
import json
import random

def cs_engines_purpow_compute(a ='input.txt'):
    from base64 import b64decode
    import random
    from io import StringIO
    import pandas as pd
    f = open("input.txt", "r")
    print(f.read())
    ### income ###
    
    df=pd.read_csv("input.txt")

    df["Buchungstag"]=pd.to_datetime(df["Buchungstag"])

    df["month"]=df["Buchungstag"].apply(lambda d:d.month)
    df["year"]=df["Buchungstag"].apply(lambda d:d.year)
    df["dow"]=df["Buchungstag"].apply(lambda d:d.dayofweek)


    #duration
    amount_income = df[(df["Lohn"]==1)].groupby(["year","month"])["Betrag"].sum().mean()
    overall_income= df[(df["Lohn"]==1) & (df["Betrag"]>0.)]["Betrag"].sum()
    months=len(df.groupby(["year","month"]))
    amount_income=overall_income/months

    print(str(df["Buchungstag"]))
    print(str(df.groupby(["year","month"]).groups))
    print("overall income:"+str(overall_income))
    print("income: "+str(amount_income))
    print("Computing income indicator..")

    ### expenses ###

    result = -df[(df["Miete"]==1) &(df["Betrag"]<0)].groupby(["year","month"])["Betrag"].sum().mean()

    print("expenses: "+str(result))
    print("Computing expense indicator..")

    purpow = amount_income - result

    print("Purchasing Power: "+str(purpow))



    res={"purchasing_power":{
                "label":"Purchasing Power",
                "value":str(purpow),
                "type":"numeric",
                "description":"Balance available after deduction of monthly expenses.",
                "property":"purchasing power"
            },
             "income":{
               "label":"Income",
               "value":str(amount_income),
               "type":"numeric",
               "description":"Monthly net income",
               "property":"income",
             },
             "expenses":{
               "label":"Expenses",
               "value":str(result),
               "type":"numeric",
               "description":"Regular monthly expenses such as rent, incidental costs, car, insurance, etc.",
               "property":"expenses"
             }
        }
    return purpow

cs_engines_purpow_compute()
