
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class TikTokApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Follower Cleaner")

        # Ввод имени пользователя
        self.label_username = tk.Label(root, text="Enter your TikTok email or phone number:")
        self.label_username.pack()

        self.entry_username = tk.Entry(root)
        self.entry_username.pack()

        # Ввод пароля
        self.label_password = tk.Label(root, text="Enter your TikTok password:")
        self.label_password.pack()

        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()

        # Кнопка для входа
        self.button_login = tk.Button(root, text="Login", command=self.on_login_click)
        self.button_login.pack()

        # Статус авторизации
        self.label_status = tk.Label(root, text="Not Authorized", fg="red")
        self.label_status.pack()

        # Иконка авторизации
        self.auth_image = ImageTk.PhotoImage(Image.open("auth_icon_green.png"))
        self.error_image = ImageTk.PhotoImage(Image.open("auth_icon_red.png"))
        self.img_status = tk.Label(root, image=self.error_image)
        self.img_status.pack()

        # Блок для отображения мини-экрана TikTok
        self.frame_browser = ttk.Frame(root, width=600, height=400)
        self.frame_browser.pack()

        # Кнопка для удаления неподписанных подписчиков
        self.button_remove = tk.Button(root, text="Remove Non-following Followers", command=self.on_remove_click)
        self.button_remove.pack()

        # Список подписчиков
        self.followers_list = tk.Listbox(root)
        self.followers_list.pack()

    def on_login_click(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()
        
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        
        self.login(self.username, self.password, self.label_status, self.img_status)
        self.display_browser()

    def login(self, username, password, label_status, img_status):
        self.driver.get("https://www.tiktok.com/login")
        
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email / Username / TikTok ID']"))).send_keys(username)
            self.driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys(password)
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]").click()
            
            # Проверка успешной авторизации
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Following')]")))
            label_status.config(text="Авторизовано", fg="green")
            img_status.config(image=self.auth_image)  # Обновляем иконку на зеленую
        except Exception as e:
            label_status.config(text="Ошибка авторизации", fg="red")
            img_status.config(image=self.error_image)  # Обновляем иконку на красную
            print("Ошибка:", e)

    def display_browser(self):
        self.driver.set_window_size(600, 400)
        self.driver.set_window_position(0, 0)
        
        handle = self.driver.current_window_handle
        self.root.after(100, lambda: self.driver.switch_to.window(handle))

    def get_followers(self, driver, username):
        driver.get(f"https://www.tiktok.com/@{username}/followers")
        followers = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "follower-username"))  # Обновите класс по необходимости
        )
        return [f.text for f in followers]

    def is_following_back(self, driver, follower, username):
        driver.get(f"https://www.tiktok.com/@{follower}/following")
        # Дополнительная логика для проверки подписки в ответ

    def on_remove_click(self):
        followers = self.get_followers(self.driver, self.username)
        self.followers_list.delete(0, tk.END)
        
        for follower in followers:
            if not self.is_following_back(self.driver, follower, self.username):
                # Логика для удаления подписчика
                self.followers_list.insert(tk.END, f"{follower} (Removed)")
            else:
                self.followers_list.insert(tk.END, follower)

if name == "__main__":
    root = tk.Tk()
    app = TikTokApp(root)
    root.mainloop()