import urllib    
import urllib2    
import re
f=open('url_dic','w')
for u in open('urls','r').readlines():
	#url=u.strip().strip('/').strip('http://').strip('https://')
	#url = 'http://www.hao123.com'
	url=u
	if len(url)<20:
		continue
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    
	headers = { 'User-Agent' : user_agent }   
	values = {'name' : 'WHY',    
			  'location' : 'SDU',    
			  'language' : 'Python' }  
	data = urllib.urlencode(values)    
	req = urllib2.Request(url, data, headers)
	try:
		response = urllib2.urlopen(req)
	except:
		continue
	content = response.read()   
	res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
	target_url = re.compile(res_url,re.DOTALL).findall(content)
	for uu in target_url:
		uu=uu.strip().strip('/').strip('http://').strip('https://')
		uu='http://%s' % uu
		uline="%s %s\n" % (uu.strip(), url.strip())
		f.writelines(uline)
f.close()