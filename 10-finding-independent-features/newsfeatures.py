import feedparser
import re

feedlist = [
#        'http://today.reuters.com/rss/topNews',
#        'http://today.reuters.com/rss/domesticNews',
#        'http://today.reuters.com/rss/worldNews',
#        'http://hosted.ap.org/lineups/TOPHEADS-rss_2.0.xml',
#        'http://hosted.ap.org/lineups/USHEADS-rss_2.0.xml',
#        'http://hosted.ap.org/lineups/WORLDHEADS-rss_2.0.xml',
#        'http://hosted.ap.org/lineups/POLITICSHEADS-rss_2.0.xml',

        'https://news.google.com/?output=rss'
]

def stripHTML(h):
    p=''
    s=0
    for c in h:
        if c == '<': s=1
        elif c == '>':
            s = 0
            p += ' '
        elif s == 0: p += c
    return p

def separateword(text):
    splitter = re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s) > 3]

def getarticlewords():
    allwords={}
    articlewords=[]
    articletitles=[]
    ec = 0 

    # Loop over every feed
    for feed in feedlist:
        print "\nfeed " + feed
        f = feedparser.parse(feed)
        print f

        # Loop over every article
        for e in f.entries:
            # Ignore identical articles
            if e.title in articletitles: continue
            # Extract the words
            txt = e.title.encode('utf-8')  + stripHTML(e.description.encode('utf-8'))
            words = separateword(txt)
            articlewords.append({})
            articletitles.append(e.title)

            # Increase the counts for this word in allwords and in articlewords
            for word in words:
                allwords.setdefault(word, 0)
                allwords[word] += 1
                articlewords[ec].setdefault(word, 0)
                articlewords[ec][word] += 1
            ec += 1

    return allwords, articlewords, articletitles

def makematrix(allw, articlew):
    wordvec=[]

    # Only take words that are common but not too common
    for w, c in allw.items():
        if c>3 and c<len(articlew)*0.6:
            wordvec.append(w)

    # Create the word matrix
    ll = [[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
    return ll, wordvec

allw, atrw, artt = getarticlewords()
wordmatrix, wordvec = makematrix(allw, atrw)
