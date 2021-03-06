import functools
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import yfinance
import math


def main():    
    print("Reading Tweets Dataset")
    sentences = []
    count = -1
    with open('tweets.csv', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile )
        for row in csvreader:
            if(count != -1):
                sentences.append([row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8]])
            count += 1
        
        if(count != len(sentences)):
            print("Reading Error: Count not equal")
    print(len(sentences))
    stocks = []
    count = -1
    with open('stocks.csv', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile )
        for row in csvreader:
            if(count != -1):
                # date, company, open, close
                stocks.append([row[0], row[1], row[6], row[3]])
            count += 1
    inputs = []
    outputs = []
    pos = 0
    neg = 0
    neu = 0
    total = 0
    for s in sentences:
        total += 1
        if s[5] >= s[6] and s[5] >= s[7]:
            pos += 1
        if s[6] >= s[5] and s[6] >= s[7]:
            neg += 1
        if s[7] >= s[5] and s[7] >= s[6]:
            neu += 1
            
    print(float(pos)/float(total))
    print(float(neg)/float(total))
    print(float(neu)/float(total))
    for sentence in sentences:
        company_name = str(sentence[0])
        company_date = str(sentence[1])
        close_price = 0
        open_price = 0
        flag = 0
        for s in stocks:
            if (s[0] == company_date and s[1] == company_name):
                flag = 1
                close_price = s[3]
                open_price = s[2]
                break
        if (flag == 1):
            
            delta = float(close_price) - float(open_price)
            if(delta >= 0):
                count += 1
            inputs.append([float(sentence[2]), float(sentence[3]), float(sentence[4]), float(sentence[5]), float(sentence[6]), float(sentence[7]), float(open_price)])
            outputs.append(float(delta))
    def errorFunction(actual, predictions):
        sum = 0
        for i in range(0, len(actual)):
            if(actual[i] < 0 or actual[i] > 0):
                sum += abs((actual[i] - predictions[i])/(actual[i]))
            else:
                sum += abs((0.001 - predictions[i])/(0.001))
        return float(sum/len(actual))

    def accuracy(actual, predictions):
        sum = 0
        for i in range(0, len(actual)):
            if(actual[i] < 0 and predictions[i] < 0):
                sum += 1
            elif(actual[i] >= 0 and predictions[i] >= 0):
                sum += 1

        return float(sum/len(actual))
    
    print(len(inputs))
    print("Creating sklearn Model")
    import numpy as np
    from sklearn.linear_model import LinearRegression
    for k in [0.75, 0.8]:
        start = int(len(inputs)*k)
        reg = LinearRegression().fit(inputs[0:start], outputs[0:start])
        predictions = reg.predict(inputs[start: len(inputs)])
        actuals = outputs[start: len(inputs)]
        print("k=" + str(k) + " Percent Error: " + str(errorFunction(actuals, predictions)*100))
        print("k=" + str(k) + " Accuracy: " + str(accuracy(actuals, predictions)*100))
        #print(reg.get_params())

    print("----------------------------------")
    def accuracy2(actual, predictions):
        sum = 0
        for i in range(0, len(actual)):
            if(actual[i] == predictions[i]):
                sum += 1

        return float(sum/len(actual))

    def accuracy3(actual, predictions3):
        zz = 0
        zo = 0
        oz = 0
        oo = 0
        for i in range(0, len(actual)):
            if(predictions3[i] == 0 and actual[i] == 0):
                zz += 1
            if(predictions3[i] == 1 and actual[i] == 0):
                zo += 1
            if(predictions3[i] == 0 and actual[i] == 1):
                oz += 1
            if(predictions3[i] == 1 and actual[i] == 1):
                oo += 1

        print(float(zz))
        print(float(oz))
        print(float(zo))
        print(float(oo))

    outputs2 = []
    for d in outputs:
        if(d < 0):
            outputs2.append(0)
        elif(d >= 0):
            outputs2.append(1)
    from sklearn.linear_model import LogisticRegression
    for k in [0.75, 0.8]:
        start = int(len(inputs)*k)
        reg = LogisticRegression(max_iter = 10000).fit(inputs[0:start], outputs2[0:start])
        predictions = reg.predict(inputs[start: len(inputs)])
        actuals = outputs2[start: len(inputs)]

if __name__ == '__main__':
    main()