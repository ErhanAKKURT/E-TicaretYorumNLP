import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import string

df=pd.read_csv('yorum.csv.zip',on_bad_lines='skip',delimiter=';')

def temizle(sutun):
    stopwords=['fakat','lakin','ancak','acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep', 'hepsi', 'her', 'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl', 'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya', 'yani'];
    semboller=string.punctuation
    sutun=sutun.lower()
    for sembol in semboller:
        sutun=sutun.replace(sembol," ")

    for stopword in stopwords:
        s=" "+stopword+" "
        sutun=sutun.replace(s," ")

    sutun=sutun.replace("  "," ")
    return sutun

df['Metin']=df['Metin'].apply(temizle)

cv=CountVectorizer(max_features=300)
X=cv.fit_transform(df['Metin']).toarray();
y=df['Durum']

x_train,x_test,y_train,y_test=train_test_split(X,y,train_size=0.75,random_state=42)

yorum=st.text_area('Yorum Metnini Giriniz')
btn=st.button('Yorumu Kategorilendir')

if btn:
    rf=RandomForestClassifier()
    model=rf.fit(x_train,y_train)
    skor=model.score(x_test,y_test)

    tahmin=cv.transform(np.array([yorum])).toarray()
    kat={
        0:"Olumsuz",1:"Olumlu",2:"Nötr"
    }
    sonuc=model.predict(tahmin)
    s=kat.get(sonuc[0])

    st.subheader(s)
    st.write('Model Skoru :',skor)

kod='''
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import string

df=pd.read_csv('yorum.csv.zip',on_bad_lines='skip',delimiter=';')

def temizle(sutun):
    stopwords=['fakat','lakin','ancak','acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep', 'hepsi', 'her', 'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl', 'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya', 'yani'];
    semboller=string.punctuation
    sutun=sutun.lower()
    for sembol in semboller:
        sutun=sutun.replace(sembol," ")

    for stopword in stopwords:
        s=" "+stopword+" "
        sutun=sutun.replace(s," ")

    sutun=sutun.replace("  "," ")
    return sutun

df['Metin']=df['Metin'].apply(temizle)

cv=CountVectorizer(max_features=300)
X=cv.fit_transform(df['Metin']).toarray();
y=df['Durum']

x_train,x_test,y_train,y_test=train_test_split(X,y,train_size=0.75,random_state=42)

yorum=st.text_area('Yorum Metnini Giriniz')
btn=st.button('Yorumu Kategorilendir')

if btn:
    rf=RandomForestClassifier()
    model=rf.fit(x_train,y_train)
    skor=model.score(x_test,y_test)

    tahmin=cv.transform(np.array([yorum])).toarray()
    kat={
        0:"Olumsuz",1:"Olumlu",2:"Nötr"
    }
    sonuc=model.predict(tahmin)
    s=kat.get(sonuc[0])

    st.subheader(s)
    st.write('Model Skoru :',skor)
'''

st.header('Kaynak Kodları')
st.code(kod,language='python')
