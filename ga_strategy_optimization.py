import random
import numpy as np
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from technical_analysis import 기술적분석



class Ga_strategy_optiomization:
    """
    data : OHLCV 데이터테이블 
    팩터들 : ex) ['RSI','VOLUME','CCI']
    팩터최소숫자 : 전략생성할 때 사용할 팩터의 최소 숫자
    팩터최대숫자 : 전략생성할 때 사용할 팩터의 최대 숫자 
    filename : 백테스팅 기록할 경로 및 파일명  ex) 'a/b/test.xlsx'
    """
    def __init__(self, data: pd.DataFrame, 팩터들:list, 팩터최소숫자:int ,팩터최대숫자:int, filename:str ) :

        self.data=기술적분석(data, weight=1)
        self.팩터들=팩터들
        self.팩터최소숫자=팩터최소숫자
        self.팩터최대숫자=팩터최대숫자
        self.filename=filename



    def 백테스팅(self, 매수전략:list, 매도전략:list) -> float:
        """
        매수전략 : 리스트안에 튜플로 팩터명과 값이 들어감 ex) [('RSI',50),('MACD',50),('CCI',50)]
        매도전략 : 매수전략과 동일
        """
        def buy(data, 매수전략):
            조건 = data[매수전략[0][0]]<매수전략[0][1]
            for i in range(1,len(매수전략)):
                조건x=data[매수전략[i][0]]<매수전략[i][1]
                조건=조건 & 조건x
            return 조건

        def sell(target, 매도전략):
            조건=target[매도전략[0][0]]>매도전략[0][1]
            for i in range(1,len(매도전략)):
                조건=조건 & target[매도전략[i][0]]<매도전략[i][1] 
            return 조건
            
        try:
            매수조건 = buy(self.data, 매수전략)

            누적수익률=1
            매도일=None
            매수날짜들=[]
            매도날짜들=[]
            누적수익률목록=[]
            수익내역=[]
            if len(self.data.index[매수조건])==0:
                return 0, 0, 0, 0, 0
            for 매수일 in self.data.index[매수조건]:
                if 매도일 != None and 매수일 <= 매도일 :
                    continue

                target= self.data.loc[매수일:]
                매수날짜들.append(매수일)

                매도조건 = sell(target, 매도전략)
                매도후보들=target.index[매도조건]

                if len(매도후보들) == 0:
                    매수가=self.data.loc[매수일,'close']
                    매도가=self.data.iloc[-1,3]
                    누적수익률 *=((매도가/매수가)-0.0003)
                    수익내역.append((매도가/매수가)-0.0003)
                    누적수익률목록.append(누적수익률)
        #      
                    break
                else:
                    매도일 = 매도후보들[0]
                    매도날짜들.append(매도일)
                    매수가=self.data.loc[매수일,'close']
                    매도가=self.data.loc[매도일,'close']

                    누적수익률 *=((매도가/매수가)-0.001)
                    수익내역.append((매도가/매수가)-0.001)
                    누적수익률목록.append(누적수익률)
            ror=pd.DataFrame(수익내역)

            ror['hpr']=ror.cumprod()

            ror['dd'] = ((ror['hpr'].cummax() - ror['hpr']) / ror['hpr'].cummax()) * 100

            누적수익률2=round(누적수익률목록[-1],2)
            mdd=ror['dd'].max()

            def 승(x):
                return x>1
            def 패(x):
                return x<=1
            매매승률=(len(list(filter(승, 수익내역)))/len(수익내역))*100

            평균수익률=round((np.mean(list(filter(승, 수익내역)))-1)*100, 2)
            평균손실률=round((np.mean(list(filter(패, 수익내역)))-1)*100, 2)
            매매기간=len(self.data)/365
            CAGR = round(((누적수익률2 ** (1/매매기간))-1)*100,2)

            매수일_df=pd.DataFrame(index=매수날짜들,data=self.data)['close']
            매도일_df=pd.DataFrame(index=매도날짜들,data=self.data)['close']

            results= [str(매수전략), str(매도전략), round((누적수익률2-1)*100,2) , round(mdd,2),CAGR ,매매승률, len(수익내역), 평균수익률, 평균손실률]
            self.전략기록(results)
            성과=round((누적수익률2-1)*100,2)

            return 성과, 매수일_df, 매도일_df, 누적수익률목록 , results 
        except Exception as ex:
            print('에러 : ',ex)
            return 0,0,0,0, 0

    def 전략생성(self):
        """
        팩터 최소, 최대값으로 전략을 생성하며 quantile 통해서 모든 팩터의 값을 분위수로 변경함        
        """
        팩터list=[random.choice(self.팩터들) for i in range(random.randint(self.팩터최소숫자, self.팩터최대숫자))]
        측정값list=[self.data[i].quantile(q=random.random(), interpolation='linear') for i in 팩터list]
        전략=list(zip(팩터list,측정값list))  
        return 전략


    def 무작위전략생성(self):
        매수전략=self.전략생성()
        매도전략=self.전략생성()
        성과, 매수일_df, 매도일_df, 누적수익률목록, results=self.백테스팅(매수전략,매도전략)
        전략결과=[매수전략,매도전략,성과]
        return 전략결과


    def 전략모음(self, 전략수):
        전략들=[]
        for i in range(전략수):
            try:
                전략들.append(self.무작위전략생성())
            except Exception as ex:
                print('전략모음함수 에러 : ' , ex)
                

        
        return 전략들





    def 생존할전략선별(self, 전략들, best_sample, lucky_few):
        next_generation=[]
        
        best_sample수=int(len(전략들)/100*best_sample)
        전략들=sorted(전략들, key=lambda x:x[2], reverse=True)
        전략들=전략들[0:best_sample수]
                
        #행운의 생존전략
        cnt=0
        for _ in range(lucky_few):
            next_generation.append(self.무작위전략생성())
            while len(next_generation) < best_sample + lucky_few:
                cnt+=1
                next_generation.append(self.무작위전략생성())
       
        random.shuffle(next_generation)
        return next_generation        


    def 자식전략만들기(self, 부모전략1,부모전략2,재시도횟수=3):
        flag=True
        flag2=True
        cnt=0
        cnt2=0

        while flag:
            cnt+=1
            if cnt>재시도횟수:
                break
            매수전략1=부모전략1[0]
            if len(매수전략1)> 1:
                매수전략1=random.choices([i for i in 매수전략1], k=random.randint(1,len(매수전략1)-1))
            else:
                매수전략1=random.choices([i for i in 매수전략1], k=random.randint(1,len(매수전략1)))

            매수전략2=부모전략2[0]
            if len(매수전략2)> 1:
                매수전략2=random.choices([i for i in 매수전략2], k=random.randint(1,len(매수전략2)-1))
            else:
                매수전략2=random.choices([i for i in 매수전략2], k=random.randint(1,len(매수전략2)))            
                
            매수전략=매수전략1+매수전략2

            팩터추출 =[i[0] for i in 매수전략] 
            if len(팩터추출)> len(set(팩터추출)): #팩터가 중복됨
                flag=True
            else:
                flag=False

        while flag2:
            cnt2+=1
            if cnt2>재시도횟수:
                break
            매도전략1=부모전략1[1]
            if len(매도전략1) >1:
                매도전략1=random.choices([i for i in 매도전략1], k=random.randint(1,len(매도전략1)-1))
            else:
                매도전략1=random.choices([i for i in 매도전략1], k=random.randint(1,len(매도전략1)))

            매도전략2=부모전략2[1]
            if len(매도전략2) >1:
                매도전략2=random.choices([i for i in 매도전략2], k=random.randint(1,len(매도전략2)-1))
            else:
                매도전략2=random.choices([i for i in 매도전략2], k=random.randint(1,len(매도전략2)))
            매도전략=매도전략1+매도전략2
            팩터추출 =[i[0] for i in 매도전략] 
            if len(팩터추출)> len(set(팩터추출)): #팩터가 중복됨
                flag2=True
            else:
                flag2=False    

        성과, 매수일_df, 매도일_df, 누적수익률목록, results=self.백테스팅(매수전략, 매도전략)
        
        자식전략=[매수전략,매도전략,성과]
        return 자식전략


    def 자식전략들만들기(self, parents, n_child):
        next_population = []
        for i in range(int(len(parents)/2)):
            for j in range(n_child):
                next_population.append(self.자식전략만들기(parents[i], parents[len(parents) - 1 - i] , 재시도횟수=3))
        return next_population


    def 돌연변이전략만들기(self, 전략):
        매수전략=전략[0]
        매도전략=전략[1]

        매수팩터추출 =[i[0] for i in 매수전략] 
        매도팩터추출 =[i[0] for i in 매도전략] 
        팩터들_subtract_매수팩터추출=[x for x in self.팩터들 if x not in 매수팩터추출]
        팩터들_subtract_매도팩터추출=[x for x in self.팩터들 if x not in 매도팩터추출]
        매수팩터=random.choice(팩터들_subtract_매수팩터추출)
        매수값=self.data[매수팩터].quantile(q=random.random(), interpolation='linear')
        매도팩터=random.choice(팩터들_subtract_매도팩터추출)
        매도값=self.data[매도팩터].quantile(q=random.random(), interpolation='linear')
        
        매수전략.append((매수팩터,매수값))
        매도전략.append((매도팩터, 매도값))
        성과, 매수일_df, 매도일_df, 누적수익률목록, results=self.백테스팅( 매수전략,매도전략)
        돌연변이전략=[매수전략,매도전략,성과]  
        return 돌연변이전략

    def 돌연변이전략들만들기(self, population, chance_of_mutation):
        
        for i in range(len(population)):
            if random.random() * 100 < chance_of_mutation:
                population[i] = self.돌연변이전략만들기(population[i])
        return population 

    def 전략기록(self, results):

        try:
        
            my_file = Path(self.filename)    
            if my_file.is_file():
                pass
            else:
                df=pd.DataFrame(columns=['매수전략', '매도전략', '누적수익률','MDD','CAGR','매매승률','매매횟수','평균수익률','평균손실률'])
                df.to_excel(self.filename,index=False)

            wb = load_workbook(self.filename)
            ws = wb.active
            ws = wb.active
            ws.append(results)
            wb.save(self.filename)
        except Exception as ex:
            print(ex)