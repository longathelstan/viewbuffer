import os
try:
    import requests, colorama, prettytable
except:
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install prettytable")
import threading, requests, ctypes, random, json, time, base64, sys, re
from prettytable import PrettyTable
import random
from time import strftime
from colorama import init, Fore, Style
from urllib.parse import urlparse, unquote, quote
from string import ascii_letters, digits

# Color setup
init(autoreset=True)
xnhac = Fore.CYAN
do = Fore.RED
luc = Fore.GREEN
vang = Fore.YELLOW
xduong = Fore.BLUE
hong = Fore.MAGENTA
trang = Fore.WHITE
whiteb = Fore.WHITE + Style.BRIGHT
red = Fore.RED + Style.NORMAL
redb = Fore.RED + Style.BRIGHT
end = Style.RESET_ALL

# Marking
edit = f"{vang}]{trang}[{do}[⟨⟩]{trang}]{vang}[{trang} ➩ {luc}"
edit1 = f"{trang}[{do}[⟨⟩]{trang}]{trang} ➩ {luc}"
os.system("cls" if os.name == "nt" else "clear")

# Banner
banner = f"""
{xduong}Tool Tiktok
"""
for X in banner:
    sys.stdout.write(X)
    sys.stdout.flush() 

print(f"{xduong}{'⏦'*50}{end}")

class Zefoy:
    def __init__(self):
        self.base_url = 'https://zefoy.com/'
        self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
        self.session = requests.Session()
        self.captcha_1 = None
        self.captcha_ = {}
        self.service = 'Views'
        self.video_key = None
        self.services = {}
        self.services_ids = {}
        self.services_status = {}
        self.url = 'None'
        self.text = 'VIEWTIKTOK'
        url1 = input(f"{luc}Nhập {vang}Link {xnhac}Video: {luc}")
        self.url = url1

    def get_captcha(self):
        if os.path.exists('session'): self.session.cookies.set("PHPSESSID", open('session',encoding='utf-8').read(), domain='zefoy.com')
        request = self.session.get(self.base_url, headers=self.headers)
        if 'Enter Video URL' in request.text: self.video_key = request.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]; return True

        try:
            for x in re.findall(r'<input type="hidden" name="(.*)" value="(.*)">', request.text): self.captcha_[x[0]] = x[1]

            self.captcha_1 = request.text.split('type="text" name="')[1].split('" oninput="this.value=this.value.toLowerCase()"')[0]
            captcha_url = request.text.split('<img src="')[1].split('" onerror="imgOnError()" class="')[0]
            request = self.session.get(f"{self.base_url}{captcha_url}", headers=self.headers)
            open('captcha.png', 'wb').write(request.content)
            print('Đang giải capcha..')
            return False
        except Exception as e:
            print(f"Không thể giải captcha: {e}")
            time.sleep(2)
            self.get_captcha()

    def send_captcha(self, new_session=False):
        if new_session: 
            self.session = requests.Session()
            os.remove('session')
            time.sleep(2)
        if self.get_captcha(): 
            print('Đang kêt nối đến session')
            return (True, 'The session already exists')
        captcha_solve = self.solve_captcha('captcha.png')[1]
        self.captcha_[self.captcha_1] = captcha_solve
        request = self.session.post(self.base_url, headers=self.headers, data=self.captcha_)

        if 'Enter Video URL' in request.text: 
            print('Session đã được tạo')
            open('session', 'w', encoding='utf-8').write(self.session.cookies.get('PHPSESSID'))
            print(f"Giải capcha thành công: {captcha_solve}")
            self.video_key = request.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            return (True, captcha_solve)
        else: 
            return (False, captcha_solve)

    def solve_captcha(self, path_to_file=None, b64=None, delete_tag=['\n', '\r']):
        task = path_to_file if path_to_file else 'temp.png'
        if not path_to_file:
            open(task, 'wb').write(base64.b64decode(b64))
        request = self.session.post('https://api.ocr.space/parse/image?K87899142388957', headers={'apikey':'K87899142388957'}, files={'task':open(task,'rb')}).json()
        solved_text = request['ParsedResults'][0]['ParsedText']
        for x in delete_tag: 
            solved_text = solved_text.replace(x, '')
        return (True, solved_text)

    def get_status_services(self):
        request = self.session.get(self.base_url, headers=self.headers).text
        for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+\n.+', request): 
            self.services[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = x.split('d-sm-inline-block">')[1].split('</small>')[0].strip()
        for x in re.findall(r'<h5 class="card-title mb-3">.+</h5>\n<form action=".+">', request): 
            self.services_ids[x.split('title mb-3">')[1].split('<')[0].strip()] = x.split('<form action="')[1].split('">')[0].strip()
        for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+<button .+', request): 
            self.services_status[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = False if 'disabled class' in x else True
        return (self.services, self.services_status)

    def get_table(self, i=1):
        table = PrettyTable(field_names=["ID", "DỊCH VỤ", "Status"], title="Status Services", header_style="upper", border=True)
        while True:
            if len(self.get_status_services()[0]) > 1:
                break
            else:
                print('Cant get services, retrying...')
                self.send_captcha()
                time.sleep(2)
        for service in self.services:
            table.add_row([f"{Fore.CYAN}{i}{Fore.RESET}", service, f"{Fore.GREEN if 'ago updated' in self.services[service] else Fore.RED}{self.services[service]}{Fore.RESET}"])
            i += 1
        table.title = f"{Fore.YELLOW}Số Dịch Vụ Hoạt Động: {len([x for x in self.services_status if self.services_status[x]])}{Fore.RESET}"
        print(table)

    def find_video(self):
        if self.service is None: 
            return (False, "You didn't choose the service")
        while True:
            if self.service not in self.services_ids: 
                self.get_status_services()
                time.sleep(1)
            request = self.session.post(f'{self.base_url}{self.services_ids[self.service]}', headers={'content-type':'multipart/form-data; boundary=----WebKitFormBoundary0nU8PjANC8BhQgjZ', 'user-agent':self.headers['user-agent'], 'origin':'https://zefoy.com'}, data=f'------WebKitFormBoundary0nU8PjANC8BhQgjZ\r\nContent-Disposition: form-data; name="{self.video_key}"\r\n\r\n{self.url}\r\n------WebKitFormBoundary0nU8PjANC8BhQgjZ--\r\n')
            try: 
                self.video_info = base64.b64decode(unquote(request.text.encode()[::-1])).decode()
            except: 
                time.sleep(3)
                continue
            if 'Session expired. Please re-login' in self.video_info:
                print('Phiên hết hạn. Đang đăng nhập lại...')
                self.send_captcha()
                return
            elif 'service is currently not working' in self.video_info:
                return (True, 'Dịch vụ hiện không hoạt động, hãy thử lại sau.')
            elif """onsubmit="showHideElements""" in self.video_info:
                self.video_info = [self.video_info.split('" name="')[1].split('"')[0], self.video_info.split('value="')[1].split('"')[0]]
                return (True, request.text)
            elif 'Checking Timer...' in self.video_info:
                try: 
                    t = int(re.findall(r'ltm=(\d*);', self.video_info)[0])
                    zyfoy = int(re.findall(r'ltm=(\d*)"', self.video_info)[0])
                    while True:
                        if t == 0:
                            return self.find_video()
                        print(f'Thời gian làm mới {zyfoy} giây...')
                        time.sleep(zyfoy)
                        t -= zyfoy
                except Exception as e:
                    print(f'Có lỗi xảy ra: {e}')
                    return
            else:
                return (False, 'Không thể tìm thấy video')

    def send_view(self, service=None):
        if service:
            self.service = service
        while True:
            find_video = self.find_video()
            if not find_video[0]: 
                print(find_video[1])
                return
            request = self.session.post(f'{self.base_url}{self.services_ids[self.service]}', headers={'content-type':'multipart/form-data; boundary=----WebKitFormBoundary0nU8PjANC8BhQgjZ', 'user-agent':self.headers['user-agent'], 'origin':'https://zefoy.com'}, data=f'------WebKitFormBoundary0nU8PjANC8BhQgjZ\r\nContent-Disposition: form-data; name="{self.video_info[0]}"\r\n\r\n{self.video_info[1]}\r\n------WebKitFormBoundary0nU8PjANC8BhQgjZ--\r\n')
            if 'Too many requests. Please slow down' in request.text:
                print('Quá nhiều yêu cầu, hãy chậm lại.')
                continue
            else:
                print('Thành công: Đã gửi view cho video.')
                return

if __name__ == '__main__':
    zefoy = Zefoy()
    if zefoy.send_captcha()[0]:
        zefoy.get_table()
        zefoy.send_view()
