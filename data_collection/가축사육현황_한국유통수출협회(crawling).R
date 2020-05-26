library(rvest)

url ="http://www.kmta.or.kr/kr/data/stats_breed_beef.php"

Sys.getlocale()
Sys.setlocale("LC_ALL","C")
cow_data = read_html(url)%>%html_node(".table1")%>%html_table(fill = TRUE)
Sys.setlocale("LC_ALL")

names(cow_data)
cow_data[1,]
name_ = c("연도","월","마리수","번식우","1세미만(암)","1세미만(수)","1~2세(암)","1~2세(수)","2세이상(암)","2세이상(수)")
names(cow_data) = name_
cow_data = cow_data[-1,]

write.csv(cow_data,"C:\\Users\\a0105\\Desktop\\DSC\\ddd\\data\\가축사육현황_한국유통수출협회.csv")



