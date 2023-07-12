from tkinter import ttk
import tkinter as tk                    
import os
import csv

class Item:
	def __init__(self, id, description, price):
		self.id = id
		self.description = description
		self.price = price

#Global Variables
usdToVes = 29.99


#Tabs

root = tk.Tk()
root.title("Caja Registradora")

tabControl = ttk.Notebook(root)

orderTab = ttk.Frame(tabControl)
itemTab = ttk.Frame(tabControl)

tabControl.add(orderTab, text ='Orden')
tabControl.add(itemTab, text ='Productos')
tabControl.pack(
				# expand = 1,
				# fill ="both"
				)

cur_path = os.path.dirname(__file__)
product_path = os.path.join(cur_path, "Items")

# Currencies = ["VES", "USD"]
		# self.currency = currency

# Populate Item List
itemDict = {}

for itemFileName in os.listdir(product_path):
	itemFile = open(os.path.join(product_path, itemFileName), "r")
	
	for itemFileLine in csv.reader(itemFile):
		# print(itemFileLine)
		if(len(itemFileLine) != 3
     		or itemFileLine[0] in itemDict.keys()
			):
			print("Invalid Item")
			continue

		id = itemFileLine[0]
		description = itemFileLine[1]
		price = float(itemFileLine[2])
		itemDict[id] = (Item(id, description, price))

# itemDict.sort(key=lambda x: x.id)

# Show Items on Item Tab
itemTreeView = ttk.Treeview(itemTab, 
							column = ("id", "description", "priceUsd", "priceVes"), 
							show = "headings",
							# height = 5
							)

itemTreeView.column("id")
itemTreeView.column("description")
itemTreeView.column("priceUsd", anchor = "e")
itemTreeView.column("priceVes", anchor = "e")

itemTreeView.heading("id", text = "ID")
itemTreeView.heading("description", text = "Descripción")
itemTreeView.heading("priceUsd", text = "Precio (USD)")
itemTreeView.heading("priceVes", text = "Precio (VES)")

for itemId in itemDict:
	itemTreeView.insert("", "end", values = (itemDict[itemId].id, itemDict[itemId].description, '{:.2f}'.format(itemDict[itemId].price), '{:.2f}'.format(itemDict[itemId].price * usdToVes)))


#Order List
orderTreeView = ttk.Treeview(orderTab, 
							column = (
									"id",
									"description",
		 							# "quantity",
									# "unitPriceUsd",
									"priceUsd",
									"priceVes"), 
							show = "headings",
							# height = 5
							)

orderTreeView.column("id")
orderTreeView.column("description")
# orderTreeView.column("quantity")
# orderTreeView.column("unitPriceUsd")
orderTreeView.column("priceUsd", anchor = "e")
orderTreeView.column("priceVes", anchor = "e")

orderTreeView.heading("id", text = "ID")
orderTreeView.heading("description", text = "Descripción")
# orderTreeView.heading("quantity", text = "Cantidad")
# orderTreeView.heading("unitPriceUsd", text = "Por Unidad (USD)")
orderTreeView.heading("priceUsd", text = "Precio (USD)")
orderTreeView.heading("priceVes", text = "Precio (VES)")




#Search bar
orderIdVar = tk.StringVar()

# orderListId = 0
def addItemToOrder(self):
	# print(orderIdVar.get())
	# if(orderIdVar.get() in (o.id for o in itemDict)):
	# 	print(orderIdVar.get())
	# 	itemTreeView.insert("", "end", values = (o.id, o.description, '{:.2f}'.format(o.price), '{:.2f}'.format(o.price * usdToVes)))
	# orderList = []
	# orderList.insert([orderListId, ])
	if orderIdVar.get() in itemDict.keys():
		orderTreeView.insert("", "end", values = (
												itemDict[orderIdVar.get()].id,
												itemDict[orderIdVar.get()].description,
					    						# 1,
					    						# '{:.2f}'.format(itemDict[orderIdVar.get()].price),
												'{:.2f}'.format(itemDict[orderIdVar.get()].price),
												'{:.2f}'.format(itemDict[orderIdVar.get()].price * usdToVes)))
		# orderTreeView.insert("", "end", values = (itemDict[orderIdVar.get()].description, 1, '{:.2f}'.format(itemDict[orderIdVar.get()].price), '{:.2f}'.format(itemDict[orderIdVar.get()].price), '{:.2f}'.format(itemDict[orderIdVar.get()].price * usdToVes)))
	updateSubtotal()

#Total
subtotalAmountLabel = tk.Label(orderTab, text = f"Subtotal:\t\t{0:.2f}\t{0:.2f}")

def updateSubtotal():
	subtotalAmount = 0
	for order in orderTreeView.get_children():
		subtotalAmount += float(orderTreeView.item(order, "values")[2])
		# print(orderTreeView.item(order, "values"))


	# print(subtotalAmount)
	subtotalAmountLabel.config(text = f"Subtotal:\t\t{subtotalAmount:.2f}\t{subtotalAmount*usdToVes:.2f}")
# subtotalTextLabel = tk.Label(orderTab, text = 'aaaaaaaaaaaaaaa:\t\t{:.2f}'.format(0))


orderEntry = tk.Entry(orderTab, textvariable = orderIdVar)
orderEntry.bind('<Return>', addItemToOrder)
orderEntry.bind('<KP_Enter>', addItemToOrder)


#Buttons
def removeSelectedItems():
	for order in orderTreeView.selection():
		# print(orderTreeView.item(order, "values"))

		orderTreeView.delete(order)
		# print(self.tree.identify(event.x,event.y))

removeSelectedItemsButton = tk.Button(orderTab, text = "Remover Selección", command = removeSelectedItems)

def removeAllItems():
	for order in orderTreeView.get_children():
		orderTreeView.delete(order)
removeAllItemsButton = tk.Button(orderTab, text = "Remover Todo", command = removeAllItems)


#Grid
itemTreeView.grid()
orderEntry.grid(sticky = 'ew')
orderTreeView.grid(sticky = "ew")
# subtotalTextLabel.grid(sticky = "e", row=2)
subtotalAmountLabel.grid(sticky = "e")
# subtotalTextLabel.grid(sticky = "e", column = 0, row=2)
# subtotalTextLabel.grid(padx=10, column = 0, row=10)

removeSelectedItemsButton.grid()

removeAllItemsButton.grid()


root.mainloop()