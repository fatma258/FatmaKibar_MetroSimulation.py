#sürücüsüz metro istasyonu projesi
import heapq  
import collections  

class MetroAgi:  
    """Metro ağı grafını oluşturan sınıf."""  
    def __init__(self):  
        self.istasyonlar = {}  # İstasyonları ve bağlantıları saklayan sözlük  
        self.hatlar = {}  # Hangi hatlar üzerinden gidildiğini takip etmek için  

    def istasyon_ekle(self, istasyon):  
        """Yeni bir istasyon ekler."""  
        if istasyon not in self.istasyonlar:  
            self.istasyonlar[istasyon] = {}  

    def baglanti_ekle(self, istasyon1, istasyon2, sure, hat_adi=None):  
        """İki istasyon arasında bağlantı ekler ve süreyi belirler."""  
        self.istasyon_ekle(istasyon1)  # Eğer istasyon1 yoksa ekle  
        self.istasyon_ekle(istasyon2)  # Eğer istasyon2 yoksa ekle  
        self.istasyonlar[istasyon1][istasyon2] = sure  # İstasyon1 -> İstasyon2 arasında bağlantı  
        self.istasyonlar[istasyon2][istasyon1] = sure  # İstasyon2 -> İstasyon1 arasında bağlantı (çift yönlü)  
        
        if hat_adi:  
            if hat_adi not in self.hatlar:  
                self.hatlar[hat_adi] = []  
            self.hatlar[hat_adi].append((istasyon1, istasyon2, sure))  # Hattı takip et  

    def en_az_aktarma_bul(self, baslangic, hedef):  
        """BFS algoritması ile en az aktarmalı rotayı bulur."""  
        if baslangic not in self.istasyonlar or hedef not in self.istasyonlar:  
            raise ValueError(f"Hata: '{baslangic}' veya '{hedef}' istasyonu bulunamadı.")  

        # BFS için kuyruk (başlangıç istasyonu ve izlenen yol bilgisi ile)  
        queue = collections.deque([(baslangic, [baslangic], None)])  # (istasyon, yol, mevcut hattı)  
        ziyaret_edilenler = set()  # Ziyaret edilen istasyonları takip etmek için  

        while queue:  
            mevcut, yol, mevcut_hatt = queue.popleft()  # Kuyruğun başındaki öğeyi al  
            
            if mevcut == hedef:  
                return yol  # Hedefe ulaşıldığında yolu döndür  
            
            if mevcut not in ziyaret_edilenler:  # Eğer mevcut istasyon daha önce ziyaret edilmediyse  
                ziyaret_edilenler.add(mevcut)  # Bu istasyonu ziyaret ettik olarak işaretle  
                for komsu in self.istasyonlar[mevcut]:  # Mevcut istasyonun komşularını dolaş  
                    yeni_hatt = None  
                    
                    # Komşuya hangi hat üzerinden gidiliyor onu bul  
                    for hat, baglantilar in self.hatlar.items():  
                        for ist1, ist2, _ in baglantilar:  
                            if (ist1 == mevcut and ist2 == komsu) or (ist2 == mevcut and ist1 == komsu):  
                                yeni_hatt = hat  
                                break  

                    # Eğer mevcut hattı ile farklı bir hattı kullanıyorsak aktarma yapıyoruz  
                    if yeni_hatt != mevcut_hatt:  
                        queue.append((komsu, yol + [komsu], yeni_hatt))  # Komşuyu kuyruğa ekle ve yolun sonuna ekle  
                    else:  
                        queue.append((komsu, yol + [komsu], mevcut_hatt))  # Aynı hattı kullanarak devam et  
        
        return None  # Eğer rota bulunamazsa None döndür  

    def en_hizli_rota_bul(self, baslangic, hedef):  
      
        if baslangic not in self.istasyonlar or hedef not in self.istasyonlar:  
            raise ValueError(f"Hata: '{baslangic}' veya '{hedef}' istasyonu bulunamadı.")  

        # A* algoritması için öncelik kuyruğu, başlangıç istasyonu ve yolu ile birlikte  
        oncelik_kuyrugu = [(0, baslangic, [baslangic])]  # (toplam süre, mevcut istasyon, izlenen yol)  
        ziyaret_edilenler = {}  # Ziyaret edilen istasyonların süre bilgilerini saklamak için sözlük  

        while oncelik_kuyrugu:  
            sure, mevcut, yol = heapq.heappop(oncelik_kuyrugu)  # En düşük süreyi olan istasyonu pop et  

            if mevcut == hedef:  
                return yol  # Hedefe ulaşıldığında yolu döndür  

            # Eğer mevcut istasyon daha önce ziyaret edilmemişse ya da daha hızlı bir yol bulunduysa  
            if mevcut not in ziyaret_edilenler or sure < ziyaret_edilenler[mevcut]:  
                ziyaret_edilenler[mevcut] = sure  # Bu istasyonun ziyaret edildiğini işaretle  

                # Mevcut istasyonun komşuları ile geçiş sürelerini kuyruğa ekle  
                for komsu, gecis_suresi in self.istasyonlar[mevcut].items():  
                    heapq.heappush(oncelik_kuyrugu, (sure + gecis_suresi, komsu, yol + [komsu]))  # Yeni istasyonu kuyruğa ekle  

        return None  # Eğer rota bulunamazsa None döndür  

# 🚇 Metro Ağı Tanımlama  
metro = MetroAgi()  

# ✅ **M7 Hattı**: Mahmutbey -> Karadeniz Mahallesi -> Alibeyköy -> Çağlayan -> Mecidiyeköy  
metro.baglanti_ekle("Mahmutbey", "Karadeniz Mahallesi", 4, "M7")  
metro.baglanti_ekle("Karadeniz Mahallesi", "Alibeyköy", 3, "M7")  
metro.baglanti_ekle("Alibeyköy", "Çağlayan", 1, "M7")  
metro.baglanti_ekle("Çağlayan", "Mecidiyeköy", 1, "M7")  

# ✅ **M2 Hattı**: Yenikapı -> Vezneciler -> Şişhane -> Taksim -> Osmanbey -> Levent -> Hacıosman  
metro.baglanti_ekle("Yenikapı", "Vezneciler", 2, "M2")  
metro.baglanti_ekle("Vezneciler", "Şişhane", 3, "M2")  
metro.baglanti_ekle("Şişhane", "Taksim", 2, "M2")  
metro.baglanti_ekle("Taksim", "Osmanbey", 3, "M2")  
metro.baglanti_ekle("Osmanbey", "Levent", 2, "M2")  
metro.baglanti_ekle("Levent", "Hacıosman", 2, "M2")  

# ✅ **M11 Hattı**: Gayrettepe -> Kağıthane -> Kargo Terminali -> İstanbul Havalimanı  
metro.baglanti_ekle("Gayrettepe", "Kağıthane", 2, "M11")  
metro.baglanti_ekle("Kağıthane", "Kargo Terminali", 2, "M11")  
metro.baglanti_ekle("Kargo Terminali", "İstanbul Havalimanı", 2, "M11")  

# ✅ **M3 Hattı**: Kirazlı -> Başakşehir -> İkitelli -> Mahmutbey  
metro.baglanti_ekle("Kirazlı", "Başakşehir", 3, "M3")  
metro.baglanti_ekle("Başakşehir", "İkitelli", 2, "M3")  
metro.baglanti_ekle("İkitelli", "Mahmutbey", 1, "M3")  

# ✅ **Aktarma Noktaları**: Farklı hatlar arasında aktarmaları ekliyoruz.  
metro.baglanti_ekle("Mecidiyeköy", "Taksim", 5)  # M7-M2 hattı aktarması  
metro.baglanti_ekle("Levent", "Gayrettepe", 2)  # M2-M11 hattı aktarması  
metro.baglanti_ekle("Mahmutbey", "Kirazlı", 4)  # M3-M7 hattı aktarması  
metro.baglanti_ekle("Yenikapı", "Şişhane", 6)  # M2 hattı aktarması  

# # ✅ **Test Senaryoları**: Çeşitli başlangıç ve hedef istasyonları arasında rota hesaplama  

# Mahmutbey -> İstanbul Havalimanı arasındaki en az aktarmalı ve en hızlı rotalar  
print("🟢 En az aktarmalı rota (Mahmutbey -> İstanbul Havalimanı):", metro.en_az_aktarma_bul("Mahmutbey", "İstanbul Havalimanı"))  
print("🟢 En hızlı rota (Mahmutbey -> İstanbul Havalimanı):", metro.en_hizli_rota_bul("Mahmutbey", "İstanbul Havalimanı"))  
print("                                                                                      ")
# Kirazlı -> Hacıosman arasındaki en az aktarmalı ve en hızlı rotalar  
print("🔵 En az aktarmalı rota (Kirazlı -> Hacıosman):", metro.en_az_aktarma_bul("Kirazlı", "Hacıosman"))  
print("🔵 En hızlı rota (Kirazlı -> Hacıosman):", metro.en_hizli_rota_bul("Kirazlı", "Hacıosman"))  
print("                                                                                      ")
# Mecidiyeköy -> Kağıthane arasındaki en az aktarmalı ve en hızlı rotalar  
print("🔴 En az aktarmalı rota (Mecidiyeköy -> Kağıthane):", metro.en_az_aktarma_bul("Mecidiyeköy", "Kağıthane"))  
print("🔴 En hızlı rota (Mecidiyeköy -> Kağıthane):", metro.en_hizli_rota_bul("Mecidiyeköy", "Kağıthane"))  
print("                                                                                      ")
# Levent -> Yenikapı arasındaki en az aktarmalı ve en hızlı rotalar  
print("🟡 En az aktarmalı rota (Levent -> Yenikapı):", metro.en_az_aktarma_bul("Levent", "Yenikapı"))  
print("🟡 En hızlı rota (Levent -> Yenikapı):", metro.en_hizli_rota_bul("Levent", "Yenikapı"))
