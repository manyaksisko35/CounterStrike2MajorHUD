# CS2 Major Style Custom HUD 🎮

Bu proje, Counter-Strike 2 için Python ve Web teknolojileri kullanılarak geliştirilmiş profesyonel bir e-spor yayın arayüzüdür (HUD). 

## ✨ Özellikler
- **Dinamik Takım Panelleri:** Canlı HP, para, silah ve bomba durumu takibi.
- **Aktif Oyuncu Kamerası:** İzlediğiniz oyuncunun mermi, can ve istatistiklerini gösteren alt panel.
- **Akıllı Killfeed:** Python verisiyle senkronize çalışan özel ölüm bildirimleri[cite: 2].
- **Bomba Takibi:** Bomba kurulduğunda devreye giren özel zamanlayıcı[cite: 2].

## 🛠️ Kurulum

1. **GSI Dosyasını Atın:** 
   `gamestate_integration_manyaksisko.cfg` dosyasını `...\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg` klasörüne kopyalayın.

2. **Gerekli Kütüphaneleri İndirin:**
    Projeyi çalıştırmadan önce terminale şunu yazın: pip install -r requirements.txt

3. **Python Sunucusunu Çalıştırın:**
   Terminali açın ve sunucuyu başlatın:
   ```bash
   python app.py
