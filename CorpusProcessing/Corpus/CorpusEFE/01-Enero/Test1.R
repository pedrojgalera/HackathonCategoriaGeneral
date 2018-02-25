require(XML)
require(plyr)
fileurl <-"18073876.xml"
#"http://www.w3schools.com/xml/simple.xml"
doc <- xmlParse(file=sub("s", "", fileurl),useInternalNodes = TRUE)
xL <- xmlToList(doc) ###is to convert xml doc into List

data <- ldply(xL, data.frame)
head(data)
