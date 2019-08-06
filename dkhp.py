import requests
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen,Request
from urllib.parse import quote
import re

user_login=input("mssv:")
pass_login=input("pass:")
headers={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
login_data={'name':user_login,'pass':pass_login,'form_id':'user_login','op':'Log in'}
data={'dsmalop':
"""CS114.K11
CS114.K11.1""",
'op':'Đăng ký',
'txtmasv':user_login,
'form_id': 'uit_dkhp_dangky_form'}
while True:
	try:
		with requests.Session() as s:
			url="https://dkhp.uit.edu.vn"
			r=s.get(url,headers=headers)
			#get content to sp login in next command
			page_soup=soup(r.content,'html.parser')
			#find a form
			login_data['form_build_id']=page_soup.find('input',attrs={'name':'name'})['value']
			#login
			r=s.post(url,data=login_data,headers=headers)
			page_soup=soup(r.content,'html.parser')
			
			#data['form_build_id']='form-I0P8xCIJqhMWvdq5HGuIu2T6Vs9wpXhejR--ycWe2Ug'#page_soup.find('textarea',attrs={'name':'dsmalop'})['value']
			#find a token for login
			data['form_token'] =page_soup.find('input',attrs={'name':"form_token"})['value']
			url='https://dkhp.uit.edu.vn/sinhvien/hocphan/dangky'
			#send the subject data
			r=s.post(url,data=data,headers=headers)
			page_soup=soup(r.content,'html.parser')
			#print(page_soup)
			try:
				#raise lỗi nếu đk không thành công
				error=page_soup.find('div',{'class':'alert alert-block alert-error'})
				print(error.get_text())
			except:
				pass
			try:
				#thông báo đk thành công
				success=page_soup.find('div',{'class':'alert alert-block alert-success'})
				print(success.get_text())
			except:
				pass
			da_dk=page_soup.find('div',{'class':'table_lophoc_dadk_wrapper'}).findAll('div',{'class':re.compile("^(form-item form-type-checkbox form-item-table-lophoc-dadk-)")})
			for i in da_dk:
				print(i.attrs['class'][2].split('-')[-1])	
			break
	except requests.exceptions.RequestException as err:
	    print ("OOps: Something Else",err)
	    pass
	except requests.exceptions.HTTPError as errh:
	    print ("Http Error:",errh)
	    pass
	except requests.exceptions.ConnectionError as errc:
	    print ("Error Connecting:",errc)
	    pass
	except requests.exceptions.Timeout as errt:
	    print ("Timeout Error:",errt)     
	    pass
