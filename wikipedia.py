import requests
from bs4 import BeautifulSoup
import csv

# Daftar URL yang ingin di-scrape beserta penyesuaian masing-masing
urls = [
    {
        'url': 'https://id.wikipedia.org/wiki/Daftar_perguruan_tinggi_swasta_di_Indonesia',
        'columns': [0, 4, 3]  # Kolom untuk Nama, Lokasi, Tahun Berdiri
    },
    {
        'url': 'https://id.wikipedia.org/wiki/Daftar_perguruan_tinggi_negeri_di_Indonesia',
        'columns': [2, 5, 4]  # Kolom untuk Nama, Lokasi, Tahun Berdiri
    },
    {
        'url': 'https://id.wikipedia.org/wiki/Daftar_perguruan_tinggi_kementerian_dan_lembaga_di_Indonesia',
        'columns': [2, 6, 4]  # Kolom untuk Nama, Lokasi, Tahun Berdiri (penyesuaian)
    },
    {
        'url': 'https://id.wikipedia.org/wiki/Daftar_perguruan_tinggi_keagamaan_negeri_di_Indonesia',
        'columns': [2, 5, 4]  # Kolom untuk Nama, Lokasi, Tahun Berdiri (penyesuaian)
    },
    {
        'url': 'https://id.wikipedia.org/wiki/Daftar_politeknik_negeri_di_Indonesia',
        'columns': [0, 2, 3]  # Kolom untuk Nama, Lokasi, Tahun Berdiri (penyesuaian)
    }
]

# Membuka file CSV untuk menulis data
with open('universities_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Nama Perguruan Tinggi', 'Lokasi', 'Tahun Berdiri']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Menulis header ke file CSV
    writer.writeheader()

    for site in urls:
        url = site['url']
        columns = site['columns']
        
        try:
            # Mengambil konten dari URL
            response = requests.get(url)
            response.raise_for_status()  # Memastikan permintaan berhasil
            
            # Menggunakan BeautifulSoup untuk parsing HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Mengambil semua tabel dengan class 'wikitable'
            tables = soup.find_all('table', {'class': 'wikitable'})
            
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Lewati header
                    cols = row.find_all('td')
                    if len(cols) >= max(columns):  # Pastikan ada cukup kolom sesuai kolom yang diinginkan
                        nama_perguruan_tinggi = cols[columns[0]].get_text(strip=True)
                        lokasi = cols[columns[1]].get_text(strip=True) if len(cols) > columns[1] else 'N/A'
                        tahun_berdiri = cols[columns[2]].get_text(strip=True) if len(cols) > columns[2] else 'N/A'
                        
                        # Menulis data ke file CSV
                        writer.writerow({
                            'Nama Perguruan Tinggi': nama_perguruan_tinggi,
                            'Lokasi': lokasi,
                            'Tahun Berdiri': tahun_berdiri
                        })
        
        except Exception as e:
            print(f"Error scraping {url}: {e}")

print("Data berhasil disimpan ke universities_data.csv")
