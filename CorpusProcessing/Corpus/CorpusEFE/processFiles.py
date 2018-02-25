import csv
import os
from pyquery import PyQuery as pq
#import ipdb

def list_files(path,rec=False, filescsv=None):

    filesList = []
    if filescsv is not None:
        with open(filescsv) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['dir'] == '01-Enero':
                    print("{}/{}".format(row['dir'],row['file']))
    elif path is not None:
        for file in os.listdir(path):
            filepath = os.path.join(path,file)
            if os.path.isdir(filepath) and rec:
                filesList.extend(list_files(path=filepath,rec=rec))
            if file.endswith(".xml"):
                filesList.append(filepath)
                #print(os.path.join(self.path, file))
    return filesList

#filesProc = FilesProcessor("/Users/luisvalencia/Projects/Hackaton/Corpus/CorpusEFE/01-Enero")
defaultPath = "."#"/Users/luisvalencia/Projects/Hackaton/Corpus/CorpusEFE"
filesList = list_files(path=defaultPath,rec=True)

def file_to_string(filepath='18073876.xml', rep=True):
    with open(filepath, 'r') as myfile:
        raw = myfile.read()
        replaced = raw.replace('\n', '') if rep else raw
        data = replaced.encode("utf-8")
    return data

from polyglot.text import Text,Word

def processChunk(chunk,text):
    textChunk = " ".join(text.words[chunk.start:chunk.end])
    return textChunk

def save_news_parlance(fileList,targetpath='ES-EFE-Training.pl'):
    with open(targetpath, 'w') as textfile:
        for filepath in fileList:
            data = file_to_string(filepath)
            data2 = data.lower()
            pq1 = pq(data)
            title = pq1('title').text()
            keyword = pq1('keyword').attr('key')
            body = pq1('body').children()
            content = ''
            for item in body:
                if item.tag == 'body.content':
                    contentText = item.text
                    pq2 = pq(contentText)
                    content = pq2('p')[0].text
                    break
            textfile.write("{}\n{}\n{}\n".format(title,keyword,content))

#Possible fields: ['title', 'keyword', 'date', 'tesauro', 'locs', 'orgs', 'pers', 'content']

'''
fieldsMap = {
    "newId": "KEY",
    "title": "HEADER",
    "keyword": "KEYWORDS",
    "tesauro": "TESAURO",
    "content": "CONTENT",
    "locs": "LOCS",
    "orgs": "ORGS",
    "pers": "PERS",
    "date": "DATETIME"
}
'''

fieldsMap = {
    "newId": "KEY",
    "title": "HEADER",
    "content": "SUBJECT",
    "keyword": "MATTER1",
    "tesauro": "MATTER2",
    "locs": "MATTER3",
    "orgs": "MATTER4",
    "date": "MATTER5",
    "pers": "MATTER6"
}

def wrap_field(key,val):
    return "\n\t{}: <<{}>>".format(fieldsMap.get(key),val)

def wrap_fields(pairs,selectedKeys):
    formatString = "{{"
    formatParams = []
    selectedPairs = filter(lambda pair: pair[0] in selectedKeys,pairs)
    for el in selectedPairs:
        formatString += "{}"
        formatParams.append(wrap_field(*el))
    formatString += "\n}}\n"
    return formatString.format(*formatParams)

def save_conceptual_scheme(fileList,targetpath='news.corpus',selectedKeys=['newId','title', 'keyword', 'tesauro', 'locs', 'orgs', 'content', 'date'],maxResults=10000):
    included = 0
    with open(targetpath, 'w') as targetfile:
        for filepath in fileList:
            pairs = []
            #fileName = os.path.basename(filepath)
            #pairs.append(("fileName",fileName))
            locs=set()
            orgs=set()
            pers=set()
            data = file_to_string(filepath)
            data2 = data.lower()
            pq1 = pq(data)
            pqlower = pq(data2)
            props = pqlower('property')
            tesauro = ''
            for prop in props:
                if prop.get('formalname')=='tesauro':
                    tesauro = prop.get('value')
                    pairs.append(("tesauro",tesauro))
                    break

            if tesauro.find("cul:")==-1:
                continue
            newId = pqlower('newsitemid').text()
            pairs.append(("newId",newId))
            title = pq1('title').text()
            pairs.append(("title",title))
            keyword = pq1('keyword').attr('key')
            pairs.append(("keyword",keyword))
            body = pq1('body').children()
            date = pq1('pubdata').attr('date.publication')
            pairs.append(("date",date))
            content = ''
            for item in body:
                if item.tag == 'body.content':
                    contentText = item.text
                    pq2 = pq(contentText)
                    content = pq2('p')[0].text
                    break

            if content is not None and content != '':
                next

            pairs.append(("content",content))
            text = Text(content, hint_language_code='es')
            try:
                if text is not None:
                    if isinstance(text.entities, list):
                        for ent in text.entities:
                            if ent.tag == 'I-LOC':
                                    locs.add(processChunk(ent,text))
                            if ent.tag == 'I-ORG':
                                    orgs.add(processChunk(ent,text))
                            if ent.tag == 'I-PER':
                                    pers.add(processChunk(ent,text))
            except ValueError:
                error = False
                pass
            pairs.append(("locs",str(locs)[1:-1]))
            pairs.append(("orgs",str(orgs)[1:-1]))
            pairs.append(("pers",str(pers)[1:-1]))

            if tesauro.find("cul:")>=0:
                targetfile.write(wrap_fields(pairs,selectedKeys))
                included += 1
                if included == maxResults:
                    return


def save_news_csv(fileList,targetpath='news.csv',selectedKeys=['newId','title', 'keyword', 'tesauro', 'locs', 'orgs', 'content', 'date']):
    with open(targetpath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=selectedKeys)
        writer.writeheader()
        for filepath in fileList:
            pairs = []
            locs=set()
            orgs=set()
            pers=set()
            data = file_to_string(filepath)
            data2 = data.lower()
            pq1 = pq(data)
            pqlower = pq(data2)
            newId = pqlower('newsitemid').text()
            title = pq1('title').text()
            keyword = pq1('keyword').attr('key')
            body = pq1('body').children()
            date = pq1('pubdata').attr('date.publication')
            content = ''
            for item in body:
                if item.tag == 'body.content':
                    contentText = item.text
                    pq2 = pq(contentText)
                    content = pq2('p')[0].text
                    break
            pqprops = pq(data2)
            props = pqprops('property')
            tesauro = ''
            for prop in props:
                if prop.get('formalname')=='tesauro':
                    tesauro = prop.get('value')
                    break
            text = Text(content, hint_language_code='es')
            #ipdb.set_trace()
            try:
                if text is not None:
                    if isinstance(text.entities, list):
                        for ent in text.entities:
                            if ent.tag == 'I-LOC':
                                    locs.add(processChunk(ent,text))
                            if ent.tag == 'I-ORG':
                                    orgs.add(processChunk(ent,text))
                            if ent.tag == 'I-PER':
                                    pers.add(processChunk(ent,text))
            except ValueError:
                error = False
                pass #continue
            resultObject = {
                'newId': newId, 'title': title, 'keyword': keyword, 'content': content,
                'locs': locs, 'orgs': orgs, 'pers': pers, 'date': date,
                'tesauro': tesauro
            }
            resultObject = {
                k: resultObject.get(k) for k in resultObject.keys() if k in selectedKeys
            }
            writer.writerow(resultObject)

filesNo = 100000000
filesNumber = min(filesNo,len(filesList))
selectedFiles = filesList[0:filesNumber]
selectedFields = ['newId','title', 'keyword', 'tesauro', 'locs', 'orgs', 'content', 'date']
save_conceptual_scheme(fileList=selectedFiles,targetpath='news.corpus',selectedKeys=selectedFields)
#save_news_csv(fileList=selectedFiles,targetpath='news.csv',selectedKeys=selectedFields)
#save_news_parlance(fileList=selectedFiles,targetpath='news.pl')
