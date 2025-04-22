# UTS-IoT
Tugas Ujian Tengah Semester IF4051 - Pengembangan Sistem IoT menugaskan mahasiswa untuk mengembangkan sistem sederhana untuk mengirimkan gambar dari ESP board ke sebuah dashboard melalui MQTT dan database

![Screenshot from 2025-04-22 22-00-44](https://github.com/user-attachments/assets/a85ed229-e566-4f09-9908-d40fba262fed)

## Table of Contents
- [Configuration](#configuration)
- [Usage](#usage)

## Configuration
1. Buat sebuah berkas konfigurasi `.env` pada folder utama dengan isi sesuai [`.env.example`](https://github.com/Marthenn/UTS-IoT/blob/main/.env.example)
2. Isi konfigurasi pada `.env` dan `esp32/secrets.h`
3. Install seluruh package python yang diperlukan sesuai dengan requirements.txt `pip install -r requirements.txt`

## Usage
1. Upload projek Arduino pada folder [`esp32`](https://github.com/Marthenn/UTS-IoT/tree/main/esp32)
2. Pastikan ESP32 berhasil terkoneksi dengan MQTT Broker dan NTP telah tersinkronisasi
3. Jalankan dashboard `python3 app.py`
