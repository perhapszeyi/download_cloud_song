from selenium import webdriver
from tqdm import tqdm
import time,re,requests,os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

# 创建歌单文件夹
def create_file(user):
    if not os.path.exists(user):
        os.mkdir(user)

# 获取并保存创建的播放列表
def get_play_list(user,user_url):
    driver = webdriver.Chrome()
    driver.get(user_url)
    driver.switch_to.frame("g_iframe")
    menu = driver.find_element_by_class_name('m-cvrlst').find_elements_by_tag_name('li')
    for i in range(len(menu)):
        hf = menu[i].find_element_by_class_name('msk').get_attribute('href')
        name = menu[i].find_element_by_class_name('tit').get_attribute('title')
        with open(user+'/'+user+'.txt','a',encoding='utf-8') as f:
            f.write(name+' '+hf+'\n')
        print(name,hf)
    driver.close()
    song_list = input('请输入要下载歌曲的链接：')
    main(song_list)

def main(song_list):
    # 登录操作
    driver = webdriver.Chrome()
    driver.get(song_list)
    driver.maximize_window()
    time.sleep(3)

    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[2]/div/div[3]/a').click()
    driver.find_element_by_xpath('//*[@id="j-official-terms"]').click()
    driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[1]/div[1]/div[2]/ul/li[1]/a').click()
    time.sleep(7)

    driver.minimize_window()
    # 获取歌单歌曲
    driver.switch_to.frame("g_iframe")
    info=driver.find_element_by_xpath('//table[@class="m-table "]/tbody').find_elements_by_tag_name("tr")

    # 获取歌曲链接及名字
    for i in tqdm(range(len(info))):
        hf=info[i].find_element_by_tag_name("a").get_attribute('href')
        name = info[i].find_element_by_tag_name("b").get_attribute('title')
        res = re.findall('(?<=id=).*$', hf)
        # 下载歌曲
        if not os.path.exists('歌曲'):
            os.mkdir('歌曲')
        download_song_url = 'http://music.163.com/song/media/outer/url?id=' + res[0] + '.mp3'
        ans = requests.get(download_song_url,headers=headers)
        print('正在下载：',name)
        if name in ":" or '*' or "?" or '<' or '>' or '|' or '/' or '"' or '\\':
            name = name.replace(":",'_').replace('*','_').replace("?",'_').replace('<','_').replace('>','_').replace('|','_').replace('/','_').replace('"','_').replace('\\','_')
        with open('歌曲/'+name+'.mp3','ab') as f:
            f.write(ans.content)
    driver.quit()
    print('下载完成！')

if __name__ == '__main__':
    home_url = 'https://music.163.com/#/user/home?id='
    user = input('请输入用户昵称：')
    id = input('请输入用户ID：')
    user_url = home_url + id
    create_file(user)
    get_play_list(user,user_url)