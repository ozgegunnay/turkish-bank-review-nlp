"""Google Play'den Turk banka uygulamasi yorumlarini toplar.

Kullanim:
    python src/scrape_playstore.py            # her banka icin 2000 yorum
    python src/scrape_playstore.py --count 500
"""
import argparse
from pathlib import Path

import pandas as pd
from google_play_scraper import Sort, app, reviews, search

# Uygulama ID'leri. Biri hata verirse script banka adiyla arayip bulmaya calisir.
BANKS = {
    "akbank": ("com.akbank.android.apps.akbank_direkt", "Akbank"),
    "denizbank": ("com.denizbank.mobildeniz", "MobilDeniz DenizBank"),
    "garanti_bbva": ("com.garanti.cepsubesi", "Garanti BBVA Mobil"),
    "halkbank": ("com.tmobtech.halkbank", "Halkbank Mobil"),
    "isbankasi": ("com.pozitron.iscep", "IsCep Is Bankasi"),
}

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def resolve_app_id(app_id: str, query: str) -> str:
    try:
        app(app_id, lang="tr", country="tr")
        return app_id
    except Exception:
        results = search(query, lang="tr", country="tr", n_hits=1)
        if not results:
            raise ValueError(f"Uygulama bulunamadi: {query}")
        print(f"  ! {app_id} bulunamadi, '{results[0]['title']}' kullaniliyor")
        return results[0]["appId"]


def scrape_bank(key: str, app_id: str, query: str, count: int) -> pd.DataFrame:
    app_id = resolve_app_id(app_id, query)
    result, _ = reviews(app_id, lang="tr", country="tr", sort=Sort.NEWEST, count=count)
    df = pd.DataFrame(result)
    if df.empty:
        return df
    df = df.rename(columns={"at": "tarih", "score": "puan", "content": "yorum"})
    df["banka"] = key
    df["kaynak"] = "google_play"
    return df[["banka", "kaynak", "reviewId", "tarih", "puan", "yorum", "thumbsUpCount"]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=2000, help="Banka basina yorum sayisi")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for key, (app_id, query) in BANKS.items():
        print(f"{key}: yorumlar cekiliyor...")
        df = scrape_bank(key, app_id, query, args.count)
        df = df.drop_duplicates(subset="reviewId")
        path = OUT_DIR / f"{key}_playstore.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  {len(df)} yorum -> {path.name}")


if __name__ == "__main__":
    main()
