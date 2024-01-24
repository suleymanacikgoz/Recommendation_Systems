
import pandas as pd
import datetime as dt
pd.set_option("display.max_columns",None)
pd.set_option("display.width",500)
pd.set_option("display.expand_frame_repr",False)
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df=pd.read_csv("Odevler/5.Hafta/armut_data.csv")

df.head()
df.shape


df["Hizmet"]=df["ServiceId"].astype(str)+"_"+df["CategoryId"].astype(str)

df.head()

df["CreateDate"]=pd.to_datetime(df["CreateDate"])
df["CreateDate"].info
df['new_date'] = df['CreateDate'].dt.strftime('%Y-%m')
df.head()

df["SepetId"]=df["UserId"].astype(str)+"_"+df["new_date"].astype(str)
df.head()

df['new_date'] = pd.to_datetime(df['new_date'])


pivot_df=df.groupby(["SepetId","Hizmet"])["Hizmet"].count().unstack().fillna(0).applymap(lambda x:1 if x > 0 else 0)

birlikte=apriori(pivot_df,min_support=0.01,use_colnames=True)
birlikte.sort_values("support",ascending=False)
rules=association_rules(birlikte,metric="support",min_threshold=0.01)


servis=25_0
sorted_rules=rules.sort_values("lift",ascending=False)
recommendation_list=[]

for i,item in enumerate(sorted_rules["antecedents"]):
    for j in list(item):
        if j == servis:
            recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])


recommendation_list
