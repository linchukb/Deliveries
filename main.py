# Bogdan Linchuk 003581636
import csv
import datetime
from datetime import timedelta
#Credit for hash Table: WGU Webinar - Dr. Cemal Tepe

# Used to 'deliver' packages
class Truck:

    # used to calculate drive time
    avgSpeedMph = 18

    # Constructor
    def __init__(self, truckNumber):
        self.truckNumber = truckNumber
        self.maxPackages = 16
        self.packages = []
        self.packageCount = len(self.packages)
        self.distanceTravelled = 0.0



    # Generic method may be used for any truck
    def loadTruck(self):
        global deliverTogetherPackagesLoaded
        global truck2_OnlyPackagesLoaded
        global deliverTogetherIds
        global truck2_OnlyPackageIds
        global undeliveredPackages
        global allPriorityPackagesLoaded
        global priorityPackageIds

        # Generic to load any package
        def loadPackage(self, package):
            global undeliveredPackages
            package.deliveryStatus = 'en route'
            package.enRouteTime = currentTime
            undeliveredPackages -= 1
            self.packages.append(package)
            package.deliveryTruckNum = self.truckNumber
            self.packageCount += 1

        # Update Delayed Packages
        for package in packages:
            if (package.deliveryStatus == 'Delayed') and (currentTime.time() > delayedByFlightTime.time()):
                package.deliveryStatus = 'at Hub'
            elif (package.deliveryStatus == 'Delayed - Wrong address listed') and (currentTime.time() > delayedWrongAddressUpdatedTime.time()):
                package.deliveryStatus = 'at Hub'
                package.deliveryAddress = '410 S State St'
                package.deliveryZipCode = '84111'

        # Load priority Packages
        if not allPriorityPackagesLoaded:
            tempList = []
            for id in priorityPackageIds:
                if self.packageCount < 16:
                    tempPackage = packagesHashTable.search(id)
                    if 'Delayed' not in tempPackage.deliveryStatus:
                        loadPackage(self,tempPackage)
                        tempList.append(id)
                else:
                    for tempId in tempList:
                        priorityPackageIds.remove(tempId)
                    break
            for tempId in tempList:
                priorityPackageIds.remove(tempId)
            if len(priorityPackageIds) == 0:
                allPriorityPackagesLoaded = True

        # Load packages marked 'truck 2 only'
        if (self.truckNumber == 2) and (not truck2_OnlyPackagesLoaded):
            for id in truck2_OnlyPackageIds:
                tempPackage = packagesHashTable.search(id)
                loadPackage(self,tempPackage)
            truck2_OnlyPackagesLoaded = True

        # Load remaining packages
        if (undeliveredPackages > 0) and (self.packageCount < 16):
            # Load packages marked 'Must be delivered together'
            if not deliverTogetherPackagesLoaded:
                for package in packages:
                    if not deliverTogetherPackagesLoaded:
                        if package.packageId in deliverTogetherIds:
                            for id in deliverTogetherIds:
                                priorityPackage = packagesHashTable.search(id)
                                if priorityPackage not in self.packages:
                                    loadPackage(self, priorityPackage)
                            deliverTogetherPackagesLoaded = True
            # Load non-priority packages
            for package in packages:
                if (package.deliveryStatus == 'at Hub') and ('truck 2' not in package.remarks):
                    if (undeliveredPackages > 0) and (self.packageCount < 16):
                        loadPackage(self,package)
                    else:
                        break



    # 'Delivers packages.' Contains main 'Nearest Neighbor' algorithm
    def deliverPackages(self):
        # returns index of address in list of locations

        global currentTime
        currentLocation = locations[0] #Start at hub

        # Nearest Neighbor Algorithm - Delivers next closest package onboard
        while self.packageCount > 0:
            deliveryAddressesList = []
            deliveryDistancesList = []
            tempPackageIds = []

            def loadLists(package):
                deliveryAddressesList.append(package.deliveryAddress)
                distanceToPackage = currentLocation.distances[getLocationIndex(package.deliveryAddress)]
                deliveryDistancesList.append(float(distanceToPackage))
                tempPackageIds.append(package.packageId)

            # creates list of undelivered packages on board
            for tempPackage in self.packages:
                if 'Delivered' not in tempPackage.deliveryStatus:
                    loadLists(tempPackage)

            shortestDistanceIndex = index = 0
            shortestDistance = deliveryDistancesList[0]
            tempPackageId = tempPackageIds[0]
            # finds package with nearest delivery address
            for distance in deliveryDistancesList:
                if distance < shortestDistance:
                    shortestDistance = distance
                    shortestDistanceIndex = index
                    tempPackageId = tempPackageIds[index]
                index += 1


            priorityPackageId = '6'
            if priorityPackageId in tempPackageIds:
                tempPackageId = priorityPackageId
                shortestDistance = float(currentLocation.distances[13])


            # Delivery of package
            deliveryLocation = distanceHashTable.search(deliveryAddressesList[shortestDistanceIndex])
            self.distanceTravelled += shortestDistance
            currentLocation = deliveryLocation
            package = packagesHashTable.search(tempPackageId)
            travelTimeMinutes = float(shortestDistance) / self.avgSpeedMph * 60
            currentTime = package.deliveryTime = currentTime + timedelta(minutes=travelTimeMinutes)
            package.deliveryStatus = 'Delivered at: ' + str(currentTime.strftime('%H:%M') + ' (truck ' + str(self.truckNumber) + ')')
            self.packageCount -= 1
        self.packages = []
        distanceToDeliveryLocation = currentLocation.distances[0] # Calculate Distance to hub
        self.distanceTravelled += float(distanceToDeliveryLocation) #return truck to hub
        travelTimeMinutes = float(currentLocation.distances[0]) / self.avgSpeedMph * 60
        currentTime = currentTime + timedelta(minutes=travelTimeMinutes) # Drive time back to hub


    # Displays truck details
    def printContents(self):
        print('Distance Travelled: ' + str(self.distanceTravelled))
        print('Packages on Board: ' + str(self.packageCount))
        for package in self.packages:
            package.printContents()

# Holds location details
class Location:
    def __init__(self, name, address, postalCode, distances):
        self.name = name
        self.address = address
        self.postalCode = postalCode
        self.distances = distances

# Holds package details
class Package:
    def __init__(self, id, deliveryAddress, deliveryDeadline, deliveryCity, deliveryZipCode, packageWeight, remarks):
        self.packageId = id
        self.deliveryAddress = deliveryAddress
        self.deliveryDeadline = deliveryDeadline
        self.deliveryCity = deliveryCity
        self.deliveryZipCode = deliveryZipCode
        self.packageWeight = packageWeight
        self.deliveryStatus = 'at Hub'
        self.remarks = remarks
        self.deliveryTime = None
        self.enRouteTime = None
        self.deliveryTruckNum = 0

    def printContents(self):
        print(self.packageId + ' | ' +
              self.deliveryAddress + ' | ' +
              self.deliveryDeadline + ' | ' +
              self.deliveryCity + ' | ' +
              self.deliveryZipCode + ' | ' +
              self.packageWeight + 'kg' + ' | ' +
              self.deliveryStatus
              )

# HashTable class using chaining.
class HashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])


def getLocationIndex(address):
    index = 0
    for location in locations:
        if address == location.address:
            return index
        index += 1

# Displays list of all packages at given time
def displayAllPackagesStatus(
        time):
    for package in packages:
        lookupPackage(package.packageId, time)

# used by displayAllPackageStatus
def lookupPackage(packageId, time):
    global delayedByFlightTime
    time = time.strftime('%H:%M')
    foundPackage = packagesHashTable.search(packageId)

    if foundPackage.enRouteTime:
        enRouteTime = foundPackage.enRouteTime.strftime('%H:%M')
    else:
        enRouteTime = None
    if foundPackage.deliveryTime:
        deliveryTime = foundPackage.deliveryTime.strftime('%H:%M')
    else:
        deliveryTime = None

    if foundPackage:
        temp = foundPackage.deliveryStatus
        if ('Delayed' in foundPackage.remarks) and (time < delayedByFlightTime.strftime('%H:%M')):
            foundPackage.deliveryStatus = 'Delayed By flight. En route to Hub'
            foundPackage.printContents()
            foundPackage.deliveryStatus = temp
        elif enRouteTime and (time < enRouteTime):
            foundPackage.deliveryStatus = 'at Hub'
            foundPackage.printContents()
            foundPackage.deliveryStatus = temp
        elif deliveryTime and (time < deliveryTime):
            foundPackage.deliveryStatus = 'en route at ' + str(enRouteTime) + '(Truck ' + str(
                package.deliveryTruckNum) + ')'
            foundPackage.printContents()
            foundPackage.deliveryStatus = temp
        else:
            foundPackage.printContents()
    else:
        print('Package not found')

# Delivers all packages
def simulateDeliveries():
    global currentTime, truck1Time,truck2Time, delayedByFlightTime
    while undeliveredPackages > 0:
        currentTime = truck1Time
        truck1.loadTruck()
        truck1.deliverPackages()
        truck1Time = currentTime
        if (undeliveredPackages > 0) and (currentTime >= delayedByFlightTime): #hold truck 2 for remaining priority packages
            truck2.loadTruck()
            truck2.deliverPackages()
            truck2Time = currentTime

# Displays menu for user interface
def printMenu():
    print('1 - View all packages status')
    print('2 - Lookup Package')
    print('3 - Truck Mileage')
    print('0 - Quit')

# Main
if __name__ == '__main__':

    # Initialize and Declare global lists and variables
    global delayedByFlightTime
    global delayedWrongAddressUpdatedTime
    dayStartTime = delayedByFlightTime = delayedWrongAddressUpdatedTime = datetime.datetime.now()
    dayStartTime = dayStartTime.replace(hour=8, minute=0)
    global currentTime
    currentTime = dayStartTime
    truck1Time = truck2Time = dayStartTime
    delayedByFlightTime = delayedByFlightTime.replace(hour=9,minute=5)
    delayedWrongAddressUpdatedTime = delayedWrongAddressUpdatedTime.replace(hour=10,minute=20)
    packages = []
    locations = []
    truck1 = Truck(1)
    truck2 = Truck(2)
    global deliverTogetherPackagesLoaded
    deliverTogetherPackagesLoaded = False
    global deliverTogetherIds
    deliverTogetherIds = ['13', '14', '15', '16', '19', '20']
    global truck2_OnlyPackagesLoaded
    truck2_OnlyPackagesLoaded = False
    global truck2_OnlyPackageIds
    truck2_OnlyPackageIds = ['3','18','36','38']
    global allPriorityPackagesLoaded
    allPriorityPackagesLoaded = False
    global priorityPackageIds
    priorityPackageIds = []

    # Create hash Table for distances
    distanceHashTable = HashTable()
    # Load distance from file
    with open('Distances.csv', newline='') as distanceCsvFile:
        file = csv.reader(distanceCsvFile, delimiter=',')
        for row in file:
            distances = [
                row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13],
                row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23],
                row[24], row[25], row[26], row[27], row[28], row[29]
            ]
            location = Location(row[0], row[1], row[2], distances)
            locations.append(location)
            distanceHashTable.insert(location.address, location)

    # Create hash Table for packages
    packagesHashTable = HashTable()
    # Load packages from file
    with open('package_new.csv', newline='') as packagesCsvFile:
        file = csv.reader(packagesCsvFile, delimiter=',')
        for row in file:
            package = Package(row[0], row[1], row[5], row[2], row[4], row[6], row[7])
            packages.append(package)
            packagesHashTable.insert(package.packageId, package)
    global undeliveredPackages
    undeliveredPackages = len(packages)

    # set delayed packages
    for package in packages:
        if 'Delayed' in package.remarks:
            package.deliveryStatus = 'Delayed'
        if 'Wrong address listed' in package.remarks:
            package.deliveryStatus = 'Delayed - Wrong address listed'

    # Set priority PackageId list
    for package in packages:
        if package.deliveryDeadline != 'EOD':
            priorityPackageIds.append(package.packageId)

    # Deliver all packages
    simulateDeliveries()

    # Main Menu Loop
    userInput = -1
    while (1):
        print()
        # Displays all packages info at certain time
        if userInput == 1:  # Print packages info
            print('\n\n')
            print('ALL PACKAGES STATUS')
            searchTime = input('Enter a time (HH:MM): ')
            searchTime = datetime.datetime.strptime(searchTime, '%H:%M').time()  # searchtime to time format
            print()
            displayAllPackagesStatus(searchTime)
            print('\n\n')
        # Displays selected package at certain time
        elif userInput == 2:
            print('\n\n')
            packageId = input('Package Id: ')
            searchTime = input('Enter a time (HH:MM): ')
            searchTime = datetime.datetime.strptime(searchTime, '%H:%M').time()
            lookupPackage(packageId, searchTime)
            print('\n\n')
        # Displays combined truck mileage
        elif userInput == 3:
            print('\n\n')
            print('Final combined truck mileage: ' + str(truck1.distanceTravelled + truck2.distanceTravelled))
            print('\n\n')
        # Terminates program
        elif userInput == 0:  # Exit program
            exit()
        printMenu()
        userInput = int(input('Choose an option: '))