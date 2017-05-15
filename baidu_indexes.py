#coding=utf-8
#工作：根据软件发布的标题查询是否有收录
import requests
import re
from bs4 import BeautifulSoup
import sys  
reload(sys)
sys.setdefaultencoding( "utf-8" )
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
headers={
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
}
url='http://www.ciku5.com/s?wd=%e9%a6%99%e8%8f%87&citype=0&p=1'
gethtml=requests.get(url,headers=headers).text
words=re.findall('<tr id="tr.*?">(.*?)</tr>',gethtml,re.S)

for word in words:
	word=BeautifulSoup(word,"xml")
	word=word.a.text
	print 'words','0'
	print word,'0'