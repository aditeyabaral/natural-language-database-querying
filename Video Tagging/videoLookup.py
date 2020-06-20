import os

import keywords
import objectDetection
import speechRecognition
import tagUtils
import videoUtils


def getOnlineTags(imgfilename, frame_keywords):
    link_obj = tagUtils.getLinks(imgfilename)
    if link_obj is not None:
        all_links = [str(i.get("href")) for i in link_obj]
        youtube_links = tagUtils.getYouTubeLinks(all_links)
        if youtube_links:
            youtube_tags = tagUtils.getYouTubeTags(youtube_links)
            return youtube_tags

    image_tags = tagUtils.getGoogleRelevantTerms(frame_keywords)
    return image_tags


def getTagsfromAudio(videofilename):
    _, translated = speechRecognition.video_to_text(videofilename)
    watson_features = keywords.getKeywordsWatson(translated)
    if watson_features is None:
        audio_keywords = keywords.getKeywordsRAKE(translated)
        audio_NER = keywords.getKeywordsNER(translated)
    else:
        audio_keywords = watson_features["keywords"]
        audio_NER = watson_features["entities"]
    return audio_keywords, audio_NER


def getFrameTags(videopath):
    path_to_images = objectDetection.getFramesFromVideo(videopath, cluster=True)
    frame_tags = []
    l = len(path_to_images)
    for count, p in enumerate(path_to_images):
        print("{}/{}".format(count + 1, l))
        frame_objects, frame_description = objectDetection.getFrameDetails(p)
        print(frame_description)
        frame_keywords = keywords.getKeywordsWatson(frame_description)
        if frame_keywords is None:
            frame_keywords = keywords.getKeywordsRAKE(frame_description)
        else:
            frame_keywords = frame_keywords["keywords"]
        online_tags = getOnlineTags(p, frame_keywords)
        frame_tags.extend(online_tags + frame_keywords)
    return frame_tags


def getTags(videofilename):
    videofilename = os.path.join(
        os.path.dirname(os.getcwd()), "Database", "Video", videofilename
    )
    audio_keywords, audio_NER = getTagsfromAudio(videofilename)
    frame_tags = getFrameTags(videofilename)
    return audio_keywords, audio_NER, frame_tags


videofilename = r"vid3.mp4"
res = getTags(videofilename)
filtered = videoUtils.getTopKCounter(res, 20)
print(filtered)
