#python -m PyInstaller main.py --onefile --windowed
# pyinstaller --font-path /usr/share/fonts my_script.py
#  pyinstaller --windowed  --add-data "image1.jpg;." --add-data "image2.jpg;." --add-data "image3.jpg;." --icon=myLogo.ico myPythonFile.py


#importing stuff
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import sys
import os
import qrcode
from PIL import Image,ImageTk 

#backend stuff
#region
#======================================================================================
#all the backend is here
# if not os.path.exists('data'):
#     # Create the folder
#     os.makedirs('data')
# if not os.path.exists('assets'):
#     # Create the folder
#     os.makedirs('data')

product_list=[]
id=""


def add_item():
    product_name = itemname_entry_var.get()
    price = float(price_entry_var.get())
    quantity = int(quantity_entry_var.get())

    if product_name and price and quantity:
        product_list.append([product_name, price, quantity,price*quantity])
        table.insert('', "end", values=(product_name, price, quantity,price*quantity))
        itemname_entry.delete(0,"end")
        
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


def new_bill():
    result=messagebox.askquestion("WARNING","Do you want to add more entries ? ")

    if result=="yes":
        
        var_entry_customer_contact.set("")
        var_label_customer_name.set("")
        price_entry_var.set(float(0))
        itemname_entry_var.set("")
        quantity_entry_var.set(int(0))
        var_combobbox.set("")
        total_bill.set(float(0))
        product_list.clear()

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
        for item in table.get_children():
            table.delete(item)


def stop_program():
        result=messagebox.askquestion("Exit","Are you Sure ?")
        if result=="yes":
            new_bill2
            messagebox.showinfo("Made by","Shrey \nNaman \nPushkraj \nJack\nMayur")
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
\t\t\t                           Z-Mart Shoppy
==========================================================================================
Bill ID : {id}                                    
Pay Mode:{pay}   
Name: {name}                                                    
Phone:{phone}



Sr.No  |Item Name\t\t|Price\t\t|Quantity\t\t|Total
_________________________________________________________________________________________
'''


        total_gross=str(total_bill.get())
        f=open("bill.txt","w")
        f.write(str_start)

        k=1
        for i in product_list:
            f.write(f"{k}.   ")
            for j in i:
            
                f.write(f"\t{j}\t")
      

            f.write(f"\n_________________________________________________________________________________________\n") 
            k+=1

        f.write(f"\n\nAmount Paid: Rs {total_gross}")  
        f.write("\n==========================================================================================\n\t\t\t\tThank You. Please visit again.")  
        os.startfile("bill.txt",'print')
        f.close()
        id=""
        new_bill2()


def combo_clicked(e):
    a=combo.get()
    if a=="Online":
       button_qr.configure(state=ctk.NORMAL,fg_color="#3b8ed0")
    else:
        button_qr.configure(state=ctk.DISABLED)


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
    
           
#endregion





#frontend stuff
#region



ctk.set_appearance_mode("light")
#ctk.set_default_color_theme("dark-blue")

#create display
window = ctk.CTk()

#gives title to the app
window.title("Z-Mart")
#window.iconbitmap("bill_icon.ico")

#size of window
window.geometry('1366x768+0+0')
window.maxsize(1366,768)
window.minsize(1355,700)


heading=ctk.CTkLabel(master=window,text="Z- Mart Shoppy",height=50,font=("Airstrike",50))
heading.pack(fill='x')


#======================================================================================

frame_main=ctk.CTkFrame(window)
frame_main.pack(fill='both',expand=True)

frame_1=ctk.CTkFrame(frame_main,width=200,border_width=2)
frame_1.pack(side='left',fill='y')
label_1=ctk.CTkLabel(frame_1,text="CUSTOMER DETAILS:",width=200,font=("Calibri",25))
label_1.pack(padx=20,pady=70)


#================================================================================
frame_2=ctk.CTkFrame(frame_main,border_width=2)
frame_2.pack(side='left',fill='both',expand=True)
frame_3=ctk.CTkFrame(frame_2,border_width=2)
frame_3.pack(fill='x')

#================================================================================
# #frame 1 Customer details



label_customer_name=ctk.CTkLabel(master=frame_1,text="Name",font=("CAlibri",30))
label_customer_name.pack(pady=10)
var_label_customer_name=ctk.StringVar()
entry_customer_name=ctk.CTkEntry(master=frame_1,textvariable=var_label_customer_name)
entry_customer_name.pack(pady=1)

label_customer_contact=ctk.CTkLabel(master=frame_1,text="Phone",font=("CAlibri",30))
label_customer_contact.pack(pady=10)

var_entry_customer_contact=ctk.StringVar()
entry_customer_contact=ctk.CTkEntry(master=frame_1,textvariable=var_entry_customer_contact)
entry_customer_contact.pack(pady=1)

label_customer_mode=ctk.CTkLabel(master=frame_1,text="Payment Mode",font=("CAlibri",30))
label_customer_mode.pack(pady=10)

var_combobbox=tk.StringVar()
combo = tk.ttk.Combobox(frame_1, textvariable=var_combobbox,values=["Offline", "Online"])
combo.pack(padx=10, pady=15)
combo.bind("<<ComboboxSelected>>", combo_clicked)

# Button
button_qr = ctk.CTkButton(frame_1, text="Create QR", state=tk.DISABLED,fg_color="silver",text_color="white",command=create_qr)
button_qr.pack(padx=10, pady=20)


#=================================================================
#frame 3
itemname_label=ctk.CTkLabel(master=frame_3,text="PRODUCT",font=("Calibri",25))
itemname_label.pack(side='left',anchor='n',padx=15,pady=12)

itemname_entry_var=ctk.StringVar() 
itemname_entry=ctk.CTkEntry(master=frame_3,font=("Calibri",25),width=225,textvariable=itemname_entry_var)
itemname_entry.pack(side='left',anchor='nw',pady=12)

price_label=ctk.CTkLabel(master=frame_3,text="Price",font=("Calibri",25))
price_label.pack(side='left',anchor='n',padx=12,pady=12)

price_entry_var=ctk.DoubleVar()
price_entry=ctk.CTkEntry(master=frame_3,font=("Calibri",25),textvariable=price_entry_var,width=100)
price_entry.pack(side='left',anchor='nw',pady=12)

quantity_label=ctk.CTkLabel(master=frame_3,text="Quantity",font=("Calibri",25))
quantity_label.pack(side='left',anchor='n',padx=12,pady=12)


quantity_entry_var=ctk.IntVar()
quantity_entry=ctk.CTkEntry(master=frame_3,font=("Calibri",25),textvariable=quantity_entry_var,width=70)
quantity_entry.pack(side='left',anchor='nw',pady=12)

Add_button=ctk.CTkButton(master=frame_3,text="ADD ITEM",height=40,command=add_item)
Add_button.pack(side="left",padx=50)

delete_button=ctk.CTkButton(master=frame_3,text="DELETE ITEM",height=40,command=delete_item)
delete_button.pack(side="left")

#================================================================================

frame_4=ctk.CTkFrame(master=frame_2,height=400)
frame_4.pack(fill="both",expand=True)
frame_4_1=ctk.CTkFrame(master=frame_4,height=400,width=850)
frame_4_1.pack(side="left")
frame_4_2=ctk.CTkFrame(master=frame_4,height=400,border_width=2)
frame_4_2.pack(side="left",fill="both",expand=True)

#================================================================================
frame_5=ctk.CTkFrame(master=frame_2)
frame_5.pack(fill="both")
frame_5_1=ctk.CTkFrame(master=frame_5,width=850)
frame_5_1.pack(side="left")
frame_5_2=ctk.CTkFrame(master=frame_5,border_width=2)
frame_5_2.pack(side="left",fill="both",expand=True)
#================================================================================
#frame4_1


table= ttk.Treeview(master=frame_4_1,columns= ("Item","Price","Quantity","Total"),show="headings",height=22)

table.column("Item", width=400)
table.column("Price", anchor=tk.W, width=150)
table.column("Quantity", anchor=tk.W, width=100)
table.column("Total", anchor=tk.W, width=150)


#table.heading("Item Code",text="Item Code ")
table.heading("Item",text="Item Name" )
table.heading("Price",text="Price")
table.heading("Quantity",text="Quantity")
table.heading("Total",text="Total")

table.pack(anchor="n",fill="both",expand=True)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview" , background="white", fieldbackground="white", foreground="black")

style.map("Treeview", background=[('selected', '#5ab3e0')])

#===========================================================
#frame_4_2

label_total=ctk.CTkLabel(master=frame_4_2,text="TOTAL:",font=("Calibri", 40))
total_bill=ctk.DoubleVar()
label_rupee=ctk.CTkLabel(master=frame_4_2,text="Rs ",text_color="red",font=("Calibri", 60))

label_total_bill=ctk.CTkLabel(master=frame_4_2,text="0",textvariable=total_bill,text_color="red",font=("Calibri", 60))
label_total.pack(pady=70)
label_rupee.pack(padx=10,side="left")
label_total_bill.pack(side="left")

#============================================================
#frame_5_1
button_1=ctk.CTkButton(frame_5_1,text="SAVE BILL", height=40,command=save_that_shit)
button_1.pack(side="left",padx=40,fill="both",expand=True)
button_2=ctk.CTkButton(frame_5_1,text="PRINT", height=40,command=print_bill)
button_2.pack(side="left",padx=27,fill="both",expand=True)
button_3=ctk.CTkButton(frame_5_1,text="NEW BILL", height=40,command=new_bill)
button_3.pack(side="left",padx=27,fill="both",expand=True)
button_4=ctk.CTkButton(frame_5_1,text="EXIT", height=40,command=stop_program)
button_4.pack(side="left",padx=27,fill="both",expand=True)
#=============================================================



#run the window
window.mainloop()


#endregion



