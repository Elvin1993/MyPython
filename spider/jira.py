#coding=utf-8
from bs4 import BeautifulSoup
import requests,os,shutil,sys,math,schedule,time

baseurl = 'http://jira.xxx.com:8080'
loginurl = baseurl+'login.jsp'
logpath = 'C:\\log\\'
formData = {'os_username':'xxxxx',
            'os_password':'xxxxx',
            'os_destination':'',
            'atl_token':'',
            'login':'%E7%99%BB%E5%BD%95'
            }
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

def getJIRALists():
    session = login()
    jiralisthtml = session.get(baseurl+'/browse/xxxxx?jql=assignee = currentUser() AND resolution = unresolved ORDER BY priority DESC, created ASC')
    soup = BeautifulSoup(jiralisthtml.text,'lxml')
    issuelist = soup.select('ol.issue-list li')
    print('+++++++++++++++++++++++++++++++++++++JIRA LISTS++++++++++++++++++++++++++++++++++++++')
    for issue in issuelist:
        jiraid = issue.get('data-key')
        jiratitle = issue.get('title')
        print('jiraid: %s title: %s' %(jiraid,jiratitle))
        getJIRAParams(session,jiraid)
    print('+++++++++++++++++++++++++++++++++++++JIRA LISTS++++++++++++++++++++++++++++++++++++++')
    
def getJIRAParams(session,jiraid):
    jirahtml = session.get(baseurl+'/browse/'+jiraid)
    soup = BeautifulSoup(jirahtml.text,'lxml')
    #projectname = soup.select('#project-name-val')[0].get_text()
    #K600_CLA_CO_8.1
    #jiraissue = soup.select('.issue-link')
    #jiraid = jiraissue[0].get_text()
    #GAAOCOA-64
    #jirahref = jiraissue[0].get('href')
    #/browse/GAAOCOA-64
    #jirasummary = soup.select('#summary-val')[0].get_text()
    #[BUG][Edward Monroy][CO][M5CLAROCO-63] Call to voice mail fail
    jiradescription = soup.select('#description-val')[0].get_text()
    if jiradescription.find('\\\\') > 0:
        logstartpos = jiradescription.index('\\\\')
        logurl = jiradescription[logstartpos:]
        logendpos = logurl.index('\n')
        logurl = logurl[:logendpos]
        print('logurl: '+logurl)
        #logurl = logurl.replace('\\','/')
        if not os.path.isdir(logurl):
            destfileindex = logurl.rindex('\\') +1
            destfile = logurl[destfileindex:]
            copyFile(jiraid,logurl,destfile,False)
        else:
            srcfiles = os.listdir(logurl)
            for name in srcfiles:
                if name.find(jiraid):
                    if os.path.isdir(name):
                        copyFile(jiraid,srcfile,name,True)
                    else:
                        srcfile = logurl+'\\'+name
                        copyFile(jiraid,srcfile,name,False)

    else:
        attachment = soup.select('.attachment-title a')
        if len(attachment) > 0:
            attachment = baseurl+attachment[0].get('href')
            print('download log: %s' %attachment)
            downloadfile(session,attachment,jiraid)
        else:
            print('%s has not log' %jiraid)



def copyFile(jiraid,srcFile,destfile,srcFileIsDir):
    print('download log for %s srcfile: %s destfile: %s srcFileIsDir: %s ' %(jiraid,srcFile,destfile,srcFileIsDir))
    jiraid = logpath+jiraid
    if not os.path.exists(srcFile):
        print ('no found '+srcFile)  
        return False
    if os.path.exists(jiraid):
        print ('%s has been download' %jiraid)
        return False
    os.makedirs(jiraid)
    destfile = jiraid+'\\'+destfile
    if srcFileIsDir:
        shutil.copy(srcFile,destfile)
    else:
        shutil.copyfile(srcFile,destfile)
        

def downloadfile(session,url,jiraid):
    jiraid = logpath+jiraid
    if os.path.exists(jiraid):
        print ('%s\'s log has been download' %jiraid)
        return False
    os.makedirs(jiraid)
    s = session.get(url,stream=True)
    chunk_size = 1024
    content_size = int(s.headers['content-length'])
    fileindex = url.rindex('/')+1
    destfile = jiraid+'\\'+url[fileindex:]
    with open(destfile, "wb") as file:
        for data in s.iter_content(chunk_size=chunk_size):
            file.write(data)
            file_size = os.path.getsize(destfile)
            progressbar(file_size,content_size)

def progressbar(cur,total):  
    percent = '{:.2%}'.format(cur / total)  
    sys.stdout.write('\r')  
    sys.stdout.write('[%-50s] %s' % ( '=' * int(math.floor(cur * 50 /total)),percent))  
    sys.stdout.flush()  
    if cur == total:  
        sys.stdout.write('\n')


def login():
    session = requests.session()
    session.post(loginurl, data=formData)
    return session

schedule.every(1).minutes.do(getJIRALists)

while True:
    schedule.run_pending()
    time.sleep(1)