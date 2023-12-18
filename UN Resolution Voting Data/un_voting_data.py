from requests import get
import json
import pandas as pd
from bs4 import BeautifulSoup

request = get('https://api.unvoting.org/unhrcTexts?Year=2021&Type=Resolution&VoteType=RECORDED')

json_data = json.loads(request.content)

vote_date = list()
resolution_title = list()
vote_summary = list()
vote_record = list()
count_vote_summary = 0
count_vote_record = 0
url_record = list()
count_json = 0
df = pd.read_csv("un_voting_2021.csv")

for i in json_data:
    if count_json!=1:
     vote_date.append(i['vote_date'])
     resolution_title.append(i['title'])
     url = i['url_record']
     url_record.append(url)
     request_record = get(url)
     page = BeautifulSoup(request_record.content,'html.parser')
     div_tag_vote_record = page.select('div.transclusion-inner-block')[9]

     for i in div_tag_vote_record:
        if count_vote_summary == 0:
         count_vote_summary = count_vote_summary+1
         
        else:
         vote_summary.append(i.text)
        
     div_tag_country = page.select('div.transclusion-inner-block')[11]
    
     for i in div_tag_country:
        if count_vote_record ==0:
           count_vote_record = count_vote_record+1
        else:
          vote_record.append(i.text)
          
    elif count_json==1:
     vote_date.append(i['vote_date'])
     resolution_title.append(i['title'])
     url = i['url_record']
     url_record.append(url)
     request_record = get(url)
     page = BeautifulSoup(request_record.content,'html.parser')
     div_tag_vote_record = page.select('div.transclusion-inner-block')[9]

     for i in div_tag_vote_record:
        if count_vote_summary == 0:
         count_vote_summary = count_vote_summary+1
         
        else:
         vote_summary.append(i.text)
        
     div_tag_country = page.select('div.transclusion-inner-block')[11]
    
     for i in div_tag_country:
        if count_vote_record ==0:
           count_vote_record = count_vote_record+1
        else:
          vote_record.append(i.text)
          
    count_vote_record=0
    count_vote_summary=0
    count_json = count_json+1
    print(count_json)
df['vote_date'] = vote_date
df['resolution_title'] = resolution_title
df['vote_summary'] = vote_summary
df['vote_record'] = vote_record
df['url_record'] = url_record
df.to_csv("un_voting_2021.csv")