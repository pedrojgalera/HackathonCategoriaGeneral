require(XML)
require(plyr)
fileurl <-"../01-Enero/18073876.xml"
#"http://www.w3schools.com/xml/simple.xml"
doc <- xmlParse(file=fileurl,useInternalNodes = TRUE) ### xmlParse()- is to parse the xml content, the parsed content is stored into doc
doc
xL <- xmlToList(doc) ###is to convert xml doc into List

data <- ldply(xL, data.frame)
head(data)