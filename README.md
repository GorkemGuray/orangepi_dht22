# Orange Pi Zero DHT22 Ortam İzleme Sistemi

Bu proje, Orange Pi Zero (H2+) ve DHT22 sensörü kullanarak bir ortamın sıcaklık ve nem değerlerini sürekli izlemeyi ve dakikalık ortalama değerler sunmayı amaçlar.

## Proje Amacı ve Özellikleri

### Ana Özellikler
- Ortam sıcaklık ve nem değerlerinin dakikalık ortalamasını ölçme
- Anlık değişimlerden etkilenmeyen kararlı ölçüm
- Hata toleranslı veri toplama
- Otomatik veri düzeltme ve filtreleme

### Çalışma Prensibi
- Sensörden saniyede bir veri okunur
- Son 60 saniyenin verileri saklanır
- Her dakika başında ortalama değerler hesaplanır
- Anlık değişimler ve okuma hataları filtrelenir

## Donanım Gereksinimleri

### Gerekli Bileşenler
- Orange Pi Zero (h2+)
- DHT22 (AM2301) sıcaklık ve nem sensörü
- 3.3V güç kaynağı (Orange Pi'den sağlanıyor)
- 4.7K - 10K pull-up direnci (opsiyonel)

### Bağlantı Şeması
```
DHT22 Sensör     Orange Pi Zero
-------------    --------------
VCC (pin 1)  ->  3.3V
DATA (pin 2) ->  PA6 (default)
GND (pin 4)  ->  GND
```

## Yazılım Kurulumu

### Ön Gereksinimler
- Python 3.7 veya üzeri
- pip3
- venv modülü
- MQTT broker hesabı (HiveMQ Cloud önerilir)

### Kurulum Adımları

1. Projeyi klonlayın:
```bash
git clone https://github.com/GorkemGuray/orangepi_dht22.git
cd orangepi_dht22
```

2. Virtual environment oluşturun:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Gerekli kütüphaneleri yükleyin:
```bash
pip3 install -r requirements.txt
```

4. Yapılandırma dosyasını oluşturun:
```bash
cp .env.example .env
```

5. `.env` dosyasını MQTT bilgilerinizle güncelleyin:
```properties
MQTT_BROKER=your.broker.address
MQTT_PORT=8883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_password
```

### Paket Olarak Kurulum

Projeyi bir Python paketi olarak kurmak için:

```bash
pip install -e .
```

Bu kurulum sonrasında `dht22_monitor` komutu ile programı doğrudan çalıştırabilirsiniz:

```bash
sudo dht22_monitor
```

## Kullanım

### MQTT Entegrasyonu
- Veriler MQTT broker'a dakikalık olarak gönderilir
- Veri iletimi için QoS 1 kullanılır (en az bir kez iletim garantisi)
- SSL/TLS ile güvenli bağlantı kullanılır
- Her cihaz için benzersiz client ID kullanılır
- Cihaz durumu (online/offline) otomatik olarak izlenir

#### MQTT Topic Yapısı
- Sıcaklık verileri: `sensors/dht22/temperature`
- Nem verileri: `sensors/dht22/humidity`
- Cihaz durumu: `sensors/dht22/status`

#### Örnek MQTT Mesajları
```json
// Temperature topic (sensors/dht22/temperature)
{
    "value": 25.6,
    "unit": "C",
    "timestamp": "2024-01-01T12:00:00Z"
}

// Humidity topic (sensors/dht22/humidity)
{
    "value": 45.2,
    "unit": "%",
    "timestamp": "2024-01-01T12:00:00Z"
}

// Status topic (sensors/dht22/status)
{
    "status": "online",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

#### Cihaz Durumu İzleme
- Program başladığında "online" mesajı yayınlanır
- Program normal kapatıldığında veya çöktüğünde "offline" mesajı yayınlanır
- Status mesajları `retain` flag'i ile saklanır
- Beklenmeyen bağlantı kopmaları otomatik olarak yeniden bağlanır

### Programı Çalıştırma
```bash
# Doğrudan script olarak
sudo $(which python3) src/monitor.py

# veya paket kurulumu yapıldıysa
sudo dht22_monitor
```

### Örnek Çıktı
```
2024-01-01 12:00:00 - INFO - 1 Dakikalık Ortalama - Sıcaklık: 25.6°C, Nem: 45.2%
2024-01-01 12:01:00 - INFO - 1 Dakikalık Ortalama - Sıcaklık: 25.7°C, Nem: 45.3%
```

### Veri Yorumlama
- Her satır bir dakikalık ortalama değeri gösterir
- Değerler son 60 saniyenin ortalamasıdır
- Anlık değişimler ve gürültüler filtrelenmiştir
- Hata durumlarında son geçerli değerler kullanılır

### Veri Güvenilirliği
- Sensör okuma hataları durumunda son geçerli değer kullanılır
- Önbellek sistemi ile gereksiz okumalar engellenir
- Deque veri yapısı ile verimli hafıza kullanımı sağlanır
- İstatistiksel hesaplamalar ile gürültü filtrelenir

## Yapılandırma

### Örnek Yapılandırma Parametreleri
```python
dht22_reader = DHT22Reader(
    gpio_pin=PIN,
    max_retries=2,     # Okuma başarısız olursa deneme sayısı
    retry_delay=0.1,   # Denemeler arası bekleme süresi
    cache_time=1       # Önbellek süresi (saniye)
)
```

### Zaman Aralıkları
- Veri okuma sıklığı: 1 saniye
- Ortalama hesaplama süresi: 60 saniye
- Önbellek yenileme süresi: 1 saniye

## Sorun Giderme

### Sık Karşılaşılan Sorunlar

1. Veri Okunamıyor:
   - Kablo bağlantılarını kontrol edin
   - Sensör güç kaynağını kontrol edin
   - GPIO pin numarasını doğrulayın

2. Yüksek Hata Oranı:
   - Kablo uzunluğunu kontrol edin
   - Elektromanyetik girişim kaynaklarını uzaklaştırın
   - Pull-up direnci kullanmayı deneyin

3. Tutarsız Değerler:
   - Havalandırmayı kontrol edin
   - Sensörü direkt güneş ışığından koruyun
   - Sensörü ısı kaynaklarından uzak tutun

4. MQTT Bağlantı Sorunları:
   - `.env` dosyasındaki broker bilgilerini kontrol edin
   - Bağlantı hatası kodlarını kontrol edin:
     * 1: Protokol versiyonu uyumsuzluğu
     * 2: Geçersiz client identifier
     * 3: Broker kullanılamıyor
     * 4: Hatalı kullanıcı adı veya şifre
     * 5: Yetkilendirme hatası
   - SSL/TLS sertifikalarının güncel olduğunu kontrol edin
   - Internet bağlantınızı kontrol edin
   - Broker'ın aktif olduğunu kontrol edin

### Yapılandırma Detayları

#### MQTT Yapılandırması
`.env` dosyası aşağıdaki formatta olmalıdır:
```properties
MQTT_BROKER=your.broker.address
MQTT_PORT=8883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_password
```

Not: Port 8883, SSL/TLS kullanılan MQTT bağlantıları için standart porttur.

## Krediler

Bu proje aşağıdaki açık kaynak projeleri temel almaktadır:

- [DHT11-DHT22-Python-library-Orange-PI](https://github.com/jingl3s/DHT11-DHT22-Python-library-Orange-PI) - DHT sensör okuma implementasyonu için temel alınmıştır.
- [pyA20](https://github.com/LinhDNguyen/orangepi_zero_gpio) - Orange Pi Zero GPIO kontrolü için kullanılmıştır.

## Lisans
MIT License
