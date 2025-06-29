from google.colab import files  # dosya yükleme işlemi için

import numpy as np  # sayısal işlemler için
import matplotlib.pyplot as plt  # grafikleri çizmek için

uploaded = files.upload()  # txt dosyasını buradan seçtiriyorum
filename = list(uploaded.keys())[0]  # yüklenen dosyanın ismini al

with open(filename, encoding='latin1') as f:  # latin1 şart yoksa hata veriyor
    data = np.genfromtxt(f)  # txt'yi array'e çeviriyorum

# zaman ve emg sinyallerini ayrı ayrı alıyorum
time = data[:, 0]  # ilk sütun zaman
emg = data[:, 1]  # ikinci sütun sinyal değeri

# sinyali olduğu gibi çiziyorum
plt.figure(figsize=(12, 4))
plt.plot(time, emg, label='EMG Signal')
plt.title('Raw EMG Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()
plt.show()

# kayan pencere ile rms hesaplayan fonksiyon
def sliding_rms(signal, window_size, step_size):
    rms_values = []  # sonuçları buraya koyacağım
    for i in range(0, len(signal) - window_size, step_size):
        window = signal[i:i+window_size]  # pencereyi kes
        rms = np.sqrt(np.mean(window ** 2))  # rms formülü
        rms_values.append(rms)
    return np.array(rms_values)

# örnekleme frekansı – zaman farkından hesaplıyorum
fs = int(1 / (time[1] - time[0]))

# pencere 200ms, adım 100ms
window_size = int(0.2 * fs)
step_size = int(0.1 * fs)

# rms değerlerini hesaplıyorum
rms_values = sliding_rms(emg, window_size, step_size)

# rms grafiğini çiziyorum
plt.figure(figsize=(10, 4))
plt.plot(rms_values, label='RMS (Sliding Window)')
plt.title('RMS Feature Over Time')
plt.xlabel('Window Index')
plt.ylabel('RMS Amplitude')
plt.grid(True)
plt.legend()
plt.show()
