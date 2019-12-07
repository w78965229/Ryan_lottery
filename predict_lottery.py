from gurobipy import *
import csv
import random
import math
class balls(object):
    def __init__(self,index,prob):
        self.index=index
        self.prob=prob

#read data
with open('97_108_data.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    data=[]
    for row in rows:
        data.append(row)
    # print(type(data[0][0]))
#calculate probs of balls
floatspot=10
number_of_times=len(data)
print('有',number_of_times,'期')
first_zone_times=[0 for i in range(38)]
second_zone_times=[0 for i in range(8)]
for i in range(len(data)):
    for j in range(0,6):
        first_zone_times[int(data[i][j])-1]+=1
for i in range(len(data)):
    second_zone_times[int(data[i][-1])-1]+=1
print('一區球出現次數:\n',first_zone_times)
print('二區球出現次數:\n',second_zone_times)

turn_integer=pow(10,floatspot)

first_zone_prob=[]
second_zone_prob=[]
for i in range(len(first_zone_times)):
    first_zone_prob.append(int(int(first_zone_times[i])/(number_of_times*6)*turn_integer))
for i in range(len(second_zone_times)):
    second_zone_prob.append(int(int(second_zone_times[i])/number_of_times*turn_integer))

print('一區球出現機率:\n',first_zone_prob)
print('二區球出現機率:\n',second_zone_prob)

ball_one_zone=[]
ball_two_zone=[]
number_of_balls_first_zone=38
number_of_balls_second_zone=8
avgprob_first_zone=int(sum(first_zone_prob)/number_of_balls_first_zone)
avgprob_second_zone=int(sum(second_zone_prob)/number_of_balls_second_zone)
orgprob_first_zone=int(1/38*turn_integer)
orgprob_second_zone=int(1/8*turn_integer)

print('avgprob_first_zone=',avgprob_first_zone,'org_prob_first_zone=',orgprob_first_zone)
print('avgprob_second_zone',avgprob_second_zone,'orgprob_second_zone',orgprob_second_zone)
for i in range(1,len(first_zone_prob)+1):
    ball=balls(i,first_zone_prob[i-1])
    ball_one_zone.append(ball)
for i in range(1,len(second_zone_prob)+1):
    ball=balls(i,second_zone_prob[i-1])
    ball_two_zone.append(ball)

# for i in range(len(ball_one_zone)):
#     print('index=',ball_one_zone[i].index,'prob=',ball_one_zone[i].prob)

#gurobi_1st
M=1000000000000000
try:
    m=Model('predict_lottery')
    #set variables
    P=m.addVars(number_of_balls_first_zone,vtype=GRB.BINARY,lb=0,ub=1)
    A=m.addVars(number_of_balls_first_zone,vtype=GRB.INTEGER)

    # set obj
    obj=LinExpr()
    for i in range(number_of_balls_first_zone):
        obj+=A[i]
    m.setObjective(((obj/number_of_balls_first_zone)-orgprob_first_zone),GRB.MINIMIZE)

    # set constraint1
    cons1=LinExpr()
    for i in range(number_of_balls_first_zone):
        cons1+=P[i]
    m.addConstr(cons1==6)

    # set constraint2
    for i in range(number_of_balls_first_zone):
        m.addConstr(M*(1-P[i])+A[i]>=((first_zone_times[i]+1)/(number_of_times*6+1))*turn_integer)
    # for i in range(number_of_balls_first_zone):
    #     m.addConstr(((first_zone_times[i])/(number_of_times*6+1))*turn_integer<=A[i])

    # for i in range(number_of_balls_first_zone):
    #     m.addConstr(A[i]<=+M*(1-P[i])+((first_zone_times[i]+1)/(number_of_times*6+1))*turn_integer)

    # optimize

    m.update()
    m.optimize()

    #check out
    predict_number=[]
    predict_prob=[]
    for i in range(number_of_balls_first_zone):
        if P[i].X==1:
            predict_number.append(ball_one_zone[i].index)
            predict_prob.append(A[i].X)
    # print('號碼機率:',predict_prob)
    for i in range(number_of_balls_first_zone):
        if P[i].X==1:
            print('i=',i,'P=',P[i].X,'A=',str(A[i].X),'org_prob=',str(first_zone_prob[i]))






except GurobiError as e:
    print('Error code ' + str(e.message) + ": " + str(e))

try:
    M2=1000000000000000
    m=Model('predict_lottery_2')
    #set variables
    P=m.addVars(number_of_balls_second_zone,vtype=GRB.BINARY,lb=0,ub=1)
    A=m.addVars(number_of_balls_second_zone,vtype=GRB.INTEGER)

    # set obj
    obj=LinExpr()
    for i in range(number_of_balls_second_zone):
        obj+=A[i]
    m.setObjective(((obj/number_of_balls_second_zone)-orgprob_second_zone),GRB.MINIMIZE)

    # set constraint1
    cons1=LinExpr()
    for i in range(number_of_balls_second_zone):
        cons1+=P[i]
    m.addConstr(cons1==1)

    # set constraint2
    for i in range(number_of_balls_second_zone):
        m.addConstr(M2*(1-P[i])+A[i]>=((second_zone_times[i]+1)/(number_of_times+1))*turn_integer)


    for i in range(number_of_balls_second_zone):
        m.addConstr(((second_zone_times[i])/(number_of_times+1))*turn_integer<=A[i])
    #
    # for i in range(number_of_balls_second_zone):
    #     m.addConstr(A[i]<=M2*(1-P[i])+((second_zone_times[i]+1)/(number_of_times+1))*turn_integer)

    # optimize

    m.update()
    m.optimize()

    #check out
    predict_number_2=[]
    predict_prob_2=[]
    for i in range(number_of_balls_second_zone):
        if P[i].X==1:
            predict_number_2.append(ball_two_zone[i].index)
            predict_prob_2.append(A[i].X)

    # print('號碼機率:',predict_prob_2)
    # for i in range(number_of_balls_second_zone):
    #     if P[i].X==1:
    #         print('i=',i,'P=',P[i].X,'A=',str(A[i].X),'org_prob=',str(second_zone_prob[i]))

except GurobiError as e:
    print('Error code ' + str(e.message) + ": " + str(e))


#predict max_prob
# for i in range(number_of_balls_first_zone):
#     print('ball_index',ball_one_zone[i].index,'prob',ball_one_zone[i].prob)
ball_one_zone=sorted(ball_one_zone,key=lambda x:x.prob)
ball_two_zone=sorted(ball_two_zone,key=lambda x:x.prob)

# for i in range(number_of_balls_first_zone):
#     print('ball_index',ball_one_zone[i].index,'prob',ball_one_zone[i].prob)
# print('\n')
# for i in range(number_of_balls_second_zone):
#     print('ball_index',ball_two_zone[i].index,'prob',ball_two_zone[i].prob)

predict_max_first_list=[]
predict_max_second_list=[]
for i in range(-6,0):
    predict_max_first_list.append(ball_one_zone[i].index)

predict_max_second_list.append(ball_two_zone[-1].index)



#predict close min

minus_first_zone_list=[0 for i in range(number_of_balls_first_zone)]
minus_second_zone_list=[0 for i in range(number_of_balls_second_zone)]
for i in range(number_of_balls_first_zone):
    minus_first_zone_list[i]=abs(int(first_zone_prob[i])-orgprob_first_zone)
for i in range(number_of_balls_second_zone):
    minus_second_zone_list[i]=abs(int(second_zone_prob[i])-orgprob_second_zone)
# print(minus_first_zone_list)
# print(minus_second_zone_list)
minus_first_zone=[]
minus_second_zone=[]

for i in range(number_of_balls_first_zone):
    ball=balls(i+1,minus_first_zone_list[i])
    minus_first_zone.append(ball)
minus_first_zone=sorted(minus_first_zone,key=lambda x:x.prob)

predict_mean_first_zone=[]
predict_mean_second_zone=[]
for i in range(0,6):
    predict_mean_first_zone.append(minus_first_zone[i].index)
predict_mean_second_zone.append(minus_second_zone_list.index(min(minus_second_zone_list))+1)

print('\n')
##random predict
random_array_fst=[]
random_array_sec=[]
while len(random_array_fst)<6:
    ballll=random.randint(1,38)
    if ballll not in random_array_fst:
        random_array_fst.append(ballll)
    else:
        continue
random_array_sec.append(random.randint(1,8))

print('\n')
#simulate to matching
#gurobi version
# print('data=',data)
guro_sim_array=[[0,0] for i in range(len(data))]
count_fst_zone=0
count_sec_zone=0
for i in range(len(data)):
    for j in range(6):
        if str(predict_number[j]) in data[i][0:6]:
            count_fst_zone+=1
    guro_sim_array[i][0]=count_fst_zone
    count_fst_zone=0
    if predict_number_2[0]==int(data[i][7]):
        count_sec_zone=1
    guro_sim_array[i][1]=count_sec_zone
    count_sec_zone=0
# print('guro_sim_array=',guro_sim_array)
avg_fst_times =0
avg_money_times=0
for i in range(len(guro_sim_array)):
    avg_fst_times += guro_sim_array[i][0]
    if guro_sim_array[i][1]==1:
        avg_money_times+=guro_sim_array[i][0]
print('Gurobi---------------------------------------------')
print('Gurobi預測一區號碼:',predict_number)
print('Gurobi預測二區號碼:',predict_number_2)
print('預測命中幾顆球=',avg_fst_times,'平均一期命中第一區命中=',round((avg_fst_times/number_of_times),3),'顆球')
print('第二區有中且預測命中幾顆球',avg_money_times,'第二區有中且平均一期第一區命中=',round(avg_money_times/number_of_times,3),'顆球')
print('最大預測中獎=',max(guro_sim_array))
# max version
max_sim_array=[[0,0] for i in range(len(data))]
max_count_fst_zone=0
max_count_sec_zone=0
for i in range(len(data)):
    for j in range(6):
        if str(predict_max_first_list[j]) in data[i][0:6]:
            max_count_fst_zone+=1
    max_sim_array[i][0]=max_count_fst_zone
    max_count_fst_zone=0
    if predict_max_second_list[0]==int(data[i][7]):
        max_count_sec_zone=1
    max_sim_array[i][1]=max_count_sec_zone
    max_count_sec_zone=0
print('\nMAX PROB---------------------------------------------')
# print('max_sim_array=',max_sim_array)
max_avg_fst_times =0
max_avg_money_times=0
for i in range(len(max_sim_array)):
    max_avg_fst_times += max_sim_array[i][0]
    if max_sim_array[i][1]==1:
        max_avg_money_times+=max_sim_array[i][0]
print('Max預測一區號碼:',sorted(predict_max_first_list))
print('Max預測二區號碼:',predict_max_second_list)
print('預測命中幾顆球=',max_avg_fst_times,'平均一期命中第一區命中=',round((max_avg_fst_times/number_of_times),3),'顆球')
print('第二區有中且預測命中幾顆球',max_avg_money_times,'第二區有中且平均一期第一區命中=',round(max_avg_money_times/number_of_times,3),'顆球')
print('最大預測中獎=',max(max_sim_array))

#mean version
mean_sim_array=[[0,0] for i in range(len(data))]
mean_count_fst_zone=0
mean_count_sec_zone=0
for i in range(len(data)):
    for j in range(6):
        if str(predict_mean_first_zone[j]) in data[i][0:6]:
            mean_count_fst_zone+=1
    mean_sim_array[i][0]=mean_count_fst_zone
    mean_count_fst_zone=0
    if predict_mean_second_zone[0]==int(data[i][7]):
        mean_count_sec_zone=1
    mean_sim_array[i][1]=mean_count_sec_zone
    mean_count_sec_zone=0
print('\nMEAN PROB--------------------------------')
# print('mean_sim_array=',mean_sim_array)
mean_avg_fst_times =0
mean_avg_money_times=0
for i in range(len(mean_sim_array)):
    mean_avg_fst_times += mean_sim_array[i][0]
    if mean_sim_array[i][1]==1:
        mean_avg_money_times+=mean_sim_array[i][0]
print('Mean預測一區號碼:',sorted(predict_mean_first_zone))
print('Mean預測二區號碼:',predict_mean_second_zone)
print('預測命中幾顆球=',mean_avg_fst_times,'平均一期命中第一區命中=',round((mean_avg_fst_times/number_of_times),3),'顆球')
print('第二區有中且預測命中幾顆球',mean_avg_money_times,'第二區有中且平均一期第一區命中=',round(mean_avg_money_times/number_of_times,3),'顆球')
print('最大預測中獎=',max(mean_sim_array))
#random version
random_sim_array=[[0,0] for i in range(len(data))]
random_count_fst_zone=0
random_count_sec_zone=0
random_array_fst_list=list(random_array_fst)
random_array_sec_list=list(random_array_sec)

for i in range(len(data)):
    for j in range(6):
        if str(random_array_fst_list[j]) in data[i][0:6]:
            random_count_fst_zone+=1
    random_sim_array[i][0]=random_count_fst_zone
    random_count_fst_zone=0
    if random_array_sec_list[0]==int(data[i][7]):
        random_count_sec_zone=1
    random_sim_array[i][1]=random_count_sec_zone
    random_count_sec_zone=0
print('\nRandom--------------------------------------------------')
# print('random_sim_array=',random_sim_array)
random_avg_fst_times =0
random_avg_money_times=0
for i in range(len(random_sim_array)):
    random_avg_fst_times += random_sim_array[i][0]
    if random_sim_array[i][1]==1:
        random_avg_money_times+=random_sim_array[i][0]
print('Random預測一區號碼=',sorted(list(random_array_fst)))
print('Random第二區號碼=',list(random_array_sec))
print('預測命中幾顆球=',random_avg_fst_times,'平均一期命中第一區命中=',round((random_avg_fst_times/number_of_times),3),'顆球')
print('第二區有中且預測命中幾顆球',random_avg_money_times,'第二區有中且平均一期第一區命中=',round(random_avg_money_times/number_of_times,3),'顆球')
print('最大預測中獎=',max(random_sim_array))
print('--------------------------------------------------------')

