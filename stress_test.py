import time
import json
import random
from concurrent.futures import ThreadPoolExecutor
import threading
from hash_utils import is_valid_person

class VotingStressTest:
    def __init__(self, num_users=1000):
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
    
    def simulate_vote(self, user_id):
        # Tek bir oy verme işlemini simüle ediyorum
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
            
            # Çifte oy kontrolü (basit simülasyon)
            # Gerçek sistemde voted_tc_tracker.py kullanılır
            
            # Oy verme işlemi simülasyonu
            # Gerçek sistemde smart contract çağrısı yapılır
            time.sleep(0.1)  # Simüle edilmiş işlem süresi
            
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
    
    def run_sequential_test(self):
        # Sıralı test yapıyorum (tek thread)
        print(f"🔄 Sıralı Test Başlatılıyor ({self.num_users} kullanıcı)")
        self.start_time = time.time()
        
        for i in range(self.num_users):
            result = self.simulate_vote(i)
            self.results.append(result)
            
            if (i + 1) % 100 == 0:
                print(f"   {i + 1}/{self.num_users} tamamlandı")
        
        self.end_time = time.time()
        self.print_results("Sıralı Test")
    
    def run_parallel_test(self, max_workers=50):
        # Paralel test yapıyorum (çoklu thread)
        print(f"🔄 Paralel Test Başlatılıyor ({self.num_users} kullanıcı, {max_workers} thread)")
        self.start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.simulate_vote, i) for i in range(self.num_users)]
            
            for i, future in enumerate(futures):
                result = future.result()
                self.results.append(result)
                
                if (i + 1) % 100 == 0:
                    print(f"   {i + 1}/{self.num_users} tamamlandı")
        
        self.end_time = time.time()
        self.print_results("Paralel Test")
    
    def run_concurrent_test(self, batch_size=100):
        # Eşzamanlı test yapıyorum (batch processing)
        print(f"🔄 Eşzamanlı Test Başlatılıyor ({self.num_users} kullanıcı, {batch_size} batch)")
        self.start_time = time.time()
        
        # Batch'ler halinde işle
        for batch_start in range(0, self.num_users, batch_size):
            batch_end = min(batch_start + batch_size, self.num_users)
            batch_users = list(range(batch_start, batch_end))
            
            # Batch içinde paralel işle
            with ThreadPoolExecutor(max_workers=min(20, len(batch_users))) as executor:
                futures = [executor.submit(self.simulate_vote, user_id) for user_id in batch_users]
                
                for future in futures:
                    result = future.result()
                    self.results.append(result)
            
            print(f"   Batch {batch_start//batch_size + 1}: {batch_end}/{self.num_users} tamamlandı")
        
        self.end_time = time.time()
        self.print_results("Eşzamanlı Test")
    
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
    
    def reset(self):
        # Test sonuçlarını sıfırlıyorum
        self.results = []
        self.success_count = 0
        self.error_count = 0
        self.start_time = None
        self.end_time = None

def main():
    print("🧪 ZKP Oylama Sistemi Stress Test")
    print("=" * 50)
    
    # Test parametreleri
    num_users = 1000
    test = VotingStressTest(num_users)
    
    print(f"📋 Test Parametreleri:")
    print(f"   👥 Kullanıcı Sayısı: {num_users}")
    print(f"   🎯 Amaç: Sistem performansını ölçmek")
    print(f"   ⚠️  Not: Bu test simülasyondur, gerçek blockchain işlemleri yapılmaz")
    
    # Test seçenekleri
    print(f"\n🔧 Test Seçenekleri:")
    print(f"   1. Sıralı Test (tek thread)")
    print(f"   2. Paralel Test (50 thread)")
    print(f"   3. Eşzamanlı Test (batch processing)")
    print(f"   4. Tüm Testler")
    
    # Otomatik olarak tüm testleri çalıştır
    choice = "4"
    
    if choice == "1":
        test.run_sequential_test()
    elif choice == "2":
        test.run_parallel_test()
    elif choice == "3":
        test.run_concurrent_test()
    elif choice == "4":
        print("\n🔄 Tüm testler çalıştırılıyor...")
        
        # Sıralı test
        test.run_sequential_test()
        test.reset()
        
        # Paralel test
        test.run_parallel_test()
        test.reset()
        
        # Eşzamanlı test
        test.run_concurrent_test()
    else:
        print("❌ Geçersiz seçim!")
        return
    
    print(f"\n✅ Stress test tamamlandı!")
    print(f"💡 Gerçek sistemde blockchain işlemleri daha yavaş olabilir")

if __name__ == "__main__":
    main()
