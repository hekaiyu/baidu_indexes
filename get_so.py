#coding=utf-8
#工作：根据url查询百度、360、搜狗是否有收录
#搜狗数量有限
import urllib
import requests
import time
import sys  
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class UnicodeStreamFilter:  
	def __init__(self, target):  
		self.target = target  
		self.encoding = 'utf-8'  
		self.errors = 'replace'  
		self.encode_to = self.target.encoding  
	def write(self, s):  
		if type(s) == str:  
			s = s.decode("utf-8")  
		s = s.encode(self.encode_to, self.errors).decode(self.encode_to)  
		self.target.write(s)  
		  
if sys.stdout.encoding == 'cp936':  
	sys.stdout = UnicodeStreamFilter(sys.stdout)  
#以上为cmd下utf-8中文输出的终极解决方案！
print "************************************"
print "**用处：收录查询工具"
print "**平台：360，百度，搜狗"
print "**作者：开水"
print "**网站：www.hekaiyu.cn"
print "************************************\n"
headers={
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
}
def get_so(url):
	myurl="http://www.so.com/s?q=%s"%url
	r=requests.get(myurl,headers=headers)
	ret=r.text
	if "找不到该URL" in ret:
		print url,'360未收录'
		f = open('sourl.txt','a')
		f.write(url+'\t'+'未收录'+'\n')
		f.close()
		return 0
	if "找到相关结果约" in ret:
		print url,'360已收录'
		f = open('sourl.txt','a')
		f.write(url+'\t'+'已收录'+'\n')
		f.close()
		return 1
		
		
def baidu_html(baiduURL):
	print baiduURL
	x=1
	while x<5:
		try:
			print "第%s次查询"%x,baiduURL
			html= requests.get(baiduURL, headers = headers,timeout=30)
			r=html.json()
			break
		except:
			x=x+1
			continue
	if x>=5:
		r={"feed":{"all": "0","entry":[{"title":"开水网络","url":"超时，请重查"}]}}
	return r
def get_baidu_html(r):
	all=r.get('feed').get ('all')
	if all==0:
		print url,'百度未收录'
		f = open('baiduurl.txt','a')
		f.write(url+'\t'+'未收录'+'\n')
		f.close()
		return 0
	else:
		print url,'百度已收录'
		f = open('baiduurl.txt','a')
		f.write(url+'\t'+'已收录'+'\n')
		f.close()
		return 1
def get_sogou(url):
	myurl="http://www.sogou.com/web?query=%s"%url
	r=requests.get(myurl,headers=headers)
	ret=r.text
	if "您是不是想直接访问" in ret:
		print url,'搜狗未收录'
		f = open('sogouurl.txt','a')
		f.write(url+'\t'+'未收录'+'\n')
		f.close()
		return 0
	if "找到约" in ret:
		print url,'搜狗已收录'
		f = open('sogouurl.txt','a')
		f.write(url+'\t'+'已收录'+'\n')
		f.close()
		return 1
	elif "verify_page" in ret:
		print "\n搜狗出现异常,想其他办法把！"
		return
if __name__=="__main__":
	urls=open('url.txt','r').readlines()
	x=0
	y=0
	oknum=0
	lostnum=0
	sgx=0
	sgy=0
	for url in urls:
		baiduURL= 'http://www.baidu.com/s?wd=%s&tn=json' % url.strip()
		r=baidu_html(baiduURL)
		if get_baidu_html(r):
			oknum+=1
		else:
			lostnum+=1
	for url in urls:
		if get_so(url.strip()):
			x=x+1
		else:
			y=y+1
	for url in urls:
		if get_sogou(url.strip()):
			sgx=sgx+1
		else:
			sgy=sgy+1
	z=x+y
	print "\n************************************"
	print "**本次共查询链接：%s 条"%z
	print "**百度收录数据共 %s 条"%oknum
	print "**百度未收录数据共 %s 条"% lostnum
	print "**360收录数据共 %s 条"%x
	print "**360未收录数据共 %s 条"% y
	print "**搜狗收录数据共 %s 条"%sgx
	print "**搜狗未收录数据共 %s 条"% sgy
	print "************************************"