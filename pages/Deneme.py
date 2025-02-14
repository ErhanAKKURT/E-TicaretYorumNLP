import streamlit as st
import pandas as pd
import datetime


def baslik(anaPara, aylikGelir, evFiyat, kiraGelir, krediSure, krediAy, pesinatYuzde, krediOdeme, belirtilenYas, pesinat):
    # Başlık ve açıklamaları gösteren fonksiyon.
    st.markdown('<h1 style="color:#274866;">Konut Yatırım Projesi</h1>', unsafe_allow_html=True)
    with st.container():
        with st.container(border=True):
            st.write(":blue[Form'da Doldurduğunuz Bilgiler:]")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"Birikiminiz: :blue[{anaPara} ₺]")
            with col2:
                st.caption(f"Aylık Geliriniz: :blue[{aylikGelir} ₺]")
            with col3:
                st.caption(f"Daire Fiyatı: :blue[{evFiyat} ₺]")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"Kira Gelir Beklentisi: :blue[{kiraGelir} ₺]")
            with col2:
                st.caption(f"Kredi Süresi: :blue[{krediSure} yıl - ({krediAy}) ay]")
            with col3:
                st.caption(f"Belirtmiş Olduğunuz Yaş: :blue[{belirtilenYas[0]}-{belirtilenYas[1]} yaş]")
            st.caption(f"Ödenecek Peşinat: Seçmiş olduğunuz Peşinat :blue[%{pesinatYuzde}]'dir. "
                       f"Buna göre, :blue[{format(int(evFiyat), ',')} ₺] değerindeki bir dairenin :blue[{format(int(pesinat), ',')}] ₺ peşinatını ödediğinizi varsayarsak, "
                       f" Aylık kredi :blue[{round(krediOdeme)} ₺] ödemeniz çıkmaktadır.")

    st.caption(
        ':blue[NOT: Butonuna tıkladığınız an da yukarıda belirtmiş olduğunuz değerler çerçevesinde hesaplama yapılacaktır!]')


def kullanici_veriler():
    # Kullanıcıdan gerekli verileri alıp ve döndüren fonksiyon.
    with st.sidebar:
        st.caption(
            "Form'da belirtecek olduğunuz değerler arasında Daire alma ve Borç süreçlerinizi inceleyebilirsiniz.")
        belirtilenYas = st.slider("Yaş Aralığını Belirtiniz:", 0, 120, (25, 65))
        st.caption(f":blue[Belirtmiş olduğunuz yaş ' {belirtilenYas[0]}-{belirtilenYas[1]} ' yaş aralığıdır.]")
        toplamAy = int((belirtilenYas[1] - belirtilenYas[0]) * 12)
        mevcutAy = 1

        anaPara = st.number_input("Mevcut Ana Para (₺):", value=0, step=100000)
        aylikGelir = st.number_input("Aylık Geliriniz (₺):", value=3000, step=1000)
        kiraGelir = st.number_input("Daireniz için Kira Geliri (₺):", value=8000, step=1000)
        evFiyat = st.number_input("Daire Fiyatını Belirtiniz (₺):", value=1250000, step=50000)
        pesinatYuzde = st.slider("Peşinat Yüzdesini Belirtiniz (%):", 0, 100, 20)
        pesinat = evFiyat * pesinatYuzde / 100
        krediSure = st.number_input("Kredi süresini seçiniz (Yıl):", value=15)
        krediAy = krediSure * 12
        krediOdeme = (evFiyat - pesinat) / krediAy

        return belirtilenYas, toplamAy, anaPara, aylikGelir, kiraGelir, evFiyat, pesinatYuzde, pesinat, krediSure, krediAy, krediOdeme


def finansal_hesaplama(belirtilenYas, toplamAy, anaPara, aylikGelir, kiraGelir, evFiyat, pesinatYuzde, pesinat,
                         krediSure, krediAy, krediOdeme):
    # Başlangıç değerleri
    mevcutEv = 0
    toplamKrediBorcu = 0
    aylikNetGelirList = []
    krediBorcList = []
    anaParaList = []
    krediAdetList = []
    mevcutEvList = []
    dateList = []
    aylikKrediList = []

    for i in range(1, toplamAy + 1):
        krediAdet = len([j for j in aylikKrediList if j > 0])
        anaPara -= krediAdet * krediOdeme
        anaPara += aylikGelir
        toplamKrediBorcu -= krediAdet * krediOdeme
        aylikNetGelir = aylikGelir - (krediAdet * krediOdeme)

        # Kredi listelerini güncelle
        krediBorcSure = [kredi - 1 for kredi in aylikKrediList]
        aylikKrediList = krediBorcSure

        # Daire alımı
        while anaPara >= pesinat:
            anaPara -= pesinat
            mevcutEv += 1
            aylikKrediList.append(krediAy)
            aylikGelir += kiraGelir
            toplamKrediBorcu += (evFiyat - pesinat)

        # Tarih ve yaş hesaplama
        aktifKredi = sum(1 for k in aylikKrediList if k > 0)
        baslangicTarihi = datetime.datetime.now()
        yilBelirle = i // 12
        ayBelirle = i % 12
        if ayBelirle == 0:
            ayBelirle = 12
            yilBelirle -= 1
        guncelTarih = baslangicTarihi.replace(year=baslangicTarihi.year + yilBelirle, month=ayBelirle)
        tarihStr = guncelTarih.strftime("%d/%m/%Y")
        mevcutYas = belirtilenYas[0] + yilBelirle
        dateList.append(f"{mevcutYas} - {tarihStr}")
        aylikNetGelirList.append(aylikNetGelir)
        anaParaList.append(anaPara)
        krediBorcList.append(toplamKrediBorcu)
        krediAdetList.append(aktifKredi)
        mevcutEvList.append(mevcutEv)

    return dateList, aylikNetGelirList, anaParaList, mevcutEvList, krediBorcList, krediAdetList



def create_tablo(dateList, aylikNetGelirList, anaParaList, mevcutEvList, krediBorcList, krediAdetList):
    # Hesaplanan verilerle bir pandas DataFrame oluşturan fonksiyon.
    veriler = {
        "Yaş / Tarih": dateList,
        "Aylık Net gelir": aylikNetGelirList,
        "Ana Para": anaParaList,
        "Mevcut Daire": mevcutEvList,
        "Toplam Kredi Borç": krediBorcList,
        "Aktif Kredi Adet": krediAdetList,
    }
    df = pd.DataFrame(veriler)
    df = df.sort_values("Yaş / Tarih")
    return df


def sonuc_gosterim(df, belirtilenYas, mevcutEv, kiraGelir, toplamKrediBorcu, krediAdet):
    # Sonuçları gösteren fonksiyon.
    with st.container():
        st.caption(f":blue[Belirtmiş olduğunuz bilgiler dahilinde {belirtilenYas[0]} - {belirtilenYas[1]} Yaş aralığı Yatırım Durumu]")
        with st.expander('Tablo Özet Bilgiler İçin Tıklayınız.'):
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"Toplam Daire Sayısı: :blue[{mevcutEv}]")
                st.caption(f"Toplam Kira Geliri: :blue[{mevcutEv * kiraGelir} ₺]")
            with col2:
                st.caption(f"Toplam Kredi Borcu: :blue[{toplamKrediBorcu} ₺]")
                st.caption(f"Toplam Kalan Kredi Adeti: :blue[{krediAdet}]")

        st.dataframe(df)

    with st.container():
        st.markdown(
            """<style>.custom-container {border: 2px solid #315d85; padding: 20px; border-radius: 10px; color: #315d85;margin-bottom:10px;}</style>""",
            unsafe_allow_html=True)
        with st.container():
            st.markdown(
                '<div class="custom-container"><p style="text-align:center">- PROJE İÇİN İSTENİLEN ÖZET -</p>'
                '<small>- 25 - 65 yaş aralığı baz alınmıştır.</small><br>'
                '<small>- Aylık net gelir başlangıçta sabit. Daha sonra daire alımı ve kredi borcu ödemesine göre orantılıdır.</small><br>'
                '<small>- Aylık net gelir düzenli olarak her ay ana paraya eklenmektedir.</small><br>'
                '<small>- Daire satın alımı gerçekleşti ise buna orantılı olarak mevcut daire artış göstermektedir.</small><br>'
                '<small>- Daire satın alımına duyarlı olarak peşinat ödenerek kalan borç toplam kredi borcuna dahil edilmiştir.</small><br>'
                '<small>- Daire satın alımına duyarlı olarak aktif kredi adeti artmakta ve biten kredi borçları silinmektedir.</small><br>'
                '<small>- Son kullanıcının da farklı senaryolar üretebilmesi hedeflenerek kodlanmıştır.</small></div>',
                unsafe_allow_html=True)


# Ana Fonksiyon
def main():
    belirtilenYas, toplamAy, anaPara, aylikGelir, kiraGelir, evFiyat, pesinatYuzde, pesinat, krediSure, krediAy, krediOdeme = kullanici_veriler()
    baslik(anaPara, aylikGelir, evFiyat, kiraGelir, krediSure, krediAy, pesinatYuzde, krediOdeme, belirtilenYas,
           pesinat)  # Başlık fonksiyonu burada çağrılır
    dateList, aylikNetGelirList, anaParaList, mevcutEvList, krediBorcList, krediAdetList = finansal_hesaplama(
        belirtilenYas, toplamAy, anaPara, aylikGelir, kiraGelir, evFiyat, pesinatYuzde, pesinat, krediSure, krediAy,
        krediOdeme)
    df = create_tablo(dateList, aylikNetGelirList, anaParaList, mevcutEvList, krediBorcList, krediAdetList)

    # Hesaplama butonuna basıldığında aşağıdaki gibi toplam verileri hesapla ve göster
    if st.button("Hesaplamak İçin Tıklayınız"):
        # Toplam veriler
        toplamDaireSayisi = mevcutEvList[-1]
        toplamKiraGeliri = toplamDaireSayisi * kiraGelir
        toplamKrediBorcu = krediBorcList[-1]
        toplamKrediAdeti = krediAdetList[-1]

        # Sonuçları göster
        sonuc_gosterim(df, belirtilenYas, toplamDaireSayisi, kiraGelir, toplamKrediBorcu, toplamKrediAdeti)


if __name__ == "__main__":
    main()


btn = st.button(":green[Kaynak Kodlar]")
if btn:
    kod = '''
    import streamlit as st
import pandas as pd
import datetime


def baslik(anaPara, aylikGelir, evFiyat, kiraGelir, krediSure, krediAy, pesinatYuzde, krediOdeme, belirtilenYas, pesinat):
    # Başlık ve açıklamaları gösteren fonksiyon.
    st.markdown('<h1 style="color:#274866;">Konut Yatırım Projesi</h1>', unsafe_allow_html=True)
    with st.container():
        with st.container(border=True):
            st.write(":blue[Form'da Doldurduğunuz Bilgiler:]")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"Birikiminiz: :blue[{anaPara} ₺]")
            with col2:
                st.caption(f"Aylık Geliriniz: :blue[{aylikGelir} ₺]")
            with col3:
                st.caption(f"Daire Fiyatı: :blue[{evFiyat} ₺]")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"Kira Gelir Beklentisi: :blue[{kiraGelir} ₺]")
            with col2:
                st.caption(f"Kredi Süresi: :blue[{krediSure} yıl - ({krediAy}) ay]")
            with col3:
                st.caption(f"Belirtmiş Olduğunuz Yaş: :blue[{belirtilenYas[0]}-{belirtilenYas[1]} yaş]")
            st.caption(f"Ödenecek Peşinat: Seçmiş olduğunuz Peşinat :blue[%{pesinatYuzde}]'dir. "
                       f"Buna göre, :blue[{format(int(evFiyat), ',')} ₺] değerindeki bir dairenin :blue[{format(int(pesinat), ',')}] ₺ peşinatını ödediğinizi varsayarsak, "
                       f" Aylık kredi :blue[{round(krediOdeme)} ₺] ödemeniz çıkmaktadır.")

    st.caption(
        ':blue[NOT: Butonuna tıkladığınız an da yukarıda belirtmiş olduğunuz değerler çerçevesinde hesaplama yapılacaktır!]')


def kullanici_veriler():
    # Kullanıcıdan gerekli verileri alıp ve döndüren fonksiyon.
    with st.sidebar:
        st.caption(
            "Form'da belirtecek olduğunuz değerler arasında Daire alma ve Borç süreçlerinizi inceleyebilirsiniz.")
        belirtilenYas = st.slider("Yaş Aralığını Belirtiniz:", 0, 120, (25, 65))
        st.caption(f":blue[Belirtmiş olduğunuz yaş ' {belirtilenYas[0]}-{belirtilenYas[1]} ' yaş aralığıdır.]")
        toplamAy = int((belirtilenYas[1] - belirtilenYas[0]) * 12)
        mevcutAy = 1

        anaPara = st.number_input("Mevcut Ana Para (₺):", value=0, step=100000)
        aylikGelir = st.number_input("Aylık Geliriniz (₺):", value=3000, step=1000)
        kiraGelir = st.number_input("Daireniz için Kira Geliri (₺):", value=8000, step=1000)
        evFiyat = st.number_input("Daire Fiyatını Belirtiniz (₺):", value=1250000, step=50000)
        pesinatYuzde = st.slider("Peşinat Yüzdesini Belirtiniz (%):", 0, 100, 20)
        pesinat = evFiyat * pesinatYuzde / 100
        krediSure = st.number_input("Kredi süresini seçiniz (Yıl):", value=15)
        krediAy = krediSure * 12
        krediOdeme = (evFiyat - pesinat) / krediAy

        return belirtilenYas, toplamAy, anaPara, aylikGelir, kiraGelir, evFiyat, pesinatYuzde, pesinat, krediSure, krediAy, krediOdeme


def finansal_hesaplama(belirtilenYas, toplamAy, anaPara, aylikGelir, kiraGelir, evFiyat, pesinatYuzde, pesinat,
                         krediSure, krediAy, krediOdeme):
    # Başlangıç değerleri
    mevcutEv = 0
    toplamKrediBorcu = 0
    aylikNetGelirList = []
    krediBorcList = []
    anaParaList = []
    krediAdetList = []
    mevcutEvList = []
    dateList = []
    aylikKrediList = []

    for i in range(1, toplamAy + 1):
        krediAdet = len([j for j in aylikKrediList if j > 0])
        anaPara -= krediAdet * krediOdeme
        anaPara += aylikGelir
        toplamKrediBorcu -= krediAdet * krediOdeme
        aylikNetGelir = aylikGelir - (krediAdet * krediOdeme)

        # Kredi listelerini güncelle
        krediBorcSure = [kredi - 1 for kredi in aylikKrediList]
        aylikKrediList = krediBorcSure

        # Daire alımı
        while anaPara >= pesinat:
            anaPara -= pesinat
            mevcutEv += 1
            aylikKrediList.append(krediAy)
            aylikGelir += kiraGelir
            toplamKrediBorcu += (evFiyat - pesinat)

        # Tarih ve yaş hesaplama
        aktifKredi = sum(1 for k in aylikKrediList if k > 0)
        baslangicTarihi = datetime.datetime.now()
        yilBelirle = i // 12
        ayBelirle = i % 12
        if ayBelirle == 0:
            ayBelirle = 12
            yilBelirle -= 1
        guncelTarih = baslangicTarihi.replace(year=baslangicTarihi.year + yilBelirle, month=ayBelirle)
        tarihStr = guncelTarih.strftime("%d/%m/%Y")
        mevcutYas = belirtilenYas[0] + yilBelirle
        dateList.append(f"{mevcutYas} - {tarihStr}")
        aylikNetGelirList.append(aylikNetGelir)
        anaParaList.append(anaPara)
        krediBorcList.append(toplamKrediBorcu)
        krediAdetList.append(aktifKredi)
        mevcutEvList.append(mevcutEv)

    return dateList, aylikNetGelirList, anaParaList, mevcutEvList, krediBorcList, krediAdetList



def create_tablo(dateList, aylikNetGelirList, anaParaList, mevcutEvList, krediBorcList, krediAdetList):
    # Hesaplanan verilerle bir pandas DataFrame oluşturan fonksiyon.
    veriler = {
        "Yaş / Tarih": dateList,
        "Aylık Net gelir": aylikNetGelirList,
        "Ana Para": anaParaList,
        "Mevcut Daire": mevcutEvList,
        "Toplam Kredi Borç": krediBorcList,
        "Aktif Kredi Adet": krediAdetList,
    }
    df = pd.DataFrame(veriler)
    df = df.sort_values("Yaş / Tarih")
    return df


def sonuc_gosterim(df, belirtilenYas, mevcutEv, kiraGelir, toplamKrediBorcu, krediAdet):
    # Sonuçları gösteren fonksiyon.
    with st.container():
        st.caption(f":blue[Belirtmiş olduğunuz bilgiler dahilinde {belirtilenYas[0]} - {belirtilenYas[1]} Yaş aralığı Yatırım Durumu]")
        with st.expander('Tablo Özet Bilgiler İçin Tıklayınız.'):
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"Toplam Daire Sayısı: :blue[{mevcutEv}]")
                st.caption(f"Toplam Kira Geliri: :blue[{mevcutEv * kiraGelir} ₺]")
            with col2:
                st.caption(f"Toplam Kredi Borcu: :blue[{toplamKrediBorcu} ₺]")
                st.caption(f"Toplam Kalan Kredi Adeti: :blue[{krediAdet}]")

        st.dataframe(df)

    with st.container():
        st.markdown(
            """<style>.custom-container {border: 2px solid #315d85; padding: 20px; border-radius: 10px; color: #315d85;margin-bottom:10px;}</style>""",
            unsafe_allow_html=True)
        with st.container():
            st.markdown(
                '<div class="custom-container"><p style="text-align:center">- PROJE İÇİN İSTENİLEN ÖZET -</p>'
                '<small>- 25 - 65 yaş aralığı baz alınmıştır.</small><br>'
                '<small>- Aylık net gelir başlangıçta sabit. Daha sonra daire alımı ve kredi borcu ödemesine göre orantılıdır.</small><br>'
                '<small>- Aylık net gelir düzenli olarak her ay ana paraya eklenmektedir.</small><br>'
                '<small>- Daire satın alımı gerçekleşti ise buna orantılı olarak mevcut daire artış göstermektedir.</small><br>'
                '<small>- Daire satın alımına duyarlı olarak peşinat ödenerek kalan borç toplam kredi borcuna dahil edilmiştir.</small><br>'
                '<small>- Daire satın alımına duyarlı olarak aktif kredi adeti artmakta ve biten kredi borçları silinmektedir.</small><br>'
                '<small>- Son kullanıcının da farklı senaryolar üretebilmesi hedeflenerek kodlanmıştır.</small></div>',
                unsafe_allow_html=True)


# Ana Fonksiyon
def main():
    belirtilenYas, toplamAy, anaPara, aylikGelir, kiraGelir, evFiyat, pesinatYuzde, pesinat, krediSure, krediAy, krediOdeme = kullanici_veriler()
    baslik(anaPara, aylikGelir, evFiyat, kiraGelir, krediSure, krediAy, pesinatYuzde, krediOdeme, belirtilenYas,
           pesinat)  # Başlık fonksiyonu burada çağrılır
    dateList, aylikNetGelirList, anaParaList, mevcutEvList, krediBorcList, krediAdetList = finansal_hesaplama(
        belirtilenYas, toplamAy, anaPara, aylikGelir, kiraGelir, evFiyat, pesinatYuzde, pesinat, krediSure, krediAy,
        krediOdeme)
    df = create_tablo(dateList, aylikNetGelirList, anaParaList, mevcutEvList, krediBorcList, krediAdetList)

    # Hesaplama butonuna basıldığında aşağıdaki gibi toplam verileri hesapla ve göster
    if st.button("Hesaplamak İçin Tıklayınız"):
        # Toplam veriler
        toplamDaireSayisi = mevcutEvList[-1]  # Son eleman
        toplamKiraGeliri = toplamDaireSayisi * kiraGelir
        toplamKrediBorcu = krediBorcList[-1]  # Son eleman
        toplamKrediAdeti = krediAdetList[-1]  # Son eleman

        # Sonuçları göster
        sonuc_gosterim(df, belirtilenYas, toplamDaireSayisi, kiraGelir, toplamKrediBorcu, toplamKrediAdeti)


if __name__ == "__main__":
    main()
    '''
    st.markdown(
        '<h2 style="color: #315d85; font-weight:bold;">Kaynak Kodlar</h2>',
        unsafe_allow_html=True)
    st.code(kod, language='python')
