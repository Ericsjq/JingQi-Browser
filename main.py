from ui_conf import *




from cefpython3 import cefpython as cef
import tkinter as tk
import platform
import urllib.request
import requests
from tkinter import ttk

def pd(text):
    try:
        a=requests.get('https://openphish.com/feed.txt')
        t=a.text.split('\n')
        if text in t:
            return 1
        if text[:text.replace('//','||').index('/')+1] in t:
            return 1
        if text[:text.replace('//','||').index('/')] in t:
            return 1

        if not '/' in text:
            text=text+'/'
        if text in t:
            return 1
        if text[:text.replace('//','||').index('/')+1] in t:
            return 1
        if text[:text.replace('//','||').index('/')] in t:
            return 1
        
        return 0
    except:
        return 0

WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")
# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()
var=None
hfnf=None

cef.Initialize() #init
class Browser(ttk.Frame):
    class LoadHandler(object):
        def __init__(self, browser):
            self.browser = browser
        def OnBeforePopup(self,target_url,**a):
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            res = self.browser.NewWindow(target_url)
            if res == "break":
                return True
    class FocusHandler(object):
        "From cefpython3.example.tkinter_"
        def __init__(self, browser_frame):
            self.browser_frame = browser_frame
        def OnSetFocus(self, source, **_):
            return False
        def OnGotFocus(self, **_):
            """Fix CEF focus issues (#255). Call browser frame's focus_set
               to get rid of type cursor in url entry widget."""
            self.browser_frame.focus_set()
    def __init__(self,*a,url="",**b):
        global var,stp,hfnf
        
        super().__init__(*a,**b)
        print('Start Load:','='*15,hfnf)
        #if hfnf is not None:hfnf.configure(text='JQnet网络：正在传递数据')
        #create browser
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        if not url:
            url="https://main-server.jq/search"#"https://www.baidu.com/"
        if is_jq_domain(url):
            if '?data=' in url:
                ut=url
                url=url[:url.index('?')]
                da=ut[ut.index('?data=')+6:]
                print(url,da)
                html_to_data_uri(url,send_request(strip_jq_domain(url), da)[1])
                url=f'http://localhost:{stp}'
            else:
                html_to_data_uri(url,send_request(strip_jq_domain(url))[1])
                url=f'http://localhost:{stp}'
        else:
            #if (var is not None):print('var',var.get())
            
            if (var is not None) and var.get():
                print('使用网桥打开:',url)
                print('——'*4,'\n')
                if var.get()==1:
                    html_to_data_uri(url,send_request('main-server/web-cdn-a',url)[1])
                    url=f'http://localhost:{stp}'
                elif var.get()==2:
                    html_to_data_uri(url,send_request('main-server/web-cdn-b',url)[1])
                    url=f'http://localhost:{stp}'
            else:
                print('普通模式打开:',url)
                print('——'*4,'\n')
                url=url#url=html_to_data_uri(url,send_request('main-server/web-cdn',url)[1])
        #url=''
        self.browser = cef.CreateBrowserSync(window_info,url=url)
        #hfnf.configure(text='JQnet网络：空闲')
        assert self.browser
        self.browser.SetClientHandler(self.LoadHandler(self))
        self.browser.SetClientHandler(self.FocusHandler(self))
        #fit frame
        self.bind("<Configure>", self._configure)
       
        
    def _configure(self, event):
        res=self.event_generate("<<Configure>>")
        if res=="break":
            return
        width = event.width
        height = event.height
        if WINDOWS:
            WindowUtils.OnSize(self.winfo_id(), 0, 0, 0)
        elif LINUX:
            self.browser.SetBounds(0, 0, width, height)
        self.browser.NotifyMoveOrResizeStarted()
    def NewWindow(self,url):
        self.load(url)
        return "break"
    def loadurl(self,url):
        self.browser.StopLoad()
        self.browser.LoadUrl(url)
    def geturl(self):
        return self.browser.GetUrl()
    def reload(self):
        self.browser.Reload()
    def get_window_handle(self):
        "From cef"
        if self.winfo_id() > 0:
            return self.winfo_id()
        elif MAC:
            # On Mac window id is an invalid negative value (Issue #308).
            # This is kind of a dirty hack to get window handle using
            # PyObjC package. If you change structure of windows then you
            # need to do modifications here as well.
            # noinspection PyUnresolvedReferences
            from AppKit import NSApp
            # noinspection PyUnresolvedReferences
            import objc
            # Sometimes there is more than one window, when application
            # didn't close cleanly last time Python displays an NSAlert
            # window asking whether to Reopen that window.
            # noinspection PyUnresolvedReferences
            return objc.pyobjc_id(NSApp.windows()[-1].contentView())
        else:
            raise Exception("Couldn't obtain window handle")     
def maincefloop(n=int(1/70*1000)):
    cef.MessageLoopWork()
    tk._default_root.after(n, maincefloop,n)
def bye():
    cef.Shutdown()
    quit()
    
def my_print(t):
    import tkinter.messagebox
    tkinter.messagebox.showinfo(title='打印', message=t)
    print(t)
    print('——'*4,'\n')
    
def test():
    global var,widget,hfn,hfnf
    def makenew(url):
        b = Browser(note,url=url)
        note.add(b,
                 text=str(note.index("end"))+'： '+url.replace("https://","").replace("http://","").replace("blob://","")[:20],
                 padding=40,#random.randint(14,35),
                 )
        note.select(note.index("end")-1)
        b.NewWindow=lambda url:makenew(url) or "break"

    def rm():
        import tkinter.simpledialog
        result = tk.simpledialog.askstring(title = '获取信息',prompt='请输入标签页编号：',initialvalue = str(note.index("end")-1))
        if result is not None:
            url=int(result)
            note.hide(url)

    

    def is_url(input_str):
        """
        判断给定的字符串是否为有效的URL。
        
        Args:
        input_str (str): 用户输入的字符串。
        
        Returns:
        bool: 如果是有效的URL返回True，否则返回False。
        """
        if  '.com' in input_str or '.cn' in input_str or\
           '.org' in input_str or '.jp' in input_str or\
           '.uk' in input_str or '.top' in input_str or\
           '.net' in input_str or '.edu' in input_str or\
           '.com' in input_str or '.gov' in input_str or\
           '.mil' in input_str or '.jq' in input_str or\
           '.app' in input_str or '.blog' in input_str or\
           '.fun' in input_str or '.tv' in input_str or '.co' in input_str :
            return True
        # 使用正则表达式来匹配URL
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return bool(re.match(url_pattern, input_str))
    
    def ntb():
        import tkinter.simpledialog
        result = tk.simpledialog.askstring(title = '获取信息',prompt='请输入网址：',initialvalue = 'https://main-server.jq/search')
        if result!=None:
            if not pd(result):
                if is_url(result):
                    makenew(result)
                else:
                    makenew('https://main-server.jq/search?data='+result)
    #############
    
    import re
    import random
    root = tk.Tk()
    note = ttk.Notebook()
    note.pack(expand=1,fill="both")
    
    
    root.title("JingQi Browser")
    root.geometry("1400x730+70+20")#("980x760")
    maincefloop()
    ##################
    '''
    
    root2 = tk.Tk()
    root2.title('用户命令')
    
    root2.geometry("240x200")
    bu=ttk.Button(root2,text='新建标签页',command=ntb)
    bu.pack()
    bu=ttk.Button(root2,text='删除标签页',command=rm)
    bu.pack()
    
    ttk.Separator(root2, orient="horizontal").pack(pady=(10, 5), fill="x")
    
    hf = ttk.Label(root2, text="【使用网桥】",font=('none',10))
    hf.pack()
    var = tk.IntVar()
    var.set(0)
    #widgetkg = tk.Checkbutton(root2, text='开关')#, variable=var)

    
    def pdu(a=None):
        global var,hfn
        if var.get()==2:
            hfn.configure(text='网桥已关闭')
            my_print('网桥已关闭，无法完全保障您的安全性')
            var.set(0)
        elif var.get()==1:
            hfn.configure(text=f'网桥已开启：【我】 -> 【中国 江苏 扬州 腾讯云】 -> 【JQnet中转服务器{["一","二","三","四"][random.randint(0,3)]}】 -> 【中国 香港 Cogent】 -> 【网站服务器】')
            my_print(f'网桥已开启：【我】 -> 【中国 江苏 扬州 腾讯云】 -> 【JQnet中转服务器{["一","二","三","四"][random.randint(0,3)]}】 -> 【中国 香港 Cogent】 -> 【网站服务器】\n网桥加载较慢')
            var.set(2)
        else:
            hfn.configure(text=f'网桥已开启：【我】 -> 【中国 江苏 扬州 腾讯云】 -> 【JQnet中转服务器{["一","二","三","四"][random.randint(0,3)]}】 -> 【中国 浙江 杭州 阿里云】 -> 【网站服务器】')
            my_print(f'网桥已开启：【我】 -> 【中国 江苏 扬州 腾讯云】 -> 【JQnet中转服务器{["一","二","三","四"][random.randint(0,3)]}】 -> 【中国 浙江 杭州 阿里云】 -> 【网站服务器】\n网桥加载较慢')
            var.set(1)#label.config(text="关")
            
    bu2=ttk.Button(root2,text='切换网桥',command=pdu)
    bu2.pack()
    hfn = ttk.Label(root2, text="当前：未使用",font=('none',10))
    hfn.pack()
    #tk.Label(root2, text="——————"*3,font=('none',8)).pack()
    ttk.Separator(root2, orient="horizontal").pack(pady=(10, 5), fill="x")

    #widgetkg.pack()
    '''
    def pdu(a=0):
        try:
            global var, hfn
            if var.get() == 2:
                hfn.configure(text='网桥已关闭')
                my_print('网桥已关闭，无法完全保障您的安全性')
                var.set(0)
            elif var.get() == 0:
                hfn.configure(text=f'网桥已开启：我 -> 中国 江苏 扬州 腾讯云 -> JQnet中转{["一","二","三","四"][random.randint(0,3)]} -> 中国 香港 Cogent -> 加利福尼亚州 洛杉矶 -> 网站服务器')
                my_print(f'网桥已开启：【我】 -> 【中国 江苏 扬州 腾讯云】 -> 【JQnet中转{["一","二","三","四"][random.randint(0,3)]}】 -> 【中国 香港 Cogent】 -> 【加利福尼亚州 洛杉矶】 -> 【网站服务器】\n网桥加载较慢')
                var.set(1)
            else:
                hfn.configure(text=f'网桥已开启：我 -> 中国 江苏 扬州 腾讯云 -> JQnet中转{["一","二","三","四"][random.randint(0,3)]} -> 中国 浙江 杭州 阿里云 -> 网站服务器')
                my_print(f'网桥已开启：【我】 -> 【中国 江苏 扬州 腾讯云】 -> 【JQnet中转{["一","二","三","四"][random.randint(0,3)]}】 -> 【中国 浙江 杭州 阿里云】 -> 【网站服务器】\n网桥加载较慢')
                var.set(2)
        except:
            time.sleep(1)
            if a>3:
                return
            print('PDU Err')
            pdu(a=a+1)
                
                

    print(111)
    # Create the menu bar
    menu_bar = tk.Menu(root)

    # Create the file menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="新建标签页", command=ntb)
    file_menu.add_command(label="删除标签页", command=rm)
    file_menu.add_separator()
    file_menu.add_command(label="退出", command=lambda: bye())

    # Create the options menu
    options_menu = tk.Menu(menu_bar, tearoff=0)
    options_menu.add_command(label="切换网桥", command=pdu)

    # Add the menus to the menu bar
    menu_bar.add_cascade(label="标签页", menu=file_menu)
    menu_bar.add_cascade(label="网桥", menu=options_menu)

    # Configure the root window to use the menu bar
    root.config(menu=menu_bar)

    # Rest of your code for labels and other widgets
    #root.geometry("240x200")

    status_frame = tk.Frame(root)
    status_frame.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=5)
    status_framel = tk.Frame(root)
    status_framel.pack(side=tk.LEFT, anchor=tk.NE, padx=10, pady=5)

    var = tk.IntVar()
    var.set(0)

    # Label for current status
    hfn = ttk.Label(status_frame, text="当前未开启网桥", font=('none', 9))
    hfn.pack(side=tk.RIGHT)
    
    #hfnf = ttk.Label(status_framel, text="JQnet网络：空闲", font=('none', 8))
    #hfnf.pack(side=tk.LEFT)
    print(222)
    def c_s():
        global hfnf
        while True:
            
            try:
                
                requests.get(serv_url)
                hfnf.configure(text='JQnet网络已连接')
            except Exception as ee:
                hfnf.configure(text=('JQnet网络连接失败:'+str(ee)))
            time.sleep(20)
    #thread = threading.Thread(target=c_s)
    #thread.start()

    makenew('https://main-server.jq/search')

    root.mainloop()
    bye()

if __name__ == "__main__":
    test()



               
