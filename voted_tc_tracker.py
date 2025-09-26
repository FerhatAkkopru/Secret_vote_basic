import json
import hashlib
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Hash utility fonksiyonları
SALT = os.getenv('SALT', 'zkp_voting_salt_2024')
PEPPER = os.getenv('PEPPER', 'mina_protocol_pepper')

def hash_id(tc_id):
    # TC kimlik numarasını hash'liyorum
    combined = SALT + tc_id + PEPPER
    return hashlib.sha256(combined.encode()).hexdigest()

def load_voted_tc_list():
    # Oy vermiş TC kimlik numaralarını yüklüyorum
    try:
        with open('voted_tc_hashes.json', 'r') as f:
            data = json.load(f)
            return data.get('voted_hashes', [])
    except:
        return []

def save_voted_tc_list(voted_hashes):
    # Oy vermiş TC kimlik numaralarını kaydediyorum
    data = {
        "voted_hashes": voted_hashes,
        "description": "Oy vermiş TC kimlik numaralarının hash'leri (salt+pepper ile)",
        "salt": SALT,
        "algorithm": "SHA-256",
        "note": "Pepper değeri .env dosyasında saklanır ve GitHub'a yüklenmez"
    }
    
    with open('voted_tc_hashes.json', 'w') as f:
        json.dump(data, f, indent=2)

def has_voted(tc_id):
    # Bu TC kimlik numarası daha önce oy vermiş mi kontrol ediyorum
    tc_hash = hash_id(tc_id)
    voted_hashes = load_voted_tc_list()
    return tc_hash in voted_hashes

def mark_as_voted(tc_id):
    # Bu TC kimlik numarasını oy vermiş olarak işaretliyorum
    tc_hash = hash_id(tc_id)
    voted_hashes = load_voted_tc_list()
    
    if tc_hash not in voted_hashes:
        voted_hashes.append(tc_hash)
        save_voted_tc_list(voted_hashes)
        return True
    return False

def get_vote_proof(tc_id):
    # Oy verme yetkisi proof'u döndürüyorum
    # 1 = oy verebilir, 0 = daha önce oy vermiş
    return 0 if has_voted(tc_id) else 1

def reset_votes():
    # Tüm oy kayıtlarını sıfırlıyorum (test için)
    save_voted_tc_list([])
    print("✅ Tüm oy kayıtları sıfırlandı")

if __name__ == "__main__":
    print("🧪 Çifte Oy Engelleme Testi")
    print("=" * 50)
    
    test_tc = "12345678901"
    
    # İlk kontrol
    print(f"TC ID: {test_tc}")
    print(f"Hash: {hash_id(test_tc)[:16]}...")
    print(f"Daha önce oy vermiş mi: {has_voted(test_tc)}")
    print(f"Oy verme yetkisi: {get_vote_proof(test_tc)}")
    
    # Oy verme simülasyonu
    if mark_as_voted(test_tc):
        print("✅ Oy kaydedildi")
    
    # İkinci kontrol
    print(f"Daha önce oy vermiş mi: {has_voted(test_tc)}")
    print(f"Oy verme yetkisi: {get_vote_proof(test_tc)}")
    
    # Test sıfırlama
    reset_votes()
    print(f"Sıfırlama sonrası oy verme yetkisi: {get_vote_proof(test_tc)}")
