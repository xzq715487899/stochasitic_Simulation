library(fitdistrplus)
Data <- read.csv("SemiconductorData.csv", header=TRUE,
                    sep=",", na.strings=c("NA", ""), stringsAsFactors=FALSE, as.is=TRUE)
MyData <- Data$LOADUNLOAD
plotdist(Data$LOADUNLOAD, histo = TRUE, demp = TRUE)
descdist(MyData)
# fit a lognormal distribution to the LOS samples
fln <- fitdist(MyData, "lnorm")
summary(fln)
plot(fln)

# fit a weibull distribution
fw <- fitdist(MyData, "weibull")
summary(fw)
plot(fw)

# fit a gamma distribution
fg <- fitdist(MyData, "gamma")
summary(fg)
plot(fg)


# compare the fits
par(mfrow = c(2, 2))
plot.legend <- c("Weibull", "lognormal", "gamma")
denscomp(list(fw, fln, fg), legendtext = plot.legend)
qqcomp(list(fw, fln, fg), legendtext = plot.legend)
cdfcomp(list(fw, fln, fg), legendtext = plot.legend)

# Perform GofFit tests
gof_results <- gofstat(list(fw, fln, fg), fitnames = c("weibull", "lnorm", "gamma"))
gof_results
gof_results$kstest

gof_results$chisq
gof_results$chisqpvalue
gof_results$chisqtable
