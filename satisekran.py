import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import csv
from datetime import datetime
import sqlite3

# Veritabanı Bağlantısı
veritabani = sqlite3.connect("satis.db")
im = veritabani.cursor()
im.execute("CREATE TABLE IF NOT EXISTS nalbur(urun TEXT, alis INT, satis INT,adet INT, tarih TEXT)")

# UYARILAR
def kayıt_başarılı(text):
    mesaj = messagebox.showinfo(text, "Dosya Başarıyla Yazdırıldı..")

def kayıt_sil(text):
    mesaj = messagebox.showinfo(text, "Kayıt Silindi...")

def emin_misin(text):
    mesaj = messagebox.showinfo(text, "Veritabanı Temizlendi...")

# Yenile Tuşu Fonksiyonu
def yeniden():
    python = sys.executable
    os.execl(python,python, * sys.argv)

# DB Kayıt ve Listeleme
def kayit():
    urunad = urun.get()
    urunalis = alis.get()
    urunadet = adet.get()
    urunsatis = satis.get()
    time = datetime.now().strftime("%d.%m.%Y | %H:%M")

    def Ürünler():
        im.execute("insert into nalbur values(?,?,?,?,?)", [urunad, urunalis, urunsatis,urunadet,time])
        veritabani.commit()

    kod = 0
    im.execute("""SELECT urun FROM nalbur""")
    kontrol = im.fetchall()
    for i in kontrol:  # KONTROL PANELİ ÜRÜNÜN OLUP OLMADIĞINI KONTROL EDER
        ad_kontrol = i[0]

    if kod == 0:
        Ürünler()

        urun.delete(0, "end")
        alis.delete(0, "end")
        satis.delete(0,'end')
        adet.delete(0,'end')

        for item in tree.get_children():
            tree.delete(item)

        for degisken in im.execute("""SELECT urun, alis, satis, adet  FROM nalbur"""):
            if degisken[0]:
                tree.insert("", tkinter.END, values=degisken)

# Alış Satış ve Kar Kısımlarının fonksiyonu
def toplami_yazdir():
    satir_verileri = [tree.item(item_id)["values"]
                      for item_id in tree.get_children()]
    ilgili_sutunun_indeksi = sutunlar.index("alis")
    ilgili_sutunun_verileri = [satir[ilgili_sutunun_indeksi]
                               for satir in satir_verileri]
    toplam = sum(ilgili_sutunun_verileri)
    tp.insert('end', toplam)

    ilgili_sutunun_indeksi2 = sutunlar.index("satis")
    ilgili_sutunun_verileri2 = [satir[ilgili_sutunun_indeksi2]
                                for satir in satir_verileri]
    toplam = sum(ilgili_sutunun_verileri2)
    tp4.insert('end', toplam)
    # Kar Hesaplayıcı
    sayi = 0
    for degisken3 in im.execute("SELECT SUM(satis-alis) FROM nalbur"):
        if degisken3[0]:
            tp3.insert('end', degisken3)
    gunlukkar = tp3.get()
    tarih = datetime.now().strftime("| %d.%m.%Y | %H:%M")
    im.execute("CREATE TABLE IF NOT EXISTS aysonu(kar INT,tarih TEXT)")
    im.execute("insert into aysonu values(?,?)", [gunlukkar,tarih])

    veritabani.commit()
    sayi+1

def yazdir():

    con = sqlite3.connect("satis.db")
    cur = con.cursor()

    # 1. başlıklar
    kod = 0
    cur.execute("PRAGMA table_info(nalbur)")
    basliklar = [baslik_adi for _,baslik_adi, *_ in cur.fetchall()]

    # 2. veriler
    cur.execute("select * from nalbur")
    veriler = cur.fetchall()

    # 3. CSV dosyası işlemleri
    with open("gunsonu.csv", mode="a", newline="") as fh:
        # dosyaya bir CSV yazarı bağlıyoruz
        yazar = csv.writer(fh)

        # 1 tek satır ("row" ile bitiyor) yazıyoruz o da `basliklar`
        yazar.writerow(basliklar)
        # Bir sürü satır ("rows" ile bitiyor) yazıyoruz sonra, asıl veriler
        yazar.writerows(veriler)
    if kod == 0:
        kayıt_başarılı("Yazdırıldı!")

        #DB TEMİZLEME
    msg2 = messagebox.askyesno("EMİN MİSİN?", "Bu İşlemi Onaylarsanız Gün İçinde Girilen Verilerin Tümü Yedeklendikten Sonra Silinecek  Onaylıyor Musunuz?")
    if msg2 == True:
        bagla = sqlite3.connect("satis.db")
        curs = bagla.cursor()
        curs.execute("""DELETE FROM nalbur""")
        bagla.commit()
        curs.close()
        emin_misin("Veritabanı Temizlendi...")
    # Yeniden Başlatır
    python = sys.executable
    os.execl(python,python, * sys.argv)

def Ürün_Silme():
    A = urun.get()
    # STOKTAN KAYIT SILME
    im.execute("""SELECT urun FROM nalbur""")
    kontrol_ara = im.fetchall()
    for i in kontrol_ara:
        silmek = i[0]
    msg = messagebox.askyesno("SİLME İŞLEMİ", "EMİN MİSİN?")
    if msg == True:
        im.execute("delete from nalbur where urun= ? ", [A])
        im.execute("delete from nalbur where alis= ? ", [silmek])
        veritabani.commit()
        urun.delete(0, "end")
        alis.delete(0, "end")
        kayıt_sil("SİLME İŞLEMİ YAPILDI...")
        for i in tree.get_children():
            tree.delete(i)
    python = sys.executable
    os.execl(python,python, * sys.argv)

def aysonu_ekrani():
    from aysonu import newwindow

# Pencere Oluşturma
pencere = Tk()
pencere.geometry("1300x680")
pencere.maxsize(1300,680)
pencere.configure(bg="#696969")
pencere.title("Satış Otomasyon Sistemi")

# Ürün Satış
satisyazi = tkinter.Label(pencere, text="Ürün Sat", font="EthnocentricRg-Italic 17", bg="#696969", fg="white")
satisyazi.place(x=180, y=10)

yazi = tkinter.Label(pencere,text="Ürün Adı", font="Evogria 13", bg="#696969", fg="white")
yazi.place(x=5, y=80)

urun = tkinter.Entry(pencere, font="Arial 13", width=20, bd=3,bg="#f4e509")
urun.place(x=110, y=83)

# Alış Fiyatı
yazi1 = tkinter.Label(pencere,text="Alış Fiyatı", font="Evogria 13", bg="#696969", fg="white")
yazi1.place(x=5,y=130)
alis = tkinter.Entry(pencere, font="Arial 13", width=5, bd=3,bg="#f4e509")
alis.place(x=110, y=133)

tl = tkinter.Label(pencere,text="tl", font="Evogria 10", bg="#696969", fg="white")
tl.place(x=165,y=138)

# Satış Fiyatı
yazi2 = tkinter.Label(pencere,text="Satış Fiyatı", font="Evogria 13", bg="#696969", fg="white")
yazi2.place(x=5,y=183)
satis = tkinter.Entry(pencere, font="Arial 13" ,width=5 ,bd=3,bg="#f4e509")
satis.place(x=110, y=183)
tl = tkinter.Label(pencere,text="tl", font="Evogria 10", bg="#696969", fg="white")
tl.place(x=165,y=188)

# Adet
yazi4 = tkinter.Label(pencere,text="Adet", font="Evogria 13", bg="#696969", fg="white")
yazi4.place(x=5, y=230)
adet = tkinter.Entry(pencere, font="Arial 13", width=5, bd=3, bg="#f4e509")
adet.place(x=110, y=230)

buton = tkinter.Button(pencere, width=7, height=1,bg="#dcdcdc" ,text="SAT",bd=3 ,command=kayit)
buton.place(x=180, y=230)

silsene = tkinter.Button(pencere, width=7, height=1,bg="#dcdcdc", bd=3, text="Kayıt Sil", command=Ürün_Silme)
silsene.place(x=400, y=150)

restart = tkinter.Button(pencere, width=7, height=1,bg="#dcdcdc", bd=3, text="Yenile", command=yeniden)
restart.place(x=400, y=200)

# tree için örnek tablo
sutunlar = ("ürün", "alis","satis","adet")
veriler = [(f"ürün_{n}", n * 3) for n in range(1, 6)]
# tree style
style = ttk.Style(pencere)
style.theme_use("alt")
style.configure("Treeview", background="#e8e8e8",fieldbackground="#696969", font=("Arial", 12),foreground="black", wheight=30)
style.map("Treeview", background=[("selected", "#009df2")])
# tree'nin kendisi & verilerin eklenmesi
tree = ttk.Treeview(pencere, columns=sutunlar, height=31,show="headings")
tree.heading("adet", text="ADET")
tree.heading("ürün", text="ÜRÜN")
tree.heading("alis", text="ALIŞ FİYATI")
tree.heading("satis", text="SATIŞ FİYATI")

#tree kolonları
tree.column("adet", width=100, anchor=CENTER)
tree.column("ürün", width=200, anchor=CENTER)
tree.column("alis", width=200, anchor=CENTER)
tree.column("satis", width=200, anchor=CENTER)

tree.place(x=550, y=10)

for degisken2 in im.execute("""SELECT urun, alis, satis, adet  FROM nalbur"""):
    if degisken2[0]:
        tree.insert("", tkinter.END, values=degisken2)

vsb = Scrollbar(pencere, orient="vertical", command=tree.yview)
vsb.place(relx=0.965, rely=0.02, relheight=0.950, relwidth=0.010)

tree.configure(yscrollcommand=vsb.set)

# GÜN SONU EKRANI

    # Alış Fiyatı Toplamı
gunsonuyazi = tkinter.Label(pencere, text="Gün Sonu Al", font="EthnocentricRg-Italic 17", bg="#696969", fg="white")
gunsonuyazi.place(x=150, y=300)

alfiyat = tkinter.Label(pencere,text="Alış Fiyatı Toplamı", font="Evogria 12", bg="#696969", fg="white" )
alfiyat.place(x=5, y=380)
tp = tkinter.Listbox(pencere, width=10, height=1, bd=3 ,bg="#f4e509")
tp.configure(font="Arial 15")
tp.place(x=10, y=410)
    # Küsürat Toplamı
tl = tkinter.Label(pencere,text="TL", font="Evogria 11", bg="#696969", fg="white", bd=3)
tl.place(x=128, y=418)



    # Satış Fiyatı Toplamı

satfiyat = tkinter.Label(pencere,text="Satış Fiyatı Toplamı", font="Evogria 12", bg="#696969", fg="white")
satfiyat.place(x=5,y=470)
tp4 = tkinter.Listbox(pencere, width=10, height=1,bd=3 ,bg="#f4e509")
tp4.configure(font="Arial 15")
tp4.place(x=10, y=500)
tl2 = tkinter.Label(pencere,text="TL", font="Evogria 11", bg="#696969", fg="white", bd=3)
tl2.place(x=128, y=508)


    # Kar Toplamı
kar = tkinter.Label(pencere,text="Günlük Kâr", font="Evogria 12", bg="#696969", fg="white")
kar.place(x=5, y=560)

tp3 = tkinter.Entry(pencere, width=10,bd=3 ,bg="#f4e509")
tp3.configure(font="Arial 15")
tp3.place(x=10, y=590)

tl3 = tkinter.Label(pencere,text="TL", font="Evogria 11", bg="#696969", fg="white", bd=3)
tl3.place(x=128, y=598)
    # Butonlar

exbuton = tkinter.Button(pencere, width=11, height=1,bg="#dcdcdc", bd=3, text="Yazdır" , command=yazdir)
exbuton.place(x=400, y=450)

aysonual = tkinter.Button(pencere, width=11, height=1, bg="#dcdcdc", bd=3, text="Ay Sonu Al", command=aysonu_ekrani)
aysonual.place(x=400, y=500)

cikis = tkinter.Button(pencere, width=11, height=1,bg="#dcdcdc", bd=3, text="Çıkış", command=pencere.quit)
cikis.place(x=400, y=550)

top = tkinter.Button(pencere, width=11, height=1,bg="#dcdcdc" ,bd=3, text="GÜN SONU AL" , command=toplami_yazdir)
top.place(x=160, y=598)

pencere.mainloop()

    ####################################################################
    # Bu program Furkan Yorulmaz tarafınan OpenSource olarak           #
    # kodlanmıştır. Dilediğiniz gibi kullanıp düzenleyebilirsiniz.     #
    # Program hakkında sorularınız için:                               #
    #   İnstagram: furkanroot                                          #
    #   Mail: furkanyorulmaz_@hotmail.com                              #
    ####################################################################

