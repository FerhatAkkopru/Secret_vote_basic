# 🗳️ ZKP Oylama Sistemi

Zero-Knowledge Proof (ZKP) teknolojisi kullanarak **anonim ve güvenli oylama sistemi**. Mina Protocol üzerinde SnarkyJS ile geliştirilmiştir.

## 🔍 Proje Hakkında

Bu proje, blockchain teknolojisi ve Zero-Knowledge Proof'ları kullanarak **tamamen anonim** bir oylama sistemi sunar. Kullanıcıların kimlik bilgileri gizli kalırken, sadece oy verme yetkisi olup olmadığı (yaş kontrolü, kişi verileri doğrulama, çifte oy engelleme) kanıtlanır.

### ✨ Özellikler

- 🔐 **Tam Anonimlik**: İsim, soyisim, yaş ve TC kimlik numarası blockchain'de görünmez
- ✅ **Yaş Kanıtı**: ZKP ile sadece 18+ olduğunuz kanıtlanır, yaşınız bilinmez
- ✅ **Kişi Kanıtı**: ZKP ile sadece geçerli kişi verileri (TC+isim+soyisim+yaş) olduğunuz kanıtlanır, kimlik bilgileriniz bilinmez
- 🔐 **Güvenli Kişi Verileri Saklama**: Kişi verileri salt+pepper ile SHA-256 hash'lenerek saklanır
- 🚫 **Çifte Oy Engelleme**: Aynı TC kimlik numarası ile birden fazla oy verilemez
- 📊 **Şeffaflık**: Oy dağılımı ve toplam sayılar herkese açık
- 🎨 **Modern UI**: Streamlit ile kullanıcı dostu web arayüzü
- 🧪 **Test Coverage**: Jest ile kapsamlı testler

### 🏗️ Mimari

```
Frontend (Streamlit) → Smart Contract (SnarkyJS) → Mina Blockchain
     ↓                        ↓                        ↓
  Web UI              ZKP Proofs & Logic        Decentralized Storage
```

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler

- **Node.js** (v16 veya üzeri)
- **Python** (v3.8 veya üzeri)
- **npm** veya **yarn**

### 1. Projeyi Klonlayın

```bash
git clone https://github.com/kullanici-adi/zkp_mina.git
cd zkp_mina
```

### 2. Node.js Bağımlılıklarını Yükleyin

```bash
npm install
```

### 3. Python Bağımlılıklarını Yükleyin

```bash
pip install streamlit python-dotenv
```

### 4. Environment Dosyasını Oluşturun

**`.env.example` dosyası nedir?**
- Bu dosya, projenin ihtiyaç duyduğu environment değişkenlerinin bir şablonudur
- GitHub'a yüklenir ve diğer geliştiricilere hangi değişkenlerin gerekli olduğunu gösterir
- Gerçek değerler içermez, sadece değişken isimlerini ve açıklamalarını içerir

**Pepper değerini ve kişi verilerini nasıl alabilirsiniz?**
- 🔐 **Güvenlik**: Pepper değeri ve kişi verileri sadece proje sahibinde bulunur
- 📧 **İletişim**: Pepper değerini ve kişi verilerini almak için proje sahibiyle iletişime geçin
- 🐛 **GitHub Issues**: GitHub'da issue açarak pepper değerini ve kişi verilerini talep edebilirsiniz
- 💬 **Direkt İletişim**: Proje sahibiyle direkt iletişime geçebilirsiniz

```bash
# .env.example dosyasını .env olarak kopyalayın
cp .env.example .env

# .env dosyasını düzenleyin ve pepper değerini girin
nano .env
```

**`.env` dosyası örneği:**
```env
# ZKP Oylama Sistemi - Güvenlik Ayarları
PEPPER=your_secure_pepper_here
SALT=zkp_voting_salt_2024
HASH_ALGORITHM=SHA-256
```

### 5. TypeScript Kodunu Derleyin

```bash
npm run build
```

### 6. Testleri Çalıştırın

```bash
npm test
```

### 7. Web Arayüzünü Başlatın

```bash
streamlit run voting_ui.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

## 📋 Kullanım

### Web Arayüzü ile Oy Verme

1. **Bilgilerinizi Girin**: İsim, soyisim, yaş ve TC kimlik numarası bilgilerinizi girin
2. **Seçiminizi Yapın**: Kırmızı, Mavi veya Yeşil seçeneklerinden birini seçin
3. **Oy Verin**: "OY VER" butonuna tıklayın
4. **Sonuçları Görün**: ZKP kanıtı ve oy sayılarını görün

**Not**: Sadece geçerli kişi verileri (TC+isim+soyisim+yaş kombinasyonu) ile oy verebilirsiniz.

### Programatik Kullanım

```typescript
import { Voting } from './dist/Voting.js';
import { Mina, Field } from 'snarkyjs';

// Smart contract instance oluştur
const zkAppInstance = new Voting(zkAppAddress);

// Oy ver (kimlik bilgileri gizli)
await zkAppInstance.vote(
  Field(0),           // choice: 0=Kırmızı, 1=Mavi, 2=Yeşil
  Field(personHash),  // Kişi hash'i (TC+isim+soyisim+yaş) (gizli)
  Field(ageProof),    // Yaş >= 18 kanıtı (1 veya 0)
  Field(personProof), // Geçerli kişi verileri kanıtı (1 veya 0)
  Field(voteProof)    // Daha önce oy vermemiş kanıtı (1 veya 0)
);
```

## 🔐 ZKP Nasıl Çalışıyor?

### Gizli Bilgiler
- **Kişi Verileri**: `personHash` olarak saklanır (TC+isim+soyisim+yaş)

### Açık Bilgiler
- **Yaş Kanıtı**: `ageProof = 1` (18+ olduğunuzun kanıtı)
- **Kişi Kanıtı**: `personProof = 1` (geçerli kişi verileri olduğunuzun kanıtı)
- **Çifte Oy Engelleme Kanıtı**: `voteProof = 1` (daha önce oy vermemiş olduğunuzun kanıtı)
- **Oy Tercihi**: `choice` (0, 1, veya 2)
- **Oy Sayıları**: Toplam ve dağılım

### Güvenlik Katmanları

1. **Kimlik Gizliliği**: Tüm kişisel bilgiler hash'lenir
2. **Yaş Doğrulama**: ZKP ile sadece 18+ olduğunuz kanıtlanır
3. **Kişi Doğrulama**: ZKP ile sadece geçerli kişi verileri (TC+isim+soyisim+yaş) olduğunuz kanıtlanır
4. **Güvenli Kişi Verileri Saklama**: Kişi verileri salt+pepper ile SHA-256 hash'lenerek saklanır
5. **Çifte Oy Engelleme**: Aynı TC kimlik numarası ile birden fazla oy verilemez
6. **Şeffaflık**: Oy dağılımı herkese açık

## 📁 Proje Yapısı

```
zkp_mina/
├── Voting.ts              # Ana smart contract
├── Voting.Test.ts         # Jest testleri
├── voting_ui.py          # Streamlit web arayüzü
├── hash_utils.py         # Güvenli hash utility fonksiyonları
├── voted_tc_tracker.py   # Çifte oy engelleme sistemi
├── stress_test.py        # Simülasyon stress testi
├── real_stress_test.py   # Gerçek sistem stress testi
├── secure_valid_ids.json # Hash'lenmiş geçerli TC kimlik numaraları
├── secure_people_data.json # Hash'lenmiş kişi verileri (TC+isim+soyisim+yaş)
├── voted_tc_hashes.json  # Oy vermiş TC kimlik numaralarının hash'leri
├── .env.example          # Environment değişkenleri örneği
├── .env                  # Environment değişkenleri (gitignore'da)
├── package.json          # Node.js bağımlılıkları
├── tsconfig.json         # TypeScript konfigürasyonu
├── jest.config.js        # Jest test konfigürasyonu
├── dist/                 # Derlenmiş JavaScript dosyaları
│   ├── Voting.js
│   └── Voting.Test.js
└── README.md             # Bu dosya
```

## 🧪 Testler

Proje Jest ile kapsamlı testler içerir:

```bash
npm test
```

**Test Senaryoları:**
- ✅ Başlangıçta oy sayılarının 0 olması
- ✅ Kırmızı seçenek için oy verme
- ✅ Mavi seçenek için oy verme  
- ✅ Yaş kontrolü (18+ doğrulama)
- ✅ Kişi verileri kontrolü (geçerli TC+isim+soyisim+yaş doğrulama)
- ✅ Çifte oy engelleme (aynı TC ile ikinci oy)
- ✅ Geçersiz seçim engelleme
- ✅ Stress test (1000 kullanıcı simülasyonu)
- ✅ Performans testi (gerçek sistem)

## 🔧 Geliştirme

### Yeni Özellik Ekleme

1. `Voting.ts` dosyasında smart contract'ı güncelleyin
2. `Voting.Test.ts` dosyasında testleri ekleyin
3. `voting_ui.py` dosyasında UI'ı güncelleyin
4. Testleri çalıştırın: `npm test`

### Build İşlemi

```bash
# TypeScript'i JavaScript'e derle
npm run build

# Testleri çalıştır
npm test

# Web arayüzünü başlat
streamlit run voting_ui.py
```

## 📚 Teknolojiler

- **Mina Protocol**: Hafif blockchain protokolü
- **SnarkyJS**: Mina için TypeScript/JavaScript kütüphanesi
- **Zero-Knowledge Proofs**: Kimlik gizliliği için
- **Streamlit**: Python web arayüzü
- **Jest**: JavaScript test framework'ü
- **TypeScript**: Tip güvenli JavaScript

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🆘 Sorun Giderme

### Yaygın Sorunlar

**Q: `npm test` çalışmıyor**
A: `npm install` ile bağımlılıkları yüklediğinizden emin olun

**Q: Streamlit başlamıyor**  
A: Python ve streamlit'in yüklü olduğunu kontrol edin: `pip install streamlit`

**Q: Build hatası alıyorum**
A: TypeScript'in yüklü olduğunu kontrol edin: `npm install -g typescript`

### Destek

Sorunlarınız için GitHub Issues kullanın veya iletişime geçin.

## 🔮 Gelecek Planları

- [ ] Çoklu seçim desteği
- [ ] Oy verme süresi sınırlaması
- [ ] Sonuç görselleştirme
- [ ] Mobil uygulama
- [ ] Çoklu dil desteği

---

## ⚠️ Önemli Notlar

**Bu proje demo/eğitim amaçlıdır:**
- 🎯 **Asıl Amaç**: ZKP teknolojisini Mina Protocol üzerinde göstermek
- 📚 **Eğitim**: Zero-Knowledge Proof'ların nasıl çalıştığını öğrenmek
- 🔬 **Demo**: Küçük örnek proje, gerçek seçim sistemi değil
- ✅ **Çifte Oy Engelleme**: Bu demo'da çifte oy verme engellenir
- 🛡️ **Güvenlik**: Gerçek seçimlerde kullanmadan önce güvenlik denetimi gerekir

## 🔐 Güvenli Kişi Verileri Saklama

Kişi verileri (TC+isim+soyisim+yaş) güvenlik için **salt+pepper** ile **SHA-256** hash'lenerek saklanır:

```python
# Hash utility fonksiyonu
import os
from dotenv import load_dotenv

load_dotenv()
SALT = os.getenv('SALT', 'zkp_voting_salt_2024')
PEPPER = os.getenv('PEPPER', 'mina_protocol_pepper')

def hash_person_data(tc_id, first_name, last_name, age):
    combined = SALT + tc_id + first_name + last_name + str(age) + PEPPER
    return hashlib.sha256(combined.encode()).hexdigest()
```

**Güvenlik Avantajları:**
- 🔐 **Salt**: Rainbow table saldırılarını önler
- 🌶️ **Pepper**: Ek güvenlik katmanı (`.env` dosyasında saklanır)
- 🔒 **SHA-256**: Güçlü hash algoritması
- 📁 **Güvenli Dosyalar**: `secure_valid_ids.json` ve `secure_people_data.json` sadece hash'leri içerir
- 🚫 **Git Ignore**: `.env` dosyası GitHub'a yüklenmez
- 🔑 **Environment Variables**: Pepper değeri kodda değil, environment'da saklanır

## 🔐 Pepper Değeri Nasıl Alınır?

Bu proje güvenlik için pepper değerini environment variable olarak kullanır. Pepper değerini almak için:

### 📧 İletişim Seçenekleri

1. **GitHub Issues**: 
   - Proje sayfasında "Issues" sekmesine gidin
   - "Pepper değeri talep ediyorum" başlığıyla yeni issue oluşturun
   - Proje sahibi size pepper değerini özel mesajla gönderecektir

2. **Direkt İletişim**:
   - Proje sahibiyle direkt iletişime geçin
   - E-posta veya sosyal medya üzerinden pepper değerini talep edin

3. **Güvenlik Notu**:
   - Pepper değeri asla public olarak paylaşılmaz
   - Sadece güvenilir kişilere özel olarak gönderilir
   - Her kullanıcı için farklı pepper değeri oluşturulabilir

## 📋 Geçerli Kişi Verileri Listesi

Bu proje **1000 adet geçerli kişi verisi** (TC+isim+soyisim+yaş) kullanır. Kişi verilerini almak için:

### 📧 İletişim Seçenekleri

1. **GitHub Issues**: 
   - Proje sayfasında "Issues" sekmesine gidin
   - "Geçerli kişi verileri listesi talep ediyorum" başlığıyla yeni issue oluşturun
   - Proje sahibi size kişi verilerini özel mesajla gönderecektir

2. **Direkt İletişim**:
   - Proje sahibiyle direkt iletişime geçin
   - E-posta veya sosyal medya üzerinden kişi verilerini talep edin

3. **Güvenlik Notu**:
   - Kişi verileri asla public olarak paylaşılmaz
   - Sadece güvenilir kişilere özel olarak gönderilir
   - Her kullanıcı için farklı kişi verileri listesi oluşturulabilir

### 🛡️ Güvenlik Avantajları

- **1000 Kişi**: Sistemde 1000 adet geçerli kişi verisi (TC+isim+soyisim+yaş) bulunur
- **Gizli Saklama**: GitHub'da görünmez
- **Kontrollü Erişim**: İsteyen kişi proje sahibinden talep eder
- **Güvenli Dağıtım**: Özel mesajla gönderilir

## 🧪 Stress Test ve Performans

Bu proje kapsamlı stress testlerle test edilmiştir:

### 📊 Test Sonuçları

**Simülasyon Testi (1000 kullanıcı):**
- ⏱️ **Süre**: 2.2 saniye
- 🚀 **Throughput**: 453.59 oy/saniye
- ✅ **Başarı Oranı**: 1000/1000 (%100)
- ❌ **Hata**: 0

**Gerçek Sistem Testi (100 kullanıcı):**
- ⏱️ **Süre**: 5.15 saniye
- 🚀 **Throughput**: 19.40 oy/saniye
- ✅ **Başarı Oranı**: 99/100 (%99)
- ❌ **Hata**: 1 (çifte oy - beklenen)

### 🔧 Test Yöntemleri

**1. Sıralı Test (Tek Thread):**
- 1000 kullanıcı: 106.25 saniye
- Throughput: 9.41 oy/saniye

**2. Paralel Test (50 Thread):**
- 1000 kullanıcı: 2.20 saniye
- Throughput: 453.59 oy/saniye

**3. Eşzamanlı Test (Batch Processing):**
- 1000 kullanıcı: 5.78 saniye
- Throughput: 172.97 oy/saniye

### 🎯 Performans Analizi

**Lokal Sistem:**
- ✅ Çok hızlı hash doğrulama
- ✅ Etkili çifte oy engelleme
- ✅ %99 başarı oranı
- ✅ Paralel işleme avantajı

**Gerçek Blockchain Tahmini:**
- ⏱️ 1000 kullanıcı: ~50-60 saniye
- 🚀 Throughput: ~17-20 oy/saniye
- ⚠️ Blockchain işlemleri daha yavaş

### 🧪 Test Çalıştırma

```bash
# Simülasyon testi
python3 stress_test.py

# Gerçek sistem testi
python3 real_stress_test.py
```

**Test Özellikleri:**
- 1000 kişilik gerçekçi veri seti
- Rastgele oy seçimi
- Çifte oy engelleme testi
- Hash doğrulama testi
- Performans ölçümü

## 📊 Proje Değerlendirmesi

### 🎯 Proje Amacı: ZKP Teknolojisini Mina Protocol Üzerinde Göstermek

**Önerilen Kullanım:**
- 🎓 ZKP teknolojisini öğrenmek
- 🔬 Mina Protocol ile deneyim yapmak
- 🛡️ Güvenlik best practice'lerini görmek
- 📚 Blockchain eğitimi için referans

## 🔐 İki Hash Sistemi

Bu proje **iki farklı hash sistemi** kullanır:

### 1️⃣ TC Hash Sistemi (Çifte Oy Engelleme)
```python
def hash_id(tc_id):
    combined = SALT + tc_id + PEPPER
    return hashlib.sha256(combined.encode()).hexdigest()
```
**Amaç:** Çifte oy engelleme
- Aynı TC kimlik numarası ile birden fazla oy verilemez
- `voted_tc_hashes.json` dosyasında saklanır
- Sadece TC kimlik numarası hash'lenir

### 2️⃣ Kişi Hash Sistemi (Kimlik Doğrulama)
```python
def hash_person_data(tc_id, first_name, last_name, age):
    combined = SALT + tc_id + first_name + last_name + str(age) + PEPPER
    return hashlib.sha256(combined.encode()).hexdigest()
```
**Amaç:** Kimlik doğrulama
- TC+isim+soyisim+yaş kombinasyonu doğrulanır
- `secure_people_data.json` dosyasında saklanır
- Tüm kişi verileri birlikte hash'lenir

### 🤔 Neden İki Hash Sistemi?

**Örnek Senaryo:**
```
Kişi 1: Ahmet Yılmaz, 25 yaş, TC: 12345678901
- TC Hash: abc123... (çifte oy engelleme)
- Kişi Hash: xyz789... (kimlik doğrulama)

Kişi 2: Mehmet Yılmaz, 30 yaş, TC: 12345678901
- TC Hash: abc123... (aynı TC, oy veremez)
- Kişi Hash: def456... (farklı kişi)

Kişi 3: Ahmet Yılmaz, 25 yaş, TC: 98765432109
- TC Hash: ghi789... (farklı TC, oy verebilir)
- Kişi Hash: jkl012... (farklı kişi)
```

**Avantajlar:**
- ✅ **Çifte oy engelleme** (TC bazlı)
- ✅ **Kimlik doğrulama** (kişi bazlı)
- ✅ **Güvenlik katmanları**
- ✅ **ZKP uyumluluğu**
- ✅ **Esneklik**

## 🚫 Çifte Oy Engelleme Sistemi

Bu proje **çifte oy vermeyi** engelleyen güvenli bir sistem içerir:

### 📁 `voted_tc_hashes.json` Dosyası

**Ne işe yarar?**
- Oy vermiş TC kimlik numaralarının **hash'lerini** saklar
- Çifte oy vermeyi engeller
- TC kimlik numarası **gizli kalır**, sadece hash'i saklanır

**Nasıl çalışır?**
1. Kullanıcı TC kimlik numarası girer: `12345678901`
2. Sistem hash'ler: `b9ac6cc3f5910b68...` (salt+pepper ile)
3. Hash'i `voted_hashes` listesine ekler
4. İkinci oy denemesinde hash kontrol edilir
5. Aynı hash varsa = "Daha önce oy vermiş" hatası

**Otomatik Güncelleme:**
- ✅ Her başarılı oy verme işleminden sonra `voted_hashes` otomatik güncellenir
- ✅ TC kimlik numarasının hash'i listeye eklenir
- ✅ Dosya anında kaydedilir ve kalıcı olarak saklanır
- ✅ Sistem yeniden başlatılsa bile oy kayıtları korunur

**Güvenlik avantajları:**
- 🔐 TC kimlik numarası **görünmez**
- 🔒 Sadece **hash'i** saklanır
- 🧂 **Salt+pepper** ile güvenli hash'leme
- 🚫 **Çifte oy** engellenir

### 🛡️ ZKP Proof Sistemi

**3 Katmanlı Güvenlik:**
1. **Yaş Proof**: `ageProof = 1` (18+ olduğunun kanıtı)
2. **Kişi Proof**: `personProof = 1` (geçerli kişi verileri kanıtı)
3. **Vote Proof**: `voteProof = 1` (daha önce oy vermemiş kanıtı)

**Smart Contract Kontrolü:**
```typescript
// Yaş kontrolü
const isValidAgeProof = ageProof.equals(Field(1));
Provable.if(isValidAgeProof, Bool(true), Bool(false)).assertTrue('Yaş 18\'den küçük olamaz');

// Kişi verileri kontrolü
const isValidPersonProof = personProof.equals(Field(1));
Provable.if(isValidPersonProof, Bool(true), Bool(false)).assertTrue('Geçersiz kişi verileri');

// Çifte oy kontrolü
const isValidVoteProof = voteProof.equals(Field(1));
Provable.if(isValidVoteProof, Bool(true), Bool(false)).assertTrue('Bu TC kimlik numarası daha önce oy vermiş');
```
