# pyinstaller --font-path /usr/share/fonts my_script.py
#pyinstaller --windowed  --add-data "image1.jpg;." --add-data "image2.jpg;." --add-data "image3.jpg;." --icon=myLogo.ico myPythonFile.py


import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import sys
import os
import qrcode
from PIL import Image
from time import *


#all the backend is here
#region
product_list=[]
id=""

#initial items in the product section
items = {
    "apple": 100.0,
    "maggi": 20.0,
    "oil": 120.0,
    "shampoo": 10.0,
    "almond": 40.0,
    "jam": 80.0,
    "ghee 1kg": 500.0,
    "bread": 40.0
    # Add more items here
}


def add_item():
    product_name = itemname_entry_var.get()
    price = float(price_entry_var.get())
    quantity = int(quantity_entry_var.get())

    if product_name and price and quantity:
        product_list.append([product_name, price, quantity,price*quantity])
        table.insert('', "end", values=(product_name, price, quantity,price*quantity))
        #itemname_entry.delete(0,"end")
        
        j=0
        total=0.0
        for i in product_list:
            total=total+product_list[j][3]
            j+=1
        total_bill.set(total)           
    else:
        messagebox.showerror("ERROR","Product name, price and quantity can't be empty. \nPrice and Quantity must be numeric. ") 

    price_entry_var.set(float(0.0))
    quantity_entry_var.set(int(0))
    itemname_entry_var.set("")
    combo_item.focus_set()


def on_enter(event):
    add_item()


def delete_item():
    selected_item = table.selection()
    if selected_item:
        item=table.item(selected_item)
        table.delete(selected_item)
        for product in product_list:
            if product[0]== item['values'][0]:
                product_list.remove(product)
    total=0.0
    if product_list==[]:
        total_bill.set(total)

    else:
        j=0
        for i in product_list:
            total=total+product_list[j][3]
            j+=1
            total_bill.set(total)


def combo_clicked(event):
    a=combo.get()
    if a=="Online":
       
        button_qr.configure(state=ttk.NORMAL)
               
    else:
        button_qr.configure(state=ttk.DISABLED)
        var_label_recieved.set("")
        var_label_return.set("")
        button_return.configure(state=ttk.DISABLED)
        entry_recieved.configure(state=ttk.DISABLED)
        label_return_money.configure(state=ttk.DISABLED)
        var_return.set(0)
        

    if a=="Offline":
        button_return.configure(state=ttk.NORMAL)
        entry_recieved.configure(state=ttk.NORMAL)
        label_return_money.configure(state=ttk.NORMAL)
        var_label_recieved.set("RECIEVED MONEY")
        var_label_return.set("RETURN: RS. ")

    else:
        var_label_recieved.set("")
        var_label_return.set("")
        button_return.configure(state=ttk.DISABLED)
        entry_recieved.configure(state=ttk.DISABLED)
        label_return_money.configure(state=ttk.DISABLED)
        var_return.set(0)


def create_qr():
    
    link="upi://pay?pa=mayurkunde@kotak&cu=INR&pn=ZMART&am="+str(total_bill.get())+"&tn=ZMART+BILL"
    code=qrcode.make(link)
    code.save("QR.png")


    
    # new_window = ctk.CTkToplevel(window)
    # new_window.title("SCAN")


    
    # imgpath=os.path.join(os.path.dirname(__file__),'QR.png')
    # img=ctk.CTkImage(light_image=Image.open(imgpath),size=(350,350))
    # label = ctk.CTkLabel(master=new_window, image=img,text="")
    # label.pack()

    img =Image.open("QR.png")
    img.show()

    # label1 = ctk.CTkLabel(master=new_window,text="SCAN TO PAY",font=("calibri",45,"bold"))
    # label1.pack(fill="both")
    # new_window.attributes('-topmost', 'true')
    # new_window.mainloop()
    

def new_bill():
    result=messagebox.askquestion("WARNING","All your entries will be gone !! ")

    if result=="yes":
        
        var_entry_customer_contact.set("")
        var_label_customer_name.set("")
        price_entry_var.set(float(0))
        itemname_entry_var.set("")
        quantity_entry_var.set(int(0))
        var_combobbox.set("")
        total_bill.set(float(0))
        product_list.clear()
        var_label_recieved.set("")
        var_label_return.set("")
        button_return.configure(state=ttk.DISABLED)
        entry_recieved.configure(state=ttk.DISABLED)
        label_return_money.configure(state=ttk.DISABLED)
        var_return.set(0)
        button_qr.configure(state=ttk.DISABLED)
        var_label_recieved.set("")
        var_label_return.set("")
        button_return.configure(state=ttk.DISABLED)
        entry_recieved.configure(state=ttk.DISABLED)
        label_return_money.configure(state=ttk.DISABLED)
        var_return.set(0)

        for item in table.get_children():
            table.delete(item)


def new_bill2():
        var_entry_customer_contact.set("")
        var_label_customer_name.set("")
        price_entry_var.set(float(0))
        itemname_entry_var.set("")
        quantity_entry_var.set(int(0))
        var_combobbox.set("")
        total_bill.set(float(0))
        product_list.clear()
        var_label_recieved.set("")
        var_label_return.set("")
        button_return.configure(state=ttk.DISABLED)
        entry_recieved.configure(state=ttk.DISABLED)
        label_return_money.configure(state=ttk.DISABLED)
        var_return.set(0)
        button_qr.configure(state=ttk.DISABLED)
        var_label_recieved.set("")
        var_label_return.set("")
        button_return.configure(state=ttk.DISABLED)
        entry_recieved.configure(state=ttk.DISABLED)
        label_return_money.configure(state=ttk.DISABLED)
        var_return.set(0)
        for item in table.get_children():
            table.delete(item)


def stop_program():
        result=messagebox.askquestion("Exit","Are you Sure ?")
        if result=="yes":
            new_bill2
            messagebox.showinfo("Made by","Shrey \nNaman \nPushkraj \nMayur")
            sys.exit(0)


def save_that_shit():
    global id
    if var_label_customer_name.get()=="" or var_entry_customer_contact.get()=="" or var_combobbox.get()=="":
        messagebox.showerror("ERROR","Customer details not found!!!")
    else:
        result=messagebox.askquestion("WARNING","Are you sure about this ?")
        if result=='yes':
            d=datetime.now()
            st=str(d)
            id=""
            x=0
            for i in st: 
                id=id+i #id is being created
                x+=1
                if x==19:   #to reduce the decimal places of milliseceonds
                    break

              

            cur=sqlite3.connect("database.db")

            #create table customer info
            query_create_customer='''
                            CREATE TABLE IF NOT EXISTS customer
                            (
                            bill_ID TEXT,
                            name TEXT,
                            phone TEXT,
                            pay_mode TEXT
                            )
                        '''
            #create table item purchased
            query_create_item='''
                            CREATE TABLE IF NOT EXISTS item
                            (
                            Tran_ID TEXT,
                            item_name TEXT,
                            price REAL,
                            quantity INT,
                            total REAL
                            )
                        '''
            
            #insert data into customer table
            query_insert_customer='''
                        INSERT INTO customer
                        (
                        bill_ID,
                        name,
                        phone,
                        pay_mode
                        )
                        VALUES
                        (
                        ?,?,?,?
                        )
                        ''' 
            
            #insert data into item table
            query_insert_item='''
                        INSERT INTO item
                        (
                        Tran_ID,
                        item_name,
                        price,
                        quantity,
                        total
                        )
                        VALUES
                        (
                        ?,?,?,?,?
                        )
                        ''' 

            cur.execute(query_create_customer)    
            cur.execute(query_create_item)
            #=================================================
            name=str(var_label_customer_name.get())
            phone=str(var_entry_customer_contact.get())
            pay=str(var_combobbox.get())
            custom=[id,name,phone,pay]
            cur.execute(query_insert_customer,custom)
            cur.commit()
            #==================================================    
            for z in product_list:
                final=[id]+z
                cur.execute(query_insert_item,final)
                cur.commit()
                final.clear()
            
            messagebox.showinfo("Success","Bill was added to the database.")                    
            cur.close()            


def print_bill():
    global id
   
    name=str(var_label_customer_name.get())
    phone=str(var_entry_customer_contact.get())
    pay=str(var_combobbox.get())

    if len(id)==0:
        messagebox.showinfo("Error","Please save the bill before printing")
    else:
        str_start=f'''
\t\t\t                         Z-Mart Shoppy
====================================================================================
Bill ID : {id}                                    
Pay Mode:{pay}   
Name: {name}                                                    
Phone:{phone}



Sr.No  |Item Name\t\t|Price\t\t|Quantity\t\t|Total
______________________________________________________________________________________
'''


        total_gross=str(total_bill.get())
        f=open("bill.txt","w")
        f.write(str_start)

        k=1
        for i in product_list:
            f.write(f"{k}.   ")
            for j in i:
            
                f.write(f"\t{j}\t")
      

            f.write(f"\n_____________________________________________________________________________________\n") 
            k+=1

        f.write(f"\n\nAmount Paid: Rs {total_gross}")  
        f.write("\n====================================================================================\n\t\t\tThank You. Please visit again.")  
        os.startfile("bill.txt",'print')
        f.close()
        id=""
        new_bill2()


def return_func():
   
    var_return.set(float(var_recieved.get())-float(total_bill.get()))


def activate_add_new_item():
    a= int(var_checkbutton_new_item.get())
    if a==0:

        label_new_item_name.configure(text="")
        label_New_item_price.configure(text="")
        

        entry_new_item_name.configure(state=DISABLED)
        entry_New_item_price.configure(state=DISABLED)
        button_new_item_add.configure(state=DISABLED)
        
    if a==1:
        label_new_item_name.configure(text="NEW ITEM NAME")
        label_New_item_price.configure(text="           PRICE       ")
        

        entry_new_item_name.configure(state=NORMAL)
        entry_New_item_price.configure(state=NORMAL)
        button_new_item_add.configure(state=NORMAL)
       

def change_theme():
#light themes: litera,journal,cosmo,flatly,lumen,
# minty,pulse,sandstone,united,yeti,morph, 
# Dark themes: solar,superhero,cyborg,vapor
#gives title to the app

    a= int(var_button.get())
    if a==0:
        style.theme_use("litera")
    if a==1:
        style.theme_use("solar")


def update_time():
    time_string=strftime("%I:%M:%S %p")
    time_label.configure(text=time_string)
    time_label.after(1000,update_time)


def on_key(event):
    global items
    # Get the typed text from the combobox
    typed_text = combo_item.get()

    # Filter the values based on the typed text
    filtered_values = [value for value in items if value.startswith(typed_text)]
    
    for i in items:
        if i ==typed_text:
            price_entry_var.set(items[i])
            


    # Update the combobox values with filtered values
    combo_item['values'] = filtered_values

    # Open the dropdown list
    combo_item.event_generate('<Down>')


def update_price(event):
    selected_item = combo_item.get()

    # If the selected item exists in the dictionary, update the price label
    if selected_item in items:
        price_entry_var.set(items[selected_item])
        quantity_entry.focus_set()
    else:
        price_entry_var.set(0.0)
       

def add_new_items():
    global items
    a=var_new_item_name.get()
    b=float(var_entry_New_item_price.get())

    if a=="" or b==0.0:
        messagebox.showinfo("Fill Correctly","Item name or price cannot be empty")
    else:   
        items.update({a:b})
        combo_item['values'] = sorted(list(items.keys()))
        messagebox.showinfo("Success","New Item Successfully added.")

        

#endregion




#all the frontend is here

#region

window = ttk.Window() 
window.title("Z-Mart")
#window.iconbitmap("bill_icon.ico")
#window.overrideredirect(True)


# #size of window
#window.geometry('1300x650+25+25')
window.geometry('1366x768+-10+-10')
# window.resizable(False,False)
style = ttk.Style()


#================================================================================
frame_heading=ttk.Frame(master=window, relief="raised")#FLAT RAISED SUNKEN GROOVE RIDGE
frame_heading.pack(fill='x',expand=False,anchor="n")




heading=ttk.Label(master=frame_heading,text="Z- Mart Shoppy",font=("vogue",40,"bold"))
heading.pack(padx=250,pady=10)


# #======================================================================================

frame_main=ttk.Frame(master=window,relief="raised")
frame_main.pack(anchor="n",fill='both',expand=True)



frame_1=ttk.Frame(frame_main,relief="raised")
frame_1.pack(side='left',fill='y')

date=datetime.now()
date_label=ttk.Label(master=frame_1,text=f"{date:%A, %B %d, %Y}",font=("comfortaa",12))
date_label.pack(pady=10)


time_label=ttk.Label(master=frame_1,font=("comfortaa",12))
time_label.pack(pady=10)
update_time()

label_1=ttk.Label(frame_1,text="CUSTOMER DETAILS:",font=("comfortaa",16,"bold"))
label_1.pack(padx=20,pady=50)
# # #frame 1 Customer details



label_customer_name=ttk.Label(master=frame_1,text="NAME",font=("comfortaa",15))
label_customer_name.pack(pady=10)
var_label_customer_name=ttk.StringVar()
entry_customer_name=ttk.Entry(master=frame_1,textvariable=var_label_customer_name)
entry_customer_name.pack(pady=1)

label_customer_contact=ttk.Label(master=frame_1,text="PHONE",font=("comfortaa",15))
label_customer_contact.pack(pady=10)

var_entry_customer_contact=ttk.StringVar()
entry_customer_contact=ttk.Entry(master=frame_1,textvariable=var_entry_customer_contact)
entry_customer_contact.pack(pady=1)

label_customer_mode=ttk.Label(master=frame_1,text="PAYMENT MODE",font=("comfortaa",15))
label_customer_mode.pack(pady=15)

var_combobbox=ttk.StringVar()
combo = ttk.Combobox(frame_1, textvariable=var_combobbox,values=["Offline", "Online"])
combo.pack(padx=10, pady=15)
combo.bind("<<ComboboxSelected>>", combo_clicked)

# Button
button_qr = ttk.Button(frame_1, text="Create QR", state=ttk.DISABLED,command=create_qr)
button_qr.pack(padx=10, pady=25)


# #================================================================================
frame_2=ttk.Frame(frame_main)
frame_2.pack(side='left',fill='both',expand=True)
frame_3=ttk.Frame(frame_2,relief="raised")
frame_3.pack(fill='x',expand=False,anchor="n")

# #================================================================================



# #=================================================================
#frame 3
itemname_label=ttk.Label(master=frame_3,text="PRODUCT",font=("comfortaa",15))
itemname_label.pack(side='left',anchor='n',padx=15,pady=12)

# itemname_entry_var=ttk.StringVar() 
# itemname_entry=ttk.Entry(master=frame_3,width=20,font=("comfortaa",13),textvariable=itemname_entry_var)
# itemname_entry.pack(side='left',anchor='nw',pady=12)

itemname_entry_var=ttk.StringVar() 
combo_item = ttk.Combobox(frame_3,textvariable=itemname_entry_var,values = sorted(list(items.keys())),width=25)
combo_item.pack(side='left',anchor='nw',pady=16)

combo_item.bind('<KeyRelease>', on_key)
combo_item.bind("<<ComboboxSelected>>", update_price)



price_label=ttk.Label(master=frame_3,text="PRICE",font=("comfortaa",15))
price_label.pack(side='left',anchor='n',padx=12,pady=12)

price_entry_var=ttk.DoubleVar()
price_entry=ttk.Entry(master=frame_3,font=("comfortaa",13),textvariable=price_entry_var,width=10)
price_entry.pack(side='left',anchor='nw',pady=12)

quantity_label=ttk.Label(master=frame_3,text="QUANTITY",font=("comfortaa",15))
quantity_label.pack(side='left',anchor='n',padx=12,pady=12)


quantity_entry_var=ttk.IntVar()
quantity_entry=ttk.Entry(master=frame_3,font=("comfortaa",13),textvariable=quantity_entry_var,width=5)
quantity_entry.pack(side='left',anchor='nw',pady=12)

Add_button=ttk.Button(master=frame_3,text="ADD ITEM",width=15,command=add_item)#,command=add_item
Add_button.pack(side="left",padx=30)
window.bind('<Return>', on_enter)

delete_button=ttk.Button(master=frame_3,text="DELETE ITEM",width=15,command=delete_item)#,command=delete_item
delete_button.pack(side="left",padx=10)

# #================================================================================

frame_4=ttk.Frame(master=frame_2,relief="raised")
frame_4.pack(fill="both",expand=True)
frame_4_1=ttk.Frame(master=frame_4,width=850,relief="raised")
frame_4_1.pack(side="left",fill="y",expand=False)
frame_4_2=ttk.Frame(master=frame_4,relief="raised")
frame_4_2.pack(side="left",fill="both",expand=True)

#================================================================================
frame_5=ttk.Frame(master=frame_2,relief="raised")
frame_5.pack(fill="both")
frame_5_1=ttk.Frame(master=frame_5,width=850,relief="raised")
frame_5_1.pack(side="left",fill="both",expand=False)
frame_5_2=ttk.Frame(master=frame_5,relief="raised")
frame_5_2.pack(side="left",fill="both",expand=True)
# #================================================================================
# #frame4_1


table= ttk.Treeview(master=frame_4_1,columns= ("Item","Price","Quantity","Total"),show="headings",height=18)

table.column("Item", width=400)
table.column("Price", anchor=ttk.W, width=150)
table.column("Quantity", anchor=ttk.W, width=100)
table.column("Total", anchor=ttk.W, width=150)


#table.heading("Item Code",text="Item Code ")
table.heading("Item",text="ITEM NAME" )
table.heading("Price",text="PRICE")
table.heading("Quantity",text="QUANTITY")
table.heading("Total",text="TOTAL")

table.pack(anchor="n",fill="y",expand=True)


style.configure("Treeview" , background="#f2f2f2", fieldbackground="black", foreground="black")

style.map("Treeview", background=[('selected', '#5ab3e0')])
 
# #===========================================================
# #extra_4
extra_4=ttk.Frame(master=frame_4_2,relief="raised")
extra_4.pack(fill="x",expand=False)

extra_4_1=ttk.Frame(master=frame_4_2)
extra_4_1.pack(padx=10,pady=4)

label_dark=ttk.Label(master=extra_4_1,text="DARK MODE",font=("comfortaa", 10))
label_dark.pack(padx=3,pady=2,side="left")

var_button=ttk.IntVar()
button_dark_mode=ttk.Checkbutton(extra_4_1,variable=var_button,bootstyle="round-toggle",command=change_theme)#,command=stop_program
button_dark_mode.pack(side="left",padx=10)

extra_4_2=ttk.Frame(master=frame_4_2)
extra_4_2.pack(padx=10,pady=4)

label_Add_new_items=ttk.Label(master=extra_4_2,text="ADD NEW ITEMS",font=("comfortaa", 10))
label_Add_new_items.pack(padx=3,pady=2,side="left")

var_checkbutton_new_item=ttk.IntVar()
button_check=ttk.Checkbutton(extra_4_2,variable=var_checkbutton_new_item,command=activate_add_new_item,bootstyle="round-toggle")#,command=stop_program
button_check.pack(side="left",padx=10)

extra_4_3=ttk.Frame(master=frame_4_2)
extra_4_3.pack(padx=10,pady=4)

label_new_item_name=ttk.Label(master=extra_4_3,text="                         ",font=("comfortaa",10))
label_new_item_name.pack(side=LEFT,padx=4,pady=10)
var_new_item_name=ttk.StringVar()
entry_new_item_name=ttk.Entry(master=extra_4_3,textvariable=var_new_item_name,state=DISABLED)
entry_new_item_name.pack(side=LEFT,padx=4,pady=1)

extra_4_4=ttk.Frame(master=frame_4_2)
extra_4_4.pack(padx=10,pady=4)
label_New_item_price=ttk.Label(master=extra_4_4,text="                       ",font=("comfortaa",10))
label_New_item_price.pack(side=LEFT,padx=4,pady=10)

var_entry_New_item_price=ttk.DoubleVar()
entry_New_item_price=ttk.Entry(master=extra_4_4,textvariable=var_entry_New_item_price,state=DISABLED)
entry_New_item_price.pack(side=LEFT,padx=4,pady=1)

button_new_item_add=ttk.Button(master=frame_4_2,text="ADD",command=add_new_items,state=DISABLED)
button_new_item_add.pack(pady=10)


# #===========================================================
# #frame_4_2


label_total=ttk.Label(master=frame_4_2,text="TOTAL:",font=("comfortaa", 20))
total_bill=ttk.DoubleVar()
label_rupee=ttk.Label(master=frame_4_2,text="Rs ",font=("comfortaa", 30),foreground="#ff3333")

label_total_bill=ttk.Label(master=frame_4_2,text="0",textvariable=total_bill,font=("comfortaa", 30),foreground="#ff3333")
label_total.pack(pady=20)
label_rupee.pack(padx=10,pady=10,side="left")
label_total_bill.pack(side="left")

# #============================================================
#frame_5_1
button_1=ttk.Button(frame_5_1,text="SAVE BILL",width=15,command=save_that_shit)#,command=save_that_shit
button_1.pack(side="left",padx=40,pady=60,fill="both",expand=True)
button_2=ttk.Button(frame_5_1,text="PRINT",width=15,command=print_bill)#,command=print_bill
button_2.pack(side="left",padx=45,pady=60,fill="both",expand=True)
button_3=ttk.Button(frame_5_1,text="NEW BILL",width=15,command=new_bill)#,command=new_bill
button_3.pack(side="left",padx=45,pady=60,fill="both",expand=True)
button_4=ttk.Button(frame_5_1,text="EXIT",width=15,command=stop_program)#,command=stop_program
button_4.pack(side="left",padx=45,pady=60,fill="both",expand=True)
# #=============================================================
#frame_5_2
var_label_recieved=ttk.StringVar()
label_recieved=ttk.Label(master=frame_5_2,text="",textvariable=var_label_recieved,font=("comfortaa", 10),state=ttk.DISABLED)
label_recieved.pack(pady=10)


frame_5_3=ttk.Frame(master=frame_5_2)
frame_5_3.pack(padx=10)

var_recieved=ttk.DoubleVar()
entry_recieved=ttk.Entry(master=frame_5_3,font=("comfortaa", 8),textvariable=var_recieved,state=ttk.DISABLED)
entry_recieved.pack(side="left")

button_return=ttk.Button(frame_5_3,text="GO",width=3,command=return_func,state=ttk.DISABLED)#,command=stop_program
button_return.pack(side="left",padx=10)

frame_5_4=ttk.Frame(master=frame_5_2)
frame_5_4.pack(pady=10)

var_label_return=ttk.StringVar()
label_return=ttk.Label(master=frame_5_4,textvariable=var_label_return,font=("comfortaa", 10),state=ttk.DISABLED)
label_return.pack(side="left")

var_return=ttk.DoubleVar()
label_return_money=ttk.Label(master=frame_5_4,textvariable=var_return,font=("comfortaa", 10),state=ttk.DISABLED)
label_return_money.pack(side="left")

# #=============================================================

#run the window
window.mainloop()

#endregion