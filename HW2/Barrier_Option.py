import numpy as np
def CI_95(data):
    a = np.array(data)
    n = len(a)
    m = np.mean(a)
    sd = np.std(a,ddof=1)
    hw = 1.96*sd / np.sqrt(n)
    return m, [m-hw,m+hw]
Maturity = 1.0
InterestRate = 0.05
Sigma = 0.3
InitialValue = 50.0
StrikePrice = 55.0
B = 60 # Set the barrier value
Steps = 64
Interval = Maturity / Steps
Sigma2 = Sigma * Sigma / 2

np.random.seed(1)
Replications = 100
ValueList = [] # List to keep the option value for each sample path
for i in range(0,Replications):
    Sum = 0.0
    Xt = [] # add a list to store stock price X at each step
    X = InitialValue
    for j in range(0,Steps):
        Z = np.random.standard_normal(1)
        X = X * np.exp((InterestRate - Sigma2) * Interval +
                       Sigma * np.sqrt(Interval) * Z)
        Sum = Sum + X
        Xt.append(X) # record the stock price at step j to the list Xt
    Value = np.exp(-InterestRate * Maturity) *int(max(Xt) < B) * max(Sum/Steps - StrikePrice, 0) # add the indicator function
    ValueList.append(float(Value))
    print(max(Xt),Sum/Steps)
print ("Mean and CI:", CI_95(ValueList))