import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
from matplotlib import font_manager, rc
import datetime
import FinanceDataReader as fdr
from mplfinance.original_flavor import candlestick2_ohlc 
import pandas as pd
from pykrx import stock
import json
import urllib.request
import random

from  utils import get_stocks, 한글, createFolder
from technical_analysis import 기술적분석

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name() 
rc('font', family=font_name) 
일년전 = (datetime.datetime.now() - datetime.timedelta(weeks=52)).strftime('%Y%m%d')
오늘=datetime.datetime.now().strftime('%Y%m%d')

base_dir='''C:/Users/PC_1M/Documents/code/tistory_auto_posting/data'''
개별주_dir=base_dir+"/개별주"
코스피=get_stocks(market='kospi')
코스닥=get_stocks(market='kosdaq')
df_krx=pd.concat([코스피,코스닥])
code_list=df_krx['종목코드'].tolist()
code=random.choice(code_list)
df_krx=df_krx[df_krx['회사명'].apply(한글)]



class Stock_report:
    def __init__(self, code, df_krx,개별주_dir ):
        수급데이터=stock.get_market_trading_value_by_date(일년전, 오늘,code)
        data=fdr.DataReader(code)
        data=data.rename(columns={"Open":'open',"High":'high','Low':'low','Close':"close","Volume":'volume'})
        data=data[['open','high','low','close','volume']]
        data=기술적분석(data, weight=1)
        
        회사명=df_krx.loc[df_krx['종목코드'] == code].iloc[0,0]
        path=개별주_dir+f"/{회사명}"
        createFolder(path)
        self.code=code
        self.수급데이터=수급데이터
        self.data=data
        self.회사명=회사명
        self.개별주_dir=개별주_dir
        #self.kospi=kospi
        
       
    def 트렌드분석(self):
        키워드=self.회사명
        if self.data.index[0] > datetime.datetime.strptime('2016-01-01', '%Y-%m-%d'):
            시작일=self.data.index[0].strftime('%Y-%m-%d')
        else:
            시작일=datetime.datetime.strptime('2016-01-01', '%Y-%m-%d').strftime('%Y-%m-%d')
        종료일=datetime.datetime.now().strftime('%Y-%m-%d')
        client_id = "D1_NLYx2BApXPF9Dhvns"
        client_secret = "EU9WJ1BrDn"
        url = "https://openapi.naver.com/v1/datalab/search";
        body = "{\"startDate\":\""+시작일+"\",\"endDate\":\""+종료일+"\",\"timeUnit\":\"date\",\"keywordGroups\":[{\"groupName\":\""+키워드+"\",\"keywords\":[\""+키워드+"\"]}]}";
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
        json.loads(response_body.decode('utf-8'))
        결과=json.loads(response_body.decode('utf-8'))
        키워드=결과['results'][0]['keywords']
        트렌드=pd.DataFrame(결과['results'][0]['data']).set_index('period')
        return 트렌드

    def 트렌드그래프(self, 트렌드):
        """
        트렌드분석함수의 리턴값인 트렌드를 인자로 받는다. 
        """
        path=f'{self.개별주_dir}/{self.회사명}/{self.회사명}_트렌드그래프.jpg'
        트렌드.index=pd.to_datetime(트렌드.index)
        주가트렌드=pd.concat([self.data, 트렌드], axis=True)
        주가트렌드=주가트렌드.dropna()
        plt.figure(figsize=(12.5, 4.5))
        plt.plot(주가트렌드['볼밴위치'], label=f'{self.회사명}',  linewidth=0.4, markersize=12)
        plt.plot(주가트렌드['ratio'], label="트렌드", alpha=1,linewidth=1, color='red' )
        plt.title(f"주가와 트렌드 비교%")
        plt.xlabel("Date")
        plt.grid(True)
        plt.ylabel('위치(0~100)')
        plt.legend(loc='best')
        plt.savefig(path, dpi=100)

        return path


    def 수급파이차트(self):
        path=f'{self.개별주_dir}/{self.회사명}/{self.회사명}_수급파이차트.jpg'
        ratio=self.수급데이터.sum().tolist()
        ratio_colors=list(map(lambda x: 'red' if x>=0 else 'blue', ratio))
        ratio_list=list(map(abs, ratio))
        ratio_list=list(map(lambda x: abs(x)/sum(ratio_list),ratio))

        explode = [0.05, 0.05, 0.05, 0.05]
        colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0']
        wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
        plt.figure(figsize=(20, 14))
        plt.title(f"{self.회사명} 수급차트", fontsize=25)
        plt.pie(ratio_list, labels=self.수급데이터.columns, autopct='%.1f%%', startangle=260, counterclock=False, shadow=False, colors=colors, wedgeprops=wedgeprops, textprops={'size':18})
        plt.legend(self.수급데이터.columns, fontsize=18,loc='best')
        plt.xticks(fontsize=20)
        plt.savefig(path, dpi=100)
     
        return path
        
    def 수급라인차트(self):
        path=f'{개별주_dir}/{self.회사명}/{self.회사명}_수급라인차트.jpg'
        plt.figure(figsize=(20, 14))
        plt.plot(self.수급데이터['기관합계'], label='기관합계',  linewidth=0.7, markersize=12,color='blue')
        plt.plot(self.수급데이터['개인'], label='개인',  linewidth=0.7, markersize=12,color='green')
        #plt.plot(수급데이터['기타법인'], label='기타법인',  linewidth=0.7, markersize=12, color='purple')
        plt.plot(self.수급데이터['외국인합계'], label='외국인합계',  linewidth=0.7, markersize=12,color='red')
        #plt.plot(수급데이터['전체'], label='전체',  linewidth=1, markersize=12)
        plt.title(f"{self.회사명} 수급차트", fontsize=25)
        plt.xlabel("Date")
        plt.grid(True)
        plt.xlim(self.수급데이터.index[0],self.수급데이터.index[-1] )
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.legend(loc='best', fontsize=20)
        plt.savefig(path, dpi=100)
   
        return path 





    def 캔들차트(self):
        
        오늘 =datetime.datetime.now().strftime('%Y%m%d')
        path=f'{self.개별주_dir}/{self.회사명}/{self.회사명}_캔들차트.jpg'
        
        두달전 = (datetime.datetime.now() - datetime.timedelta(weeks=54)).strftime('%Y%m%d')
        kospi_df=fdr.DataReader(code ,두달전)
        kospi_df['MA5'] = kospi_df['Close'].rolling(5).mean()
        kospi_df['MA20'] = kospi_df['Close'].rolling(20).mean()
        kospi_df['MA60'] = kospi_df['Close'].rolling(60).mean()

        color_fuc = lambda x : 'r' if x >= 0 else 'b'
        kospi_df['Volume'].diff().fillna(0)         
        color_df = kospi_df['Volume'].diff().fillna(0).apply(color_fuc)
        color_list = list(color_df)

        fig = plt.figure(figsize=(20,10))
        top_axes = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=4)
        bottom_axes = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4, sharex=top_axes)
        bottom_axes.get_yaxis().get_major_formatter().set_scientific(False) # 거래량 값 그대로 표현
        index = kospi_df.index.astype('str') # 캔들스틱 x축이 str로 들어감
        # 이동평균선 그리기
        top_axes.plot(index, kospi_df['MA5'], label='MA5', linewidth=0.7)
        top_axes.plot(index, kospi_df['MA20'], label='MA20', linewidth=0.7)
        top_axes.plot(index, kospi_df['MA60'], label='MA60', linewidth=0.7)
        # X축 티커 숫자 20개로 제한
        top_axes.xaxis.set_major_locator(ticker.MaxNLocator(10))
        # 그래프 title과 축 이름 지정
        top_axes.set_title(f'{self.회사명}', fontsize=32)
        candlestick2_ohlc(top_axes, kospi_df['Open'], kospi_df['High'], 
                        kospi_df['Low'], kospi_df['Close'],
                        width=0.5, colorup='r', colordown='b')
        bottom_axes.bar(index, kospi_df['Volume'], width=0.5, 
                        align='center',
                        color=color_list)

        bottom_axes.xaxis.set_major_locator(ticker.MaxNLocator(10))
        top_axes.legend(fontsize=18)
        top_axes.tick_params(labelsize=18)
        plt.grid()
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        plt.legend(fontsize=18)
        plt.savefig(path, dpi=100)
  
        return path


    def 백테스팅차트(self, data,매수일,매도일,누적수익률, 성과, 회사명, 전략명):
        path=f'{self.개별주_dir}/{self.회사명}/{self.회사명}_백테스팅차트_{전략명}.jpg'
        
        # kospi=self.kospi.loc[매수일.index[0]:매도일.index[-1]]
        # retPlus1 = kospi['Change'] + 1
        # cum_ret = (retPlus1.cumprod() - 1)*100

        누적수익률=list(map(lambda x: x*100 , 누적수익률))
        plt.figure(figsize=(24, 15))
        #subplot1###############
        plt.subplot(311)
        plt.plot(data['close'], label='ticker',  linewidth=0.2, markersize=12)
        plt.scatter(매수일.index, 매수일, label='Buy', marker="^", color='red',alpha=1)
        plt.scatter(매도일.index, 매도일, label='Sell', marker="v", color='blue',alpha=1)
        plt.title(f'{회사명} 매매타점 그래프')
        plt.xlabel("Date")
        plt.grid(True)
        plt.xlim(data.index[0],data.index[-1])
        plt.ylim(min(data['close'].tolist()), max(data['close'].tolist()))
        plt.ylabel('Close Price')
        plt.legend(loc='best')
        #subplot1###############
        plt.subplot(312)
        try:
            plt.plot(매수일.index, 누적수익률)
        except:
            plt.plot(매도일.index, 누적수익률)
        plt.title(f'{회사명} {전략명} 전략 누적수익률 : {성과}%')
        plt.ylabel('%')
        #subplot3###############
        # plt.subplot(313)
        # plt.plot(cum_ret.index, cum_ret)
        # plt.title(f'동일기간 KOSPI 누적수익률 : {cum_ret[-1]}%')
        # plt.ylabel('%')
        plt.savefig(path, dpi=200)
   
        return path