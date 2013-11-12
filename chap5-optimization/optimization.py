import time
import random
import math

people = [('Seymour', 'BOS'),
        ('Franny', 'DAL'),
        ('Zooey', 'CAK'),
        ('Walt', 'MIA'),
        ('Buddy', 'ORD'),
        ('Les', 'OMA')]

# Laguardia airport in NY
destination = 'LGA'

flights = {}
for line in file('schedule.txt'):

    # LGA,MIA,20:27,23:42,169
    origin, dest, depart, arrive, price = line.strip( ).split(',')
    flights.setdefault((origin, dest), [])

    flights[(origin, dest)].append((depart, arrive, int(price)))

def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]

def printschedule(r):
    # for d in range(0, len(r), 2):
    for d in range(0, len(r)/2, 1):
        name = people[d][0]
        origin = people[d][1]
        departure = r[2*d]
        arrive = r[2*d+1]
        out = flights[(origin, destination)][departure]
        ret = flights[(origin, destination)][arrive]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])

s = [1,4,3,2,7,3,6,3,2,4,5,3]
printschedule(s)

def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60

    for d in range(len(sol)/2):

        # Get the inbound and outbound flights
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(origin, destination)][int(sol[2*d+1])]

        # Total price is the price of all outbound and return flights
        totalprice += outbound[2]
        totalprice += returnf[2]

        # Track the latest arrival and earlist departure
        if latestarrival < getminutes(outbound[1]):
            latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]):
            earliestdep = getminutes(returnf[0])

    # Every person must wait at the airport until the latest person arrives
    # They also must arrive at the same time and wait for their flights
    totalwait = 0

    for d in range (len(sol)/2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(origin, destination)][int(sol[2*d+1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

    # Does this solution require an extra day of car rental? That'll be $50!
    if latestarrival < earliestdep: totalprice + 5

    return totalprice + totalwait

print schedulecost(s)
