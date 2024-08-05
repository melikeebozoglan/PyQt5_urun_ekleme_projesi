import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *  #başına QtWidgets yazmaya gerek kalmaz
from urun_ekle import *

app = QApplication(sys.argv) #uygulama içerisinde tüm argümanları çağır
window = QMainWindow()
ui = Ui_MainWindow() #ui dosyasındaki class adı
ui.setupUi(window) #tanımlamış olduğumuz windowu form ile ilişkilendirir
window.show() 

# veri tabanı işlemleri
import sqlite3
connect = sqlite3.connect("urunler.db")
process = connect.cursor() #databasedeki işlemleri gerçekleştirmek için imleç oluşturur
connect.commit() #yapılan değişiklikleri kaydeder

table = process.execute("create table if not exists urun (urunKodu int, urunAdi text, birimFiyat int, stokMiktari int, urunAciklamasi text, marka text, kategori text)") #veritabanına işler
connect.commit()

def add_data():
    urunKodu = int(ui.lE_kod.text())
    urunAdi = ui.lE_ad.text()
    birimFiyat = int(ui.lE_fiyat.text())
    stokMiktari = int(ui.lE_miktar.text())
    urunAciklamasi = ui.pte.toPlainText()
    marka = ui.cB_marka.currentText()
    kategori = ui.cb_kate.currentText()

    try:
        add = "insert into urun (urunKodu, urunAdi, birimFiyat, stokMiktari, urunAciklamasi, marka, kategori) values (?,?,?,?,?,?,?)"
        process.execute(add, (urunKodu, urunAdi, birimFiyat, stokMiktari, urunAciklamasi, marka, kategori))
        connect.commit()
        ui.statusbar.showMessage("Kayıt ekleme işlemi başarılı.", 10000)
        record_list()
    except Exception as error:
        ui.statusbar.showMessage("Kayıt eklenemedi === " + str(error))

def record_list():
    ui.t_listele.clear() 
    ui.t_listele.setHorizontalHeaderLabels(("Ürün Kodu", "Ürün Adı", "Birim Fiyat", "Stok Miktarı", "Ürün Açıklaması", "Marka", "Kategori"))

    ui.t_listele.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #scroll barı kaldırdı
    
    query = "select * from urun"
    process.execute(query)

    for indexSatir, kayitNumarasi in enumerate(process):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.t_listele.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))

record_list()

def list_by_cate():
    list_by_cate = ui.cB_kate_list.currentText()

    query = "select * from urun where kategori = ?"
    process.execute(query, (list_by_cate,))
    ui.t_listele.clear() 

    for indexSatir, kayitNumarasi in enumerate(process):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.t_listele.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))

def remove_data():
    remove_message = QMessageBox.question(window, "Silme Onayı", "Silmek istediğinizden emin misiniz?", QMessageBox.Yes | QMessageBox.No)

    if remove_message == QMessageBox.Yes:
        selected_record = ui.t_listele.selectedItems()
        removed_record = selected_record[0].text()

        query = "delete from urun where urunKodu = ?"
        try:
            process.execute(query, (removed_record,))
            connect.commit()
            ui.statusbar.showMessage("silme işlemi başarılı.", 10000)
            record_list()

        except Exception as error:
            ui.statusbar.showMessage("Kayıt silinemedi === " + str(error))

    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi.")

def update_data():
    update_mesagge = QMessageBox.question(window, "Güncelleme Onayı", "Güncellemek istediğinizden emin misiniz?", QMessageBox.Yes | QMessageBox.No)

    if update_mesagge == QMessageBox.Yes:
        try:
            urunKodu = ui.lE_kod.text()
            urunAdi = ui.lE_ad.text()
            birimFiyat = ui.lE_fiyat.text()
            stokMiktari = ui.lE_miktar.text()
            urunAciklamasi = ui.pte.toPlainText()
            marka = ui.cB_marka.currentText()
            kategori = ui.cb_kate.currentText()

            if birimFiyat == "" and stokMiktari == "" and urunAciklamasi == "" and marka == "" and kategori == "":
                process.execute("update urun set urunAdi = ? where urunKodu = ?", (urunAdi, urunKodu))

            elif urunAdi == "" and stokMiktari == "" and urunAciklamasi == "" and marka == "" and kategori == "":
                process.execute("update urun set birimFiyat = ? where urunKodu = ?", (birimFiyat, urunKodu))

            elif urunAdi == "" and birimFiyat == "" and urunAciklamasi == "" and marka == "" and kategori == "":
                process.execute("update urun set stokMiktari = ? where urunKodu = ?", (stokMiktari, urunKodu))

            elif urunAdi == "" and birimFiyat == "" and stokMiktari == "" and marka == "" and kategori == "":
                process.execute("update urun set urunAciklamasi = ? where urunKodu = ?", (urunAciklamasi, urunKodu))
            
            elif urunAdi == "" and birimFiyat == "" and stokMiktari == "" and urunAciklamasi == "" and kategori == "":
                process.execute("update urun set marka = ? where urunKodu = ?", (marka, urunKodu))

            elif urunAdi == "" and birimFiyat == "" and stokMiktari == "" and urunAciklamasi == "" and marka == "":
                process.execute("update urun set kategori = ? where urunKodu = ?", (kategori, urunKodu))

            else:
                process.execute("update urun set urunAdi = ?, birimFiyat = ?, stokMiktari = ?, urunAciklamasi = ?, marka = ?, kategori = ? where urunKodu = ?", (urunAdi, birimFiyat, stokMiktari, urunAciklamasi, marka, kategori, urunKodu))
            #bunları çoğalt

            connect.commit()
            ui.statusbar.showMessage("Güncelleme işlemi başarılı.", 10000)
            record_list()

        except Exception as error:
            ui.statusbar.showMessage("Kayıt güncellenemedi === " + str(error))

    else:
        ui.statusbar.showMessage("Güncelleme işlemi iptal edildi.")

# butonlar
ui.btn_ekle.clicked.connect(add_data)   
ui.btn_listeleme.clicked.connect(record_list)
ui.btn_kate_list.clicked.connect(list_by_cate)
ui.btn_sil.clicked.connect(remove_data)
ui.btn_guncelle.clicked.connect(update_data)


sys.exit(app.exec_())