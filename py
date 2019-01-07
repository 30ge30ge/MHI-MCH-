
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import statsmodels.api as sm
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus']=False
df=pd.read_csv("F:/shuju/香港期货数据/201804/20180403/HIMHI04.csv",engine='python',sep=",")
df=df[["Time","Price"]]
df=df.drop_duplicates(subset="Time", keep='first', inplace=False)
df.reset_index(drop=True, inplace=True)
df_mch=pd.read_csv("F:/shuju/香港期货数据/201804/20180403/HIMCH04.csv",engine='python',sep=",")
df_mch=df_mch[["Time","Price"]]
df_mch=df_mch.drop_duplicates(subset="Time", keep='first', inplace=False)
df_mch.reset_index(drop=True, inplace=True)
df_new=pd.merge(df,df_mch,on="Time")
df_new.rename(columns={"Price_x":"MHI", "Price_y":"MCH"}, inplace = True)
df_new["价差"]=df_new["MHI"]-df_new["MCH"]
df_new["Time"] = pd.to_datetime(df_new["Time"])
df_new.set_index("Time", inplace=True)
print(df_new)
figure=plt.subplots(figsize=(12,4))
plt.title("MCH-MHI跨品种套利分析")
plt.plot(df_new["MHI"],color="r")
plt.plot(df_new["MCH"],color="g")
plt.xticks(rotation=90)
plt.show()
#线性相关检查
X=df_new["MCH"]
Y=df_new["MHI"] 
model=sm.OLS(Y,X)
result=model.fit()
print(result.summary())
print("回归系数为：",result.params)
print("R2:",result.rsquared)
print("R2无限接近与1,线性相关显著")
y_fitted=result.fittedvalues
fig,ax=plt.subplots(figsize=(12,4))
plt.title("MCH-MHI跨品种线性相关图")
ax.plot(X,Y,"o",label="data")
ax.plot(X,y_fitted,"r--.",label="OLS")
ax.legend(loc="best")
plt.show()
#计算价差均值和标准差，并统计上下轨
print("价差为小恒指价格减去小国企指数价格")
A=list(df_new["价差"])
avg=np.mean(A)
avg=round(avg)
print("价差均值为:",avg)
up=avg+2*np.std(A)
up=round(up)
print("上轨为",up)
down=avg-2*np.std(A)
down=round(down)
print("下轨为",down)
print("价差最大数:",np.max(A))
print("价差中位数:",np.median(A))
print("价差最小数:",np.min(A))
print("因为上轨大于最大数,2018年4月做空价差机会为0")
df_long=df_new.loc[lambda df_new: df_new.价差 < 17724, :]
print("做多小恒指选取卖1价,做空小国企指数选择买1价的机会为"+str(len(list(df_long["MHI"])))+"次")
print(df_long)
spread_now=A[-1]
df_long.to_csv("F:/shuju/跨品种套利具体时间.csv")
