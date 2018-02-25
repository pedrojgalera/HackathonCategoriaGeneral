dir <- c()
file <- c()
isdir <- c()

cont <- 0
processFiles <- function (basepath,pref,filter,directory){
  for (fname in list.files(basepath,pattern=filter)) {
    path = paste(basepath,fname,sep="//")
    newpref = paste("   ",pref)
    #print(paste(pref,fname,sep=""))
    if (file.info(path)[['isdir']])
      processFiles(path,newpref,"*\\.xml",fname)
    if (endsWith(fname,".xml")){
      #dir <<- c(dir,directory)
      #file <<- c(file,fname)
      doc <- read_xml(path)
    }
  }
}

processFiles(".","","^[0-9][0-9]",".")

data.hierarchy <- data.frame(dir,file)
write.csv(data.hierarchy,"files.csv")

require(xml2)

altura <- c(150, 135, 210, 140)
peso <- c(65, 61, 100, 65)
sexo <- c("F", "F", "M", "F")
datos.muestra <- data.frame(altura, peso, sexo)
datos.muestra

fa <- file.access(dir("."))
table(fa) # count successes & failures

dir("../..", pattern = "^[a-lr]", full.names = TRUE, ignore.case = TRUE)
list.files("01-Enero/", pattern = "$.xml", full.names = TRUE, ignore.case = TRUE)

#require(XML)
#require(plyr)
require(xml2)
fileurl <-"18073876.xml"
#"http://www.w3schools.com/xml/simple.xml"
doc <- read_xml(fileurl)
#xL <- xmlToList(doc) ###is to convert xml doc into List

#data <- ldply(xL, data.frame)
#head(data)

hl2 <- xml_find_all(doc, ".//hedline")
hl <- xml_find_all(hl2, ".//hl1")
shl <- xml_find_all(hl2, ".//hl2")
l <- as_list(doc)
#$NewsItem$NewsComponent$ContentItem$DataContent$nitf$body$body.head$abstract[[1]]