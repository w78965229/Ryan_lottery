import requests
import time
import csv
from bs4 import BeautifulSoup

LOTTERY_URL='https://www.taiwanlottery.com.tw/lotto/superlotto638/history.aspx'
def main():

    parser_info=get_web(LOTTERY_URL)
    print(parser_info)
    ball_array=get_ball_info(parser_info)
    print('clawler_twice_ball_array=',ball_array)
    writecsv('97_108_data.csv',ball_array)
def writecsv(filename,data):
    with open(str(filename),'a',newline='') as csvfile:
        writer= csv.writer(csvfile)
        writer.writerows(data)
        print('finish writing into'+' '+str(filename))

def get_web(url):
    try:
        resp=requests.get(url=url)
        if resp.status_code==200:
            soup=BeautifulSoup(resp.text,'html.parser')
            return soup
    except Exception as e:
        return None
def get_ball_info(dom):
    key='SuperLotto638Control_history1_dlQuery_No'
    run_times_lottery=2
    number_of_ball=7
    ball_array = [[0 for j in range(8)] for i in range(2)]
    print('row=',len(ball_array))
    print('column=',len(ball_array[0]))

    # soup=BeautifulSoup(dom,'html5lib)
    for i in range(run_times_lottery):
        for j in range(1,number_of_ball+1):
            ball_info=dom.find(id='SuperLotto638Control_history1_dlQuery_No'+str(j)+'_'+str(i)).text



            ball_array[i][j-1]=ball_info
        ball_array[i][-1]=''
        ball_array[i][-1],ball_array[i][-2]=ball_array[i][-2],ball_array[i][-1]
    return ball_array



if __name__=='__main__':
    main()