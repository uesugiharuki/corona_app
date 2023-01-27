

from email import header
from operator import index

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from pdfminer.high_level import extract_text  
#pdfファイル名の取得
res_org=requests.get(r'https://www.pref.mie.lg.jp/YAKUMUS/HP/m0068000066_00079.htm')
soup=BeautifulSoup(res_org.text,'html.parser')

tag_span=soup.find('span',class_='attach-pdf')
tag_a=tag_span.find('a')
str=tag_a['href']

url=r'https://www.pref.mie.lg.jp'+str


#pdfファイル　ダウンロード
def pdfDwonload(url):
   # 読み込みたいPDFファイル
    res =requests.get(url) 

    with open(r'E:\DATA\temp.pdf', "wb") as f:
        #各チャンクをwrite()関数でローカルファイルに書き込む
            for chunk in res.iter_content(100000):
                f.write(chunk)

            #ファイルを閉じる
            f.close()
            print("ダウンロード・ファイル保存完了")
            
pdfDwonload(url)            





# pdfファイルから必要なデータ抽出        

text = extract_text(r"E:\DATA\temp.pdf")







print('コロナ感染者状況')
print(' ')

mdate=re.search('令和[\d]+年+[\d]+月+[\d]+日',text)
rdate=mdate.group()
print(rdate)

m = re.search('発生件数[\s　][-\d]+件', text)
r = m.group()  
print(r) 



text1=text.replace('\n',',')

text2=text1.split('２　発生件数（四日市市及び三重県発表分 ）')[1]

text3=re.sub('※ 報道機関・県民の皆さまへ,.*','',text2)

ml1=re.search(r'件数.*市町',text3)
rl1=ml1.group()
list1=rl1.split(',')
list1.remove('市町')


ml2=re.search(r'市町.*',text3)
rl2=ml2.group()


list2=rl2[:].split(',')


for c,co in zip(list2,list1):
    print(c,co)
  
'''
df_1=pd.DataFrame(list2)
df_1.columns=['col1']

print(df_1)



#df_2=df_1.set_index('col1')
#df_city=df_2.loc['市町':'件数',:]
#df_city.reset_index(inplace=True) 
#df_city2=df_city[:-1]
#df_city3=df_city2[:-1]
#df_data=df_2.loc['件数':,:]
#df_data.reset_index(inplace=True)
#df_data.columns=['count']
#df_data2=df_data[:-1]
#df_data3=df_data2[:-1]

df=pd.concat([df_city3,df_data3],axis=1)

print()
df_nabari=df[df['col1']=='名張市']
strn=df_nabari.iloc[0,1]
print(f'名張市件数　　:{strn}件')


df_iga=df[df['col1']=='伊賀市']
stri=df_iga.iloc[0,1]
print(f'伊賀市件数　　:{stri}件')

print()



df_new=df.rename(columns={'col1':'市町','count':'件数'})
df_new.drop(index=0,inplace=True)

print(df_new)


'''
cn=[j for i,j in zip(list2,list1) if i=='名張市']
print(f'名張市の件数　{cn}件')

ci=[j for i,j in zip(list2,list1) if i=='伊賀市']
print(f'伊賀市の件数　{ci}件')

input('何かキーを入力して終了してください')
