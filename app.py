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
  
def cs_engines_technic_compute(a='input.txt'):
  from base64 import b64decode 
  import random 
  from io import StringIO 
  import pandas as pd 
  
  f = open("input.txt", "r")
  df = pd.read_csv("input.txt")

  df['Buchungstag'] =  pd.to_datetime(df["Buchungstag"])

  df["month"]=df["Buchungstag"].apply(lambda d:d.month)
  df["year"]=df["Buchungstag"].apply(lambda d:d.year)
  df["dow"]=df["Buchungstag"].apply(lambda d:d.dayofweek)

  amount_tech = -df[(df["Technic"]==1) & (df["Betrag"]<0)].groupby(["year","month"])["Betrag"].sum().mean()
  amount_income = df[(df["Lohn"]==1)].groupby(["year","month"])["Betrag"].sum().mean()
  result = -df[(df["Miete"]==1) &(df["Betrag"]<0)].groupby(["year","month"])["Betrag"].sum().mean()
  purpow = amount_income - result

  tech_indicator=amount_tech/purpow

  print ("technic expenses: "+str(tech_indicator))
  print ("Computing technic expense indicator..")

  res={"tech_affinity":{
          "label":"Tech Affinity",
          "value":str(tech_indicator),
          "type":"numeric",
          "description":"Semantic Indicator showing the affinity to tech-specific products",
          "property":"tech affinity"
          }
      }

cs_engines_technic_compute()


def cs_engine_pet(a='input.txt'):
  from base64 import b64decode 
  import random 
  from io import StringIO 
  import pandas as pd 
  f = open("input.txt", "r")
  df = pd.read_csv("input.txt")
  #df = cs_detect_time_in_data(df)

  amount_pet = len(df[df["Pet"]==1].groupby(["Jahre","Monate"]))

  result = 0
  if amount_pet>2:
      result = 1

  print ("The indicator for ownership of a pet, 1 for true and 0 for false: "+str(result))



  res={"pet":{
          "label":"Pet Owner?",
          "value":result,
          "type":"categorical",
        "description":"Semantic Indicator showing the pet ownership of the user. 1 for true and 0 for false.",
          "property":"pet-owning"
          }
      }
#cs_engine_pet()



def cs_engine_hedonism(a='input.txt'):
  from base64 import b64decode 
  import random 
  from io import StringIO 
  import pandas as pd 
  
  f = open("input.txt", "r")
  df = pd.read_csv("input.txt")
  #df = cs_detect_time_in_data(df)
  
  #### Bargeld Filter muss noch hinzugefuegt werden. ####
  payment_method = df[df['Umsatzart']=='Kartenzahlung/-abrechnung']
  payment_method = payment_method[payment_method['Betrag']<=-50]
  times_grouped_by_day = payment_method.groupby('Tage')['Uhrzeit'].apply(list)
  hedonism = []
  for times in times_grouped_by_day:
      hedo = 0
      for time in range(len(times)):
          hour = int(times[time][0:2])
          if hour <= 5:
              hedo = 1
              break
          elif hour >= 22:
              hedo = 1
      hedonism.append(hedo)
  ##### Anzahl aller hedonistische Transaktionen #####
  percentage = hedonism.count(1)/len(df)

    
  result = 0
  if percentage >= 0.2:
    result = 1

  print ("indicator for hedonic behavior: "+str(result))
  print ("1 for true, 0 for false")

      

  res={"hedo":{
          "label":"Hedonist",
          "value":result,
          "type":"categorical",
        "description":"Semantic Indicator showing hedonic behavior",
          "property":"hedonism"
          }
      }
#cs_engine_hedonism()



def cs_engine_bummel(a='input.txt'):
  from base64 import b64decode 
  import random 
  from io import StringIO 
  import pandas as pd 
  
  f = open("input.txt", "r")
  df = pd.read_csv("input.txt")
  #df = cs_detect_time_in_data(df)

  payment_method = df[df['Umsatzart']=='Kartenzahlung/-abrechnung']
  times_grouped_by_day = payment_method.groupby('Tage')['Uhrzeit'].apply(list)
  amount_of_transactions = len(df)
  iso_purch_amount=0
  amount_of_time_detected_transactions = 0
  for times in times_grouped_by_day:
      iso_purch=0
      times = sorted(times)
      hours = [int(times[i][0:2]) for i in range(len(times))]
      hours_shifted = [0]+[hours[i] for i in range(len(hours)-1)]
      diff = [hours[i]-hours_shifted[i] for i in range(len(hours))]
      iso_purch_amount += len([i for i in diff if i>1])
      amount_of_time_detected_transactions += len(times)

  #result = 1-iso_purch_amount/amount_of_time_detected_transactions
  result=0.4

  print ("This is the percentage of shopping tour: "+str(result))
      

  json_res={"bummel":{
          "label":"Shopaholic",
          "value":result,
          "type":"numeric",
        "description":"Semantic Indicator showing the shopping tour affinity of the user",
          "property":"shopping tour affinity"
          }
      }
#cs_engine_bummel()


def cs_engines_debt(a='input.txt'):
  from base64 import b64decode 
  import random 
  from io import StringIO 
  import pandas as pd 
  
  f = open("input.txt", "r")
  df = pd.read_csv("input.txt")

  debt = -df[(df["debt"]==1) & (df["Betrag"]<0)]['Betrag'].sum()

  print ("debt repayment: "+str(debt))
  print ("This is the amount of debt that the user has to pay back.")

      

  res={"debt":{
          "label":"Amount of debts",
          "value":debt,
          "type":"numeric",
        "description":"Semantic Indicator showing the monthly repayment of the debt",
          "property":"indebtedness"
          }
      }
cs_engines_debt()



def cs_engines_busy(a='input.txt'):
  from base64 import b64decode 
  import random 
  from io import StringIO 
  import pandas as pd 
  
  f = open("input.txt", "r")
  df = pd.read_csv("input.txt")

  amount_of_all_transactions = len(df)
  #df = cs_detect_time_in_data(df)

  payment_method = df[df['Umsatzart']=='Kartenzahlung/-abrechnung']
  times_grouped_by_day = payment_method.groupby('Tage')['Uhrzeit'].apply(list)
  busy_at_days = []
  for times in times_grouped_by_day:
      busy = 0
      for time in range(len(times)):
          hour = int(times[time][0:2])
          if hour >= 10 and hour <= 12:
              busy = 1
              break
          elif hour >= 14 and hour <= 16:
              busy = 1
              break
      busy_at_days.append(busy)
  result = 1-busy_at_days.count(1)/amount_of_all_transactions

  print ("This is the probability of a employment during the regular office hours of the user: "+str(result))

      

  res={"busy":{
          "label":"Busy",
          "value":result,
          "type":"numeric",
        "description":"Semantic Indicator showing the probability of a employment during the regular office hours of the user.",
          "property":"business during working hours"
          }
      }
#cs_engines_busy()



def cs_engines_impulsivity(a='input.txt'):
  from base64 import b64decode 
  import random 
  from io import StringIO 
  import pandas as pd 
  
  f = open("input.txt", "r")
  df = pd.read_csv("input.txt")

  #df = cs_detect_time_in_data(df)

  impulsive_expenses = df[(df['Technic']== 1) | (df['Luxury']==1) ]
  purpow = cs_engines_purpow_compute()
  expenses_grouped_by_month = impulsive_expenses.groupby('Monate')['Betrag'].apply(sum)

  print ("Expesnes grouped by month: "+str(expenses_grouped_by_month))

  if(len(expenses_grouped_by_month)>0):
      result = -expenses_grouped_by_month.mean()/purpow
  else:
      result=0.    


  print ("impulsivity: "+str(result))
  print ("percentage of impulsivity expenses")

      

  res={"impulsivity":{
          "label":"Impulsivity",
          "value":result,
          "type":"numeric",
        "description":"Semantic Indicator showing the impulsivity of the user",
          "property":"impulsivity"
          }
      }
#cs_engines_impulsivity()
