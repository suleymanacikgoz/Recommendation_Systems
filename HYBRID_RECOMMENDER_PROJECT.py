
import pandas as pd
pd.pandas.set_option('display.max_columns', None)
pd.pandas.set_option('display.width', 100)

movie = pd.read_csv('5.Hafta/movie.csv')
movie.head() 
movie.shape

rating = pd.read_csv('5.Hafta/rating.csv')
rating.head()
rating.shape
rating["userId"].nunique() 




df = movie.merge(rating, how="left", on="movieId")

df.head(10)
df.shape





df["title"].value_counts()
comment_counts = pd.DataFrame(df["title"].value_counts()) 
comment_counts


comment_counts["title"] <= 1000
rare_movies = comment_counts[comment_counts["title"] <= 1000].index


df["title"].isin(rare_movies)


df[~df["title"].isin(rare_movies)].head()
common_movies = df[~df["title"].isin(rare_movies)] 

common_movies.shape



user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
user_movie_df.head()

def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv('/Users/dlaraalcan/Desktop/movie.csv')
    rating = pd.read_csv('/Users/dlaraalcan/Desktop/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()
user_movie_df.head()

user_movie_df.index[0:5]

random_user_df = user_movie_df[user_movie_df.index == random_user]
random_user_df.head()

random_user_df.notna()  
random_user_df.notna().any() 


movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()
movies_watched 



user_movie_df.head()
movies_watched_df = user_movie_df[movies_watched] 
movies_watched_df.head() 
movies_watched_df.shape 


user_movie_count = movies_watched_df.T.notnull().sum() # Null olanlar kişinin o filmi izlemedigini belirtir.
user_movie_count = user_movie_count.reset_index()
user_movie_count.head()
user_movie_count.columns = ["userId", "movie_count"]
user_movie_count.head(50)


# Adım 3: Seçilen kullanıcının oy verdiği filmlerin yüzde 60 ve üstünü izleyenleri benzer kullanıcılar olarak görüyoruz.
# Bu kullanıcıların id’lerinden users_same_movies adında bir liste oluşturunuz.
# user_movie_count -> zaten baz aldıgımız kullanıcının izlediği filmler üzerinden hesaplanmıstı

len(movies_watched) # sectigimiz random kullanıcının izledigi film sayısı
perc = len(movies_watched) * 60 / 100 # eşik degeri olacak film sayısını hesaplıyoruz.
perc

# benzer kullanıcıları bulmaya calısıyoruz.

#user_movie_count her kullancının sectigimiz random kullanıcı ile ortak kacar film izlediği bilgisini tutar.
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]
len(users_same_movies) # random user'a benzer kişi sayısı



#############################################
# Görev 4: Öneri Yapılacak Kullanıcı ile En Benzer Kullanıcıların Belirlenmesi
#############################################

# Adım 1: user_same_movies listesi içerisindeki seçili user ile benzerlik gösteren kullanıcıların id’lerinin bulunacağı şekilde movies_watched_df dataframe’ini filtreleyiniz.

#user_same_movies: secilen random kullanıcı ile ortak %60'dan fazla film izlemiş kişileri tutar.
movies_watched_df.head()
movies_watched_df.shape # random user'ın izledigi filmler ve tum kullanıcılar

# sectıgımız user'a benzemeyen user'ları filtreleyelim: benzerlik gösterenler ile devam edelim.
final_df = movies_watched_df[movies_watched_df.index.isin(users_same_movies)] # user_same_movies: benzerligi %60 üzerinde olan user'lar.
final_df.head()
final_df.shape #2326 benzer kullanıcı kaldı.

# Adım 2: Kullanıcıların birbirleri ile olan korelasyonlarının bulunacağı yeni bir corr_df dataframe’i oluşturunuz.

# korelasyon benzerliklerini ölçümler. (-1 ile 1 arasında değişir ilişkinin yönünü ve şiddetini belirten istatistiki bir yöntem)

# user sutuna film satıra gelecek sekilde T alınır.
final_df.T.corr().unstack() # pivot hale getiriyoruz.
corr_df = final_df.T.corr().unstack().sort_values()

corr_df = pd.DataFrame(corr_df, columns=["corr"]) # korelasyon degerlerini yeni bir sutun olusturarak bu sutuna yerleştiriyoruz.
corr_df.head()
corr_df.index.names = ['user_id_1', 'user_id_2'] #  user sutunlarını isimlendiriyoruz.
corr_df.head()
corr_df = corr_df.reset_index()
corr_df.head()
corr_df[corr_df["user_id_1"] == random_user] # sectigimiz random user ile diger izleyicilerin korelasyonuna bakıuoruz.

# Adım 3: Seçili kullanıcı ile yüksek korelasyona sahip (0.65’in üzerinde olan) kullanıcıları filtreleyerek top_users adında yeni bir dataframe oluşturunuz.

# corr_df' de kullanıcıların birbirleriyle korelasyon degerlerini tutuyorduk;

top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65)][["user_id_2", "corr"]].reset_index(drop=True)
top_users = top_users.sort_values(by='corr', ascending=False) # secilen random kulalnıcı ile 0.65 degerin üzerinde korelasyona sahip kullanıcıların sıralanmıs hali.
top_users.shape

# column adını degiştirelim:
top_users.rename(columns={"user_id_2": "userId"}, inplace=True) # sözlük yapısı sayesinde unique degerler geliyor.
top_users


# Adım 4:  top_users dataframe’ine rating veri seti ile merge ediniz
# filmleri de görmek istiyoruz.
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner') # rating veri setinde "userId", "movieId", "rating" değişkenlerini alıyoruz.
# inner: ortak olanları getirir.
top_users_ratings.tail() # sectigimiz random izleyicinin kendisine benzer -> corr degeri 0.65 üstü olan kullanıcılar ile izledigi filmlere verdiği rating degerleri.
top_users_ratings = top_users_ratings[top_users_ratings["userId"] != random_user] # veriden random user'ın kendi id'sini cıkartıyoruz
top_users_ratings["userId"].unique() #kendisine benzer izleyicilerin user'id'leri
top_users_ratings



#############################################
# Görev 5: Weighted Average Recommendation Score'un Hesaplanması ve İlk 5 Filmin Tutulması
#############################################

# sadece korelasyona göre tavsiye vermek istemedigimiz için bir skor olusturuyoruz.
# benzer user'ın filme verdigi puan yüksek olabilir fakat korelasyonu düşüktür.,
# her iki durumu da göz önünde bulundurmak adına skor olusturuyoruz.

# Adım 1: Her bir kullanıcının corr ve rating değerlerinin çarpımından oluşan weighted_rating adında yeni bir değişken oluşturunuz.

top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
top_users_ratings.head() # movie'ler coklamıs durumda 6 benzer kullanıcı oldugu için.

# Adım 2: Film id’si ve her bir filme ait tüm kullanıcıların weighted rating’lerinin ortalama değerini içeren recommendation_df adında yeni bir
# dataframe oluşturunuz.

# top_users_ratings random user'a cok benzer kullanıcılar ve izledikleri filmlere verdikleri oylar.
# bu kullanıcıların izledikleri filmlerin ortalama agırlıklandırılmıs puanı.
recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"}) # filmleri tekilleştirelim
recommendation_df.head()

recommendation_df = recommendation_df.reset_index()
recommendation_df.head()
recommendation_df.shape

# Adım 3: Adım3: recommendation_df içerisinde weighted rating'i 3.5'ten büyük olan filmleri seçiniz ve weighted rating’e göre sıralayınız.
# İlk 5 gözlemi movies_to_be_recommend olarak kaydediniz.
recommendation_df[recommendation_df["weighted_rating"] > 3.5]
movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5].sort_values("weighted_rating", ascending=False)[0:5]
movies_to_be_recommend.head()

# Adım 4:  Tavsiye edilen 5 filmin isimlerini getiriniz.
movies_to_be_recommend.merge(movie[["movieId", "title"]])["title"] # film isimleri gorebılmek adına
# movies_to_be_recommend zaten sıralı oldugu için en üstte gelen film ilk önerimiz olur.


# 0    Mystery Science Theater 3000: The Movie (1996)
# 1                               Natural, The (1984)
# 2                             Super Troopers (2001)
# 3                         Christmas Story, A (1983)
# 4                       Sonatine (Sonachine) (1993)



#############################################
# Görev 6: Item-Based Recommendation
#############################################

# Kullanıcının en son izlediği ve en yüksek puan verdiği filmin adına göre item-based öneri yapınız.
user = 108170

# Adım 1: movie,rating veri setlerini okutunuz.
movie = pd.read_csv('5.Hafta/movie.csv')
rating = pd.read_csv('5.Hafta/rating.csv')


# Adım 2: Öneri yapılacak kullanıcının 5 puan verdiği filmlerden puanı en güncel olan filmin id'sinin alınız.
# Filmi belirliyoruz.
movie_id = rating[(rating["userId"] == user) & (rating["rating"] == 5.0)].sort_values(by="timestamp", ascending=False)["movieId"][0:1].values[0]
# sadece filmi istedigim için movieID  alıyorum. yorum yapılan ilk film.
# values[0] ilk degerini almak istedigim için values liste döndürür. (ilk degeri id)


# Adım 3 :User based recommendation bölümünde oluşturulan user_movie_df dataframe’ini seçilen film id’sine göre filtreleyiniz.
# sadece secili filme ait satırlar gelsin
user_movie_df[movie[movie["movieId"] == movie_id]["title"]]
movie_df = user_movie_df[movie[movie["movieId"] == movie_id]["title"].values[0]]
# user_movie_df: satırda kullanıcılar, sutunda filmler, kesişimlerinde rating degerlerinin bulundugu df.


# Adım 4: Filtrelenen dataframe’i kullanarak seçili filmle diğer filmlerin korelasyonunu bulunuz ve sıralayınız.
user_movie_df.corrwith(movie_df).sort_values(ascending=False).head(10)

user_movie_df.head() # tum kullanıcıların filmlere ait oyları ( var veya yok)


# Son iki adımı uygulayan fonksiyon
def item_based_recommender(movie_name, user_movie_df):
    movie = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie).sort_values(ascending=False).head(10)

# Adım 5: Seçili film’in kendisi haricinde ilk 5 film’I öneri olarak veriniz.
movies_from_item_based = item_based_recommender(movie[movie["movieId"] == movie_id]["title"].values[0], user_movie_df)

# 1'den 6'ya kadar. 0'da filmin kendisi var. Onu dışarda bıraktık.
movies_from_item_based[1:6].index # 0. index kendisi.

