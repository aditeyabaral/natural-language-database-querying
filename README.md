# Natural-Language-Database-Querying

## Natural Language Querying

A novel approach to data retrieval from tagged databases using only natural language audio queries. The approach is capable of handling multiple languages and accents and retrieves data in linear time. We also present a holistic and semi-supervised approach to generate tags for any given database of videos or images. It combines both image recognition and natural language processing to identify objects and spoken entities to generate a set of words that identify the theme and content of the video.

## Execution

### Video Retrieval

Navigate to the source code directory and execute GUI.py
```sh
cd Code
python GUI.py
```

### Database Tagging

To tag the database of videos, execute the following
```sh
python tagDatabase.py
```

## Approach

* The proposed approach combines image recognition along with natural language processing to
retrieve videos matching a natural language query from a video database. The retrieval
process consists of three major steps - recognition of the natural language audio query,
extraction of features and tags from the database of videos and matching of the query to a video.

* The input audio query is first transcribed and then translated into English. This allows us
to tackle multiple natural languages and accents with the same approach. Google's Speech
Recognition API is deployed to perform rapid transcription and translation of the audio query. IBM Watson API is then used to extract features from the audio query such as the
keywords of the transcript as well as the entities mentioned. An audio processing pipeline is created to simultaneously perform the translation as well as the extraction of features.

* The database of videos is pre-tagged before the audio query is processed. Each video is split into frames, which are then filtered based on image features to retain frames depicting every scene in the video. A Google reverse image search is performed on every filtered frame, to lookup the same video on any online platforms such as YouTube and extract tags from these platforms. The frame is then analysed to look for objects and entities, which are extracted and stored. Further, a language model is used to generate a textual description of each frame. This generated description is searched on Google and suggested relevant searches are retrieved. Additionally, keywords from this description are extracted and added to the full set of results obtained.

* All the obtained image based tags are then filtered to retain only the top frequently occurring tags across all frames. These filtered tags are combined with the keywords and entities in the audio of the video to form the final set of tags for a video. A vector space is created out of these tags for every video in the dataset. The vector feature spaces obtained help represent the video's theme at a semantic level. Similarly, the query is also transformed into a vector space by using the keywords obtained earlier. Finally, the query's feature space is compared with the feature spaces of all the videos in linear time, using cosine similarity as the metric of evaluation. The video with the highest similarity is retrieved and displayed to the user.