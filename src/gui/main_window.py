
import tkinter as tk
from tkinter import ttk
import threading
import time


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Tampermonkey 本地服务器')
        self.root.geometry('800x600')
        self.root.minsize(600, 400)
        
        self._server_running = False
        self._port = 8080
        self._start_time = None
        self._uptime_thread = None
        self._uptime_stop_event = threading.Event()
        
        self.create_widgets()
        self.setup_layout()
        self.bind_events()
    
    def create_widgets(self):
        self._create_status_bar()
        self._create_control_bar()
        self._create_log_panel()
    
    def _create_status_bar(self):
        self.status_frame = ttk.Frame(self.root)
        
        self.status_label = ttk.Label(self.status_frame, text='状态: 已停止', foreground='red')
        self.port_label = ttk.Label(self.status_frame, text='端口: 8080')
        self.uptime_label = ttk.Label(self.status_frame, text='运行时间: 00:00:00')
    
    def _create_control_bar(self):
        self.control_frame = ttk.Frame(self.root)
        
        self.start_button = ttk.Button(self.control_frame, text='启动服务', command=self.on_start_server)
        self.stop_button = ttk.Button(self.control_frame, text='停止服务', command=self.on_stop_server, state=tk.DISABLED)
        self.settings_button = ttk.Button(self.control_frame, text='设置', command=self.on_settings)
        self.clear_log_button = ttk.Button(self.control_frame, text='清空日志', command=self.clear_logs)
        
        self.port_label_input = ttk.Label(self.control_frame, text='端口：')
        self.port_entry = ttk.Entry(self.control_frame, width=10)
        self.port_entry.insert(0, '8080')
    
    def _create_log_panel(self):
        self.log_frame = ttk.LabelFrame(self.root, text='日志')
        
        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.log_scrollbar = ttk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scrollbar.set)
    
    def setup_layout(self):
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.status_label.pack(side=tk.LEFT, padx=5)
        self.port_label.pack(side=tk.LEFT, padx=5)
        self.uptime_label.pack(side=tk.LEFT, padx=5)
        
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.settings_button.pack(side=tk.LEFT, padx=5)
        self.clear_log_button.pack(side=tk.LEFT, padx=5)
        
        self.port_label_input.pack(side=tk.RIGHT, padx=5)
        self.port_entry.pack(side=tk.RIGHT, padx=5)
        
        self.log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def bind_events(self):
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
    
    def _update_uptime(self):
        while not self._uptime_stop_event.is_set():
            if self._start_time and self._server_running:
                elapsed = time.time() - self._start_time
                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                seconds = int(elapsed % 60)
                self.uptime_label.config(text='运行时间: {:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds))
            time.sleep(1)
    
    def on_start_server(self):
        try:
            port = int(self.port_entry.get())
            if port < 1024 or port > 65535:
                self.add_log('端口号必须在 1024-65535 之间', 'ERROR')
                return
            
            self._port = port
            self.port_label.config(text='端口: {}'.format(port))
            self._server_running = True
            self._start_time = time.time()
            self._uptime_stop_event.clear()
            
            self._uptime_thread = threading.Thread(target=self._update_uptime, daemon=True)
            self._uptime_thread.start()
            
            self.update_status('running')
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.port_entry.config(state=tk.DISABLED)
            self.add_log('服务已启动，监听端口: {}'.format(port), 'INFO')
        except ValueError:
            self.add_log('端口号格式错误', 'ERROR')
    
    def on_stop_server(self):
        self._server_running = False
        self._uptime_stop_event.set()
        self._start_time = None
        self.uptime_label.config(text='运行时间: 00:00:00')
        
        self.update_status('stopped')
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.NORMAL)
        self.add_log('服务已停止', 'INFO')
    
    def on_settings(self):
        self.add_log('设置功能待实现', 'WARNING')
    
    def clear_logs(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def update_status(self, status):
        if status == 'running':
            self.status_label.config(text='状态: 运行中', foreground='green')
        else:
            self.status_label.config(text='状态: 已停止', foreground='red')
    
    def add_log(self, message, level='INFO'):
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = '[{}] [{}] {}\n'.format(timestamp, level, message)
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def on_closing(self):
        self._uptime_stop_event.set()
        if self._server_running:
            self.on_stop_server()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

