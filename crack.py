import base64
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
import json


class crack():
    def __init__(self):
        self.vercation_url = 'https://flights.ctrip.com/itinerary/oneway/'
        self.driver = webdriver.Chrome('Path of webdrive')

    def main(self):
        self.driver.get(self.vercation_url)
        # driver.implicitly_wait(10)
        time.sleep(2)

        # 关闭弹窗广告，若没有可注释代码
        btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="base_bd"]/div[8]/div[2]/div/i')))
        # print(btn)
        btn.click()
        print('关闭广告成功')
        time.sleep(1)

        # 破解滑动验证码
        scrollElement = self.driver.find_elements_by_class_name('cpt-img-double-right-outer')[0]
        ActionChains(self.driver).click_and_hold(on_element=scrollElement).perform()
        # 第一次滑动
        ActionChains(self.driver).move_to_element_with_offset(to_element=scrollElement, xoffset=30,
                                                              yoffset=10).perform()
        # 第二次滑动
        ActionChains(self.driver).move_to_element_with_offset(to_element=scrollElement, xoffset=100,
                                                              yoffset=20).perform()
        # 第三次滑动
        ActionChains(self.driver).move_to_element_with_offset(to_element=scrollElement, xoffset=200,
                                                              yoffset=50).perform()
        print('滑块破解成功')
        time.sleep(1)

        count=1
        while True:
            print('正在进行第{}次识别...'.format(count))
            small_image_b64, big_image_b64 = self.get_image_b64()
            small_res, big_res = self.Tencent_OCR(small_image_b64, big_image_b64)
            status,words_locations = self.get_words_locations(big_res, small_res)
            count+=1
            if status:
                print('识别成功！')
                break

        print('匹配成功，开始点击')
        self.clickWords(words_locations)
        print('准备提交')
        self.driver.find_element_by_xpath('//*[@id="J_slider_verification_qwewq-choose"]/div[2]/div[4]/a').click()
        print('提交成功')
        raw_cookie = self.driver.get_cookies()
        cookie = ''
        for i in raw_cookie:
            # print(i['name'],i['value'])
            cookie += i['name'] + "=" + i['value'] + ";"
        print(cookie)
        self.driver.close()
        self.driver.quit()
        return cookie

    def get_image_b64(self):
        # 先刷新一次
        self.driver.find_element_by_xpath('//*[@id="J_slider_verification_qwewq-choose"]/div[2]/div[4]/div/a').click()
        time.sleep(2)
        # 下载图片base64
        small_image_src = self.driver.find_element_by_xpath(
            '//*[@id="J_slider_verification_qwewq-choose"]/div[2]/div[1]/img').get_attribute('src')
        big_image_src = self.driver.find_element_by_xpath(
            '//*[@id="J_slider_verification_qwewq-choose"]/div[2]/div[3]/img').get_attribute('src')
        # 保存下载
        f = open("small.jpeg", "wb")
        # 由于其src是base64编码的，因此需要以base64编码形式写入
        f.write(base64.b64decode(small_image_src.split(',')[1]))
        f.close()
        f = open("big.jpeg", "wb")
        f.write(base64.b64decode(big_image_src.split(',')[1]))
        f.close()
        img = Image.open("small.jpeg")
        img = img.convert('L')
        img.save("small.jpeg")
        img = Image.open("big.jpeg")
        img = img.convert('L')
        img.save("big.jpeg")
        print('验证码下载完成')
        with open('small.jpeg', 'rb') as f:
            base64_data = base64.b64encode(f.read())
            small_b64 = base64_data.decode()
        with open('big.jpeg', 'rb') as f:
            base64_data = base64.b64encode(f.read())
            big_b64 = base64_data.decode()
        return small_b64, big_b64

    def clickWords(self, wordsPosInfo):
        # 获取到大图的element
        imgElement = self.driver.find_element_by_xpath(
            '//*[@id="J_slider_verification_qwewq-choose"]/div[2]/div[3]/img')
        # 根据上图文字在下图中的顺序依次点击下图中的文字
        for info in wordsPosInfo:
            ActionChains(self.driver).move_to_element_with_offset(to_element=imgElement, xoffset=info[0],
                                                                  yoffset=info[1]).click().perform()
            time.sleep(1)

    def Tencent_OCR(self, small_b64, big_b64):
        try:
            # 输入腾讯云密钥的SecretId和SecretKey
            cred = credential.Credential("SecretId", "SecretKey")
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

            req = models.GeneralBasicOCRRequest()
            params = '{"ImageBase64":"' + small_b64 + '"}'  # 输入图片的base64编码
            req.from_json_string(params)
            resp = client.GeneralBasicOCR(req)
            small_res = resp.to_json_string()  # 图片信息转化为字符串
            # print(type(small_res))
            # print(small_res)

            req = models.GeneralBasicOCRRequest()
            params = '{"ImageBase64":"' + big_b64 + '"}'  # 输入图片的base64编码
            req.from_json_string(params)
            resp = client.GeneralBasicOCR(req)
            big_res = resp.to_json_string()  # 图片信息转化为字符串
            # print(type(big_res))
            # print(big_res)
            print('验证码识别中...')
            big_res = json.loads(big_res)
            small_res = json.loads(small_res)
            return small_res, big_res
        except TencentCloudSDKException as err:
            print('OCR返回错误：', err)

    def get_words_locations(self, big, small):
        locations = {}
        words_locations = []
        for i in range(len(big["TextDetections"])):
            x = 0
            y = 0
            for j in range(len(big["TextDetections"][i]["Polygon"])):
                x += big["TextDetections"][i]["Polygon"][j]['X']
                y += big["TextDetections"][i]["Polygon"][j]['Y']
            locations[big["TextDetections"][i]["DetectedText"]] = (x / 4, y / 4)
        try:
            for i in small["TextDetections"][0]["DetectedText"]:
                words_locations.append(list(locations[i]))
            return True,words_locations
        except:
            print("OCR识别有误")
            return False,None

