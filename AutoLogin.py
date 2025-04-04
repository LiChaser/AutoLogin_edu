from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

class AutoLogin:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self._get_options()
        )
        self.username = username
        self.password = password

    def _get_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        return options

    def login(self,school):
        try:
            self.driver.get(f"https://sso.{school}.edu.cn/login")

            # 执行登录
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/div[2]/form/div[1]/nz-input-group/input"))
            ).send_keys(self.username)

            self.driver.find_element(By.XPATH, "/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/div[2]/form/div[2]/nz-input-group/input").send_keys(self.password)
            self.driver.find_element(By.XPATH, "/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/div[2]/form/div[6]/div/button").click()
            # 验证登录成功
            time.sleep(3)
            print('ok')
            self.driver.get(f"https://xgfw.{school}.edu.cn/xsfw/sys/swmzncqapp/*default/index.do")

            WebDriverWait(self.driver, 10).until(
                EC.title_contains("智能查寝")
            )

            cookies=self.driver.get_cookies()
            Success_cookie=cookies[1]["value"]
            print("获取有效cookie:"+Success_cookie)
            url = f"https://xgfw.{school}.edu.cn/xsfw/sys/swmzncqapp/kqController/addKqInfo.do"

            payload = ""
            if payload == "":
                print("请输入打卡地址payload，如不清楚私信我获取")
                exit()
            headers = {
                'User-Agent': "Mozilla/5.0 (Licharse is here); colorScheme/dark",
                'Accept': "application/json, text/plain, */*",
                'Content-Type': "application/x-www-form-urlencoded",
                'X-Requested-With': "com.alibaba.android.rimet",
                'Sec-Fetch-Site': "same-origin",
                'Sec-Fetch-Mode': "cors",
                'Sec-Fetch-Dest': "empty",
                'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                'Cookie': "EMAP_LANG=zh; _WEU="+Success_cookie
            }

            response = requests.post(url, data=payload, headers=headers)

            print(response.text)
        except Exception as e:
            print(f"登陆疑似密码错误")
            self.driver.quit()
        finally:
            self.driver.quit()


if __name__ == "__main__":
    school=''#学校域名开头 例如Licharse.edu.cn取Licharse
    if school == "":
        print("请输入学校域名开头")
        exit()
    AutoLogin("admin", "123456").login(school=school)
