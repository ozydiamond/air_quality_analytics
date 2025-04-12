# Air Quality Dashboard ༄.°

## Deskripsi Proyek

Dashboard ini menyajikan visualisasi dan analisis data kualitas udara. Anda dapat menggunakan dashboard ini untuk memahami berbagai parameter kualitas udara dan trennya.

## Setup Environment

Anda dapat menyiapkan lingkungan pengembangan menggunakan Anaconda atau Shell/Terminal dengan `pipenv`.

### Setup Environment - Anaconda

Jika Anda menggunakan Anaconda, ikuti langkah-langkah berikut:

1.  **Buat lingkungan virtual:**
    ```bash
    conda create --name air-quality-env python=3.9
    ```
    (Disarankan menggunakan Python 3.9 untuk kompatibilitas yang lebih baik dengan library yang Anda gunakan.)

2.  **Aktifkan lingkungan virtual:**
    ```bash
    conda activate air-quality-env
    ```

3.  **Instal dependensi dari file `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```
    Pastikan file `requirements.txt` Anda berisi daftar library berikut:
    ```
    matplotlib==3.10.1
    missingno==0.5.2
    pandas==2.2.3
    plotly==6.0.1
    seaborn==0.13.2
    streamlit==1.39.0
    ```

### Setup Environment - Shell/Terminal

Jika Anda menggunakan Shell/Terminal dengan `pipenv`, ikuti langkah-langkah berikut:

1.  **Buat direktori proyek dan masuk ke dalamnya:**
    ```bash
    mkdir air_quality_dashboard
    cd air_quality_dashboard
    ```

2.  **Instal `pipenv` jika belum terinstal:**
    ```bash
    pip install pipenv
    ```

3.  **Buat lingkungan virtual dan instal dependensi:**
    ```bash
    pipenv install
    ```
    (Ini akan membuat `Pipfile` dan `Pipfile.lock` berdasarkan kebutuhan proyek Anda.)

4.  **Aktifkan shell `pipenv`:**
    ```bash
    pipenv shell
    ```

5.  **Instal dependensi dari file `requirements.txt` (opsional, jika Anda sudah memiliki file ini):**
    ```bash
    pip install -r requirements.txt
    ```
    Pastikan file `requirements.txt` Anda berisi daftar library berikut:
    ```
    matplotlib==3.10.1
    missingno==0.5.2
    pandas==2.2.3
    plotly==6.0.1
    seaborn==0.13.2
    streamlit==1.39.0
    ```
    (Jika Anda menggunakan `pipenv install` tanpa `-r requirements.txt`, `pipenv` akan mencoba mendeteksi dependensi dari kode Anda atau `Pipfile` jika ada.)

## Menjalankan Aplikasi Streamlit

Setelah lingkungan Anda disiapkan dan semua dependensi terinstal, Anda dapat menjalankan aplikasi Streamlit dengan perintah berikut:

```bash
streamlit run dashboard.py
