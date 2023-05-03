set.seed(1)
a = runif(1000) # generate the random U(0,1)
b = 2*tan((a-0.5)*pi) # Use the inverse function to generate samples
b
plot(b)
summary(b)
