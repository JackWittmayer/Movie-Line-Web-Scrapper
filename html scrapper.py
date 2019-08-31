import requests, sys, webbrowser, bs4

print("Would you like to search through one movie or all movies?")
choice = input("Enter 1 for one movie, 2 for all movies.")
if choice == "1":
    search = input("Enter the title of the movie you would like to search for: ")
    search = search + " script transcripts wiki"
    res = requests.get('http://google.com/search?q=' + search)  # searches google for the search term
    res.raise_for_status()  # checks to see if the search works
    soup = bs4.BeautifulSoup(res.text, features="html.parser")  # turns the page into a beautiful soup object
    linkElems = soup.select('div#main > div > div > div > a')  # collects a list of all the hyperlinks

    #if "transcripts" in linkElems[0].get('href'):  # if the first link has the words transcripts in the url
    res = requests.get('http://google.com' + linkElems[0].get('href'))  # goes to the first link
    #webbrowser.open('http://google.com' + linkElems[0].get('href'))
    #else:
        #res2 = requests.get('http://google.com' + linkElems[1].get('href'))
    res.raise_for_status()  # checks to see if the link works
    soup = bs4.BeautifulSoup(res.text, features="html.parser")
    text = soup.get_text()  # turns the page into text
    character = input("Enter the character you would like to search for: ")

elif choice == 2:
    character = input("Enter the character you would like to search for: ")
    search = character + ""
    res = requests.get('http://google.com/search?q=' + character)  # searches google for the search term
    res.raise_for_status()  # checks to see if the search works
    soup = bs4.BeautifulSoup(res.text, features="html.parser")  # turns the page into a beautiful soup object
    linkElems = soup.select('div#main > div > div > div > a')  # collects a list of all the hyperlinks

character_all_caps = character.upper()
character_with_space = character + " "
character = character + ":"
character_with_space = character_with_space + ":"
quote_list = []
identifier = False
bracket_count = 0
curly_brace_count = 0
i = 0
for line in text.splitlines():
    words = line.split()
    if len(words) > 0:
        if len(words) > 0 and identifier == True and len(line) - len(line.lstrip()) > 5:
            if "Revision" not in words[0]:
                if ("(" in line or ")" in line):
                    continue
                elif ("{" in line or "}" in line):
                    continue
                else:
                    quote_list.append(line)
            continue
        else:
            identifier = False
        if character.lower() in words[0].lower() \
                or character_with_space.lower() in words[0].lower()\
                or character_all_caps in words[0]:
            words = line.split()
            bracket_count = 0
            curly_brace_count = 0
            i = 0
            if len(words[0]) > 1 and all([i.isupper() for i in words[0]]) and len(words) < 3:
                identifier = True
                quote_list.append(line)
                continue
            for letter in line:
                if letter == "[":
                    bracket_count += 1
                elif letter == "{":
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
    else:
        identifier = False

for line in quote_list:
    print (line)
