import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_followers(username):
    url = f"https://www.tiktok.com/@{username}/followers"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    try:
        followers = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "follower-username"))
        )
        followers = [f.text for f in followers]
    finally:
        driver.quit()
    
    return followers

def is_following_back(follower, username):
    url = f"https://www.tiktok.com/@{follower}/following"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    try:
        following = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "following-username"))
        )
        following = [f.text for f in following]
    finally:
        driver.quit()

    return username in following

def remove_follower(username, follower):
    url = f"https://www.tiktok.com/@{username}/remove-follower/{follower}"
    response = requests.get(url)
    return response.status_code == 200

def on_remove_click():
    username = entry_username.get()
    followers = get_followers(username)

    removed_followers = []
    for follower in followers:
        if not is_following_back(follower, username):
            if remove_follower(username, follower):
                removed_followers.append(follower)

    if removed_followers:
        messagebox.showinfo("Success", f"Removed followers: {', '.join(removed_followers)}")
    else:
        messagebox.showinfo("Info", "No followers to remove")

app = tk.Tk()
app.title("TikTok Follower Cleaner")

label_username = tk.Label(app, text="Enter your TikTok username:")
label_username.pack()

entry_username = tk.Entry(app)
entry_username.pack()

button_remove = tk.Button(app, text="Remove Non-following Followers", command=on_remove_click)
button_remove.pack()

app.mainloop()