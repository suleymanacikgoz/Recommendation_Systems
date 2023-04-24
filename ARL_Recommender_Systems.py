import pandas as pd
pd.set_option("display.max_columns",None)
pd.set_option("display.width",500)
pd.set_option("display.expand_frame_repr",False)
from mlxtend.frequent_patterns import apriori, association_rules

#Kullanıcı 1’in sepetinde bulunan ürünün id'si: 21987
#Kullanıcı 2’in sepetinde bulunan ürünün id'si : 23235
#Kullanıcı 3’in sepetinde bulunan ürünün id'si : 22747



#Görev 1:Veriyi hazırlama

#Adım 1: Online Retail II veri setinden 2010-2011 sheet’ini okutunuz.
df=pd.read_excel("Odevler/5.Hafta/Bonus ARL_Recommender_System/online_retail_II.xlsx", sheet_name='Year 2010-2011')
df.head()
#Adım 2:StockCode’u POST olan gözlem birimlerini drop ediniz. (POST her faturaya eklenen bedel, ürünü ifade etmemektedir.)

df=df[~(df["StockCode"]=="POST")]

df
#Adım 3:Boş değer içeren gözlem birimlerini drop ediniz

df.dropna

#Adım 4:Invoice içerisinde C bulunan değerleri veri setinden çıkarınız. (C faturanın iptalini ifade etmektedir.)

df=df[~df["Invoice"].str.contains("C",na=False)]

#Adım 5: Price değeri sıfırdan küçük olan gözlem birimlerini filtreleyiniz.

df=df[df["Price"]>0]

#Adım 6: Price ve Quantity değişkenlerinin aykırı değerlerini inceleyiniz, gerekirse baskılayınız.

df["Price"].describe().T

quartile1 = df["Price"].quantile(0.01)
quartile3 = df["Price"].quantile(0.99)
interquantile_range=quartile3-quartile1
up_limit=quartile3+1.5*interquantile_range
low_limit=quartile1-1.5*interquantile_range



df.loc[(df["Price"]<low_limit),"Price"]=low_limit
df.loc[(df["Price"]>up_limit),"Price"]=up_limit


df["Quantity"].describe().T

quartile1 = df["Quantity"].quantile(0.01)
quartile3 = df["Quantity"].quantile(0.99)
interquantile_range=quartile3-quartile1
up_limit=quartile3+1.5*interquantile_range
low_limit=quartile1-1.5*interquantile_range



df.loc[(df["Quantity"]<low_limit),"Quantity"]=low_limit
df.loc[(df["Quantity"]>up_limit),"Quantity"]=up_limit


#Görev 2: Alman Müşteriler Üzerinden Birliktelik Kuralları Üretme

#Adım 1: ürün pivot table’i oluşturacak create_invoice_product_df fonksiyonunu tanımlayınız.

df=df[df["Country"]=="Germany"]



#df.pivot_table(index="Invoice",columns="Description",values="Quantity")
create_invoice_product_df=df.groupby(["Invoice","Description"])["Quantity"].sum().unstack()
create_invoice_product_df.head()

#Adım 2: Kuralları oluşturacak create_rules fonksiyonunu tanımlayınız ve alman müşteriler için kurallarını bulunuz.

create_invoice_product_df=create_invoice_product_df.fillna(0).applymap(lambda x : 1 if x>0 else 0)

create_invoice_product_df.head()


frequent_itemsets=apriori(create_invoice_product_df,min_support=0.01,use_colnames=True)


frequent_itemsets.sort_values("support",ascending=False)

rules=association_rules(frequent_itemsets,metric="support",min_threshold=0.01)

rules


rules[(rules["confidence"]>0.1)&(rules["lift"]>5)&(rules["support"]>0.02)]

#Görev 3: Sepet İçerisindeki Ürün Id’leri Verilen Kullanıcılara Ürün Önerisinde Bulunma

#Adım 1: check_id fonksiyonunu kullanarak verilen ürünlerin isimlerini bulunuz.

#Adım 2: arl_recommender fonksiyonunu kullanarak 3 kullanıcı için ürün önerisinde bulununuz.

#Adım 3: Önerilecek ürünlerin isimlerine bakınız.




