# Dico Bike Sharing Analytics🚲

### Deskripsi :
Merupakan layanan jasa penyewaan sepeda yang berada diseluruh kota US. Dico Bike ini akan menganalisa data penyewaan sepeda di tahun 2011 & 2012. 

### Tujuan :
Tujuan ini menganalisa berdasarkan:   
 - Trend jumlah penyewaan sepeda berdasarkan bulanan
 - Kondisi penggunaan sepeda yang disebabkan faktor iklim
 - Analisa penyewaan harian yang berdasarkan hari dan waktu penyewaan sepeda melonjak padat
Analisa ini menggunakan metode *Clustering Analytics*.Pada analisa ini akan mengelompokkan trend bulanan dan jadwal penggunaan berdasarkan pengguna casual(Biasa) & registered(Member)

# Running Dashboard✨

### 1. Setup Enviroment - Command Prompt / Powershell
```
mkdir projek_analisis
cd projek_analisis
-- clone file optional,your can downloading from repo
git clone https://github.com/GadiseMustika/bikesharing_analytic.git
python -m venv .venv
.\.venv\Scripts\activate # active .venv
```
### 2. Install Libary 
```
pip install numpy
pip install matplotlib
pip install seaborn
pip install pip freeze or pip install pip reqs
pip install streamlit
```
### 3 Making Requirement
```
pip freeze > requirement.txt
-- or --

pipreqs . --force
```


