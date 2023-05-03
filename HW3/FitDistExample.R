# This file uses the fitdistrplus package. You'll need to install it first
# by running the command: 'install.packages("fitdistrplus")' in R
require(fitdistrplus)

# import the data from .csv file
# data includes length of stay of patients in the ED for different ESI (urgency) levels
LOSData <- read.csv("LOS.csv", header=TRUE,
                   sep=",", na.strings=c("NA", ""), stringsAsFactors=FALSE, as.is=TRUE)
MyData <- LOSData$LOS
plotdist(LOSData$LOS, histo = TRUE, demp = TRUE)

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

# Could it be that the data is not iid?
# Only consider data points where ESI level is 3

MyData_ESI3 <- LOSData$LOS[which(LOSData$ESILevel=="ESI Level 3")]
plotdist(MyData_ESI3, histo = TRUE, demp = TRUE)

# fit the 3 distributions again; this time only to ESI 3 LOS's
fln <- fitdist(MyData_ESI3, "lnorm")
summary(fln)
plot(fln)

fw <- fitdist(MyData_ESI3, "weibull")
summary(fw)
plot(fw)

fg <- fitdist(MyData_ESI3, "gamma")
summary(fg)
plot(fg)

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

# Seems like Gamma or Weibull adequately model the LOS for ESI 3 patients. 
# Can repeat the process for other ESI levels as well.