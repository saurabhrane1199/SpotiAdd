import re

def getTitles(txt):
    stopwords = ["full song", "lyrical", "lyric video", "title track", "lyrical Video", "offical video", "full audio song", ]
    regexWord = ["full", "lyric", "official"]
    x = list(filter(None, re.split("[^a-zA-Z0-9\s\"]",txt)))

    for i in range(len(x)):
        x[i] = x[i].lower().strip()
    
    for item in x:
        if item == "" or item in stopwords:
            x.remove(item)

    for item in regexWord:
        x[0] = re.split(item,x[0])[0]
        if(len(x)>1):
            x[1] = re.split(item,x[1])[0]
    
    if(len(x)>1):
        temp = x[1].split("from")
        if temp[0]=="" and len(temp)>1:
            x[1] = temp[1]
        else:
            x[1] = temp[0]
        temp = x[1].split("with")
        if temp[0]=="" and len(temp)>1:
            x[1] = temp[1]
        else:
            x[1] = temp[0] 
        

    return list(filter(None,x))
