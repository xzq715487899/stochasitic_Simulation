library(fitdistrplus)
Data <- read.csv("TeslaPrices.csv", header=TRUE,
                 sep=",", na.strings=c("NA", ""), stringsAsFactors=FALSE, as.is=TRUE)
Rate <- Data$Rate
plotdist(Rate, histo = TRUE, demp = TRUE)
descdist(Rate)

# fit a lognormal distribution to the LOS samples
fln <- fitdist(Rate, "lnorm")
summary(fln)
plot(fln)

gof_results <- gofstat(fln, fitnames = c("lnorm"))
gof_results
gof_results$kstest

gof_results$chisq
gof_results$chisqpvalue
gof_results$chisqtable
