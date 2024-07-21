# import spacy
# from spacy.lang.en.stop_words import STOP_WORDS
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

print(STOP_WORDS)

from string import punctuation
from heapq import nlargest

text = "Sure, raw water might be full of other stuff like bacteria, algae, and minerals. But these, say devotees, are good for us—unlike the antimicrobial agents and additives in tap water or the plastic additives leached into bottled water. Fluoride, added to tap water for dental health, has a particularly long history of health scares and conspiracy theories; in the 1950s some said fluoridation was a communist plot to undermine the health of Americans. Raw-water advocates contend that fluoride is neurotoxic even at very low levels, although there is no evidence of that."

def summarizer(rawdocs) : 
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    tokens = [token.text for token in doc ]
    # print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] +=1

    max_freq = max(word_freq.values())                

    for word in word_freq.keys():
        word_freq[word ] = word_freq[word]/max_freq

    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent :
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]    

    select_len = int(len(sent_tokens) * 0.3)

    summary = nlargest(select_len, sent_scores , key = sent_scores.get)
    # print(summary)

    final_summary = [word.text for word in summary]
    summary = " ".join(final_summary)
    # print(text)
    # print(summary)

    # print('lenght of original text',len(text.split(' ')))
    # print('lenght of original summary',len(summary.split(' ')))



    return summary , doc , len(rawdocs.split(' ')) ,len(summary.split(' '))
    