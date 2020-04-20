library(readxl)
library(dplyr)
library(reshape2)
library(tidyverse)
library(forecast)

setwd('C:\\Users\\a0105\\Desktop\\DSC\\ddd')

# 데이터 불러오기 
data = "./data/월별 배합사료 년도별 가격(00년_19년).xlsx"
wb = excel_sheets(data)

sheets = wb[c(3:12)]
sheets.data <- lapply(sheets, function(x) read_excel(path = data, sheet=x, skip = 4))
sheets.data2 <- do.call("bind_rows",sheets.data)

cow = subset(sheets.data2,sheets.data2$구분=='비육')
nrow(cow)

cow$...2 = NULL
cow$...16 = NULL
cow$...17 = NULL
cow$전체평균 = NULL

ye = sort(seq(2010,2019),decreasing=TRUE)
cow$연도 = ye

class(cow)
date = seq(1:12)
name_ = sapply(date,function(x)paste0(x,"월"))
cow2 = cow%>%gather(key='key',value='value',name_)

str(cow2)
cow2$연도=as.factor(cow2$연도)
cow2$key=as.factor(cow2$key)
names(cow2) = c("구분","연도","월","단가")

cow3 = arrange(cow2,cow2$연도)
saveRDS(cow3,"preprocessing/feed.rds")

################################################################################################### 
# 시계열 데이터로 변환 
cow_ts = ts(cow3[4],frequency = 12, start = c(2010,1) , end = c(2019,2))
plot.ts(cow_ts)

cow_de = decompose(cow_ts)
plot(cow_de)

cowseasonal = cow_ts - cow_de$seasonal
plot.ts(cowseasonal)

cowtrend = cow_ts - cow_de$trend
plot.ts(cowtrend)


cow_train = window(cow_ts,start = c(2010,1),end = c(2018,2))
cow_test = window(cow_ts,start = c(2018,3))


cow_train %>% ggtsdisplay(main="") # 추세 존재 
cow_train %>% diff %>% ggtsdisplay(main="")


# KPSS 검정 통계량 
summary(ur.kpss(cow_train))  # 통계량 값이 0.619로 임계값 10pct보다 높기 때문에 정상시계열이라는 귀무가설 기각
summary(ur.kpss(diff(cow_train))) # 통계량 값은 0.3395

fit <- Arima(cow_train, order=c(1,1,1))  # AICc=709
fit2 <- Arima(cow_train, order=c(0,1,1))  # AICc=707로 더 낮음 

auto.arima(cow_train)

checkresiduals(fit)
checkresiduals(fit2)

Box.test(fit$residuals,type="Ljung-Box") #p-value : 0.9949
Box.test(fit2$residuals,type="Ljung-Box") #p-value : 0.9708

F_cow = forecast(fit,h=12)
F_cow2 = forecast(fit2,h=12)

accuracy(F_cow,cow_test)
accuracy(F_cow2,cow_test)


library(ggplot2)
autoplot(F_cow)+autolayer(fitted(F_cow),series = "fitted")+xlab("Time")+ylab("Arima(1,1,1) with drift simualtion")+autolayer(cow_test)
autoplot(F_cow2)+autolayer(fitted(F_cow2),series = "fitted")+xlab("Time")+ylab("Arima(1,1,1) with drift simualtion")+autolayer(cow_test)

seasonplot(cow_ts, ylab="단가", xlab="", 
           main="",
           year.labels=TRUE, year.labels.left=TRUE, col=1:20, pch=19)

monthplot(cow_ts, ylab="단가", xlab="", xaxt="n", main="")
axis(1, at=1:12, labels=month.abb, cex=0.8)

# 3. 모형선정 ------------------------------------------------------------------------
models <- list (
  mod_arima = auto.arima(cow_train, ic='aicc', stepwise=FALSE),
  mod_exponential = ets(cow_train, ic='aicc', restrict=FALSE),
  mod_neural = nnetar(cow_train, p=12, size=25),
  mod_tbats = tbats(cow_train, ic='aicc', seasonal.periods=12),
  mod_bats = bats(cow_train, ic='aicc', seasonal.periods=12),
  mod_stl = stlm(cow_train, s.window=12, ic='aicc', robust=TRUE, method='ets'),
  mod_sts = StructTS(cow_train)
)

forecasts <- lapply(models, forecast, 12)
forecasts$naive <- naive(cow_train, 12)

par(mfrow=c(4, 2))
par(mar=c(2, 2, 1.5, 2), xaxs='i', yaxs='i')

for(f in forecasts){
  plot(f, ylim=c(0,600), main="", xaxt="n")
  lines(cow_test, col='red')
}


acc <- lapply(forecasts, function(x){
  accuracy(x, cow_test)[2,,drop=FALSE]
})

acc <- Reduce(rbind, acc)
row.names(acc) <- names(forecasts)
acc <- acc[order(acc[,'MASE']),]
round(acc, 2) # nnetar의 성능이 가장 좋음 

abs_fit <- nnetar(cow_train, ic='aicc', seasonal.periods=12)
F_nnetar = forecast(abs_fit,h=12)
autoplot(F_nnetar)

autoplot(F_nnetar)+autolayer(fitted(F_nnetar),series = "fitted")+xlab("Time")+ylab("nnetar")+autolayer(cow_test)
autoplot(F_cow2)+autolayer(fitted(F_cow2),series = "fitted")+xlab("Time")+ylab("nnetar")+autolayer(cow_test)

op <- par(mfrow = c(2,1))
par(mar=c(2, 2, 1.5, 2), xaxs='i', yaxs='i')

# 최적 모형
mod_sts_fit <- StructTS(cow_train)
ap_sts_fit_fcast <- forecast(mod_sts_fit)
plot(ap_sts_fit_fcast)


