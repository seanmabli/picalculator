import aiinpy as ai
import requests

open('pi.txt', "w").write('')
pi = ''
for i in range(1000):
  pi += requests.get('https://api.pi.delivery/v1/pi?start=' + str(i * 1000) + '&numberOfDigits=1000').json()["content"]

model = ai.lstm(inshape=10, outshape=10, outactivation=ai.stablesoftmax(), learningrate=0.01)

Data = np.genfromtxt('testing\data\Timeseries\Airpassenger.csv', dtype=int)
Data = (Data - min(Data)) / (max(Data) - min(Data)).astype(float)

TrainingData = Data[0 : 100, np.newaxis]
TestData = Data[100 :, np.newaxis]

NumOfTrainGen = 15000
NumOfTestGen = len(TestData) - 6

with alive_bar(NumOfTrainGen + NumOfTestGen) as bar:
  for Generation in range(NumOfTrainGen):
    Random = np.random.randint(0, len(TrainingData) - 5)

    input = TrainingData[Random : Random + 5]  
    out = model.forward(input)
    
    outError = TrainingData[Random + 1 : Random + 6] - out
    inError = model.backward(outError)

    bar()

  Error = 0
  for Generation in range(NumOfTestGen):
    input = TestData[Generation : Generation + 5]
    out = model.forward(input)

    outError = TestData[Generation + 1 : Generation + 6] - Out
    Error += abs(TestData[Generation + 6] - Out[4])
    inError = model.backward(outError)

    bar()
  
print(Error / NumOfTestGen)