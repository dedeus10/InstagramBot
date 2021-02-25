#Import the libs which we need
from selenium import webdriver
from time import sleep
import numpy as np

class instagramBot:
    def __init__(self, username, password):
        #Constructor
        self.user = username
        self.password = password

        #Open web service on instagram
        self.driver = webdriver.Chrome()
        self.driver.get('https://instagram.com')
        sleep(2)

        #Fill username
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.user)
        #Fill password
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.password)
        #Click on Log In 
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(6)
        #Choose Not now for remember password
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(4)
        #Choose Not now for notifications
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)
        #Click on the profile button
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/')]".format(self.user)).click()
        sleep(2)

    def get_names(self):
        '''
        #@brief: This method will control the scroll from the list box of followers/following
        first of all, instagram create a box with IDK maybe 20 users, then if you scroll down
        the box will load 20 more and so on. So we need a block of code to control the time b/w
        fetch the usernames and scroll down the box
        #@return: names-> a list with usernames (strings)
        '''
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        last_ht , ht = 0,1
        while(last_ht != ht):
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name != '']
        
        self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button').click()
        return names
        

    def get_following(self):
        '''
        #@brief: This method get the usernames of the ones you are currently following
        The usernames are stored in the list "following"
        '''
        #Click on Following
        self.driver.find_element_by_xpath("//a[contains(@href,'following')]").click()
        sleep(1)
        aux = self.get_names()

        self.following = []
        for user_name in aux:
            if(user_name != ''):
                self.following.append(user_name)

        print(">>Following: \n",self.following)
        print("LEN: ",len(self.following))
    
    def get_followers(self):
        '''
        #@brief: This method get the usernames of who follow you
        The usernames are stored in the list "followers"
        '''
        #Click on Followers
        self.driver.find_element_by_xpath("//a[contains(@href,'followers')]").click()
        sleep(1)
        aux = self.get_names()

        self.followers = []
        for user_name in aux:
            if(user_name != ''):
                self.followers.append(user_name)

        print(">>Followers: \n",self.followers)
        print("LEN: ",len(self.followers))

    def get_motherfuckers(self):
        '''
        #@brief: This method extract the usernames for those who don't follow you back
        The usernames are stored in the list "motherfuckers"
        While the usernames of who do follow you back are stored in the list "good_guys"
        '''
        self.mother_fuckers, self.good_guys = [],[]
        for user_following in self.following:
            if(user_following != ''):
                if(user_following in self.followers):
                    self.good_guys.append(str(user_following))
                else:
                    self.mother_fuckers.append(str(user_following))
        print(">>MotherFuckers:\n")
        print(self.mother_fuckers)
        print("LEN: ",len(self.mother_fuckers))

    def export_data(self):
        '''
        @brief: This method just export each one of the lists to txt files
        Also, print the report with the numbers of each category
        @return: void
        '''

        np.savetxt('following.txt', np.asarray(self.following), fmt='%s')
        np.savetxt('followers.txt', np.asarray(self.followers), fmt='%s')
        np.savetxt('motherfuckers.txt', np.asarray(self.mother_fuckers), fmt='%s')
        np.savetxt('good_guys.txt', np.asarray(self.good_guys), fmt='%s')
        
        print("\n## REPORT ###:")
        print(">> You have %d Followers"%(len(self.followers)))
        print(">> You are Following %d users"%(len(self.following)))
        print(">> %d motherfuckers don't follow you back"%(len(self.mother_fuckers)))


###########################################################
your_username = 'dedeus_lf'
your_password = 'PASSWORD'

myBot = instagramBot(your_username, your_password)
myBot.get_following()
myBot.get_followers()
myBot.get_motherfuckers()
myBot.export_data()