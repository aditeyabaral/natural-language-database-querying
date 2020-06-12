import requests
from bs4 import BeautifulSoup
import keywords
import speechRecognition
import os
import subprocess
import shutil
from collections import Counter
import time

def getLinks(filename):
    search_url = 'http://www.google.co.in/searchbyimage/upload'
    multipart = {'encoded_image': (filename, open(filename, 'rb')), 'image_content': ''}
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})
    response = requests.post(search_url, files = multipart, allow_redirects = False, headers = headers)
    imgsearch_url = response.headers['Location']
    page = requests.get(imgsearch_url, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("a", href = True)
    return links
       

def getYouTubeLinks(a):
    filtered = [i for i in a if i is not None and i!="#" and "google.com" not in i and 
         "google.co.in" not in i and "wikipedia" not in i]
    media_links = [i for i in filtered if i.startswith("/search?") or i.startswith("https://")]
    youtube_links = [i for i in media_links if i.startswith("https://www.youtube")]
    return youtube_links


def getYouTubeTags(yt_links):
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})
    tags = []
    for l in yt_links:
        response = requests.get(l, headers = headers)
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
        if k!=-1:
            temp_youtube_tags.append(k)
        else:
            k = keywords.getKeywordsRAKE(i)
            temp_youtube_tags.append({"keywords":k, "entities":[], "categories":[]})
    all_youtube_tags = []
    grouped_youtube_tags = []
    for i in temp_youtube_tags:
        t = []
        for j in i: 
            if j in ["keywords", "entities", "categories"]: #taking kw, ent and category
                all_youtube_tags.extend(i[j])
                t.extend(i[j])
        grouped_youtube_tags.append(set(t))
    all_youtube_tags = list(set(all_youtube_tags))
    grouped_youtube_tags = tuple(grouped_youtube_tags)
    common_youtube_tags = []
    if grouped_youtube_tags:
        common_youtube_tags = list(set.intersection(*grouped_youtube_tags))
    if len(common_youtube_tags)>=5:  #check for sufficient common tags
        return common_youtube_tags
    return all_youtube_tags #common might not return all stuff

def getImageTags(frame_keywords):
    #remove least similar words from keywords - w2v, remove last few and ensure atleast 2 keywords retain
    temp_filter = []
    for i in frame_keywords:
        for j in i.split():
            if j not in temp_filter:
                temp_filter.append(j)
    frame_keywords = temp_filter
    query = "+".join(frame_keywords)
    search_url = r"http://www.google.com/search?q={}&tbm=isch".format(query)
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", href = True)
    exclude = ["NEWS","VIDEOS","ALL","Next\xa0>"]
    google_relevant_searches = [i.text.strip() for i in links if str(i.get("href")).startswith("/search") and i.text not in exclude]
    image_search_title_texts = [i.text[:i.text.find("...")].strip() for i in links if "..." in i.text]
    image_search_titles = []
    for i in image_search_title_texts:
        k = keywords.getKeywordsWatson(i)
        if k!=-1:
            image_search_titles.append(k)
        else:
            k = keywords.getKeywordsRAKE(i)
            image_search_titles.append({"keywords":k, "entities":[],"categories":[]})
    all_image_search_tags = []
    grouped_image_search_tags = []
    for i in image_search_titles:
        t = []
        for j in i:
            if j in ["keywords", "entities"]:   #taking kw, ent and category
                all_image_search_tags.extend(i[j])
                t.extend(i[j])
        grouped_image_search_tags.append(set(t))
    all_image_search_tags = list(set(all_image_search_tags))
    grouped_image_search_tags = tuple(grouped_image_search_tags)
    common_image_search_tags = []
    if grouped_image_search_tags:
        common_image_search_tags = list(set.intersection(*grouped_image_search_tags))
    if len(common_image_search_tags)>=5:
        image_tags = common_image_search_tags
    else:
        image_tags = all_image_search_tags
    image_tags = list(set(google_relevant_searches+all_image_search_tags))
    image_tags = keywords.remove_same_name_duplicates(image_tags)
    return image_tags


def getTagsfromFrame(imgfilename, videofilename, audio_keywords):
    link_obj = getLinks(imgfilename)
    all_links = [str(i.get("href")) for i in link_obj]
    youtube_links = getYouTubeLinks(all_links)
    if youtube_links: #add '0 and youtube_links' to test image search results
        youtube_tags = getYouTubeTags(youtube_links)
        return youtube_tags
    else:
        frame_keywords = list(set(audio_keywords["keywords"]+audio_keywords["entities"]))
        #frame_objects = <get objects and text in frame>
        #frame_keywords+= frame_objects
        image_tags = getImageTags(frame_keywords)
        return image_tags
        
def videoFrames(filename, framerate = 1):
    vid_file = os.path.join(os.path.dirname(os.getcwd()), "Database", "Video", filename)
    assert os.path.isfile(vid_file), "Given path is not a valid file"
    tmpdir = os.path.join(os.getcwd(), "tmp")
    if os.path.isdir(tmpdir):
        shutil.rmtree(tmpdir)
    os.mkdir(tmpdir)
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            vid_file,
            "-r",
            f"{framerate}",
            os.path.join(tmpdir, "img_%04d.jpg"),
        ]
    )
    return [os.path.join(tmpdir, i) for i in os.listdir(tmpdir)]

def getTopKCounter(a, K):
    r = []
    for i in a:
        r.extend(i)
    c = Counter(r)
    words = [i[0] for i in c.most_common(K)]
    return words
        
def getTags(videofilename):
    path_to_images = videoFrames(videofilename)
    videofilename = os.path.join(os.path.dirname(os.getcwd()), "Database", "Video", videofilename)
    transcript, translated = speechRecognition.video_to_text(videofilename)
    keywords_translated = keywords.getKeywordsWatson(translated)
    tags = []
    for p in path_to_images:
        print(p)
        tags.append(getTagsfromFrame(p,videofilename,keywords_translated))
    return tags, getTopKCounter(tags, 10)
    #filter this list by EITHER- 
        #A. combining the list of lists into one list, take list(set(list)), 
            #then use w2v to find most similar words(top K)
        #B. find the common elements(or atleast 85%-90% presence) and return them. 
            #If len(common elements)<4, goto A.
        #C Counter to get top 10-15 occuring words

videofilename = r"sample2.mp4"
start_time = time.time()
res = getTags(videofilename)
duration = time.time()-start_time