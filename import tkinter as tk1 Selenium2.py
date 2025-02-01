following = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "following-username"))  # Обновите класс по необходимости
        )
        return username in [f.text for f in following]

    def remove_follower(self, driver, username, follower):
        driver.get(f"https://www.tiktok.com/@{username}/followers")
        follower_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{follower}']"))
        )
        follower_element.find_element(By.XPATH, "../..//button[contains(text(), 'Remove')]").click()

    def on_remove_click(self):
        username = self.entry_username.get()
        
        try:
            followers = self.get_followers(self.driver, username)
            
            removed_followers = []
            for follower in followers:
                if not self.is_following_back(self.driver, follower, username):
                    self.remove_follower(self.driver, username, follower)
                    removed_followers.append(follower)
            
            if removed_followers:
                messagebox.showinfo("Success", f"Removed followers: {', '.join(removed_followers)}")
            else:
                messagebox.showinfo("Info", "No followers to remove")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if name == "__main__":
    root = tk.Tk()
    app = TikTokApp(root)
    root.mainloop()