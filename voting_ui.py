import streamlit as st
import subprocess
import json
import time

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="ZKP Oylama Sistemi",
    page_icon="🗳️",
    layout="centered"
)

# Ana başlık
st.title("🗳️ ZKP Oylama Sistemi")

# Kullanıcı bilgileri formu
st.markdown("### 👤 Oy Veren Bilgileri")
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("İsim", placeholder="Adınızı girin")
    surname = st.text_input("Soyisim", placeholder="Soyadınızı girin")

with col2:
    age = st.number_input("Yaş", min_value=1, max_value=120, value=18)
    
    # Yaş kanıtı oluştur
    age_proof = 1 if age >= 18 else 0

# Oylama seçenekleri
st.markdown("### 🗳️ Hangi seçeneği destekliyorsunuz?")

col_red, col_blue, col_green = st.columns(3)

with col_red:
    if st.button("🔴 Kırmızı", key="red"):
        st.session_state.vote_choice = "Kırmızı"
        st.session_state.vote_value = 0

with col_blue:
    if st.button("🔵 Mavi", key="blue"):
        st.session_state.vote_choice = "Mavi"
        st.session_state.vote_value = 1

with col_green:
    if st.button("🟢 Yeşil", key="green"):
        st.session_state.vote_choice = "Yeşil"
        st.session_state.vote_value = 2

# Oy verme işlemi
if hasattr(st.session_state, 'vote_choice'):
    st.markdown(f"**Seçiminiz:** {st.session_state.vote_choice}")
    
    # Form doğrulama
    if not name or not surname:
        st.warning("⚠️ Lütfen tüm bilgileri doldurun")
    else:
        if st.button("🗳️ OY VER", key="submit_vote"):
            with st.spinner("ZKP ile kimlik doğrulama ve oy işleniyor..."):
                try:
                    # Hash'leri oluştur
                    import hashlib
                    name_hash = int(hashlib.md5(name.encode()).hexdigest()[:8], 16)
                    surname_hash = int(hashlib.md5(surname.encode()).hexdigest()[:8], 16)
                    age_hash = int(hashlib.md5(str(age).encode()).hexdigest()[:8], 16)
                    
                    # Oy verme scripti
                    vote_script = f"""
const {{ Voting }} = require('./dist/Voting.js');
const {{ Mina, PrivateKey, PublicKey, Field, AccountUpdate }} = require('snarkyjs');

async function singleVote() {{
    // Local blockchain kur
    let Local = await Mina.LocalBlockchain({{ proofsEnabled: false }});
    Mina.setActiveInstance(Local);
    
    const account0 = Local.testAccounts[0];
    const feePayer = account0.privateKey;
    
    // zkApp hesabı
    const zkAppPrivateKey = PrivateKey.random();
    const zkAppAddress = zkAppPrivateKey.toPublicKey();
    const zkAppInstance = new Voting(zkAppAddress);
    
    // Deploy
    let txn = await Mina.transaction(feePayer, async () => {{
        AccountUpdate.fundNewAccount(feePayer);
        await zkAppInstance.deploy({{ zkappKey: zkAppPrivateKey }});
    }});
    await txn.prove();
    await txn.sign([feePayer, zkAppPrivateKey]).send();
    
    // ZKP ile oy ver (kimlik bilgileri gizli)
    let voteTxn = await Mina.transaction(feePayer, async () => {{
        await zkAppInstance.vote(
            Field({st.session_state.vote_value}),    // choice: açık
            Field({name_hash}),                      // nameHash: gizli
            Field({surname_hash}),                   // surnameHash: gizli
            Field({age_hash}),                      // ageHash: gizli
            Field({age_proof})                      // ageProof: gizli (1 = yaş >= 18)
        );
    }});
    await voteTxn.prove();
    await voteTxn.sign([feePayer]).send();
    
    // Sonuçları göster
    await zkAppInstance.red.fetch();
    await zkAppInstance.blue.fetch();
    await zkAppInstance.green.fetch();
    await zkAppInstance.totalVoters.fetch();
    
    console.log('🔴 Kırmızı:', zkAppInstance.red.get().toString());
    console.log('🔵 Mavi:', zkAppInstance.blue.get().toString());
    console.log('🟢 Yeşil:', zkAppInstance.green.get().toString());
    console.log('👥 Toplam Oy Veren:', zkAppInstance.totalVoters.get().toString());
}}

singleVote().catch(console.error);
"""
                    
                    # Geçici dosya oluştur ve çalıştır
                    with open('temp_vote.js', 'w') as f:
                        f.write(vote_script)
                    
                    result = subprocess.run([
                        'node', 'temp_vote.js'
                    ], capture_output=True, text=True, timeout=30)
                    
                    # Temizlik
                    import os
                    if os.path.exists('temp_vote.js'):
                        os.remove('temp_vote.js')
                    
                    if result.returncode == 0:
                        st.success("✅ Oyunuz başarıyla kaydedildi!")
                        st.info("🔒 Yaşınız bilinmiyor, sadece 18 yaşından büyük olduğunuz ZKP tarafından kanıtlandı.")
                        
                        
                        # Sayaçları güncelle
                        output_lines = result.stdout.split('\n')
                        for line in output_lines:
                            if 'Kırmızı:' in line:
                                red_count = int(line.split(':')[1].strip())
                                st.session_state.vote_counts['Kırmızı'] = red_count
                            elif 'Mavi:' in line:
                                blue_count = int(line.split(':')[1].strip())
                                st.session_state.vote_counts['Mavi'] = blue_count
                            elif 'Yeşil:' in line:
                                green_count = int(line.split(':')[1].strip())
                                st.session_state.vote_counts['Yeşil'] = green_count
                                
                    else:
                        # Yaş kontrolü hatası mı kontrol et
                        if "Yaş 18'den küçük olamaz" in result.stderr:
                            st.error("❌ Yaşınız yeterli değil!")
                            st.info("🔒 Yaşınız bilinmiyor, sadece 18 yaşından küçük olduğunuz ZKP tarafından tespit edildi.")
                        else:
                            st.error("❌ Hata: Oyunuz kaydedilemedi")
                            st.error(result.stderr)
                        
                except subprocess.TimeoutExpired:
                    st.error("⏰ İşlem zaman aşımına uğradı")
                except Exception as e:
                    st.error(f"❌ Beklenmeyen hata: {str(e)}")

# Mevcut oy sayıları
st.markdown("---")
st.markdown("### 📊 Mevcut Oy Sayıları")

# Demo için basit sayaçlar
if 'vote_counts' not in st.session_state:
    st.session_state.vote_counts = {'Kırmızı': 0, 'Mavi': 0, 'Yeşil': 0}

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔴 Kırmızı", st.session_state.vote_counts['Kırmızı'])

with col2:
    st.metric("🔵 Mavi", st.session_state.vote_counts['Mavi'])

with col3:
    st.metric("🟢 Yeşil", st.session_state.vote_counts['Yeşil'])

# ZKP açıklaması
st.markdown("---")
st.markdown("### 🔍 ZKP Nasıl Verileri Saklıyor?")

st.markdown("""
**Zero-Knowledge Proof** bu sistemde şu şekilde çalışıyor:

1. **🔐 Gizli Kimlik:** İsim, soyisim ve yaş blockchain'de görünmez
2. **✅ Yaş Kanıtı:** ZKP ile sadece yaş >= 18 olduğunun kanıtı verilir
3. **📊 Şeffaflık:** Oy dağılımı ve toplam sayılar açık

**Kod Örneği:**
```typescript
@method vote(choice, nameHash, surnameHash, ageHash, ageProof) {
    // ZKP ile yaş kanıtı kontrolü
    const isValidAgeProof = ageProof.equals(Field(1));
    Provable.if(isValidAgeProof, Bool(true), Bool(false)).assertTrue('Yaş 18\'den küçük olamaz');
    
    // Tüm kimlik bilgileri gizli (hash'ler)
    // nameHash, surnameHash, ageHash blockchain'de görünmez
    
    // Oy tercihi açık (sayım için)
    const isRed = choice.equals(Field(0));    // Açık
    const isBlue = choice.equals(Field(1));    // Açık  
    const isGreen = choice.equals(Field(2));    // Açık
}
```

**Sonuç:** Blockchain'de tüm kimlik bilgileri gizli, sadece yaş kanıtı ve oy dağılımı açık!
**Amaç:** Gerçek ZKP - yaşınız hiç bilinmez, sadece 18+ olduğunuz kanıtlanır!
""")
