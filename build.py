#!python3

import json
import inspect

# Define functions for pieces
def build_news(news, count, standalone):
    if count > len(news):
        count = len(news)

    if count <= 0:
        return ""
    
    print("\nAdding news:")
    news_list = ""

    for n in news[:count]:
        print(n["date"])
        item =  '<div class="news-item">\n'
        item += '<div class="news-left">' + n["date"] + '</div>\n'
        item += '<div class="news-right">' + n["text"] + '</div>\n'
        item += '</div>\n'
        news_list += item

    news_html =  "<div class=\"section\">\n"

    if (count != len(news)):
        link = "<a href=\"./news.html\">See all news</a>"
        news_html += "<h1>Recent News <small style=\"font-weight: 300; float: right; margin-top: 0.23em\">(%s)</small></h1>\n" %link
    elif standalone:
        link = "<a href=\"./index.html\">%s</a>" % meta_json[0]["name"]
        news_html += "<h1>News <small style=\"font-weight: 300; float: right; margin-top: 0.23em\">%s</small></h1>\n" %link
    else:
        news_html += "<h1>News</h1>\n"
    news_html += "<div class=\"hbar\"></div>\n"
    news_html += "<div id=\"news\">\n"
    news_html += news_list
    news_html += "</div>\n" # close news
    news_html += "</div>\n" # close section
    return news_html

# Helper function to decide what publication sections to include
def get_pub_titles(pubs):
    titles = set()
    for p in pubs:
        titles.add(p["section"])
    return sorted(list(titles))

def some_not_selected(pubs):
    for p in pubs:
        if not p["selected"]:
            return True
    return False

def build_pubs_inner(pubs, title, full):
    if title == "":
        return ""

    pubs_list = ""

    for p in pubs:
        if title == p["section"] and (p["selected"] or full):
            print(p["title"])
            item =  '<div class="paper">\n'

            item += '<div class="paper-left">\n'
            item += '<div class="paper-title">' + p["title"] + '</div>'
            item += '<div class="paper-authors">' + ",\n".join(p["authors"].split(", ")) + '</div>'
            item += '<div class="paper-conference">' + p["conference"] + '</div>'
            item += '<div class="paper-early">' + p["early"] + '</div>'
            item += '</div>\n' # close paper-right
            item += '<div class="paper-right">\n'
            item += '<a href="' + p["link"] + '" alt="[PDF]"><img class="icon" src="images/paper2.jpg"/></a>\n' if p["link"] else "&nbsp; &nbsp; &nbsp;"
            item += '<a href="' + p["code"] + '" alt="[Code]"><img class="icon" src="images/github.png"/></a>\n' if p["code"] else "&nbsp; &nbsp; &nbsp;"
            item += '<a href="' + p["talk"] + '" alt="[Talk]"><img class="icon" src="images/video4.png"/></a>\n' if p["talk"] else "&nbsp; &nbsp; &nbsp;"
            item += '<a href="' + p["extra"] + '" alt="[Extra]"><img class="icon" src="images/extra.png"/></a>\n' if p["extra"] else ""
            item += '</div>\n' # close paper-left
            item += '</div>\n' # close paper
            pubs_list += item

    pubs_html =  "<h3 id=\"%spublications\">%s</h3>" % (title, title)
    pubs_html += pubs_list
    return pubs_html

def build_pubs(pubs, full):
    if len(pubs) == 0:
        return ""

    print("\nAdding publications:")

    pubs_html =  "<div class=\"section\">\n"
    if some_not_selected(pubs) and not full: 
        pubs_html += "<h1>Selected Publications <small style=\"font-weight: 300; float: right; margin-top: 0.23em\">(<a href=\"./pubs.html\">See all publications</a>)</small></h1>" 
    elif full: 
        link = "<a href=\"./index.html\">%s</a>" % meta_json[0]["name"]
        pubs_html += "<h1>Publications and Working Papers <small style=\"font-weight: 300; float: right; margin-top: 0.23em\">%s</small></h1>\n" %link
    else: 
        pubs_html += "<h1>Publications and Working Papers</h1>"

    pubs_html += "<div class=\"hbar\"></div>\n"
    pubs_html += "<div id=\"publications\">\n"
    titles = get_pub_titles(pubs)
    for i in range(len(titles)):
        title = titles[i]
        pubs_html += build_pubs_inner(pubs, title, full)
        if i != len(titles) - 1:
            pubs_html += "<p style=\"font-size: 0.4em\">&nbsp</p>\n"

    pubs_html += ""
    pubs_html += "</div>\n" # close pubs
    pubs_html += "</div>\n" # close section
    return pubs_html

def build_other(other):
    if len(other) == 0:
        return ""

    print("\nAdding other items:")

    other_html =  "<div class=\"section\">\n"
    other_html += "<h1>Other</h1>"
    other_html += "<div class=\"hbar\"></div><div class=\"other\">\n"

    #pubs_html += "<div class=\"hbar\"></div>\n"
    #pubs_html += "<div id=\"publications\">\n"
    other_html += '<ul>'
    for item in other:
        other_html += '<li>' + item["description"] + '</li>' + "\n"
    other_html += '</ul>'

    other_html += "</div></div>\n" # close section
    return other_html


def build_students(students):
    if len(students) == 0:
        return ""

    print("\nAdding students:")
    students_list = ""

    for p in students:
        print(p["name"])
        item =  '<div class="student">\n' + p["name"] + "\n"
        item += '<div class="student-project">' + p["project"] + '</div>\n'
        item += '<div class="student-result">' + p["result"] + '</div>\n'
        item += '</div>\n'
        students_list += item

    students_html =  "<div class=\"section\">\n"
    students_html += "<h1>Mentoring</h1>\n"
    students_html += "<div class=\"hbar\"></div>\n"
    students_html += "<div id=\"students\">\n"
    students_html += students_list
    students_html += "</div>\n" # close students
    students_html += "</div>\n" # close section
    return students_html

def build_profile(profile):
    profile = profile[0]
    profile_html =  "<div class=\"profile\">\n"
    profile_html += "<div class=\"profile-left\">\n"
    profile_html += "<img class=\"headshot\" src=\"%s\" alt=\"Headshot\"/>\n" % profile["headshot"]
    profile_html += profile["blurb"]
    profile_html += "</div>\n" # close profile-left
    profile_html += "</div>\n" # close profile
    return profile_html

def add_links(html, links):
    links = links[0]
    print("\nAdding links:")

    toreplace = sorted(links.keys(), key=len, reverse=True)

    for name in toreplace:
        pos = html.find(name)
        while pos != -1:
            prefix = html[:pos]
            suffix = html[pos:]

            open = html[:pos].count("<a href=")
            close = html[:pos].count("</a>")

            print(name, pos, open, close)
            if pos >= 0 and open == close:
                toreplace = "<a href=\"%s\">%s</a>" % (links[name], name)
                suffix = suffix.replace(name, toreplace, 1)
                html = prefix+suffix

            start = len(prefix) + len(toreplace) - len(name)
            tmp = html[start:].find(name)
            pos = tmp + start if tmp >= 0 else tmp
    
    return html

def build_index(profile_json, news_json, pubs_json, students_json, links):
    body_html =  "<body>\n"
    body_html += "<div class='title'><h1>Zoe Kahn</h1></div>\n"
    body_html += "<div class='subtitle'><h2><a href='resume.pdf', download='ZoeKahnCV.pdf'>CV</a> | <a href='https://scholar.google.com/citations?user=tsX7at8AAAAJ&hl=en'>Google Scholar</a> | <a href='mailto:zkahn@berkeley.edu'>zkahn@berkeley.edu</a></h2></div>\n"
    body_html += "<div class=\"hbar\"></div>\n"
    body_html += build_profile(profile_json)
    body_html += build_news(news_json, 5, False)
    body_html += build_pubs(pubs_json, False)
    body_html += build_other(other_json)
    body_html += build_students(students_json)
    body_html += footer_html
    body_html += "</body>\n"

    index_html =  "<!DOCTYPE html>\n"
    index_html += "<html lang=\"en\">\n"
    index_html += header_html + "\n\n"
    index_html += body_html
    index_html += "</html>\n"

    return inspect.cleandoc(add_links(index_html, links))

def build_news_site(news_json, links):
    body_html =  "<body>\n"
    body_html += build_news(news_json, len(news_json), True)
    body_html += footer_html
    body_html += "</body>\n"

    news_html =  "<!DOCTYPE html>\n"
    news_html += "<html lang=\"en\">\n"
    news_html += header_html + "\n\n"
    news_html += body_html
    news_html += "</html>\n"

    return inspect.cleandoc(add_links(news_html, links))

def build_pubs_site(pubs_json, links):
    body_html =  "<body>\n"
    body_html += build_pubs(pubs_json, True)
    body_html += footer_html
    body_html += "</body>\n"

    pubs_html =  "<!DOCTYPE html>\n"
    pubs_html += "<html lang=\"en\">\n"
    pubs_html += header_html + "\n\n"
    pubs_html += body_html
    pubs_html += "</html>\n"

    return inspect.cleandoc(add_links(pubs_html, links))

def replace_placeholders(text, map):
    newtext = text
    for k in map:
        newtext = newtext.replace(k+"-placeholder", map[k])
    return newtext

### Load json files
with open('data/profile.json') as f:
    profile_json = json.load(f)

##### These next four can be empty
try:
    with open('data/news.json') as f:
        news_json = json.load(f)
except Exception as e:
    print(e)
    news_json = {}

try:
    with open('data/pubs.json') as f:
        pubs_json = json.load(f)
except Exception as e:
    print(e)
    pubs_json = {}

try:
    with open('data/other.json') as f:
        other_json = json.load(f)
except Exception as e:
    print(e)
    other_json = {}

try:
    with open('data/students.json') as f:
        students_json = json.load(f)
except Exception as e:
    print(e)
    students_json = {}

try:
    with open('metadata/auto_links.json') as f:
        auto_links_json = json.load(f)
except Exception as e:
    print(e)
    auto_links_json = {}

with open('metadata/meta.json') as f:
    meta_json = json.load(f)

with open('metadata/style.json') as f:
    style_json = json.load(f)

with open('templates/main.css') as f:
    main_css = f.read()

with open('templates/header.html') as f:
    header_html = f.read()

with open('templates/footer.html') as f:
    footer_html = "\n\n" + f.read() if meta_json[0]["name"] != "Federico Mora Rocha" else ""

### Create HTML and CSS
header_html = replace_placeholders(header_html, meta_json[0])
footer_html = replace_placeholders(footer_html, meta_json[0])
main_css    = replace_placeholders(main_css, style_json[0])
index_html  = build_index(profile_json, news_json, pubs_json, students_json, auto_links_json)
news_site   = build_news_site(news_json, auto_links_json)
pubs_site   = build_pubs_site(pubs_json, auto_links_json)

# Write to files
with open('index.html', 'w') as index:
    index.write(index_html)

with open('news.html', 'w') as index:
    index.write(news_site)

with open('pubs.html', 'w') as index:
    index.write(pubs_site)

with open('main.css', 'w') as main:
    main.write(main_css)