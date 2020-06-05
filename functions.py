import requests, sys, re, os, textwrap, math, json
from bs4 import BeautifulSoup


def progress_bar (iteration, total, prefix = '', suffix = '',  length = 50, fill = '█', printEnd = "\r"):
    
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s  |%s|  %s' % (prefix, bar, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print() 


def scrap_thread(id_, lower_bound=1, upper_bound=1,forum_name="threads", json_=False, posts_by=None):
	dirname = os.path.dirname(os.path.abspath(__file__))

	if posts_by is None:	
		if not os.path.exists(f"{dirname}/output/{forum_name}/"):
			os.mkdir(f"{dirname}/output/{forum_name}/")
	else:
		if not os.path.exists(f"{dirname}/output/{posts_by.lower()}/"):
			os.mkdir(f"{dirname}/output/{posts_by.lower()}/")
	
	for page in range(lower_bound,upper_bound+1):
		
		r_thread = requests.get(f"https://forum.toribash.com/showthread.php?t={id_}&page={page}")
		soup= BeautifulSoup(r_thread.text, 'lxml')
		thread_name_tag= soup.find('li', class_="breadcrumb-item active")
		thread_name= " ".join(thread_name_tag.text.split()).replace(" ",'_').replace("/",'_')
		

		
		if posts_by is None:
			if not os.path.exists(f"{dirname}/output/{forum_name}/{thread_name}/"):
				os.mkdir(f"{dirname}/output/{forum_name}/{thread_name}/")

			progress_bar(page,upper_bound, f"{forum_name}/{thread_name}/:" ,f"page: {page}/{upper_bound}")
	


		else:
			if not os.path.exists(f"{dirname}/output/{posts_by.lower()}/{thread_name}/"):
				os.mkdir(f"{dirname}/output/{posts_by.lower()}/{thread_name}/")
			progress_bar(page,upper_bound, f"{posts_by}/{thread_name}/:" ,f"page: {page}/{upper_bound}")
	
		
	


		comments_list=[]
		for comment_wrapper in soup.find_all('div', class_="row py-3"):
			comment_div = comment_wrapper.find_next('div', class_="col-12 pb-3")
			if comment_div.div is not None: #check if exist 'last edited' tag
				comment_div.div.decompose() #and removes the content of it

			edit_div_1=comment_div.find_next('div', class_="text-right pt-1 showthread-postedited")

			if edit_div_1 is not None: #check if div with post edited tag exists
				edit_div_1.decompose() 
			
			
			comment_date= comment_wrapper.find_next('div', class_="col-lg-4 no-mobile showthread-postdateold").text
			comment_date_clean=" ".join(comment_date.split())


			text= comment_div.text.replace('-','')
			

			text_clean=" ".join(text.split())
			
			username=comment_wrapper.find_next('a', id='postUserDropdown').text #grabs username

			if posts_by is None:
				comments_list.append({"date":comment_date_clean, "user" : username , "text" : text_clean})
			else:

				if posts_by.lower()==username.lower():
					comments_list.append({"date":comment_date_clean, "user" : username , "text" : text_clean})

		
		if posts_by is None:

			if not os.path.exists(f"{dirname}/output/{forum_name}/{thread_name}/{page}.txt"):
				out_txt = open(f"{dirname}/output/{forum_name}/{thread_name}/{page}.txt", "w+")
				if json_==True:
					json_dict=json.dumps(comments_list)#if json argument is true dumps the comments in json format
					out_txt.write(json_dict)

				else:
					for comment in comments_list:
						comment_clean=textwrap.fill(comment['text'], width=90)
						out_txt.writelines([f"{comment['date']} \n",f"{comment['user']}: \n{comment_clean} \n\n"])
				out_txt.close()
			
		else:
			if len(comments_list)>0:	
				out_txt = open(f"{dirname}/output/{posts_by.lower()}/{thread_name}/{posts_by}.txt", "a+")
				if json_==True:
					json_dict=json.dumps(comments_list)#if json argument is true dumps the comments in json format
					out_txt.write(json_dict)

				else:
					for comment in comments_list:
						comment_clean=textwrap.fill(comment['text'], width=90)
						out_txt.writelines([f"\n{comment['date']} \n",f"{comment['user']}: \n{comment_clean} \n\n"])
					out_txt.close()
			
		

def scrap_forum(id, lower_bound=1 , upper_bound=1, json_=False, posts_by=None):	
	for page in range(lower_bound,upper_bound+1):
		forum_request= requests.get(f"https://forum.toribash.com/forumdisplay.php?f={id}&page={page}")
		if forum_request.status_code==200:

			soup= BeautifulSoup(forum_request.text, 'lxml')

			thread_list=[]

			forum_name_tag= soup.find('li', class_="breadcrumb-item active")
			forum_name= " ".join(forum_name_tag.text.split()).replace(" ",'_')



			rows=soup.find_all('td', {'id': re.compile(r"td_threadtitle_(\d)")} )

			for thread in rows:

				thread_id=int(thread['id'].replace("td_threadtitle_", '')) #grabs the thread id

				max_page_tag=thread.find('a', text=re.compile(r"(\d) »")) #grabs <a> tag with the max page
				
				max_page=1 
				if max_page_tag is not None:
					max_page=int(max_page_tag.text.replace(" »",''))
				else:
					page_number_tag=thread.find_all('a', text=re.compile(r"^([\s\d]+)$")) #searchs for <a> with  numbers only
					if page_number_tag is not None:

						for num in page_number_tag:
							if int(num.text) == 3:
								max_page=3
							else:
								max_page=2


				
				
				thread_list.append({'id': thread_id, 'max_page':max_page})

			
			for thread in thread_list:
				scrap_thread(thread['id'],1,thread['max_page'],forum_name.replace('/','_'),json_=json_, posts_by=posts_by)

		else:
			print(f"request failed, code:{r_thread.status}")	