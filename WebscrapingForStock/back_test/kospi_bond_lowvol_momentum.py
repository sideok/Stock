'''
Created on 2019. 7. 13.
주식과 채권의 비율 수익률 포트폴리오를 구성하여
현재 시장에 가장 적합한 모멘텀과 변동성을 갖는 포트폴리오를 특정갯수만큼 선택하였을 때의
수익측정 백테스트

일간 손절매 로직 추가 필요.
@author: SIDeok
'''
from cmath import sqrt
from turtledemo.penrose import star

import numpy;
from pandas._libs.index import datetime;
from pandas.plotting import register_matplotlib_converters;

from DBUtil import getQuery;
from StringUtil import lpad, rpad;
import matplotlib.pyplot as plt; 
from ms_access.connectDB import StockDB;


from pandas import Series, DataFrame; #pandas 라이브러리
import math
import calendar
import pandas



# db 커넥션 설정
DB = StockDB()
cs = DB.getCursor()
 
# 시작일 및 종료일 세팅
st_date = datetime(2012, 3, 1);
ed_date = datetime(2019, 6, 1);

#1개월 수익률 조회
query = getQuery("./query/1개월 수익률 추출 쿼리[코스피,채권].sql");
cs.execute(query);
rows = cs.fetchall();
rowsList = [];

BASE_DT = []
VALUE = [];

i = -1;
value = 4000; #초기 투입 금액

# 연복리 산출을 위한 변수
start_val = value;
cycle_cnt = 0;

max_val = value; # mdd 계산을 위한 변수
min_val = value; # mdd 계산을 위한 변수
mdd = 0; # mdd
mdd_dt = ""; # mdd 대상일
for info in rows :
    i += 1;
    if i > 0 :
        info = [info[0], info[1], info[2], rowsList[i-1][3]*info[3]
                                         , rowsList[i-1][4]*info[4]
                                         , rowsList[i-1][5]*info[5]
                                         , rowsList[i-1][6]*info[6]
                                         , rowsList[i-1][7]*info[7]
                                         , rowsList[i-1][8]*info[8]
                                         , rowsList[i-1][9]*info[9]
                                         , rowsList[i-1][10]*info[10]
                                         , rowsList[i-1][11]*info[11]
                                         , rowsList[i-1][12]*info[12]
                                         , rowsList[i-1][13]*info[13] ];
    rowsList.append(info);
    if i < 6 : continue;
    
    V10_0 = ((rowsList[i-1][3 ] - rowsList[i-6][3 ])/rowsList[i-6][3 ])/numpy.std([rowsList[i-6][3 ], rowsList[i-5][3 ], rowsList[i-4][3 ], rowsList[i-3][3 ], rowsList[i-2][3 ], rowsList[i-1][3 ]]);
    V9_1  = ((rowsList[i-1][4 ] - rowsList[i-6][4 ])/rowsList[i-6][4 ])/numpy.std([rowsList[i-6][4 ], rowsList[i-5][4 ], rowsList[i-4][4 ], rowsList[i-3][4 ], rowsList[i-2][4 ], rowsList[i-1][4 ]]);
    V8_2  = ((rowsList[i-1][5 ] - rowsList[i-6][5 ])/rowsList[i-6][5 ])/numpy.std([rowsList[i-6][5 ], rowsList[i-5][5 ], rowsList[i-4][5 ], rowsList[i-3][5 ], rowsList[i-2][5 ], rowsList[i-1][5 ]]);
    V7_3  = ((rowsList[i-1][6 ] - rowsList[i-6][6 ])/rowsList[i-6][6 ])/numpy.std([rowsList[i-6][6 ], rowsList[i-5][6 ], rowsList[i-4][6 ], rowsList[i-3][6 ], rowsList[i-2][6 ], rowsList[i-1][6 ]]);
    V6_4  = ((rowsList[i-1][7 ] - rowsList[i-6][7 ])/rowsList[i-6][7 ])/numpy.std([rowsList[i-6][7 ], rowsList[i-5][7 ], rowsList[i-4][7 ], rowsList[i-3][7 ], rowsList[i-2][7 ], rowsList[i-1][7 ]]);
    V5_5  = ((rowsList[i-1][8 ] - rowsList[i-6][8 ])/rowsList[i-6][8 ])/numpy.std([rowsList[i-6][8 ], rowsList[i-5][8 ], rowsList[i-4][8 ], rowsList[i-3][8 ], rowsList[i-2][8 ], rowsList[i-1][8 ]]);
    V4_6  = ((rowsList[i-1][9 ] - rowsList[i-6][9 ])/rowsList[i-6][9 ])/numpy.std([rowsList[i-6][9 ], rowsList[i-5][9 ], rowsList[i-4][9 ], rowsList[i-3][9 ], rowsList[i-2][9 ], rowsList[i-1][9 ]]);
    V3_7  = ((rowsList[i-1][10] - rowsList[i-6][10])/rowsList[i-6][10])/numpy.std([rowsList[i-6][10], rowsList[i-5][10], rowsList[i-4][10], rowsList[i-3][10], rowsList[i-2][10], rowsList[i-1][10]]);
    V2_8  = ((rowsList[i-1][11] - rowsList[i-6][11])/rowsList[i-6][11])/numpy.std([rowsList[i-6][11], rowsList[i-5][11], rowsList[i-4][11], rowsList[i-3][11], rowsList[i-2][11], rowsList[i-1][11]]);
    V1_9  = ((rowsList[i-1][12] - rowsList[i-6][12])/rowsList[i-6][12])/numpy.std([rowsList[i-6][12], rowsList[i-5][12], rowsList[i-4][12], rowsList[i-3][12], rowsList[i-2][12], rowsList[i-1][12]]);
    V0_10 = ((rowsList[i-1][13] - rowsList[i-6][13])/rowsList[i-6][13])/numpy.std([rowsList[i-6][13], rowsList[i-5][13], rowsList[i-4][13], rowsList[i-3][13], rowsList[i-2][13], rowsList[i-1][13]]);
    
    tmpDic = {3:V10_0, 4:V9_1, 5:V8_2, 6:V7_3, 7:V6_4, 8:V5_5, 9:V4_6, 10:V3_7, 11:V2_8, 12:V1_9, 13:V0_10};
    
    sum = 0;
    rg = 1;
    choice = "";
    tmp_rg = 0;
    for j in range(0,rg) :
        tmpIdx = -1;
        for data in tmpDic :
            if tmpIdx == -1 or tmpDic[data] > tmpDic[tmpIdx] :
                tmpIdx = data;
                
        if tmpDic[tmpIdx] < 0 :
            sum = value;
            choice += ", -1";
            if tmp_rg == 0 :
                tmp_rg = 1;
            break;
        else :
            sum += value * (1 + (rowsList[i][tmpIdx] - rowsList[i-1][tmpIdx])/rowsList[i-1][tmpIdx]);
            tmpDic.pop(tmpIdx);
            choice += ", " + str(tmpIdx);
            tmp_rg += 1;
    
#     print(str(info[0]) + "    " + str(sum*value/tmp_rg+60) + "    " + choice);
    print(str(info[0]) + "    " + str(sum/tmp_rg) + "    " + choice);
    BASE_DT.append(info[0]);
    VALUE.append(sum/tmp_rg);
#     value = sum*value/tmp_rg + 60;
    value = sum/tmp_rg;
    
    # mdd 계산
    if value >= max_val :
        max_val = value;
        min_val = value;
    elif value < min_val :
        min_val = value;
    
    if mdd < (max_val - min_val)/max_val :
        mdd = (max_val - min_val)/max_val;
        mdd_dt = info[0].date().__str__();
    
    cycle_cnt += 1;
# 그래프 그리기
# serAdjust = Series(adjustValue, adjustDate);
   
register_matplotlib_converters();
   
plt.plot(BASE_DT, VALUE,'r', label="1", marker="*");
# plt.plot(val_BASE_DT, val_9_1,'b', label="9:1");
# plt.plot(val_BASE_DT, val_8_2,'r', label="8:2");
# plt.plot(val_BASE_DT, val_7_3,'r', label="7:3");
# plt.plot(val_BASE_DT, val_6_4,'r', label="6:4");


# plt.plot(serAdjust.index, serAdjust.values,'b', label="M/M");
plt.legend(loc='upper left');
plt.xticks(pandas.date_range(BASE_DT[0], BASE_DT[VALUE.__len__()-1], freq="Q-DEC"), rotation=70, fontsize="small"); #x축 단위 설정
plt.xlabel("start: " + str(start_val) + " ,end: " + str(VALUE[VALUE.__len__()-1]) + "\n" + "mdd: " + str(round(mdd*100, 2)) + "%("  + mdd_dt +"), income ratio: " + str(round(math.pow(VALUE[VALUE.__len__()-1]/start_val, 1/(cycle_cnt/12)), 4)) );
plt.ylabel("value");
# plt.ylabel(adjustDate[0].__str__() + " ~ "  + adjustDate[adjustDate.__len__()-1].__str__() + ", rate: " + str(round(adjustValue[adjustValue.__len__()-1]/adjustValue[0], 2)**(1/((adjustDate[adjustDate.__len__()-1] - adjustDate[0]).days/365))));
   
plt.show();

