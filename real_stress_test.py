import time
import json
import random
import subprocess
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from hash_utils import is_valid_person
from voted_tc_tracker import has_voted, mark_as_voted, get_vote_proof, reset_votes

class RealVotingStressTest:
    def __init__(self, num_users=100):
        self.num_users = num_users
        self.results = []
        self.lock = threading.Lock()
        self.success_count = 0
        self.error_count = 0
        self.start_time = None
        self.end_time = None
        
    def generate_test_data(self):
        # Test için rastgele kişi verisi seçiyorum
        with open('people_data.json', 'r', encoding='utf-8') as f:
            people_data = json.load(f)
        
        # Rastgele kişi seç
        return random.choice(people_data)
    
    def simulate_real_vote(self, user_id):
        # Gerçek oy verme işlemini simüle ediyorum
        try:
            # Test verisi oluştur
            person = self.generate_test_data()
            tc_id = person['tc_id']
            name = person['first_name']
            surname = person['last_name']
            age = person['age']
            
            # Rastgele oy seç
            vote_choice = random.randint(0, 2)  # 0=Kırmızı, 1=Mavi, 2=Yeşil
            
            # Kişi doğrulaması
            if not is_valid_person(tc_id, name, surname, age):
                with self.lock:
                    self.error_count += 1
                return {
                    'user_id': user_id,
                    'status': 'error',
                    'error': 'Invalid person data',
                    'timestamp': time.time()
                }
            
            # Çifte oy kontrolü
            if has_voted(tc_id):
                with self.lock:
                    self.error_count += 1
                return {
                    'user_id': user_id,
                    'status': 'error',
                    'error': 'Already voted',
                    'timestamp': time.time()
                }
            
            # Hash'leri oluştur
            from hash_utils import hash_person_data
            person_hash = int(hash_person_data(tc_id, name, surname, age)[:8], 16)
            
            # Proof'ları oluştur
            age_proof = 1 if age >= 18 else 0
            person_proof = 1  # Yukarıda zaten doğrulandı
            vote_proof = get_vote_proof(tc_id)  # Daha önce oy vermemiş kanıtı
            
            # Smart contract çağrısı simülasyonu
            # Gerçek sistemde burada blockchain işlemi yapılır
            time.sleep(0.5)  # Simüle edilmiş blockchain işlem süresi
            
            # Oy vermiş olarak işaretle
            mark_as_voted(tc_id)
            
            with self.lock:
                self.success_count += 1
            
            return {
                'user_id': user_id,
                'status': 'success',
                'tc_id': tc_id,
                'vote_choice': vote_choice,
                'timestamp': time.time()
            }
            
        except Exception as e:
            with self.lock:
                self.error_count += 1
            return {
                'user_id': user_id,
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }
    
    def run_parallel_test(self, max_workers=10):
        # Paralel test yapıyorum (çoklu thread)
        print(f"🔄 Gerçek Paralel Test Başlatılıyor ({self.num_users} kullanıcı, {max_workers} thread)")
        self.start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.simulate_real_vote, i) for i in range(self.num_users)]
            
            for i, future in enumerate(futures):
                result = future.result()
                self.results.append(result)
                
                if (i + 1) % 10 == 0:
                    print(f"   {i + 1}/{self.num_users} tamamlandı")
        
        self.end_time = time.time()
        self.print_results("Gerçek Paralel Test")
    
    def print_results(self, test_name):
        # Test sonuçlarını yazdırıyorum
        duration = self.end_time - self.start_time
        throughput = self.num_users / duration
        
        print(f"\n📊 {test_name} Sonuçları:")
        print(f"   ⏱️  Toplam Süre: {duration:.2f} saniye")
        print(f"   👥 Toplam Kullanıcı: {self.num_users}")
        print(f"   ✅ Başarılı: {self.success_count}")
        print(f"   ❌ Hatalı: {self.error_count}")
        print(f"   🚀 Throughput: {throughput:.2f} oy/saniye")
        print(f"   📈 Ortalama Süre: {duration/self.num_users:.3f} saniye/oy")
        
        # Hata analizi
        if self.error_count > 0:
            error_types = {}
            for result in self.results:
                if result['status'] == 'error':
                    error_type = result['error']
                    error_types[error_type] = error_types.get(error_type, 0) + 1
            
            print(f"\n❌ Hata Analizi:")
            for error_type, count in error_types.items():
                print(f"   {error_type}: {count} kez")
        
        # Oy dağılımı
        vote_distribution = {0: 0, 1: 0, 2: 0}
        for result in self.results:
            if result['status'] == 'success':
                vote_distribution[result['vote_choice']] += 1
        
        print(f"\n🗳️ Oy Dağılımı:")
        print(f"   🔴 Kırmızı: {vote_distribution[0]} ({vote_distribution[0]/self.success_count*100:.1f}%)")
        print(f"   🔵 Mavi: {vote_distribution[1]} ({vote_distribution[1]/self.success_count*100:.1f}%)")
        print(f"   🟢 Yeşil: {vote_distribution[2]} ({vote_distribution[2]/self.success_count*100:.1f}%)")

def main():
    print("🧪 ZKP Oylama Sistemi Gerçek Stress Test")
    print("=" * 50)
    
    # Test parametreleri
    num_users = 100  # Gerçek test için daha az kullanıcı
    
    print(f"📋 Test Parametreleri:")
    print(f"   👥 Kullanıcı Sayısı: {num_users}")
    print(f"   🎯 Amaç: Gerçek sistem performansını ölçmek")
    print(f"   ⚠️  Not: Bu test gerçek hash doğrulaması ve çifte oy kontrolü yapar")
    
    # Oy kayıtlarını sıfırla
    print(f"\n🔄 Oy kayıtları sıfırlanıyor...")
    reset_votes()
    
    # Test başlat
    test = RealVotingStressTest(num_users)
    test.run_parallel_test(max_workers=10)
    
    print(f"\n✅ Gerçek stress test tamamlandı!")
    print(f"💡 Bu test gerçek sistem davranışını simüle eder")

if __name__ == "__main__":
    main()
