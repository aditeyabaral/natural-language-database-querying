import requests
from bs4 import BeautifulSoup

import keywords


def getLinks(filename):
    search_url = "http://www.google.co.in/searchbyimage/upload"
    multipart = {"encoded_image": (filename, open(filename, "rb")), "image_content": ""}
    headers = requests.utils.default_headers()
    headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }
    )
    response = requests.post(
        search_url, files=multipart, allow_redirects=False, headers=headers
    )
    imgsearch_url = response.headers["Location"]
    page = requests.get(imgsearch_url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("a", href=True)
    if "Pages that include matching images" in str(page.content):
        return links
    return None


def getYouTubeLinks(a):
    filtered = [
        i
        for i in a
        if i is not None
        and i != "#"
        and "google.com" not in i
        and "google.co.in" not in i
        and "wikipedia" not in i
    ]
    media_links = [
        i for i in filtered if i.startswith("/search?") or i.startswith("https://")
    ]
    youtube_links = [i for i in media_links if i.startswith("https://www.youtube")]
    return youtube_links


def getYouTubeTags(yt_links):
    headers = requests.utils.default_headers()
    headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }
    )
    tags = []
    for l in yt_links:
        response = requests.get(l, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.find_all("meta")
        t = list()
        for i in content:
            try:
                if i["name"] in ["title", "description"]:
                    t.append(i["content"].strip())
            except:
                pass
        tags.extend(t)
    temp_youtube_tags = []
    for i in tags:
        k = keywords.getKeywordsWatson(i)
        if k is not None:
            temp_youtube_tags.append(k)
        else:
            k = keywords.getKeywordsRAKE(i)
            temp_youtube_tags.append({"keywords": k, "entities": [], "categories": []})
    all_youtube_tags = []
    grouped_youtube_tags = []
    for i in temp_youtube_tags:
        t = []
        for j in i:
            if j in ["keywords", "entities"]:  # taking kw, ent and category
                all_youtube_tags.extend(i[j])
                t.extend(i[j])
        grouped_youtube_tags.append(set(t))
    all_youtube_tags = list(set(all_youtube_tags))
    grouped_youtube_tags = tuple(grouped_youtube_tags)
    common_youtube_tags = []
    if grouped_youtube_tags:
        common_youtube_tags = list(set.intersection(*grouped_youtube_tags))
    if len(common_youtube_tags) >= 5:  # check for sufficient common tags
        return common_youtube_tags
    return all_youtube_tags  # common might not return all stuff

def filterGoogleRelevantTerms(keywords):
    check = lambda x: "wallpaper" not in x and "iphone" not in x and "shutterstock" not in x and "shutter" not in x and "href" not in x and "https" not in x
    filtered = [k for k in keywords if check(k)]
    return filtered


def getGoogleRelevantTerms(frame_keywords):

    frame_keywords = " ".join(frame_keywords).strip().split()
    query = "+".join(frame_keywords)
    search_url = r"http://www.google.com/search?q={}&tbm=isch".format(query)
    headers = requests.utils.default_headers()
    headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }
    )
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", href=True)
    exclude = ["NEWS", "VIDEOS", "ALL", "Next\xa0>"]
    google_relevant_searches = [
        i.text.strip()
        for i in links
        if str(i.get("href")).startswith("/search") and i.text not in exclude
    ]
    filtered = filterGoogleRelevantTerms(google_relevant_searches)
    return filtered
