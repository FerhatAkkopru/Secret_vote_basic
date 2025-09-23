# 🗳️ ZKP Oylama Sistemi

Zero-Knowledge Proof (ZKP) teknolojisi kullanarak **anonim ve güvenli oylama sistemi**. Mina Protocol üzerinde SnarkyJS ile geliştirilmiştir.

## 🔍 Proje Hakkında

Bu proje, blockchain teknolojisi ve Zero-Knowledge Proof'ları kullanarak **tamamen anonim** bir oylama sistemi sunar. Kullanıcıların kimlik bilgileri gizli kalırken, sadece oy verme yetkisi olup olmadığı (yaş kontrolü) kanıtlanır.

### ✨ Özellikler

- 🔐 **Tam Anonimlik**: İsim, soyisim ve yaş bilgileri blockchain'de görünmez
- ✅ **Yaş Kanıtı**: ZKP ile sadece 18+ olduğunuz kanıtlanır, yaşınız bilinmez
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
pip install streamlit
```

### 4. TypeScript Kodunu Derleyin

```bash
npm run build
```

### 5. Testleri Çalıştırın

```bash
npm test
```

### 6. Web Arayüzünü Başlatın

```bash
streamlit run voting_ui.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

## 📋 Kullanım

### Web Arayüzü ile Oy Verme

1. **Bilgilerinizi Girin**: İsim, soyisim ve yaş bilgilerinizi girin
2. **Seçiminizi Yapın**: Kırmızı, Mavi veya Yeşil seçeneklerinden birini seçin
3. **Oy Verin**: "OY VER" butonuna tıklayın
4. **Sonuçları Görün**: ZKP kanıtı ve oy sayılarını görün

### Programatik Kullanım

```typescript
import { Voting } from './dist/Voting.js';
import { Mina, Field } from 'snarkyjs';

// Smart contract instance oluştur
const zkAppInstance = new Voting(zkAppAddress);

// Oy ver (kimlik bilgileri gizli)
await zkAppInstance.vote(
  Field(0),           // choice: 0=Kırmızı, 1=Mavi, 2=Yeşil
  Field(nameHash),    // İsim hash'i (gizli)
  Field(surnameHash), // Soyisim hash'i (gizli)  
  Field(ageHash),     // Yaş hash'i (gizli)
  Field(ageProof)     // Yaş >= 18 kanıtı (1 veya 0)
);
```

## 🔐 ZKP Nasıl Çalışıyor?

### Gizli Bilgiler
- **İsim**: `nameHash` olarak saklanır
- **Soyisim**: `surnameHash` olarak saklanır  
- **Yaş**: `ageHash` olarak saklanır

### Açık Bilgiler
- **Yaş Kanıtı**: `ageProof = 1` (18+ olduğunuzun kanıtı)
- **Oy Tercihi**: `choice` (0, 1, veya 2)
- **Oy Sayıları**: Toplam ve dağılım

### Güvenlik Katmanları

1. **Kimlik Gizliliği**: Tüm kişisel bilgiler hash'lenir
2. **Yaş Doğrulama**: ZKP ile sadece 18+ olduğunuz kanıtlanır
3. **Şeffaflık**: Oy dağılımı herkese açık

## 📁 Proje Yapısı

```
zkp_mina/
├── Voting.ts              # Ana smart contract
├── Voting.Test.ts         # Jest testleri
├── voting_ui.py          # Streamlit web arayüzü
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
- ✅ Geçersiz seçim engelleme

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
- ⚠️ **Çifte Oy**: Bu demo'da çifte oy verme engellenmez (demo amaçlı)
- 🛡️ **Güvenlik**: Gerçek seçimlerde kullanmadan önce güvenlik denetimi gerekir
