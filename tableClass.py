#table class for transportation model
import tkinter as tk
from tkinter import ttk, Canvas #importing the Tkinter libraries to be used to create the interface
#the Canvas library allows a programmer to create shapes and vector images

class tableClass:
    def __init__(self, rows, columns, factories, warehouses, totalSupply, totalDemand, matrix, entries):
        self.rows = rows
        self.columns = columns
        self.factories = factories
        self.warehouses = warehouses
        self.totalSupply = totalSupply
        self.totalDemand = totalDemand
        self.matrix = matrix
        self.entries = entries
        #initialising all variables needed throughout the class

    def createTable(self): 
        #this method creates the entry matrix where the user can enter their data
        if self.totalDemand != self.totalSupply:
            total = self.totalDemand, ',', self.totalSupply
        else:
            total = self.totalSupply #creating a variable of the total supply/ demand that will be displayed on the interface

        for y in range(self.rows):
            row = []
            for x in range(self.columns): 
            #loops through a number of times to get the right dimensions for the entry matrix 
            #there should be a column for each warehouse and a row for each factory
                if y == 0 and x == 0:
                    a = ttk.Label(self.matrix) 
                    #by creating a label, the user will not be able to change the text displayed
                    a["text"] = "Factory|Warehouse" 
                    #creating a title to show what each row and column represents
                    row.append(None) 
                elif y == self.rows-1 and x == self.columns-1:
                    a = ttk.Label(self.matrix)
                    a["text"] = "Total:", total 
                    #creating a label for the total supply and demand stated by the user
                    row.append(None)
                elif x == 0 and y == (self.rows-1):
                    a = ttk.Label(self.matrix)
                    a["text"] = "Demand" #creating a title for the Demand column
                    row.append(None)
                elif y == 0 and x == self.columns-1:
                    a = ttk.Label(self.matrix)
                    a["text"] = "Supply" #creating a title for the Supply row
                    row.append(None)
                    #all of the above cells are given a value of None so they aren't included in the 2D array used to store the user's data
                else:
                    a = ttk.Entry(self.matrix)
                    #this enables the user to change/ input a value into the cell
                    if y == 0 and x > 0:
                        a.insert(0, "W" + str(x))
                        #prepopulates cell with label ('W1', 'W2' etc) but created so the user can change it
                    elif x == 0 and y > 0:
                        a.insert(0, "F" + str(y))
                        #prepopulates cell with label ('F1', 'F2' etc) but created so the user can change it
                    else:
                        pass
                    row.append(a) #adds the row just created to the 2D matrix
                a["width"] = 14 
                a.grid(row = y, column = x) #adding the cell to the Tkinter interface
            self.entries.append(row) #adding the row created on the corresponding iteration to a single identifier
            #this will form a 2D matrix


class analysisClass:
    def __init__(self, cost, rows, columns, factories, warehouses, totalSupply, totalDemand, method, allocationArray, blankCanvas, degenerate):
        self.cost = cost
        self.rows = rows
        self.columns = columns
        self.factories = factories
        self.warehouses = warehouses
        self.totalSupply = totalSupply
        self.totalDemand = totalDemand
        self.method = method
        self.allocationArray = allocationArray
        self.blankCanvas = blankCanvas
        self.degenerate = degenerate
        #initialises variabales needed wihtin this class

    def __calculateTotal(self): 
    #calculates the total allocations made for each row and column
    #made as a private method so it cannot be called outside of the class
    #this will ensure it is not confused with other functions in the main program
        for x in range(self.factories):
            totalAllocations = 0
            for y in range(self.warehouses):
                if self.allocationArray[x][y] > 0:
                    totalAllocations += self.allocationArray[x][y]
                else:
                    pass
            #iterates through the allocation array for each row and adds together the allocations made
            self.allocationArray[x].append(totalAllocations) 
            #the allocations made are added to the end of each row of the alllcationArray

        row = [0] * self.columns 
        self.allocationArray.append(row)
        #adds an row of zeros to the end of allocationArray so it can be edited later on
        total = 0

        for y in range(self.warehouses):
            totalAllocations = 0
            for x in range(self.factories):
                if self.allocationArray[x][y] > 0: 
                    #going through each column and adding together the allocations for that column
                    totalAllocations += self.allocationArray[x][y] 
                    total += self.allocationArray[x][y]
                else:
                    pass
            self.allocationArray[-1][y] = totalAllocations 
            #apending the allocations made in the column to the end of the corresponding column

        return total, self.allocationArray #returning the array and total so the appended versions can be used

    def __balancedChecked(self):
        #to ensure dummy rows/ columns arent counted when creating the network graphs
        if self.totalDemand > self.totalSupply:
            del self.allocationArray[-1] #removing dummy row
        elif self.totalSupply > self.totalDemand:
            for j in self.allocationArray: #removing dummy column
                del j[-1]
        else:
            pass
        return self.allocationArray #returning updated allocationArray

    def __labelAllocationArray(self): 
        #adds the row and column labels to the allocation array
        #another private method not to be called out of the class
        label = ["F|W"]
        #the labels for each row/ column will be added to the array before being added to the allocation array
        for q in range(1, self.columns):
            if q == self.columns-1:
                label.append("TOTAL")
            else:
                label.append("W" + str(q)) 
                #adding warehouse labels for each column, with the 'total' label in the last column
        self.allocationArray.insert(0, label) 
        #inserting the label array into the allocationArray 

        for p in range(1, self.rows):
            if p == self.rows-1:
                label = "TOTAL"
            else:
                label = 'F'+str(p) 
                #adding factory labels to each row, with 'total' being added as the last row
            self.allocationArray[p].insert(0, label) 
            #inserting labels for each row to the allocationArray so the user can identify what each cell means
        return self.allocationArray #returning the updated allocation array


    def analysisPage(self):
        #adds the written information onto the results interface
        self.blankCanvas.create_text(150,10, text = "Using the "+ self.method +":")
        self.blankCanvas.create_text(150,30, text = "A network graph of the different routes taken.", fill = 'grey')
        self.blankCanvas.create_text(150,50, text = "The supplies to be transported are shown.", fill = 'grey')
        self.blankCanvas.create_text(150,80, text = "The total cost for this method is: £" + str(self.cost))
        self.blankCanvas.create_text(500,30, text = "This shows an adjacency matrix.\nThese are the units to be transported from the \nspecified factories to the specified warehouses", fill = "grey")
        #outputting this information to the user so they can understand the results

        if self.degenerate: #if degenerate the solution will not be optimised so the user must be told
            self.blankCanvas.create_text(150,65, text = "This is a degenerate solution.", fill = 'red')

    def networkGraph(self): 
        #creates the network graph to be displayed on the results interface
        nodes = [100, 200, 300, 400, 500, 600] 
        #each index will be used as a constant for the positioning of the graph nodes
        #the maximum number of nodes there can be are 6
        self.allocationArray = self.__balancedChecked() 
        #checks whether or not the supply and demand are equal and if not adapts the allocation array so it is in the correct syntax

        for x in range(self.factories):
            self.blankCanvas.create_oval(70, nodes[x], 100, nodes[x]+30, fill = "#aad6ff") 
            #the coordinates for each node changes because of the for loop, creating a line of nodes
            self.blankCanvas.create_text((85, nodes[x]+15), text="F"+str(x+1)) 
            #labels each node with a factory number, the indexing starts at 0 so 1 must be added to the factory number

        for y in range(self.warehouses):
            self.blankCanvas.create_oval(200, nodes[y], 230, nodes[y]+30, fill = "#ffb3ab")
            self.blankCanvas.create_text((215, nodes[y]+15), text="W"+str(y+1)) 
            #creates nodes for all the warehouses and labels each one with the warehouse number

        lineCreated = False #used as a fallback method if the solution has no allocations
        for f in range(len(self.allocationArray)):
            for w in range(self.warehouses):
                if self.allocationArray[f][w] > 0: 
                    #checking each cell to see if an allocation has been made
                    self.blankCanvas.create_line(100,nodes[f]+15,200,nodes[w]+15) 
                    #creates a line for an allocation between the corresponding factory (f) and warehouse (w)
                    lineCreated = True 
                else:
                    pass
               
        if lineCreated == False: 
            #explains why there are no connections between nodes
            self.blankCanvas.create_text(500,60, text = "The solution is degenerate and unbalanced so there is no solution", fill = "red")
    
    def resultsTable(self): 
        #creates the table showing the allocations
        xCoOrd = [300,350,400,450,500,550,600,650,700]
        yCoOrd = [100,130,160,190,220,250,280,310,340] 
        #both arrays are used to create coordinates for the table of allocations

        total, self.allocationArray = self.__calculateTotal() 
        #calculates the total allocations for each row and column and appends it to the allocationArray 
        self.allocationArray = self.__labelAllocationArray() 
        #adds the row and column labels back in from the original input matrix
        del self.allocationArray[-1][-1]
        #removes very last cell as it is replaced in the previous line

        for x in range(self.rows):
            for y in range(self.columns):
                self.blankCanvas.create_rectangle(xCoOrd[y], yCoOrd[x], xCoOrd[y+1], yCoOrd[x+1]) 
                #creates a table made up of rectangles
                #it is the easiest way to create the table since the Canvas library is in use on this window

        for x in range(self.rows):
            for y in range(self.columns):
                if x == self.rows-1 and y == self.columns-1:
                    self.blankCanvas.create_text((xCoOrd[y]+25, yCoOrd[x]+15), text= str(total)) 
                    #adds total supply and demand label to the table
                else:
                    self.blankCanvas.create_text((xCoOrd[y]+25, yCoOrd[x]+15), text=str(self.allocationArray[x][y])) 
                    #adds the allocations made at all factories/warehouses, if no allocations are made it is shown as 0

