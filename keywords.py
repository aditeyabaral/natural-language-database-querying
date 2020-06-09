import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, EmotionOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.util import ngrams
from math import log
from textPreprocessing import clean
import pytextrank
from rake_nltk import Rake
import re, string
import en_core_web_lg

lemmatizer = WordNetLemmatizer()
stopw = set(stopwords.words('english'))
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
sp = en_core_web_lg.load()
r = Rake()
textrank = pytextrank.TextRank()
sp.add_pipe(textrank.PipelineComponent, name="textrank", last=True)

def getKeywordsWatson(text):
    authenticator = IAMAuthenticator('XEy0UMdLmvbRgDt9nMUmJ2REoi96wOQqbX_SYcGUs9pw')
    service = NaturalLanguageUnderstandingV1(version='2019-07-12',authenticator=authenticator)
    service.set_service_url('https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/b0a8b557-9834-4462-bd64-b3ceccd8b7e4')

    response = service.analyze(text = text, features=Features(keywords=KeywordsOptions(),entities = EntitiesOptions(), categories = CategoriesOptions())).get_result()

    fin = json.loads(json.dumps(response, indent=2))
    keys = [fin["keywords"][i]["text"] for i in range(len(fin["keywords"])) if fin["keywords"][i]["relevance"]>=0.6]
    entities = [fin["entities"][i]["text"] for i in range(len(fin["entities"])) if fin["entities"][i]["relevance"]>=0.9]
    l = [fin["categories"][i]["label"].split('/') for i in range(len(fin["categories"]))]

    categories = list()
    for i in l:
        categories.extend([j for j in i if j!=''])

    keys = list(set(keys))
    categories = list(set(categories))
    entities = list(set(entities))

    return keys, categories, entities

def pp_set(text, op):
    key_tokenized_sentences = sent_tokenize(text)
    key_tokenized_words = word_tokenize(text)
    if op == "token_sent":
        return key_tokenized_sentences
    elif op == "token_word":
        return key_tokenized_words
    elif op == "clean_sent":
        return [clean(i) for i in key_tokenized_sentences]
    elif op == "clean_word":
        return [clean(i) for i in key_tokenized_words]
    elif op == "lem_sent":
        key_clean_sentences = pp_set(text, "clean_sent")
        return [" ".join([lemmatizer.lemmatize(j) for j in i.split()]) for i in key_clean_sentences]
    elif op == "lem_word":
        key_clean_words = pp_set(text, "clean_word")
        return [lemmatizer.lemmatize(i) for i in key_clean_words]
    elif op == "prep_sent":
        key_clean_sentences = pp_set(text, "clean_sent")
        return [" ".join([i for i in j.split() if i not in stopw]) for j in key_clean_sentences]
    elif op == "prep_word":
        key_preprocessed_sentences = pp_set(text, "prep_sent")
        key_preprocessed_words = []
        for i in key_preprocessed_sentences:
            key_preprocessed_words.extend(word_tokenize(i))
        return key_preprocessed_words
    elif op == "pp_lem_word":
        return [lemmatizer.lemmatize(i) for i in pp_set(text, "prep_word")]

def extract_keywords(text):
    r.extract_keywords_from_sentences(pp_set(text, "lem_sent")) # Effectiveness : tokenized > lemmatized > clean 
    rake_keywords = r.get_ranked_phrases()
    spdoc = sp(text)
    ner_keywords = []
    for ent in spdoc.ents:
        ner_keywords.append(ent.text)
    spdoc = sp(" ".join(pp_set(text, "clean_word")))
    pytr_keywords = []
    for p in spdoc._.phrases:
        for term in p.chunks:
            if term.text not in pytr_keywords and term.text not in stopw:
                x = term.text
                pytr_keywords.append(x)
    nounchunk_keywords = list(set([i.text for i in set(spdoc.noun_chunks) if i.text not in stopw and len(min(i.text.split(),key = len))>1]))
    
    #bigrams = list(ngrams(pp_set(text, "clean_word"),2))
    #trigrams = list(ngrams(pp_set(text, "clean_word"),3))
    quadgrams = list(ngrams(pp_set(text, "clean_word"),4))
    #pentagrams = list(ngrams(pp_set(text, "clean_word"),5))
    quadgrams = list(set([" ".join([j for j in i if j not in stopw]).strip() for i in quadgrams]))
    #quadgrams = [i for i in quadgrams if i not in stopw and i!='' and len(i.split())>1]
    ngram_vector_key = dict()
    key_clean_sentences = pp_set(text, "clean_sent")
    for i in quadgrams:
        ngram_vector_key[i] = [0 for i in range(len(key_clean_sentences))]
    for i in range(len(key_clean_sentences)):
        for phrase in ngram_vector_key:
            ngram_vector_key[phrase][i] = (key_clean_sentences[i].count(phrase)/len(word_tokenize(key_clean_sentences[i])))
            df = 0
            for j in key_clean_sentences:
                if phrase in j:
                    df+=1
            ngram_vector_key[phrase][i]*=(1+log((len(key_clean_sentences)+1)/(df+1)))
    ngram_keywords = sorted(ngram_vector_key,key = lambda x:sum(ngram_vector_key[x]),reverse = True)
    
    
    
    all_keywords = rake_keywords+pytr_keywords+ner_keywords+nounchunk_keywords#+ngram_keywords
    all_keywords = list(set(all_keywords))
    sorted_keywords = list(all_keywords)
    sorted_keywords.sort()
    for i in range(len(sorted_keywords)):
        sorted_keywords[i] = re.sub(r' +',' ',sorted_keywords[i])
    print(sorted_keywords)
    return sorted_keywords

def getKeywordsMultiple(text):
    return extract_keywords(text.lower()) 