#proj2.py


#### Problem 1 ####
import requests #Import the request module to access the html for any webpage.
from bs4 import BeautifulSoup #Import BeautifulSoup to be able to parse through it and pull out content you want.
 
base_url = 'http://www.nytimes.com' #Make the request.
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser") #Parse through it to prepare to pull things from it.

headings = []
 
for div in soup.find_all("div", class_="a-column"): #Find all the div tags with a class 'a-column.' These are the ones in the left-most column. If you just start by looking for 'story-heading' tags you'll get a mix of left-most column headlines as well as some that are elsewhere on the page. Go a few levels up.
	for heading in div.find_all("h2", class_="story-heading"): #Within the list of a-column divs, find all the h2 tags with the heading you probably wanted originally.
		headings.append((heading.get_text().strip())) #Get just the text, and make sure to strip it so the one title laid over the video doesn't look weird. Append each one to the headings list above.


print('\n*********** PROBLEM 1 ***********')
print('New York Times -- First 10 Story Headings\n')

count = 0
for h in headings: #Print just the first 10 headings.
	if count < 10:
		print (h)
	count += 1




#### Problem 2 ####

base_url = 'https://www.michigandaily.com' #Make the request.
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser") #Parse through it to prepare to pull stuff from it later.

print('\n*********** PROBLEM 2 ***********')
print('Michigan Daily -- MOST READ\n')

for item in soup.find_all("div", class_="view-most-read"): #Each "Most Read" article title directly belongs to the 'item-list' class, but if you go straight for that one you'll get other stuff you don't want. Go one level up again to zero in on the most-read section.
	for title in item.find_all("div", class_="item-list"): #THEN get each article title.
		print (title.get_text()) #But just the text.



#### Problem 3 ####

base_url = 'http://newmantaylor.com/gallery.html' #Make the request
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser") #Parse prep


print('\n*********** PROBLEM 3 ***********')
print("Mark's page -- Alt tags\n")

for image in soup.find_all("img"): #Focus on just the img tags
	if image.get('alt') == None: #If the img doesn't have an alt attribte, print the message below
		print ("No alternative text provided!")
	else: #If it does have alt text, print it
		print (image.get('alt', ''))

#### Problem 4 ####

base_url = 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4' #Make an initial request to find out how many pages you'll need to crawl through to get all the emails.
r = requests.get(base_url, headers={'User-Agent': 'SI_CLASS'}) #I'm creating a flexible list, rather than hard-coding a list of 1-6. Even though I know there are 6 pages now, there might be more or less in the futre.
soup = BeautifulSoup(r.text, "html.parser")


number_of_pages_int = 0

for pager in soup.find_all("li", class_="pager-current"): #The pager text is a list item with the class 'pager_current'
	number_of_pages_str = pager.get_text()[-1] #Get the text of the pager and focus on the last character in the string, which will be the total number of pages.
	number_of_pages_int = int(number_of_pages_str) #Turn the string into an integer so you can create a list for future iterating purposes. You'll use this number to plug back into some URLs later (as a string of course!).

page_reps = range(number_of_pages_int + 1) #Create the actual list, but make sure it ends one beyond the number you got. Since range() always end one number under the value given. Range(5) = a list of numbers 0-4.

contact_links = [] #On each page you have to find all the "Contact Details" links. You don't want to store that text every time, but you do want to store the href string associated with it. There is where you'll keep that.
all_emails = [] #This is where you'll store the actual email addresses. All of them.

def node_finder(obj): #Define a function that looks at each person's profile/section on the list of people and pulls out the href string, and appends it to the contact_links list

	for person in obj.find_all("div", class_="field-item even"):
		for contact in person.find_all('a', href=True):
			link = contact['href']
			if link[1:5] == "node": #If you don't specify that the href string must begin with 'node' you'll wind up getting a bunch of jpg links in addition to what you want.
				contact_links.append(link)

def email_finder(obj): #Define a second function to actually get to each email address from the person's individual contact page.
	for field in obj.find_all("div", "field-item even"):
		for email in field.find_all('a', href=True):
			if email['href'][:7] == 'mailto:': #There are other useless links on the page you don't care about, so focus on the href strings that start with 'mailto'. The text wrapped within those tags is the email address you want.
				all_emails.append(email.get_text()) #Save the email address with all the others.



for num in page_reps: #We're now going to iterate 6 times, each time on a new page, to collect all the individual contact pages. We'll get down to the emails in a second.
	base_url = 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4&page=' + str(num) #Every time we do, we're visiting a different page.
	r = requests.get(base_url, headers={'User-Agent': 'SI_CLASS'}) #Make the request
	soup2 = BeautifulSoup(r.text, "html.parser")
	node_finder(soup2) #Run the node_finder function you just defined above to pull out the contact subpage href strings, storing them all in the contact_links list.


print('\n*********** PROBLEM 4 ***********')
print("UMSI faculty directory emails\n")

for node in contact_links: #Now it's time to get the actual emails from all the pages you collected in the contact_links list. Iterate through it, applying a new node (href string) each time.
	base_url = 'https://www.si.umich.edu/' + node #Visit a new page.
	r = requests.get(base_url, headers={'User-Agent': 'SI_CLASS'})
	soup4 = BeautifulSoup(r.text, "html.parser") #Get all the html.
	email_finder(soup4) #Get just the email address and add it to your list of other addresses.



count = 1
for email in all_emails: #Print out all the email address you collected, each with their own count variable attached.
	print (count, email)
	count += 1

