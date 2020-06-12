import time

from selenium import webdriver


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed


class EksiSozluk():
    def __init__(self):
        self.counter = 0
        pass

    @timeit
    def get_entry_comments(self, entryurl,filename="specificentry"):
        try:
            browser = webdriver.Chrome()
            browser.get(entryurl)
            page_num = browser.find_element_by_class_name("last")
            title = browser.find_element_by_xpath('//*[@id="title"]/a/span').text.replace(" ", "-")
            with open("eksidata/{}/".format(filename) + title + ".txt", "w", encoding="utf-8") as file:
                for c in range(1, int(page_num.text) + 1):
                    browser.get(entryurl + "&p={}".format(c))  # for topic use '&' for personal use '?'
                    eksi_content = browser.find_elements_by_css_selector(".content")
                    eksi_content_author_iterator = browser.find_elements_by_css_selector(".entry-author").__iter__()
                    for i in eksi_content:
                        self.counter += 1
                        file.write(
                            i.text + "\n Entry Author : " + next(eksi_content_author_iterator).text + "\n-----\n")
                file.write("\nToplam Yorum Sayısı : {}".format(self.counter))
        except():
            import sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
        finally:
            import time
            browser.close()
            time.sleep(1)
            self.counter = 0

    @timeit
    def get_users_entrys(self, name):
        name = name.replace(" ", "-")
        txtname = name + ".txt"
        profileurl = "https://eksisozluk.com/biri/{}".format(name)
        from time import sleep
        try:
            browser = webdriver.Chrome()
            browser.get(profileurl)
            totalentry = browser.find_elements_by_id("entry-count-total")[0].text
            with open("eksidata/userentry/" + txtname, "w", encoding="utf-8") as file:
                for i in range(1, int((int(totalentry) + 30) / 10)):
                    element = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/section/div[3]/a')
                    browser.execute_script("arguments[0].click();", element)
                    sleep(0.5)
                user_entry_list = browser.find_elements_by_id("title")
                user_entry_content = browser.find_elements_by_xpath(
                    '//*[@id="entry-item-list"]/li/div').__iter__()
                user_entry_date = browser.find_elements_by_xpath(
                    '//*[@id="entry-item-list"]/li/footer/div[2]/a[1] ').__iter__()

                try:
                    for i in user_entry_list:
                        file.write(
                            "Title : " + i.text + "\nContent : " + next(user_entry_content).text.replace("\n",
                                                                                                         "") + "\nDate : " + next(
                                user_entry_date).text + "\nUrl : " + i.find_element_by_css_selector("a").get_attribute(
                                'href') + "\n---------\n")
                        self.counter += 1
                    file.write("\nKullanıcının Toplam Entry Sayısı : {}".format(self.counter))
                    print("Veriler Başarıyla Alındı")
                except():
                    import sys
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(exc_type, exc_tb.tb_lineno)
                finally:
                    browser.close()
                    self.counter = 0

        except():
            import sys
            print(sys.exc_info()[0])
        finally:
            browser.close()

    @timeit
    def get_topic_entry_comments(self):
        browser = webdriver.Chrome()

        browser.get("https://eksisozluk.com/")

        try:
            gundem = browser.find_element_by_class_name("topic-list")
            a = gundem.find_elements_by_css_selector("a")
            for i in a:
                print("Gündem Konuları : " + i.get_attribute('href'))
            for i in a:
                self.get_entry_comments(i.get_attribute('href'),"topicentrycomments")

        except():
            import sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
        finally:
            browser.close()


class Twitter():
    pass


class Instagram():
    pass


if __name__ == '__main__':
    pass
