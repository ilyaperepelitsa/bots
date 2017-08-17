import random
from random import randrange


from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from selenium.common.exceptions import StaleElementReferenceException
import selenium


import time
from datetime import date
import datetime
from datetime import timedelta


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.sql import select


from selenium.webdriver.chrome.options import Options
mobile_emulation = {
    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
# driver = webdriver.Chrome(chrome_options = chrome_options)



def find(browser):
    element = browser.find_element_by_xpath("//button[contains(text(),'Follow')]")
    if element:
        return element
    else:
        return False

def init_driver():
    path_to_chromedriver = "/Users/ilyaperepelitsa/chromedriver"
    driver = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options = chrome_options)
    # driver = webdriver.Chrome(executable_path = path_to_chromedriver)
    driver.wait = WebDriverWait(driver, 5)
    return driver

# browser.find_element_by_xpath("//button[contains(text(),'Log in')]")

def open_and_login():
    time.sleep(1)
    ### OPEN THE WEBSITE AND LOCATE LOG IN WINDOW
    browser.get("http://instagram.com")
    browser.find_element_by_link_text("Log in").click()
    time.sleep(2)

    ### LOG IN
    browser.find_element_by_xpath("//input[@name='username']").send_keys('pewgme')
    browser.find_element_by_xpath("//input[@name='password']").send_keys('isn033k01+42lib7867')
    browser.find_element_by_xpath("//button[contains(text(),'Log in')]").click()
    time.sleep(3)

    ## GO TO PROFILE
    # browser.find_element_by_link_text("Profile").click()
    # browser.find_element_by_xpath('//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[5]/a/div').click()

def get_basic_numbers():
    no_posts = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[1]/span/span').text.replace(",", "").replace(".", "").replace("k", "000").replace("m", "000000")
    no_followers = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a/span').text.replace(",", "").replace(".", "").replace("k", "000").replace("m", "000000")
    no_following = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a/span').text.replace(",", "").replace(".", "").replace("k", "000").replace("m", "000000")

    basic_number = [int(no_posts), int(no_followers), int(no_following)]

    return basic_number

def get_list_of_following():

    # CLICK "FOLLOWING"
    browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a').click()
    time.sleep(3)
    following_links = []
    i = 0
    while i < int(browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a/span').text.replace(",", "").replace(".", "").replace("k", "000").replace("m", "000000"))-5:
        time.sleep(1)
        following_links = [pew.find_element_by_css_selector('a').get_attribute('href') for pew in browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div/div[2]/ul').find_elements_by_tag_name("li")]
        action_chains.ActionChains(browser).move_to_element(browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div/div[2]/ul').find_elements_by_tag_name("li")[-1]).perform()
        # print(i)
        i = len(following_links)
    browser.refresh()
    return following_links

def get_list_of_followers():

    # CLICK "FOLLOWING"
    browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a/span').click()
    time.sleep(3)
    following_links = []
    i = 0
    while i < int(browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a/span').text.replace(",", "").replace(".", "").replace("k", "000").replace("m", "000000"))-6:
        time.sleep(1)
        followers_links = [pew.find_element_by_css_selector('a').get_attribute('href') for pew in browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div/div[2]/ul').find_elements_by_tag_name("li")]
        action_chains.ActionChains(browser).move_to_element(browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div/div[2]/ul').find_elements_by_tag_name("li")[-1]).perform()
        print(i)
        i = len(followers_links)
    browser.refresh()
    return followers_links

# browser.find_element_by_xpath("//h2[contains(.,'Sorry, this page isn't available.')]")

def inst_to_dict(inst, delete_id = True):
    dat = {}
    for column in inst.__table__.columns:
        dat[column.name] = getattr(inst, column.name)
    if delete_id:
        dat.pop("num")
    return dat

def create_my_followers_table():
    my_followers = get_list_of_followers()
    list_followers = []

    for i in my_followers:
        entry = {"name" : i.split("/")[-2],
                "date_checked" : str(time.strftime("%Y-%m-%d"))}
        list_followers.append(entry)

    engine1 = create_engine("sqlite:///table1.db", echo = False)
    Base1 = declarative_base()

    class My_follower(Base1):
        __tablename__ = "my_followers"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        date_checked = Column(String)


        def __repr__(self):
            return "<My_follower(name='%s', date_checked='%s')>"\
            %(self.name, self.date_checked)


    Base1.metadata.create_all(engine1)

    Session1 = sessionmaker(bind = engine1)
    session1 = Session1()
    my_followers_rows = [My_follower(**w) for w in list_followers]
    session1.add_all(my_followers_rows)
    session1.commit()

 # if len(list(session1.query(My_follower).filter(My_follower.name == w["name"])))==0
 # if len(list(session2.query(Me_following).filter(Me_following.name == w["name"])))==0

def create_me_following_table():
    me_following = get_list_of_following()
    list_following = []

    for i in me_following:
        entry = {"name" : i.split("/")[-2],
                "link" : i,
                "date_checked" : str(time.strftime("%Y-%m-%d"))}
        list_following.append(entry)

    engine2 = create_engine("sqlite:///table2.db", echo = False)
    Base2 = declarative_base()

    class Me_following(Base2):
        __tablename__ = "me_following"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        link = Column(String)
        date_checked = Column(String)


        def __repr__(self):
            return "<My_follower(name='%s', link='%s', date_checked='%s')>"\
            %(self.name, self.link, self.date_checked)


    Base2.metadata.create_all(engine2)


    Session2 = sessionmaker(bind = engine2)
    session2 = Session2()
    me_following_rows = [Me_following(**w) for w in list_following]
    session2.add_all(me_following_rows)
    session2.commit()

def update_my_followers_table():
    my_followers = get_list_of_followers()
    list_followers = []

    for i in my_followers:
        entry = {"name" : i.split("/")[-2],
                "date_checked" : str(time.strftime("%Y-%m-%d"))}
        list_followers.append(entry)

    engine1 = create_engine("sqlite:///table1-1.db", echo = False)
    Base1 = declarative_base()

    class My_follower(Base1):
        __tablename__ = "my_followers"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        date_checked = Column(String)


        def __repr__(self):
            return "<My_follower(name='%s', date_checked='%s')>"\
            %(self.name, self.date_checked)


    Base1.metadata.create_all(engine1)

    Session1 = sessionmaker(bind = engine1)
    session1 = Session1()
    my_followers_rows = [My_follower(**w) for w in list_followers if len(list(session1.query(My_follower).filter(My_follower.name == w["name"])))==0]
    session1.add_all(my_followers_rows)
    session1.commit()

 # if len(list(session1.query(My_follower).filter(My_follower.name == w["name"])))==0
 # if len(list(session2.query(Me_following).filter(Me_following.name == w["name"])))==0

def update_me_following_table():
    me_following = get_list_of_following()
    list_following = []

    for i in me_following:
        entry = {"name" : i.split("/")[-2],
                "link" : i,
                "date_checked" : str(time.strftime("%Y-%m-%d"))}
        list_following.append(entry)

    engine2 = create_engine("sqlite:///table2-1.db", echo = False)
    Base2 = declarative_base()

    class Me_following(Base2):
        __tablename__ = "me_following"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        link = Column(String)
        date_checked = Column(String)


        def __repr__(self):
            return "<Me_following(name='%s', link='%s', date_checked='%s')>"\
            %(self.name, self.link, self.date_checked)


    Base2.metadata.create_all(engine2)


    Session2 = sessionmaker(bind = engine2)
    session2 = Session2()
    me_following_rows = [Me_following(**w) for w in list_following if len(list(session2.query(Me_following).filter(Me_following.name == w["name"])))==0]
    session2.add_all(me_following_rows)
    session2.commit()

def alt_update_me_following_table():

    engine2 = create_engine("sqlite:////Users/ilyaperepelitsa/quant/bot/table2-1.db", echo = False)
    Base2 = declarative_base()

    class Me_following(Base2):
        __tablename__ = "me_following"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        link = Column(String)
        date_checked = Column(String)


        def __repr__(self):
            return "<Me_following(name='%s', link='%s', date_checked='%s')>"\
            %(self.name, self.link, self.date_checked)


    Base2.metadata.create_all(engine2)


    Session2 = sessionmaker(bind = engine2)
    session2 = Session2()

    engine5 = create_engine("sqlite:////Users/ilyaperepelitsa/quant/bot/table5.db", echo = False)
    Base5 = declarative_base()

    class To_follow(Base5):
        __tablename__ = "to_follow"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        test_train = Column(String)
        date = Column(String)
        link = Column(String)


        def __repr__(self):
            return "<To_follow(name_grandchild='%s', test_train='%s', date='%s', link='%s')>"\
            %(self.name_grandchild, self.test_train, self.date, self.link)


    Base5.metadata.create_all(engine5)

    Session5 = sessionmaker(bind = engine5)
    session5 = Session5()

    # [inst_to_dict(w) for w in session5.query(To_follow)]
    big_list = [inst_to_dict(w) for w in session5.query(To_follow).filter(To_follow.date == "2017-07-22")]
    for row in big_list:
        if len([inst_to_dict(q) for q in session2.query(Me_following).filter(Me_following.name == row["name_grandchild"])]) == 0:
            browser.get(row["link"])
            time.sleep(0.6)
            try:
                if browser.find_element_by_xpath("//button[contains(text(),'Following')]"):
                    entry = {"name" : row["name_grandchild"],
                            "link" : row["link"],
                            "date_checked" : str(time.strftime("%Y-%m-%d"))}

                    # following_rows.append()
                    session2.add(Me_following(**entry))
                    session2.commit()


            except NoSuchElementException:
                continue

def create_grandchild_following_table():
    engine1 = create_engine("sqlite:///table1.db", echo = False)
    Base1 = declarative_base()
    class My_follower(Base1):
        __tablename__ = "my_followers"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        date_checked = Column(String)
        def __repr__(self):
            return "<My_follower(name='%s', date_checked='%s')>"\
            %(self.name, self.date_checked)
    Base1.metadata.create_all(engine1)
    Session1 = sessionmaker(bind = engine1)
    session1 = Session1()



    engine2 = create_engine("sqlite:///table2.db", echo = False)
    Base2 = declarative_base()
    class Me_following(Base2):
        __tablename__ = "me_following"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        link = Column(String)
        date_checked = Column(String)
        def __repr__(self):
            return "<My_follower(name='%s', link='%s', date_checked='%s')>"\
            %(self.name, self.link, self.date_checked)
    Base2.metadata.create_all(engine2)
    Session2 = sessionmaker(bind = engine2)
    session2 = Session2()




    engine3 = create_engine("sqlite:///table3.db", echo = False)
    Base3 = declarative_base()

    class Following_following(Base3):
        __tablename__ = "following_following"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        name_grandchild = Column(String)
        grandchild_link = Column(String)


        def __repr__(self):
            return "<Following_following(name='%s', name_grandchild='%s', grandchild_link='%s')>"\
            %(self.name, self.name_grandchild, self.grandchild_link)
    Base3.metadata.create_all(engine3)
    Session3 = sessionmaker(bind = engine3)
    session3 = Session3()









    list_following = session2.query(Me_following)
    for i in list_following:
        if len(list(session3.query(Following_following).filter(Following_following.name == inst_to_dict(i)["name"])))==0:
            browser.get(inst_to_dict(i)["link"])
            if get_basic_numbers()[2] < 1200:
                grandchild_list = get_list_of_following()
                grandchildren_rows = []
                for pew in grandchild_list:
                    entry = {"name" : inst_to_dict(i)["name"], "name_grandchild" : pew.split("/")[-2], "grandchild_link" : pew}
                    if len(list(session3.query(Following_following).filter(Following_following.name_grandchild == entry["name_grandchild"])))==0 and \
                       len(list(session2.query(Me_following).filter(Me_following.name == entry["name_grandchild"])))==0 and \
                       len(list(session1.query(My_follower).filter(My_follower.name == entry["name_grandchild"])))==0 :
                    #    print("pew")
                       grandchildren_rows.append(Following_following(**entry))
                    else:
                        continue

                session3.add_all(grandchildren_rows)
                session3.commit()
            else:
                continue

def create_grandchild_images():
    engine3 = create_engine("sqlite:///table3.db", echo = False)
    Base3 = declarative_base()

    class Following_following(Base3):
        __tablename__ = "following_following"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        name_grandchild = Column(String)
        grandchild_link = Column(String)

        def __repr__(self):
            return "<Following_following(name='%s', name_grandchild='%s', grandchild_link='%s')>"\
            %(self.name, self.name_grandchild, self.grandchild_link)
    Base3.metadata.create_all(engine3)
    Session3 = sessionmaker(bind = engine3)
    session3 = Session3()



    engine4 = create_engine("sqlite:///table4.db", echo = False)
    Base4 = declarative_base()
    class Grandchild_image(Base4):
        __tablename__ = "grandchild_image"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        num_posts = Column(Integer)
        num_followers = Column(Integer)
        num_following = Column(Integer)
        link_image = Column(String)


        def __repr__(self):
            return "<Following_following(name_grandchild='%s', num_posts='%d', num_followers='%d', num_following='%d', link_image='%s')>"\
            %(self.name_grandchild, self.num_posts, self.num_followers, self.num_following, self.link_image)

    Base4.metadata.create_all(engine4)
    Session4 = sessionmaker(bind = engine4)
    session4 = Session4()

    list_grandchildren = session3.query(Following_following)
    counter = 0
    for grandchild in list_grandchildren:
        print(counter)
        counter += 1
        if len(list(session4.query(Grandchild_image).filter(Grandchild_image.name_grandchild == inst_to_dict(grandchild)["name_grandchild"])))==0:
            browser.get(inst_to_dict(grandchild)["grandchild_link"])
            print(inst_to_dict(grandchild)["grandchild_link"])
            try:
                stats = get_basic_numbers()
            except NoSuchElementException:
                todel = session3.query(Following_following).filter(Following_following.name_grandchild == inst_to_dict(grandchild)["name_grandchild"])
                todel.delete(synchronize_session = False)
                session3.commit()
                print("deleted")
                continue
            # print("___" + str(stats[0]) + "___")
            # delete_test = "testing"
            try :
                # pew = browser.find_element_by_xpath("//p[contains(.,'Follow to see their photos and videos.')]").text
                # pew = browser.find_element_by_xpath("//h2[contains(.,'Sorry, this page isn't available.')]").text

                # delete_test = browser.find_element_by_xpath("//h2[contains(text(),'No posts yet.')]").text

                if browser.find_element_by_xpath("//p[contains(.,'Follow to see their photos and videos.')]").text :
                    todel = session3.query(Following_following).filter(Following_following.name_grandchild == inst_to_dict(grandchild)["name_grandchild"])
                    todel.delete(synchronize_session = False)
                    session3.commit()
                    print("deleted")


            except NoSuchElementException :
            # print("Not a private account")

                if stats[0] == 0:
                    todel = session3.query(Following_following).filter(Following_following.name_grandchild == inst_to_dict(grandchild)["name_grandchild"])
                    todel.delete(synchronize_session = False)
                    session3.commit()
                    print("deleted")
                else:
                    # print(stats)
                    if stats[0] > 12:
                        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/a').click()
                    flag = True
                    while len([pew.get_attribute('href') for pew in browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")]) < stats[0] and \
                              len([pew.get_attribute('href') for pew in browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")]) < 100 and \
                              flag == True:
                        try:
                            browser.find_element_by_xpath('//a[contains(text(),"Retry")]').click()
                        except NoSuchElementException:
                            pass
                        action_chains.ActionChains(browser).move_to_element(browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")[-1]).perform()
                        if len([pew.get_attribute('href') for pew in browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")]) > int(stats[0])-5 :
                            flag = False
                    image_links = [pew.get_attribute('href') for pew in browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")]

                    image_list = []

                    for i in image_links:
                        entry = {"name_grandchild" : inst_to_dict(grandchild)["name_grandchild"],
                                "num_posts" : stats[0],
                                "num_followers" : stats[1],
                                "num_following" : stats[2],
                                "link_image" : str(i)}
                        image_list.append(entry)

                    image_list_rows = [Grandchild_image(**w) for w in image_list]
                    session4.add_all(image_list_rows)
                    session4.commit()

def create_tofollow_table():

    engine3 = create_engine("sqlite:///table3.db", echo = False)
    Base3 = declarative_base()

    class Following_following(Base3):
        __tablename__ = "following_following"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        name_grandchild = Column(String)
        grandchild_link = Column(String)


        def __repr__(self):
            return "<Following_following(name='%s', name_grandchild='%s', grandchild_link='%s')>"\
            %(self.name, self.name_grandchild, self.grandchild_link)
    Base3.metadata.create_all(engine3)
    Session3 = sessionmaker(bind = engine3)
    session3 = Session3()


    engine4 = create_engine("sqlite:///table4.db", echo = False)
    Base4 = declarative_base()
    class Grandchild_image(Base4):
        __tablename__ = "grandchild_image"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        num_posts = Column(Integer)
        num_followers = Column(Integer)
        num_following = Column(Integer)
        link_image = Column(String)


        def __repr__(self):
            return "<Following_following(name_grandchild='%s', num_posts='%d', num_followers='%d', num_following='%d', link_image='%s')>"\
            %(self.name_grandchild, self.num_posts, self.num_followers, self.num_following, self.link_image)

    Base4.metadata.create_all(engine4)
    Session4 = sessionmaker(bind = engine4)
    session4 = Session4()





    engine5 = create_engine("sqlite:///table5.db", echo = False)
    Base5 = declarative_base()

    class To_follow(Base5):
        __tablename__ = "to_follow"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        test_train = Column(String)
        date = Column(String)
        link = Column(String)


        def __repr__(self):
            return "<To_follow(name_grandchild='%s', test_train='%s', date='%s', link='%s')>"\
            %(self.name_grandchild, self.test_train, self.date, self.link)


    Base5.metadata.create_all(engine5)

    Session5 = sessionmaker(bind = engine5)
    session5 = Session5()

    tocheck = [inst_to_dict(w) for w in session3.query(Following_following)]
    list_tofollow = []



    engine6 = create_engine("sqlite:///table6.db", echo = False)
    Base6 = declarative_base()

    class To_like(Base6):
        __tablename__ = "to_like"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        date_to_follow = Column(String)
        date_to_like = Column(String)
        post_link = Column(String)


        def __repr__(self):
            return "<To_like(name_grandchild='%s', date_to_follow='%s', date_to_like='%s', post_link='%s')>"\
            %(self.name_grandchild, self.date_to_follow, self.date_to_like, self.post_link)


    Base6.metadata.create_all(engine6)

    Session6 = sessionmaker(bind = engine6)
    session6 = Session6()



    tocheck = [inst_to_dict(w) for w in session3.query(Following_following)]
    list_tofollow = []

    for node in tocheck:
        if len([inst_to_dict(grand_link) for grand_link in session4.query(Grandchild_image).filter(Grandchild_image.name_grandchild == node["name_grandchild"])]) > 30:
            name_to_follow = node["name_grandchild"]
            link_to_follow = node["grandchild_link"]
            test_train_to_follow = random.choice(["test", "train"])
            date_to_follow = random_date("2017-07-20", "2017-07-23")

            entry = {"name_grandchild" : name_to_follow,
                    "test_train" : test_train_to_follow,
                    "date" : date_to_follow,
                    "link" : link_to_follow}

            list_tofollow.append(To_follow(**entry))


            tolike = [inst_to_dict(post) for post in session4.query(Grandchild_image).filter(Grandchild_image.name_grandchild == node["name_grandchild"])]
            like_rows = []
            for delta in list(range(3)):
                day = datetime.datetime.strptime(date_to_follow, "%Y-%m-%d")
                date_to_like = (day + timedelta(delta)).strftime("%Y-%m-%d")
                like_today = pop_images(tolike)
                for image in like_today:
                    like_entry = {"name_grandchild" : image["name_grandchild"],
                            "date_to_follow" : date_to_follow,
                            "date_to_like" : date_to_like,
                            "post_link" : image["link_image"]}

                    like_rows.append(To_like(**like_entry))

            session6.add_all(like_rows)
            session6.commit()

    session5.add_all(list_tofollow)
    session5.commit()

def random_date(start, end):
    start = datetime.datetime.strptime(str(start), "%Y-%m-%d")
    end = datetime.datetime.strptime(str(end), "%Y-%m-%d")

    delta = end - start
    int_delta = delta.days
    random_add = randrange(int_delta)
    result = start + timedelta(random_add)
    return str(result.strftime("%Y-%m-%d"))

def pop_images(input_list):
    count_rand = randrange(5, 11)
    popped = []
    while count_rand > 0:
        popped.append(input_list.pop(random.randrange(len(input_list))))
        count_rand -= 1
    return popped

def follow_and_like():

    # update_me_following_table()

    engine8 = create_engine("sqlite:///table8.db", echo = False)
    Base8 = declarative_base()

    class Following_cache(Base8):
        __tablename__ = "following_cache"
        num = Column(Integer, primary_key = True)
        link = Column(String)



        def __repr__(self):
            return "<Following_cache(link='%s')>" %(self.link)


    Base8.metadata.create_all(engine8)

    Session8 = sessionmaker(bind = engine8)
    session8 = Session8()


    engine2 = create_engine("sqlite:///table2.db", echo = False)
    Base2 = declarative_base()

    class Me_following(Base2):
        __tablename__ = "me_following"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        link = Column(String)
        date_checked = Column(String)


        def __repr__(self):
            return "<Me_following(name='%s', link='%s', date_checked='%s')>"\
            %(self.name, self.link, self.date_checked)


    Base2.metadata.create_all(engine2)


    Session2 = sessionmaker(bind = engine2)
    session2 = Session2()

    engine7 = create_engine("sqlite:///table7.db", echo = False)
    Base7 = declarative_base()

    class Log(Base7):
        __tablename__ = "log"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        kind = Column(String)
        link = Column(String)
        date_time = Column(String)
        date = Column(String)


        def __repr__(self):
            return "<Log((name_grandchild='%s', kind='%s', link='%s', date_time='%s', date='%s')>"\
            %(self.name_grandchild, self.kind, self.link, self.date_time, self.date)


    Base7.metadata.create_all(engine7)

    Session7 = sessionmaker(bind = engine7)
    session7 = Session7()


    engine5 = create_engine("sqlite:///table5.db", echo = False)
    Base5 = declarative_base()

    class To_follow(Base5):
        __tablename__ = "to_follow"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        test_train = Column(String)
        date = Column(String)
        link = Column(String)


        def __repr__(self):
            return "<To_follow(name_grandchild='%s', test_train='%s', date='%s', link='%s')>"\
            %(self.name_grandchild, self.test_train, self.date, self.link)


    Base5.metadata.create_all(engine5)

    Session5 = sessionmaker(bind = engine5)
    session5 = Session5()

    tocheck = [inst_to_dict(w) for w in session3.query(Following_following)]
    list_tofollow = []



    engine6 = create_engine("sqlite:///table6.db", echo = False)
    Base6 = declarative_base()

    class To_like(Base6):
        __tablename__ = "to_like"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        date_to_follow = Column(String)
        date_to_like = Column(String)
        post_link = Column(String)


        def __repr__(self):
            return "<To_like(name_grandchild='%s', date_to_follow='%s', date_to_like='%s', post_link='%s')>"\
            %(self.name_grandchild, self.date_to_follow, self.date_to_like, self.post_link)


    Base6.metadata.create_all(engine6)

    Session6 = sessionmaker(bind = engine6)
    session6 = Session6()





    follow_iterate = [inst_to_dict(w) for w in session5.query(To_follow).filter(To_follow.date == str(time.strftime("%Y-%m-%d")))]

    for user in follow_iterate:
        log_rows = []
        if len([inst_to_dict(w) for w in session8.query(Following_cache).filter(Following_cache.link == user["link"])]) == 0:
            browser.get(user["link"])
            time.sleep(0.2)
            try:
                if browser.find_element_by_xpath("//button[contains(text(),'Following')]"):
                    following_row = {"link" : user["link"]}

                    session8.add_all(Following_cache(**following_row))
                    session8.commit()

                    continue
            except NoSuchElementException:
                try:
                    # element = WebDriverWait(browser, 1).until(find)
                    browser.find_element_by_xpath("//button[contains(text(),'Follow')]").click()
                    time.sleep(0.5)
                except NoSuchElementException:
                    continue

            follow_log = {"name_grandchild" : user["name_grandchild"],
                        "kind" : "follow",
                        "link" : user["link"],
                        "date_time" : str(time.strftime("%Y-%m-%d  %H-%M-%S")),
                        "date" : str(time.strftime("%Y-%m-%d"))}



            first_likes = [inst_to_dict(link) for link in \
                                session6.query(To_like).filter(To_like.name_grandchild == user["name_grandchild"],
                                To_like.date_to_follow == str(time.strftime("%Y-%m-%d")),
                                To_like.date_to_like == str(time.strftime("%Y-%m-%d")))]

            for xoo in first_likes:
                if len([inst_to_dict(w) for w in session7.query(Log).filter(Log.link == xoo["post_link"])]) == 0:
                    browser.get(xoo["post_link"])
                    time.sleep(0.2)
                    try:
                        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/a[1]').click()
                    except NoSuchElementException:
                        continue
                    like_log = {"name_grandchild" : xoo["name_grandchild"],
                                "kind" : "like",
                                "link" : xoo["post_link"],
                                "date_time" : str(time.strftime("%Y-%m-%d  %H-%M-%S")),
                                "date" : str(time.strftime("%Y-%m-%d"))}

                    log_rows.append(Log(**like_log))
            log_rows.append(Log(**follow_log))


        session7.add_all(log_rows)
        session7.commit()

def follow_and_like():

    # update_me_following_table()

    engine8 = create_engine("sqlite:///table8.db", echo = False)
    Base8 = declarative_base()

    class Following_cache(Base8):
        __tablename__ = "following_cache"
        num = Column(Integer, primary_key = True)
        link = Column(String)



        def __repr__(self):
            return "<Following_cache(link='%s')>" %(self.link)


    Base8.metadata.create_all(engine8)

    Session8 = sessionmaker(bind = engine8)
    session8 = Session8()


    engine2 = create_engine("sqlite:///table2.db", echo = False)
    Base2 = declarative_base()

    class Me_following(Base2):
        __tablename__ = "me_following"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        link = Column(String)
        date_checked = Column(String)


        def __repr__(self):
            return "<Me_following(name='%s', link='%s', date_checked='%s')>"\
            %(self.name, self.link, self.date_checked)


    Base2.metadata.create_all(engine2)


    Session2 = sessionmaker(bind = engine2)
    session2 = Session2()

    engine7 = create_engine("sqlite:///table7.db", echo = False)
    Base7 = declarative_base()

    class Log(Base7):
        __tablename__ = "log"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        kind = Column(String)
        link = Column(String)
        date_time = Column(String)
        date = Column(String)


        def __repr__(self):
            return "<Log((name_grandchild='%s', kind='%s', link='%s', date_time='%s', date='%s')>"\
            %(self.name_grandchild, self.kind, self.link, self.date_time, self.date)


    Base7.metadata.create_all(engine7)

    Session7 = sessionmaker(bind = engine7)
    session7 = Session7()


    engine5 = create_engine("sqlite:///table5.db", echo = False)
    Base5 = declarative_base()

    class To_follow(Base5):
        __tablename__ = "to_follow"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        test_train = Column(String)
        date = Column(String)
        link = Column(String)


        def __repr__(self):
            return "<To_follow(name_grandchild='%s', test_train='%s', date='%s', link='%s')>"\
            %(self.name_grandchild, self.test_train, self.date, self.link)


    Base5.metadata.create_all(engine5)

    Session5 = sessionmaker(bind = engine5)
    session5 = Session5()

    tocheck = [inst_to_dict(w) for w in session3.query(Following_following)]
    list_tofollow = []



    engine6 = create_engine("sqlite:///table6.db", echo = False)
    Base6 = declarative_base()

    class To_like(Base6):
        __tablename__ = "to_like"
        num = Column(Integer, primary_key = True)
        name_grandchild = Column(String)
        date_to_follow = Column(String)
        date_to_like = Column(String)
        post_link = Column(String)


        def __repr__(self):
            return "<To_like(name_grandchild='%s', date_to_follow='%s', date_to_like='%s', post_link='%s')>"\
            %(self.name_grandchild, self.date_to_follow, self.date_to_like, self.post_link)


    Base6.metadata.create_all(engine6)

    Session6 = sessionmaker(bind = engine6)
    session6 = Session6()





    follow_iterate = [inst_to_dict(w) for w in session5.query(To_follow).filter(To_follow.date == "2017-07-22")]

    for user in follow_iterate:
        log_rows = []
        if len([inst_to_dict(w) for w in session8.query(Following_cache).filter(Following_cache.link == user["link"])]) == 0:
            browser.get(user["link"])
            time.sleep(0.6)
            try:
                if browser.find_element_by_xpath("//button[contains(text(),'Following')]"):
                    following_row = {"link" : user["link"]}
                    following_rows = []

                    following_rows.append(Following_cache(**following_row))
                    session8.add_all(following_rows)
                    session8.commit()

                    continue
            except NoSuchElementException:
                try:
                    # element = WebDriverWait(browser, 1).until(find)
                    browser.find_element_by_xpath("//button[contains(text(),'Follow')]").click()
                    time.sleep(10)

                    if browser.find_element_by_xpath("//button[contains(text(),'Following')]"):
                        following_row = {"link" : user["link"]}
                        following_rows = []

                        following_rows.append(Following_cache(**following_row))
                        session8.add_all(following_rows)
                        session8.commit()

                        follow_log = {"name_grandchild" : user["name_grandchild"],
                                    "kind" : "follow",
                                    "link" : user["link"],
                                    "date_time" : str(time.strftime("%Y-%m-%d  %H-%M-%S")),
                                    "date" : "2017-07-22"}



                        first_likes = [inst_to_dict(link) for link in \
                                            session6.query(To_like).filter(To_like.name_grandchild == user["name_grandchild"],
                                            To_like.date_to_follow == "2017-07-22",
                                            To_like.date_to_like == "2017-07-22")]

                        for xoo in first_likes:
                            if len([inst_to_dict(w) for w in session7.query(Log).filter(Log.link == xoo["post_link"])]) == 0:
                                browser.get(xoo["post_link"])
                                time.sleep(0.2)
                                try:
                                    browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/a[1]').click()
                                except NoSuchElementException:
                                    continue
                                like_log = {"name_grandchild" : xoo["name_grandchild"],
                                            "kind" : "like",
                                            "link" : xoo["post_link"],
                                            "date_time" : str(time.strftime("%Y-%m-%d  %H-%M-%S")),
                                            "date" : "2017-07-22"}

                                log_rows.append(Log(**like_log))

                except NoSuchElementException:
                    continue


            log_rows.append(Log(**follow_log))


        session7.add_all(log_rows)
        session7.commit()

def unfollow():
    engine2 = create_engine("sqlite:///table2-1.db", echo = False)
    Base2 = declarative_base()

    class Me_following(Base2):
        __tablename__ = "me_following"
        num = Column(Integer, primary_key = True)
        name = Column(String)
        link = Column(String)
        date_checked = Column(String)


        def __repr__(self):
            return "<Me_following(name='%s', link='%s', date_checked='%s')>"\
            %(self.name, self.link, self.date_checked)


    Base2.metadata.create_all(engine2)
    Session2 = sessionmaker(bind = engine2)
    session2 = Session2()



    # engine2 = create_engine("sqlite:///table2.db", echo = False)
    # Base2 = declarative_base()

    list_unfollow = [inst_to_dict(w) for w in session2.query(Me_following).filter(Me_following.date_checked != "2017-07-15")]

    for unfollow_item in list_unfollow:
        browser.get(str(unfollow_item["link"]))
        try :
            time.sleep(1)
            browser.find_element_by_xpath("//button[contains(text(),'Following')]").click()
            time.sleep(1)
        except NoSuchElementException:
            print("Passing")
            continue
        except StaleElementReferenceException:
            continue




# browser.find_element_by_xpath("//button[contains(text(),'Follow')]").click()
# browser.find_element_by_xpath("//button[contains(text(),'Following')]")
#
#
# browser.get("https://www.instagram.com/lavria/")




# delete_test = browser.find_element_by_xpath("//p[contains(.,'Follow to see their photos and videos.')]").text
# delete_test = browser.find_element_by_xpath("//h2[contains(text(),'No posts yet.')]").text


# if browser.find_element_by_xpath("//p[contains(.,'Follow to see their photos and videos.')]").text or browser.find_element_by_xpath("//h2[contains(text(),'No posts yet.')]").text:
#     print("pew")
#
# if browser.find_element_by_xpath("//h2[contains(text(),'No posts yet.')]").text or find_element_by_xpath("//p[contains(.,'Follow to see their photos and videos.')]").text:
#     print("pew")


# [pew.find_element_by_css_selector('a').get_attribute('href') for pew in browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div[1]').find_elements_by_tag_name("div")]
#
#
# ### get rows
# rows = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div[1]').find_elements_by_tag_name("div")
# ## get first rows
# rows[0]
# ## get the first image giv
# rows[0].find_elements_by_tag_name("div")
#
#
# driver.find_element_by_css_selector("a[href*='example@example.com']")
# [pew.get_attribute('href') for pew in browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")]
#
#
# while len([pew.get_attribute('href') for pew in browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")]) < stats[0]:
#     action_chains.ActionChains(browser).move_to_element(browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")[-1]).perform()
#
# while len([pew.get_attribute('href') for pew in browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")]) < 600:
#     action_chains.ActionChains(browser).move_to_element(browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")[-1]).perform()


Base1 = declarative_base()
Base2 = declarative_base()
Base3 = declarative_base()
Base4 = declarative_base()
Base5 = declarative_base()
Base6 = declarative_base()
Base7 = declarative_base()
Base8 = declarative_base()

class My_follower(Base1):
    __tablename__ = "my_followers"
    num = Column(Integer, primary_key = True)
    name = Column(String)
    date_checked = Column(String)


    def __repr__(self):
        return "<My_follower(name='%s', date_checked='%s')>"\
        %(self.name, self.date_checked)

class Me_following(Base2):
    __tablename__ = "me_following"
    num = Column(Integer, primary_key = True)
    name = Column(String)
    link = Column(String)
    date_checked = Column(String)


    def __repr__(self):
        return "<Me_following(name='%s', link='%s', date_checked='%s')>"\
        %(self.name, self.link, self.date_checked)

class Following_following(Base3):
    __tablename__ = "following_following"
    num = Column(Integer, primary_key = True)
    name = Column(String)
    name_grandchild = Column(String)
    grandchild_link = Column(String)


    def __repr__(self):
        return "<Following_following(name='%s', name_grandchild='%s', grandchild_link='%s')>"\
        %(self.name, self.name_grandchild, self.grandchild_link)

class Grandchild_image(Base4):
    __tablename__ = "grandchild_image"
    num = Column(Integer, primary_key = True)
    name_grandchild = Column(String)
    num_posts = Column(Integer)
    num_followers = Column(Integer)
    num_following = Column(Integer)
    link_image = Column(String)


    def __repr__(self):
        return "<Following_following(name_grandchild='%s', num_posts='%d', num_followers='%d', num_following='%d', link_image='%s')>"\
        %(self.name_grandchild, self.num_posts, self.num_followers, self.num_following, self.link_image)

class To_follow(Base5):
    __tablename__ = "to_follow"
    num = Column(Integer, primary_key = True)
    name_grandchild = Column(String)
    test_train = Column(String)
    date = Column(String)
    link = Column(String)


    def __repr__(self):
        return "<To_follow(name_grandchild='%s', test_train='%s', date='%s', link='%s')>"\
        %(self.name_grandchild, self.test_train, self.date, self.link)

class To_like(Base6):
    __tablename__ = "to_like"
    num = Column(Integer, primary_key = True)
    name_grandchild = Column(String)
    date_to_follow = Column(String)
    date_to_like = Column(String)
    post_link = Column(String)


    def __repr__(self):
        return "<To_like(name_grandchild='%s', date_to_follow='%s', date_to_like='%s', post_link='%s')>"\
        %(self.name_grandchild, self.date_to_follow, self.date_to_like, self.post_link)

class Log(Base7):
    __tablename__ = "log"
    num = Column(Integer, primary_key = True)
    name_grandchild = Column(String)
    kind = Column(String)
    link = Column(String)
    date_time = Column(String)
    date = Column(String)


    def __repr__(self):
        return "<Log((name_grandchild='%s', kind='%s', link='%s', date_time='%s', date='%s')>"\
        %(self.name_grandchild, self.kind, self.link, self.date_time, self.date)

class Following_cache(Base8):
    __tablename__ = "following_cache"
    num = Column(Integer, primary_key = True)
    link = Column(String)

    def __repr__(self):
        return "<Following_cache(link='%s')>" %(self.link)
# pew = browser.find_element_by_xpath("//h2[contains(text(),'Sorry, this page isn't available.')]").text

# len([inst_to_dict(link) for link in \
#                     session6.query(To_like).filter(To_like.date_to_follow == str(time.strftime("%Y-%m-%d")),
#                     To_like.date_to_like == str(time.strftime("%Y-%m-%d")))])

# len([pew.get_attribute('href') for pew in browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "taken-by")])
# get_basic_numbers()[0]

# def inst_to_dict(inst, delete_id = True):
#     dat = {}
#     for column in inst.columns:
#         dat[column.name] = getattr(inst, column.name)
#     if delete_id:
#         dat.pop("id")
#     return dat


# dict = {'Name': 'Zara', 'Age': 7}
#
# print "Value : %s" %  dict.values()

# session.query(Winner).filter(Winner.category == "Physics", Winner.nationality != "Swiss")




### Open the browser
browser = init_driver()
browser.wait = WebDriverWait(browser, 5)

### Go log in account
open_and_login()

### Get my account Stats
# me = get_basic_numbers()
# get_basic_numbers()

### create the first followers table
# create_my_followers_table()
# create_me_following_table()
# create_me_following_table()
# update_me_following_table()
# alt_update_me_following_table()

unfollow()

# update_my_followers_table()
# ###
# # create_tofollow_table()
#
# ###
# follow_and_like()
#
#
# ## Update my stuff
# # update_my_followers_table()
# # update_me_following_table()
#
# ## create the table of grandchildren
# #create_grandchild_following_table()
# ### actual grandchildren table
# # create_grandchild_images()
#
#
#
#
# engine3 = create_engine("sqlite:///table3.db", echo = False)
# Base3 = declarative_base()
#
# class Following_following(Base3):
#     __tablename__ = "following_following"
#     num = Column(Integer, primary_key = True)
#     name = Column(String)
#     name_grandchild = Column(String)
#     grandchild_link = Column(String)
#
#     def __repr__(self):
#         return "<Following_following(name='%s', name_grandchild='%s', grandchild_link='%s')>"\
#         %(self.name, self.name_grandchild, self.grandchild_link)
# Base3.metadata.create_all(engine3)
# Session3 = sessionmaker(bind = engine3)
# session3 = Session3()
#
#
#
# engine4 = create_engine("sqlite:///table4.db", echo = False)
# Base4 = declarative_base()
#
#
#
#
#
#
#
#
#
#
# kaahzvi
# # len(list(session3.query(Following_following)))
# len([inst_to_dict(w) for w in session3.query(Following_following).filter(Following_following.name_grandchild == "daria.raz00m")])
#
# todel = session3.query(Following_following).filter(Following_following.name_grandchild == "daria.raz00m")
# todel.delete(synchronize_session = False)
# session3.commit()
#
#
# browser.get("https://www.instagram.com/sharrrapova/")
# try : pew = browser.find_element_by_xpath("//p[contains(.,'Follow to see their photos and videos.')]").text
# except NoSuchElementException:
#     print("Not a private account")
#
# pew = browser.find_element_by_xpath("//p[contains(.,'Follow to see their photos and videos.')]").text
# browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/h2')
#
# browser.get("https://www.instagram.com/do.not.beautiful.girl/")
# browser.get("https://www.instagram.com/sharrrapova/")
# # https://www.instagram.com/do.not.beautiful.girl/
# # https://www.instagram.com/sharrrapova/
#
#
#
#
#
#
# engine4 = create_engine("sqlite:///table4.db", echo = False)
# Base4 = declarative_base()
# class Grandchild_image(Base4):
#     __tablename__ = "grandchild_image"
#     num = Column(Integer, primary_key = True)
#     name_grandchild = Column(String)
#     num_posts = Column(Integer)
#     num_followers = Column(Integer)
#     num_following = Column(Integer)
#     link_image = Column(String)
#
#
#     def __repr__(self):
#         return "<Following_following(name_grandchild='%s', num_posts='%d', num_followers='%d', num_following='%d', link_image='%s')>"\
#         %(self.name_grandchild, self.num_posts, self.num_followers, self.num_following, self.link_image)
#
# Base4.metadata.create_all(engine4)
# Session4 = sessionmaker(bind = engine4)
# session4 = Session4()
#
#
# len([inst_to_dict(w) for w in session4.query(Grandchild_image).filter(Grandchild_image.name_grandchild == "daria.raz00m")])
#
# todel = session4.query(Grandchild_image).filter(Grandchild_image.name_grandchild == "daria.raz00m")
# todel.delete(synchronize_session = False)
# session4.commit()
#
# len([inst_to_dict(w) for w in session4.query(Grandchild_image)])
#
#
#
#
#
#
# engine1 = create_engine("sqlite:///table1-1.db", echo = False)
# Base1 = declarative_base()
#
# class My_follower(Base1):
#     __tablename__ = "my_followers"
#     num = Column(Integer, primary_key = True)
#     name = Column(String)
#     date_checked = Column(String)
#
#
#     def __repr__(self):
#         return "<My_follower(name='%s', date_checked='%s')>"\
#         %(self.name, self.date_checked)
#
#
# Base1.metadata.create_all(engine1)
# Session1 = sessionmaker(bind = engine1)
# session1 = Session1()
#
# len([inst_to_dict(w) for w in session1.query(My_follower)])
#
#
#
#
#
#
#
#
#
# engine2 = create_engine("sqlite:///table2-1.db", echo = False)
# Base2 = declarative_base()
#
# class Me_following(Base2):
#     __tablename__ = "me_following"
#     num = Column(Integer, primary_key = True)
#     name = Column(String)
#     link = Column(String)
#     date_checked = Column(String)
#
#
#     def __repr__(self):
#         return "<Me_following(name='%s', link='%s', date_checked='%s')>"\
#         %(self.name, self.link, self.date_checked)
#
#
# Base2.metadata.create_all(engine2)
# Session2 = sessionmaker(bind = engine2)
# session2 = Session2()
#
#
#
# engine2 = create_engine("sqlite:///table2.db", echo = False)
# Base2 = declarative_base()
#
#
# [inst_to_dict(w) for w in session2.query(Me_following)]
# len([inst_to_dict(w) for w in session2.query(Me_following)])
# len([inst_to_dict(w) for w in session2.query(Me_following).filter(Me_following.date_checked != "2017-07-15")])
#
#
#
#
#
#
#
#
#
#
#
# engine5 = create_engine("sqlite:///table5.db", echo = False)
# Base5 = declarative_base()
#
# class To_follow(Base5):
#     __tablename__ = "to_follow"
#     num = Column(Integer, primary_key = True)
#     name_grandchild = Column(String)
#     test_train = Column(String)
#     date = Column(String)
#     link = Column(String)
#
#
#     def __repr__(self):
#         return "<To_follow(name_grandchild='%s', test_train='%s', date='%s', link='%s')>"\
#         %(self.name_grandchild, self.test_train, self.date, self.link)
#
#
# Base5.metadata.create_all(engine5)
#
# Session5 = sessionmaker(bind = engine5)
# session5 = Session5()
#
# [inst_to_dict(w) for w in session5.query(To_follow)]
# len([inst_to_dict(w) for w in session5.query(To_follow)])
# len([inst_to_dict(w) for w in session5.query(To_follow).filter(To_follow.test_train == "test")])
# len([inst_to_dict(w) for w in session5.query(To_follow).filter(To_follow.test_train == "train")])
#
#
#
# engine6 = create_engine("sqlite:///table6.db", echo = False)
# Base6 = declarative_base()
#
# class To_like(Base6):
#     __tablename__ = "to_like"
#     num = Column(Integer, primary_key = True)
#     name_grandchild = Column(String)
#     date_to_follow = Column(String)
#     date_to_like = Column(String)
#     post_link = Column(String)
#
#
#     def __repr__(self):
#         return "<To_like(name_grandchild='%s', date_to_follow='%s', date_to_like='%s', post_link='%s')>"\
#         %(self.name_grandchild, self.date_to_follow, self.date_to_like, self.post_link)
#
#
# Base6.metadata.create_all(engine6)
#
# Session6 = sessionmaker(bind = engine6)
# session6 = Session6()
#
#
# [inst_to_dict(w) for w in session6.query(To_like)]
# len([inst_to_dict(w) for w in session6.query(To_like)])
# len([inst_to_dict(w) for w in session6.query(To_like).filter(To_like.name_grandchild == "josephinenoel")])
# len([inst_to_dict(w) for w in session6.query(To_like).filter(To_follow.test_train == "train")])
#
# #
# # "1,255.".replace(",", "").replace(".", "")
# #
# #
# #
# #
# #
# #
# #
# #
# # engine2 = create_engine("sqlite:///table2.db", echo = True)
# # Base2 = declarative_base()
# # Base2.metadata.create_all(engine2)
# # Session2 = sessionmaker(bind = engine2)
# # session2 = Session2()
# # pew = session2.query(Me_following)
# # session2.query(Me_following).count()
# # [inst_to_dict(w)["link"] for w in pew]
# #
# #
# # # me_following_rows = [Me_following(**w) for w in list_following]
# # # session2.add_all(me_following_rows)
# # # session2.commit()
# #
# #
# #
# #
# #
# #
# # # me_following_rows = [Me_following(**w) for w in list_following]
# # # session2.add_all(me_following_rows)
# # # session2.commit()
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# # me_following = get_list_of_following()
# # # me_following
# # # following_ids = list(map(lambda x: x.split("/")[-2], my_following))
# # my_followers = get_list_of_followers()
# #
# # # followers_ids = list(map(lambda x: x.split("/")[-2], my_followers))
# #
# # list_of_things = []
# #
# # for i in my_followers:
# #     entry = {"name" : i.split("/")[-2],
# #             "date_checked" : str(time.strftime("%Y-%m-%d"))}
# #     list_of_things.append(entry)
# #
# # list_of_things
# #
# #
# # engine = create_engine("sqlite:///table1.db", echo = True)
# # Base = declarative_base()
# #
# #
# #
# #
# # # class My_follower(Base):
# # #     __tablename__ = "my_followers"
# # #     id = Column(Integer, primary_key = True)
# # #     name = Column(String)
# # #     date_checked = Column(String)
# # #
# # #
# # #     def __repr__(self):
# # #         return "<My_follower(name='%s', date_checked='%s')>"\
# # #         %(self.name, self.date_checked)
# #
# # Base.metadata.create_all(engine)
# #
# #
# # Session = sessionmaker(bind = engine)
# # session = Session()
# # session.new
# # my_followers_rows = [My_follower(**w) for w in list_of_things]
# # [w["name"] for w in list_of_things]
# # list_of_things[0]["name"]
# # session.add_all(my_followers_rows)
# # # session.new
# # session.commit()
# #
# # session.query(Winner).filter(Winner.category == "Physics", Winner.nationality != "Swiss")
# #
# # len(list(session.query(My_follower).filter(My_follower.name == "arinaromanova__").order_by("name")))
# # len(list(session.query(My_follower).filter(My_follower.name == list_of_things[0]["name"])))==0
# #
# # pew = session.query(My_follower).filter(My_follower.name == "arinaromanova__")
# # pew = session.query(My_follower)
# # session2.query(Me_following)
# # list_pew = [inst_to_dict(w) for w in pew]
# # list_pew[1]
# #
# # session.query(My_follower).get(1)
# # from sqlalchemy import inspect
# # insp = inspect(pew)
# #
# #
# # inst_to_dict(pew)
# # pew = [w for w in pew]
# # pew
# # session.close()
# # engine.dispose()
#
# # get_basic_numbers()[2]
#
# # print(random_date("2017-07-20", "2017-07-23"))
# # random.choice(["test", "train"])
# # str(time.strftime("%Y-%m-%d"))
