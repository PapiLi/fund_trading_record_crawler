# 导入selenium的浏览器驱动接口
from selenium import webdriver
# 导入chrome选项
from selenium.webdriver.chrome.options import Options

from mongodb import Mongodb
import time

fundid=["370027","000001","110011","000286","161716"]
def crawl(id):
    # 创建chrome浏览器驱动，无头模式
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-gpu")  # 规避bug
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_page_load_timeout(10)
    """
    　在使用webdriver的get方法打开页面时，可能页面需要加载的元素较多导致加载时间很长，
    而时间过长会导致后面的操作无法进行，甚至直接报错；所以在页面加载到一定时间，
    实际需要定位的元素很大可能上已经加载出来时，需要停止页面的加载，进而进行下面的操作；
    通过set_page_load_time()方法来设定页面加载超时时间，若超出就会之后如果页面还没有加载完成则抛出超时异常timeout, 并
     通过执行Javascript来停止页面加载 window.stop()
    """

    url="http://fund.eastmoney.com/f10/jjjz_{}.html"
    driver.get(url.format(id))

    name_xpath="//*[@id='bodydiv']/div[8]/div[3]/div[1]/div[1]/div[1]/h4/a"
    fund_name=driver.find_element_by_xpath(name_xpath).text
    data = dict(
        _id=int(id),  # 输入获得
        name=fund_name,  # 根据路径+xpath获得
        fdata=[]
    )

    i=0
    fund_data=[]
    for i in range(2):
        time.sleep(1)
        table_xpath="//*[@id='jztable']/table/tbody/tr"
        table=driver.find_elements_by_xpath(table_xpath)
        for row in table:
            row_data = row.text.split(' ')
            row_dict = {
                "日期":row_data[0],  # 日期
                "单位净值":float(row_data[1]),  # 单位净值
                "累计净值":float(row_data[2]),  # 累计净值
                "日增长率":row_data[3],  # 日增长率
                "申购状态":row_data[4],  # 申购状态
                "赎回状态":row_data[5]  # 赎回状态
           }
            fund_data.append(row_dict)

        cur_xpath="//*[@id='pagebar']/div[1]/label[@class='cur']"
        value=driver.find_element_by_xpath(cur_xpath).get_attribute("value")
        next="//*[@id='pagebar']/div[1]/label[@value='{}']"
        driver.find_element_by_xpath(next.format(int(value)+1)).click()

    data["fdata"].extend(fund_data)
    return data

def main():
    db = Mongodb()
    for id in fundid:
        fund_data=crawl(id)
        db.append_one(fund_data)



if __name__ == '__main__':
    main()
