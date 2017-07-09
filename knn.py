import csv
import random as r
import operator as op

def loadDataset(file, splitRatio, training=[], test=[]):
    with open(file, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        data = list(lines)
        data.pop(0)
        for i in data:
            for j in xrange(2, len(i)):
                i[j] = float(i[j])
            if r.random() < splitRatio:
                training.append(i)
            else:
                test.append(i)

def distance(first, second, length):
    d = 0                           #distancia
    for i in xrange(3, length-7):
        d += (first[i] - second[i])**2
    return d**(0.5)

def neighbors(training, test, k):
    d = []                          #distancias
    length = len(test)-1
    for i in training:
        dist = distance(test, i, length)
        d.append((i, dist))
    d.sort(key=op.itemgetter(1)) #############################
    neighbors = []
    for i in range(k):
        neighbors.append(d[i][0])
    return neighbors

def testRight(test, prediction):
    right = 0
    for i in range(len(test)):
        if test[i][-1] == prediction[i]:
            right += 1
    return (right/float(len(test))) * 100.0

def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=op.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

if __name__ == "__main__":
    training = []
    test = []
    splitRatio = 0.67
    loadDataset('2015.csv', splitRatio, training, test)

    prediction = []
    k = 12
    for i in test:
        neighbor = neighbors(training, i, k)
        result = getResponse(neighbor)
        prediction.append(result)
        print('> predicted=' + repr(result) + ', actual=' + repr(i[-1]))
    accuracy = testRight(test, prediction)
    print accuracy
