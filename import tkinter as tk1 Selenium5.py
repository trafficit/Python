import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import logging
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

service = ChromeService(ChromeDriverManager().install())
self.driver = webdriver.Chrome(service=service, options=options)


logging.basicConfig(level=logging.INFO)

class TikTokApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Follower Cleaner")

        self.label_username = tk.Label(root, text="Введите ваш TikTok email или номер телефона:")
        self.label_username.pack()

        self.entry_username = tk.Entry(root)
        self.entry_username.pack()

        self.label_password = tk.Label(root, text="Введите ваш TikTok пароль:")
        self.label_password.pack()

        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()

        self.button_login = tk.Button(root, text="Вход", command=self.on_login_click)
        self.button_login.pack()

        self.label_status = tk.Label(root, text="Не авторизовано", fg="red")
        self.label_status.pack()

        self.frame_browser = ttk.Frame(root, width=600, height=400)
        self.frame_browser.pack()

        self.button_remove = tk.Button(root, text="Удалить неподписанных подписчиков", command=self.on_remove_click)
        self.button_remove.pack()

        self.followers_list = tk.Listbox(root)
        self.followers_list.pack()

    def on_login_click(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()
        
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        
        self.login(self.username, self.password, self.label_status)
        self.display_browser()

    def login(self, username, password, label_status):
        self.driver.get("https://www.tiktok.com/login")
        
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email / Username / TikTok ID']"))).send_keys(username)
            self.driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys(password)
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]").click()
            
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Following')]")))
            label_status.config(text="Авторизовано", fg="green")
        except Exception as e:
            label_status.config(text="Ошибка авторизации", fg="red")
            logging.error("Ошибка:", e)

    def display_browser(self):
        self.driver.set_window_size(600, 400)
        self.driver.set_window_position(0, 0)
        
        handle = self.driver.current_window_handle
        self.root.after(100, lambda: self.driver.switch_to.window(handle))

    def on_remove_click(self):
        self.remove_non_followers()

    def remove_non_followers(self):
        self.driver.get(f"https://www.tiktok.com/@{self.username}/followers")
        
        followers = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "follower-username")) 
        )
        
        for follower in followers:
            follower_username = follower.text
            self.driver.get(f"https://www.tiktok.com/@{follower_username}")
            
            try:
                follow_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Follow back')]"))
                )
                follow_button.click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Following')]"))).click()
            except:
                continue
        
        messagebox.showinfo("Информация", "Удаление завершено")

if __name__ == "__main__":
    root = tk.Tk()
    app = TikTokApp(root)
    root.mainloop()
