# 🐄 Zootekni Pro - Intelligent Rationing System

**Versiyon:** 5.0  
**Dil:** Türkçe & English

Zootekni Pro, Türkiye'deki hayvancılık sektörü için geliştirilmiş kapsamlı bir **Rasyon Mühendisliği ve Ekonomik Zeka Platformu**dur. Precision Livestock Farming ve Computational Nutrition alanlarında uzmanlaşmış yazılım mimarisi ile modern, verimli ve ekonomik çözümler sunar.

![Python](https://img.shields.io/badge/Python-3.13+-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green)
![License](https://img.shields.io/badge/License-Proprietary-orange)

## ✨ Özellikler

### 🎨 Modern Kullanıcı Arayüzü
- **PyQt5** tabanlı modern dashboard
- Karanlık tema (Dark Mode)
- Sol sidebar navigasyon menüsü
- Adobe/Linear tarzı tasarım
- Responsive layout

### 📊 Biyolojik Algoritmalar
- **NRC 2021** süt ineği besleme standartları
- **INRA** ve **ARC** desteği
- Dinamik Kuru Madde Alımı (DMI) hesabı
- Net Enerji Laktasyon (NEL) hesaplamaları
- Protein fraksiyonları (RDP/RUP)
- Mineral oranları (Ca/P dengesi, DCAD)
- Çevresel etki (metan, azot salınımı)

### ⚡ Rasyon Optimizasyonu
- **SciPy** lineer programlama (Simplex algoritması)
- Minimum maliyetli rasyon hesaplama
- Besin kısıtlamaları (eNDF, protein, enerji, mineraller)
- Gölge fiyatlar (Shadow Pricing)
- Çözülemeyen durumlar için öneri sistemi

### 💰 Ekonomik Analiz
- **IOFC** (Income Over Feed Cost)
- Duyarlılık analizi (%10 fiyat artışı etkisi)
- Marjinal analiz
- Yem maliyeti/kg süt hesabı

### 📈 Görselleştirme
- Radar chart (besin örümcek ağı)
- Donut chart (maliyet dağılımı)
- Bar chart (karşılaştırma grafikleri)

### 📄 Raporlama
- Profesyonel PDF raporları
- Besleme talimatları
- Ekonomik özetler
- Çevresel etki raporları

### 🗄️ Veri Yönetimi
- **SQLite** veritabanı
- 39 kalem yem veritabanı
- CRUD işlemleri (Yem Editörü)
- Rasyon arşivleme (v1, v2, v3)

## 📁 Proje Yapısı

```
zootekni-pro/
├── main.py                      # Uygulama giriş noktası
├── pyproject.toml               # Bağımlılıklar
├── AGENTS.md                    # Proje dokümantasyonu
├── controllers/                  # İş mantığı
│   ├── auth_controller.py      # Kimlik doğrulama
│   └── dashboard_controller.py # Dashboard yönetimi
├── views/                       # PyQt5 UI
│   ├── login_view.py           # Giriş ekranı
│   └── dashboard_view.py       # Ana dashboard
├── models/                      # Veri modelleri
│   ├── nutrition_models.py     # NRC 2021, INRA, ARC
│   └── optimization_model.py    # Linear programming
├── utils/                       # Yardımcı modüller
│   ├── database.py             # SQLite yönetimi
│   ├── logger.py               # Logging
│   ├── auth.py                # Şifre güvenliği
│   ├── visualization.py        # Grafikler
│   └── reporting.py           # PDF raporları
└── data/
    └── yemler.csv              # Yem veritabanı
```

## 🚀 Kurulum

### Gereksinimler
- Python 3.13+
- uv (paket yöneticisi)

### Adımlar

```bash
# Projeyi klonla
git clone https://github.com/animalscienc/rasyon_ogulcan.git
cd rasyon_ogulcan

# Bağımlılıkları yükle
uv sync

# Çalıştır
uv run python main.py
```

## 🔐 Giriş Bilgileri

| Kullanıcı | Şifre |
|-----------|-------|
| admin | admin123 |

## 📖 Kullanım

### 1. Giriş
Uygulamayı başlattığınızda karşınıza giriş ekranı gelecektir. Yukarıdaki kimlik bilgileri ile giriş yapın.

### 2. Dashboard
Ana dashboard'ta şunları yapabilirsiniz:
- 📊 Genel istatistikleri görüntüle
- 🌾 Yem kütüphanesine eriş
- 🐄 Hayvan grupları oluştur
- 📋 Rasyon oluştur
- ⚡ Optimize et
- 💰 Ekonomik analiz yap
- 📄 Rapor al

### 3. Rasyon Oluşturma
1. Hayvan grubu seçin
2. Besin hedeflerini belirleyin (DMI, HP, NDF, NEL)
3. Yem seçin ve miktarları girin
4. Kaydedin veya optimize edin

### 4. Ekonomik Analiz
- Süt fiyatı ve verimini girin
- IOFC hesaplayın
- Duyarlılık analizi yapın

## 🛠️ Teknik Detaylar

### Kullanılan Teknolojiler
- **Python 3.13** - Ana programlama dili
- **PyQt5 5.15** - GUI framework
- **NumPy 2.4** - Sayısal hesaplama
- **SciPy 1.17** - Optimizasyon algoritmaları
- **Pandas 3.0** - Veri işleme
- **Matplotlib 3.10** - Grafikler
- **FPDF 1.7** - PDF üretimi

### Mimari
- **MVC (Model-View-Controller)** tasarım kalıbı
- Çoklu iş parçacığı (QThread) desteği
- Hata yönetimi ve loglama

## 📝 Lisans

Tüm hakları saklıdır. © 2024 Zootekni

## 🤝 Katkıda Bulunun

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için önce tartışma açın.

---

> **Not:** Bu yazılım Türkiye'deki hayvancılık sektörü için özel olarak geliştirilmiştir. NRC, INRA ve ARC standartları referans alınmıştır.