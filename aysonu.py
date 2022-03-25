import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import messagebox
import csv


import sqlite3

def newwindow():
	# Veritabanı Bağlantısı
	bagla = sqlite3.connect("satis.db")
	sor = bagla.cursor()
	def kayıt_başarılı(text):
		mesaj = messagebox.showinfo(text, "Dosya Başarıyla Yazdırıldı..")

	def emin_misin(text):
		mesaj = messagebox.showinfo(text, "Veritabanı Temizlendi...")


	def toplama():

		sayi = 0
		for kontrol in sor.execute("SELECT SUM(kar) FROM aysonu"):
			if kontrol[0]:
				goster.insert('end', kontrol)
		bagla.commit()
		sayi+1
	def rapor():
		pen.geometry("1000x500")
		# veri tabanı bağlantısı
		con = sqlite3.connect("satis.db")

		# cursor ile sorgu yaparız
		cur = con.cursor()

		# 1. başlıklar
		kod = 0
		cur.execute("PRAGMA table_info(aysonu)")
		basliklar = [baslik_adi for _, baslik_adi, *_ in cur.fetchall()]

		# 2. veriler
		cur.execute("select * from aysonu")
		veriler = cur.fetchall()

		# 3. CSV dosyası
		with open("aysonu.csv", mode="a", newline="") as fh:
			# dosyaya bir CSV yazarı bağlıyoruz
			yazar = csv.writer(fh)

			# 1 tek satır ("row" ile bitiyor) yazıyoruz evvela, o da `basliklar`
			yazar.writerow(basliklar)

			# Bir sürü satır ("rows" ile bitiyor) yazıyoruz sonra, asıl veriler
			yazar.writerows(veriler)
		if kod == 0:
			kayıt_başarılı("Yazdırıldı!")

		def treesorgu():
			sayi = 0
			for degisken in cur.execute("SELECT tarih, kar FROM aysonu"):
				if degisken[0]:
					tree.insert("", tkinter.END, values=degisken)


			sayi + 1
			con.commit()



			# DB TEMİZLEME
			msg2 = messagebox.askyesno("EMİN MİSİN?",
									   "Bu İşlemi Onaylarsanız Gün İçinde Girilen Verilerin Tümü Yedeklendikten Sonra Silinecek  Onaylıyor Musunuz?")
			if msg2 == True:
				bagla = sqlite3.connect("satis.db")
				curs = bagla.cursor()
				curs.execute("DELETE FROM aysonu")
				bagla.commit()
				curs.close()
				emin_misin("Veritabanı Temizlendi...")


		treesorgu()

	# Pencere İşlemleri
	pen = tkinter.Tk()
	pen.geometry("500x400")
	pen.configure(bg="#696969")
	pen.maxsize(1000,500)
	pen.title("Has Çınar Nalbur Ay Sonu Ekranı")

	yazi = tkinter.Label(pen, text="Ay Sonu Raporu", bg="#696969", foreground="white")
	yazi.configure(font="EthnocentricRg-Italic 17")
	yazi.place(x=90, y=3)

	cizgi = tkinter.Label(pen, text="---------------------------------------------------------------------------------------------",  bg="#696969", fg="white", bd=3)
	cizgi.place(x=10, y=30)

	goster = tkinter.Entry(pen, font="Arial 20", width=10, bg="#f4e509", bd=3)
	goster.place(x=178, y=100)

	yazi2 = tkinter.Label(pen, text="Bu Ayın Toplam Kârı", bg="#696969", foreground="white")
	yazi2.configure(font="Impact 13")
	yazi2.place(x=180, y=70)

	tl = tkinter.Label(pen, text="TL", font="Evogria 13", bg="#696969", fg="white", bd=3)
	tl.place(x=335, y=110)

	topla = tkinter.Button(pen, text="Ay Sonu Al", height=1,width=12 ,bg="#e6e6fa",bd=3,command=toplama)
	topla.configure(font="Arial 10")
	topla.place(x=203, y=150)

	detay = tkinter.Button(pen, text="Detay Yazdır", height=1,width=10 ,bd=3 ,bg="#e6e6fa",command=rapor)
	detay.configure(font="Arial 9")
	detay.place(x=215, y=190)


# TREE ALANI

	style = ttk.Style(pen)
	style.theme_use("alt")
	style.configure("Treeview", background="#e8e8e8", fieldbackground="#696969", font=("Arial", 12), foreground="black",
					wheight=30)
	style.map("Treeview", background=[("selected", "#009df2")])
	tree = ttk.Treeview(pen, columns=("A", "B"), show='headings', height=23)

	tree.heading("A", text="TARİH")
	tree.heading("B", text="KÂR TL")

	tree.column("A", width=150)
	tree.column("B", width=150, anchor=CENTER)

	tree.place(x=605, y=10)

	scrlabel = tkinter.Label(pen, width=10, height=31, bg="#696969")
	scrlabel.place(x=910, y=13)

	vsb = Scrollbar(scrlabel, orient="vertical", command=tree.yview)
	vsb.place(relx=0.100, rely=0.02, relheight=0.980, relwidth=0.300)

	tree.configure(yscrollcommand=vsb.set)


	pen.mainloop()




newwindow()

####################################################################
# Bu program Furkan Yorulmaz tarafınan OpenSource olarak           #
# kodlanmıştır. Dilediğiniz gibi kullanıp düzenleyebilirsiniz.     #
# Program hakkında sorularınız için:                               #
#   İnstagram: furkanroot                                          #
#   Mail: furkanyorulmaz_@hotmail.com                              #
####################################################################


