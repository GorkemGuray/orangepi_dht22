# Orange Pi Zero DHT22 Sıcaklık ve Nem Sensörü

Bu proje, Orange Pi Zero üzerinde DHT22 sıcaklık ve nem sensörünü kullanarak ölçüm yapmanızı sağlar.

## Gereksinimler

### Donanım
- Orange Pi Zero
- DHT22 (AM2302) sensör
- 3.3V güç kaynağı (Orange Pi'den sağlanıyor)
- 4.7K - 10K pull-up direnci (opsiyonel, kod içinde yazılımsal pull-up kullanılıyor)

### Bağlantı Şeması
```
DHT22 Sensör     Orange Pi Zero
-------------    --------------
VCC (pin 1)  ->  3.3V
DATA (pin 2) ->  PA6 (default)
GND (pin 4)  ->  GND
```

### Yazılım Gereksinimleri
- Python 3.7+
- pyA20 kütüphanesi

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullanici_adi/orangepi_dht22.git
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

## Kullanım

1. Programı çalıştırın:
```bash
sudo $(which python3) src/example.py
```

2. Çıktı örneği:
```
2024-01-01 12:00:01 - INFO - Sıcaklık: 25.6°C, Nem: 45.2%
```

## Özellikler
- DHT22 sensör desteği (DHT11 için de uyumlu)
- Otomatik hata yakalama ve yeniden deneme mekanizması
- Detaylı loglama
- GPIO pin temizleme
- Modüler yapı

## Pin Değiştirme
Varsayılan olarak PA6 pini kullanılmaktadır. Farklı bir pin kullanmak için `example.py` dosyasındaki `PIN` değişkenini değiştirin:

```python
PIN = port.PA6  # Başka bir pin için değiştirin, örn: port.PA7
```

## Sorun Giderme

### Sık Karşılaşılan Hatalar

1. "Permission denied" hatası:
   - Programı `sudo` ile çalıştırın

2. "No module named 'pyA20'" hatası:
   - Virtual environment'ın aktif olduğundan emin olun
   - requirements.txt dosyasındaki kütüphaneleri yükleyin

3. Sensör okuma hataları:
   - Kablo bağlantılarını kontrol edin
   - Pull-up direncinin bağlı olduğundan emin olun
   - Sensör ve Orange Pi arasındaki mesafenin çok uzun olmadığından emin olun

## Krediler

Bu proje aşağıdaki açık kaynak projeleri temel almaktadır:

- [DHT11-DHT22-Python-library-Orange-PI](https://github.com/jingl3s/DHT11-DHT22-Python-library-Orange-PI) - DHT sensör okuma implementasyonu için temel alınmıştır.
- [pyA20](https://github.com/LinhDNguyen/orangepi_zero_gpio) - Orange Pi Zero GPIO kontrolü için kullanılmıştır.

## Lisans
MIT License

## Katkıda Bulunma
1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Açıklama'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun
