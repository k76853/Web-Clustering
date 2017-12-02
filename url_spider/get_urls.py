import urllib    
import urllib2    
import re
url_dic={}
url = 'http://www.hao123.com'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    
headers = { 'User-Agent' : user_agent }   
values = {'name' : 'WXJ',    
          'location' : 'SZ',    
          'language' : 'Python' }  
data = urllib.urlencode(values)    
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
content = response.read()   
res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
target_url = re.compile(res_url,re.DOTALL).findall(content)
f=open('urls','w')
for u in target_url:
	u=u.strip().strip('/').strip('http://').strip('https://')
	u='http://%s' % u
	url_dic[url]=u
	f.writelines(u);
	f.writelines('\n');
f.close()