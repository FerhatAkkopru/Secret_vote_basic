import hashlib
import json
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Güvenlik için salt ve pepper değerleri
SALT = os.getenv('SALT', 'zkp_voting_salt_2024')  # Varsayılan değer
PEPPER = os.getenv('PEPPER', 'mina_protocol_pepper')  # Varsayılan değer

def hash_id(tc_id):
    """
    TC kimlik numarasını salt + pepper ile SHA-256 hash'ler
    """
    # Salt + TC ID + Pepper kombinasyonu
    combined = SALT + tc_id + PEPPER
    return hashlib.sha256(combined.encode()).hexdigest()

def hash_person_data(tc_id, first_name, last_name, age):
    """
    TC kimlik numarası + isim + soyisim + yaş bilgilerini salt + pepper ile SHA-256 hash'ler
    """
    # Salt + TC ID + First Name + Last Name + Age + Pepper kombinasyonu
    combined = SALT + tc_id + first_name + last_name + str(age) + PEPPER
    return hashlib.sha256(combined.encode()).hexdigest()

def create_hashed_id_list():
    """
    Geçerli TC kimlik numaralarını hash'leyerek güvenli liste oluşturur
    """
    # TC kimlik numaralarını people_data.json dosyasından oku
    try:
        with open('people_data.json', 'r', encoding='utf-8') as f:
            people_data = json.load(f)
        valid_tc_ids = [person['tc_id'] for person in people_data]
    except FileNotFoundError:
        # Fallback: Eğer dosya yoksa eski listeyi kullan
        valid_tc_ids = [
            "12345678901",
            "23456789012", 
            "34567890123",
            "45678901234",
            "56789012345"
        ]
    
    hashed_ids = []
    for tc_id in valid_tc_ids:
        hashed_id = hash_id(tc_id)
        hashed_ids.append(hashed_id)
    
    return {
        "hashed_ids": hashed_ids,
        "description": "SHA-256 ile hash'lenmiş geçerli TC kimlik numaraları (salt+pepper ile)",
        "salt": SALT,
        "algorithm": "SHA-256",
        "note": "Pepper değeri .env dosyasında saklanır ve GitHub'a yüklenmez"
    }

def create_hashed_people_list():
    """
    Kişi verilerini hash'leyerek güvenli liste oluşturur
    """
    # Kişi verilerini dosyadan oku
    try:
        with open('people_data.json', 'r', encoding='utf-8') as f:
            people_data = json.load(f)
    except FileNotFoundError:
        # Fallback: Eğer dosya yoksa boş liste döndür
        people_data = []
    
    hashed_people = []
    for person in people_data:
        hashed_person = hash_person_data(
            person['tc_id'], 
            person['first_name'], 
            person['last_name'], 
            person['age']
        )
        hashed_people.append(hashed_person)
    
    return {
        "hashed_people": hashed_people,
        "description": "SHA-256 ile hash'lenmiş kişi verileri (TC+isim+soyisim+yaş+salt+pepper)",
        "salt": SALT,
        "algorithm": "SHA-256",
        "note": "Pepper değeri .env dosyasında saklanır ve GitHub'a yüklenmez"
    }

def is_valid_id(tc_id):
    """
    Verilen TC kimlik numarasının geçerli olup olmadığını kontrol eder
    """
    try:
        with open('secure_valid_ids.json', 'r') as f:
            data = json.load(f)
            hashed_ids = data['hashed_ids']
            
        # Gelen TC ID'yi hash'le
        input_hash = hash_id(tc_id)
        
        # Hash'lenmiş listede var mı kontrol et
        return input_hash in hashed_ids
    except:
        return False

def is_valid_person(tc_id, first_name, last_name, age):
    """
    Verilen kişi verilerinin geçerli olup olmadığını kontrol eder
    """
    try:
        with open('secure_people_data.json', 'r') as f:
            data = json.load(f)
            hashed_people = data['hashed_people']
            
        # Gelen kişi verilerini hash'le
        input_hash = hash_person_data(tc_id, first_name, last_name, age)
        
        # Hash'lenmiş listede var mı kontrol et
        return input_hash in hashed_people
    except:
        return False

if __name__ == "__main__":
    # Güvenli ID listesi oluştur
    secure_data = create_hashed_id_list()
    
    with open('secure_valid_ids.json', 'w') as f:
        json.dump(secure_data, f, indent=2)
    
    print("✅ Güvenli ID listesi oluşturuldu: secure_valid_ids.json")
    print(f"📊 Toplam {len(secure_data['hashed_ids'])} hash'lenmiş ID")
    
    # Güvenli kişi verileri listesi oluştur
    secure_people_data = create_hashed_people_list()
    
    with open('secure_people_data.json', 'w') as f:
        json.dump(secure_people_data, f, indent=2)
    
    print("✅ Güvenli kişi verileri listesi oluşturuldu: secure_people_data.json")
    print(f"📊 Toplam {len(secure_people_data['hashed_people'])} hash'lenmiş kişi verisi")
    
    # Test
    test_id = "12345678901"
    print(f"\n🧪 Test ID: {test_id}")
    print(f"🔐 Hash: {hash_id(test_id)}")
    print(f"✅ Geçerli mi: {is_valid_id(test_id)}")
    
    # Kişi verisi testi
    test_person = ("04738777654", "Sevgi", "Özkan", 33)
    print(f"\n🧪 Test Kişi: {test_person[1]} {test_person[2]} - {test_person[3]} yaş - TC: {test_person[0]}")
    print(f"🔐 Hash: {hash_person_data(*test_person)}")
    print(f"✅ Geçerli mi: {is_valid_person(*test_person)}")
