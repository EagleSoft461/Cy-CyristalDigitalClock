import tkinter as tk
from time import strftime, sleep
from tkinter import messagebox
from threading import Thread
import winsound
import itertools

# Pencereyi oluştur
root = tk.Tk()
root.title("CyCyristal DigitalClock")
root.geometry("600x300")
root.configure(bg="black")

# Saat ve tarih etiketleri
saat_label = tk.Label(root, font=("Arial", 80), bg="black", fg="cyan")
saat_label.pack(anchor='center')
tarih_label = tk.Label(root, font=("Arial", 30), bg="black", fg="white")
tarih_label.pack(anchor='center')

# Tema renkleri
tema_renkleri = [
    ("darkblue", "black"),
    ("darkgreen", "black"),
    ("darkred", "white"),
    ("purple", "white"),
    ("orange", "black")
]
tema_index = itertools.cycle(range(len(tema_renkleri)))

# Font listesi
fontlar = ["Arial", "Consolas", "Courier", "Times New Roman", "Comic Sans MS"]
font_index = itertools.cycle(range(len(fontlar)))

# Tema değiştir
def tema_degistir():
    i = next(tema_index)
    saat_label.config(fg=tema_renkleri[i][0], bg=root["bg"])
    tarih_label.config(fg=tema_renkleri[i][1], bg=root["bg"])

# Font değiştir
def font_degistir():
    i = next(font_index)
    yeni_font = fontlar[i]
    saat_label.config(font=(yeni_font, 80))
    tarih_label.config(font=(yeni_font, 30))

# Renkler (açık pastel tonlar)
arka_plan_renkleri = ["#C18AEE", "#5231AF", "#3324B4", "#2356B4", "#7946CA", "#6417B6", "#DFBCFF"]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

# Yumuşak geçiş animasyonu
def arka_plan_animasyonu():
    while True:
        for i in range(len(arka_plan_renkleri)):
            start = hex_to_rgb(arka_plan_renkleri[i])
            end = hex_to_rgb(arka_plan_renkleri[(i+1) % len(arka_plan_renkleri)])
            steps = 50
            for s in range(steps):
                r = int(start[0] + (end[0]-start[0]) * s/steps)
                g = int(start[1] + (end[1]-start[1]) * s/steps)
                b = int(start[2] + (end[2]-start[2]) * s/steps)
                renk = rgb_to_hex((r, g, b))
                root.configure(bg=renk)
                saat_label.config(bg=renk)
                tarih_label.config(bg=renk)
                alarm_button.config(bg=renk)
                tema_button.config(bg=renk)
                font_button.config(bg=renk)
                root.update()
                sleep(0.05)

# Alarm ikon butonu
def alarm_ayarla():
    def set_alarm():
        alarm_time = alarm_entry.get()
        if alarm_time:
            t = Thread(target=alarm_kontrol, args=(alarm_time,), daemon=True)
            t.start()
            messagebox.showinfo("Bilgi", f"Alarm ayarlandı: {alarm_time}")
        alarm_window.destroy()

    alarm_window = tk.Toplevel(root)
    alarm_window.title("Alarm Ayarla")
    tk.Label(alarm_window, text="Alarm Saati (HH:MM:SS):", font=("Arial",12)).pack(padx=10, pady=10)
    alarm_entry = tk.Entry(alarm_window, font=("Arial",12))
    alarm_entry.pack(padx=10, pady=5)
    tk.Button(alarm_window, text="Ayarla", command=set_alarm).pack(pady=10)

alarm_button = tk.Button(root, text="⏰", font=("Arial", 30), bg="white", fg="red", command=alarm_ayarla)
alarm_button.pack(pady=5)

# Tema ve font değiştirme butonları
tema_button = tk.Button(root, text="🎨 Tema Değiştir", font=("Arial", 14), command=tema_degistir)
tema_button.pack(pady=5)

font_button = tk.Button(root, text="🔤 Font Değiştir", font=("Arial", 14), command=font_degistir)
font_button.pack(pady=5)

# Alarm kontrol fonksiyonu (buzzer ile)
def alarm_kontrol(alarm_time):
    while True:
        current_time = strftime('%H:%M:%S')
        if current_time == alarm_time:
            for _ in range(5):
                winsound.Beep(1200, 500)  # daha tiz beep
                sleep(0.2)
            animasyon()
            messagebox.showinfo("Alarm!", f"Alarm zamanı: {alarm_time}")
            break
        sleep(1)

# Animasyon fonksiyonu (alarm çalarken)
def animasyon():
    for _ in range(6):
        saat_label.config(fg="red")
        root.update()
        sleep(0.3)
        saat_label.config(fg="darkblue")
        root.update()
        sleep(0.3)

# Saat ve tarih güncelleme
def zaman():
    saat = strftime('%H:%M:%S')
    tarih = strftime('%d/%m/%Y %A')
    saat_label.config(text=saat)
    tarih_label.config(text=tarih)
    root.after(1000, zaman)

# Arka plan animasyonunu ayrı thread'te çalıştır
Thread(target=arka_plan_animasyonu, daemon=True).start()

zaman()
root.mainloop()