import requests, sys, webbrowser, bs4

search = input("Enter the title of the movie you would like to search for: ")
search = search + " transcripts wiki"
res = requests.get('http://google.com/search?q=' + search) #searches google for the search term
res.raise_for_status() #checks to see if the search works
soup = bs4.BeautifulSoup(res.text, features="html.parser") #turns the page into a beautiful soup object
linkElems = soup.select('div#main > div > div > div > a') #collects a list of all the hyperlinks

res2 = requests.get('http://google.com' + linkElems[0].get('href')) #goes to the first link
res2.raise_for_status()#checks to see if the link works
soup = bs4.BeautifulSoup(res2.text, features="html.parser")
text = soup.get_text()#turns the page into text

character = input("Enter the character you would like to search for: ")
character_all_caps = character.upper()
character_with_space = character + " "
character = character + ":"
character_with_space = character_with_space + ":"
quote_list = []
for line in text.splitlines():
    bracket_count = 0
    curly_brace_count = 0
    i = 0
    if character.lower() in line.lower() \
            or character_with_space.lower() in line.lower()\
            or character_all_caps in line:
        for letter in line:
            if letter == "[":
                bracket_count += 1
            if letter == "{":
                curly_brace_count += 1
        if bracket_count != 0:
            newstr = line
            while i < bracket_count:
                bracket_beginning = newstr.find("[")
                bracket_end = newstr.find("]")
                newstr = newstr[:bracket_beginning] + newstr[bracket_end + 1:]
                i += 1
            quote_list.append(newstr)
        elif curly_brace_count != 0:
            newstr = line
            while i < curly_brace_count:
                curly_beginning = newstr.find("{")
                curly_end = newstr.find("}")
                newstr = newstr[:curly_beginning] + newstr[curly_end + 1:]
                i += 1
            quote_list.append(newstr)
        else:
            quote_list.append(line)

for line in quote_list:
    print (line)
