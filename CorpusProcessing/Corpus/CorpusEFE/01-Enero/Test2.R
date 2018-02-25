require(XML)
#require(plyr)
require(xml2)
fileurl <-paste(getwd(),"01-Enero","18073876.xml",sep="//")
#"http://www.w3schools.com/xml/simple.xml"
doc <- read_xml(fileurl)
#xL <- xmlToList(doc) ###is to convert xml doc into List

#data <- ldply(xL, data.frame)
#head(data)

hl <- xml_find_all(doc, ".//HeadLine")
shl <- xml_find_all(doc, ".//SubHeadLine")
abstract <- xml_find_all(doc, ".//abstract")
text <- xml_find_all(doc, ".//body.content")
date <- xml_find_all(doc, ".//story.date")
l <- as_list(doc)
props <- xml_find_all(doc, ".//Property")
#$NewsItem$NewsComponent$ContentItem$DataContent$nitf$body$body.head$abstract[[1]]

doc2 <- xmlParse(fileurl,useInternalNodes = TRUE)

for (i in 1:length(props)){
  print(xml_attrs(props[i]))
}
