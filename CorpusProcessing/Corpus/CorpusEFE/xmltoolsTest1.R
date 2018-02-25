library(xmltools)
library(magrittr)

# USING ebay.xml ------------------------------------------------
# load the data
file <- "01-Enero//18073876.xml"
doc <- file %>%
  xml2::read_xml(file)
nodeset <- doc %>%
  xml2::xml_children() # get top level nodeset
doc %>% 
  xml_view_tree()
doc %>% # we can also vary the depth
  xml_view_tree(depth = 2)

doc %>% # we can also vary the depth
  xml_view_tree(depth = 4)

nodeset[2] %>%
  xml_view_trees(3)

library(xml2)
xml_children(nodeset[2])

nodeset3 <- nodeset[2] %>%
  xml2::xml_children()

nodeset3[4]

head <- xml_find_all(doc, ".//head")
xml_children(head)

terminal_paths <- doc %>%
  xml_get_paths(only_terminal_parent = TRUE)

terminal_xpaths <- terminal_paths %>% ## collapse xpaths to unique only
  unlist() %>%
  unique()

df1 <- lapply(terminal_xpaths, xml_to_df, file = file, is_xml = FALSE, dig = FALSE) %>%
  dplyr::bind_cols()
df1

library(purrr)

empty_as_na <- function(x){
  if("factor" %in% class(x)) x <- as.character(x) ## since ifelse wont work with factors
  if(class(x) == "character") ifelse(as.character(x)!="", x, NA) else x
}

terminal_nodesets <- lapply(terminal_xpaths, xml2::xml_find_all, x = doc) # use xml docs, not nodesets! I think this is because it searches the 'root'.
df2 <- terminal_nodesets %>%
  purrr::map(xml_dig_df) %>%
  purrr::map(dplyr::bind_rows) %>%
  dplyr::bind_cols() %>%
  dplyr::mutate_all(empty_as_na)
df2

names(df2)

doc %>%
  xml_get_paths()

doc %>%
  xml_get_paths(mark_terminal = ">>")

df0 <- lapply(terminal_xpaths, function(x) {
  doc <- file %>% XML::xmlInternalTreeParse()
  nodeset <- XML::getNodeSet(doc, x)
  XML::xmlToDataFrame(nodeset, stringsAsFactors = FALSE) %>%
    dplyr::as_data_frame()
})

df1 <- lapply(terminal_xpaths, xml_to_df, file = doc, is_xml = TRUE, dig = FALSE) %>%
  dplyr::bind_cols()

devtools::install_github("statsmaths/coreNLP")
coreNLP::downloadCoreNLP()

