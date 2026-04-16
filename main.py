import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def run_sitemap_robot():
    try:
        # 1. Mengambil data JSON dari Secrets GitHub
        if 'GOOGLE_SERVICE_ACCOUNT_JSON' not in os.environ:
            print("❌ Error: Secret GOOGLE_SERVICE_ACCOUNT_JSON belum diisi di Settings!")
            return
            
        service_account_info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'])
        
        # Ambil URL dari secret, jika tidak ada pakai default domain Anda
        site_url = os.environ.get('SITE_URL', 'https://royal-visa88-uk.vercel.app/')

        # 2. Autentikasi ke Google Search Console API
        scopes = ['https://www.googleapis.com/auth/webmasters.readonly']
        creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=scopes)
        service = build('searchconsole', 'v1', credentials=creds)

        # 3. Memanggil API untuk mengecek daftar sitemap
        results = service.sitemaps().list(siteUrl=site_url).execute()
        
        print(f"--- LAPORAN ROBOT SEO ---")
        print(f"🌐 Website: {site_url}\n")

        if 'sitemap' in results:
            for smap in results['sitemap']:
                path = smap.get('path', 'N/A')
                last_mod = smap.get('lastSubmitted', 'N/A')
                errors = smap.get('errors', '0')
                
                # Cek apakah ada error
                status = "✅ AMAN (Sitemap terbaca)" if int(errors) == 0 else f"⚠️ ERROR ({errors} Masalah)"
                
                print(f"📍 Path: {path}")
                print(f"📊 Status: {status}")
                print(f"📅 Terakhir Update: {last_mod}")
                print("-" * 30)
        else:
            print("⚠️ Tidak ada sitemap yang terdaftar di Search Console untuk domain ini.")
            
    except Exception as e:
        print(f"❌ Terjadi Kesalahan: {str(e)}")
        print("\nTips: Pastikan email Service Account sudah di-invite di Search Console!")

if __name__ == "__main__":
    run_sitemap_robot()
