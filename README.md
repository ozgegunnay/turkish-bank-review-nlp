# turkish-bank-review-nlp

Turkce banka musteri yorumlarindan sikayet tespiti ve ilgili birime yonlendirme projesi (YTU Matematik Muhendisligi tasarim projesi / bitirme tezi).

## Asamalar
- [x] **Asama 1:** Google Play'den Akbank, DenizBank, Garanti BBVA, Halkbank ve Is Bankasi yorumlarinin toplanmasi
- [ ] App Store yorumlari
- [ ] Veri temizleme ve etiketleme
- [ ] BERTurk ile duygu / sikayet siniflandirma
- [ ] Sikayetleri ilgili birime yonlendirme
- [ ] Dashboard / web demo

## Kurulum
```bash
pip install -r requirements.txt
python src/scrape_playstore.py --count 2000
```
Ciktilar `data/raw/<banka>_playstore.csv` olarak kaydedilir (kolonlar: banka, kaynak, reviewId, tarih, puan, yorum, thumbsUpCount). Ham veri repoya yuklenmez.

## Proje yapisi
```
src/          veri toplama ve model kodlari
data/raw/     ham veri (git'e eklenmez)
notebooks/    analiz defterleri
```
