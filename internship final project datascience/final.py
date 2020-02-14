import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
import random
import plotly
import plotly.graph_objs as go
import statsmodels.api as sm

from string import ascii_letters
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time 
from datetime import date
from tkinter import*
from tkinter import messagebox
from tkinter import Tk
import tkinter as tk
import pymysql
from PIL import ImageTk, Image
import calendar

def adjustscreen(window):
    x = 700
    y = 700
    dx = window.winfo_screenwidth()
    dy = window.winfo_screenheight()
    w = (dx/2) - (x/2)
    h = (dy/2) - (y/2)
    window.geometry('%dx%d+%d+%d' %(x, y, w, h))
    window.resizable(False, False)
    window.configure(background = 'white')
    
def adjustscreen1(window):
    x = 700
    y = 300
    dx = window.winfo_screenwidth()
    dy = window.winfo_screenheight()
    w = (dx/2) - (x/2)
    h = (dy/2) - (y/2)
    window.geometry('%dx%d+%d+%d' %(x, y, w, h))
    window.resizable(False, False)
    window.configure(background = 'white')

import time
def is_date_valid(year, month, day):
    this_date = '%d/%s/%s' % (month, day, year)
    try:
        time.strptime(this_date, '%m/%d/%Y')
    except ValueError:
        return False
    else:
        return True
    
def common():
    apps=pd.read_excel("appdatabook.xlsx")
    apps_columns=apps.columns.tolist()
    db_connection = pymysql.connect(host="localhost", database="playstore", user="root", password=None)
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT * FROM app_details')
    table_rows = db_cursor.fetchall()
    db_connection.commit() 
    db_connection.close()
    mysql_data1 = pd.DataFrame(list(table_rows), columns = apps_columns)
    apps=pd.concat([apps,mysql_data1],axis=0)
    apps=apps.drop_duplicates(['App'],keep='last')
    apps = apps[apps['Android Ver'] != np.nan]
    apps = apps[apps['Android Ver'] != 'NaN']
    apps = apps[apps['Installs'] != 'Free']
    apps = apps[apps['Installs'] != 'Paid']
    apps['Installs'] = apps['Installs'].apply(lambda x: x.replace(',', '') if ',' in str(x) else x)
    apps['Installs']=apps['Installs'].apply(lambda x: int(str(x).replace('+','')) + 1000 if '+' in str(x) else x)
    apps['Installs'] = apps['Installs'].apply(lambda x: int(x))
    apps['Size'] = apps['Size'].apply(lambda x: str(x).replace('Varies with device', 'NaN') if 'Varies with device' in str(x) else x)
    apps['Size'] = apps['Size'].apply(lambda x: str(x).replace('M', '') if 'M' in str(x) else x)
    apps['Size'] = apps['Size'].apply(lambda x: str(x).replace(',', '') if 'M' in str(x) else x)
    apps['Size'] = apps['Size'].apply(lambda x: float(str(x).replace('k', '')) / 1000 if 'k' in str(x) else x)
    apps['Size'] = apps['Size'].apply(lambda x: float(x))
    apps['Price'] = apps['Price'].apply(lambda x: str(x).replace('$', '') if '$' in str(x) else str(x))
    apps['Price'] = apps['Price'].apply(lambda x: float(x))
    apps['Reviews'] = apps['Reviews'].apply(lambda x: int(x))
    apps['Rating'] = apps['Rating'].apply(lambda x: float(x))
    return apps

def common2():
    apprev=pd.read_excel("appreview.xlsx")
    apprev_columns=apprev.columns.tolist()
    db_connection = pymysql.connect(host="localhost", database="playstore", user="root", password=None)
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT * FROM app_reviews')
    table_rows = db_cursor.fetchall()
    db_connection.commit() 
    db_connection.close()
    mysql_data2 = pd.DataFrame(list(table_rows), columns = apprev_columns)
    apprev=pd.concat([apprev,mysql_data2],axis=0)
    apprev['Sentiment_Polarity'] = apprev['Sentiment_Polarity'].apply(lambda x: float(x))
    apprev['Sentiment_Subjectivity'] = apprev['Sentiment_Subjectivity'].apply(lambda x: float(x))
    return apprev
    
    
def enter_dataset1():
    def enable_size():
        size_entry.configure(state="normal")
    def disable_size():
        size_entry.configure(state="disabled")
    def enable_price():
        price_entry.configure(state="normal")
    def disable_price():
        price_entry.configure(state="disabled")
    def enable_cver():
        cver_entry.configure(state="normal")
    def disable_cver():
        cver_entry.configure(state="disabled")
    def enable_aver():
        aver_entry.configure(state="normal")
    def disable_aver():
        aver_entry.configure(state="disabled")
    apps=common()
    x='disabled'
    global dataset1
    dataset1 = Toplevel(myroot)
    dataset1.title("Data Entry")
    adjustscreen(dataset1)
    global appname, category, rating, reviews, size, size_value, installs, atype, price, content_rating, genres, day, month, year, c_ver, c_verog, a_ver, a_verog
    appname=StringVar()
    category=StringVar()
    rating=StringVar()
    reviews=StringVar()
    size=StringVar()
    size_value=StringVar()
    installs=StringVar()
    atype=StringVar()
    price=StringVar()
    content_rating=StringVar()
    genres=StringVar()
    day=StringVar()
    month=StringVar()
    year=StringVar()
    c_ver=StringVar()
    c_verog=StringVar()
    a_ver=StringVar()
    a_verog=StringVar()
    
    photo = ImageTk.PhotoImage(Image.open("blacktheme.jpg")) # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(dataset1, image=photo, text="") # attaching image to the label
    label.place(x=0, y=0)
    label.image = photo
    Label(dataset1, text="Fill App Data", width='40', height="2", font=("Times New Roman", 24,'bold'), fg='black', bg='goldenrod1',).place(x=0, y=0)
    Label(dataset1, text="App Name:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=10, y=110)
    Entry(dataset1, textvar=appname, width='25').place(x=100, y=110)
    Label(dataset1, text="Category:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=10, y=150)
    list1 = apps['Category'].unique().tolist()
    droplist = OptionMenu(dataset1, category, *list1)
    droplist.config(width=17)
    category.set('--Select Category--')
    droplist.place(x=100, y=150)
    Label(dataset1, text="App Rating:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=10, y=200)
    Entry(dataset1, textvar=rating, width='5').place(x=100, y=200)
    Label(dataset1, text="*Enter a value between 0 and 5", font=("Open Sans", 9, 'bold'), fg='yellow',bg='black', anchor=W).place(x=10, y=220)
    Label(dataset1, text="No. of reviews:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=10, y=250)
    Entry(dataset1, textvar=reviews, width='6').place(x=130, y=250)
    Label(dataset1, text="Size:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=10, y=280)
    Label(dataset1, text="Specify Size:", font=("Open Sans", 10, 'bold'), fg='gray64',bg='black', anchor=W).place(x=10, y=345)
    Label(dataset1, text="MB", font=("Open Sans", 10, 'bold'), fg='gray64',bg='black', anchor=W).place(x=140, y=345)
    size_entry=Entry(dataset1, textvar=size_value, width='4', state=x)
    size_entry.place(x=110, y=345)
    Radiobutton(dataset1, text="Varies with device", variable=size, value="Varies",bg='gainsboro',command=disable_size).place(x=80, y=280)
    Radiobutton(dataset1, text="Specify Size", variable=size, value=" ",bg='gainsboro',command=enable_size).place(x=80, y=310)         
    Label(dataset1, text="Number of Installs:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=10, y=380)
    Entry(dataset1, textvar=installs, width='11').place(x=160, y=380)
    Label(dataset1, text="Type:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=350, y=110)
    Radiobutton(dataset1, text="Free", variable=atype, value="Free", bg='gainsboro',command=disable_price).place(x=400, y=110)
    Radiobutton(dataset1, text="Paid", variable=atype, value="Paid", bg='gainsboro',command=enable_price).place(x=400, y=150)         
    Label(dataset1, text="Enter Price:", font=("Open Sans", 10, 'bold'), fg='gray64',bg='black', anchor=W).place(x=350, y=190)
    Label(dataset1, text="$", font=("Open Sans", 10, 'bold'), fg='gray64',bg='black', anchor=W).place(x=430, y=190)
    price_entry=Entry(dataset1, textvar=price, width='5', state=x)
    price_entry.place(x=450, y=190)
    Label(dataset1, text="Content Rating:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=350, y=230)
    list1 = apps['Content Rating'].unique().tolist()
    droplist = OptionMenu(dataset1, content_rating, *list1)
    droplist.config(width=20)
    content_rating.set('--Select Content Rating--')
    droplist.place(x=490, y=230)
    Label(dataset1, text="Genre:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=350, y=280)
    list1 = apps['Genres'].unique().tolist()
    droplist = OptionMenu(dataset1, genres, *list1)
    droplist.config(width=17)
    genres.set('--Select Genre--')
    droplist.place(x=430, y=280)
    Label(dataset1, text="Enter Date of Last Update:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=350, y=350)
    day_list=list(range(1, 31))
    import calendar
    month_list=calendar.month_name[1:13]
    year_list=list(range(2014,2019))
    droplista = OptionMenu(dataset1, day, *day_list)
    droplista.config(width=3)
    day.set('--Day--')
    droplista.place(x=350, y=380)
    droplistb = OptionMenu(dataset1, month, *month_list)
    droplistb.config(width=9)
    month.set('--Month--')
    droplistb.place(x=410, y=380)
    droplistc = OptionMenu(dataset1, year, *year_list)
    droplistc.config(width=4)
    year.set('--Year--')
    droplistc.place(x=510, y=380)
    Label(dataset1, text="Current Version:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=10, y=420)
    Radiobutton(dataset1, text="Varies with device", variable=c_ver, value="Varies with device", bg='gainsboro',command=disable_cver).place(x=10, y=450)
    Radiobutton(dataset1, text="Specify current app version:", variable=c_ver, value=0, bg='gainsboro',command=enable_cver).place(x=10, y=480)         
    cver_entry=Entry(dataset1, textvar=c_verog, width='16', state=x)
    cver_entry.place(x=200, y=485)
    Label(dataset1, text="*eg:-6.5.1", font=("Open Sans", 9, 'bold'), fg='yellow',bg='black', anchor=W).place(x=10, y=505)
    Label(dataset1, text="Android Version:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=350, y=420)
    Radiobutton(dataset1, text="Varies with device", variable=a_ver, value="Varies with device", bg='gainsboro',command=disable_aver).place(x=350, y=450)
    Radiobutton(dataset1, text="Specify Android version:", variable=a_ver, value=0, bg='gainsboro',command=enable_aver).place(x=350, y=480)         
    Label(dataset1, text="and up", font=("Open Sans", 10, 'bold'), fg='white',bg='black', anchor=W).place(x=615, y=485)
    aver_entry=Entry(dataset1, textvar=a_verog, width='10', state=x)
    aver_entry.place(x=540, y=485)
    Label(dataset1, text="*eg:-2.3.3 and up", font=("Open Sans", 9, 'bold'), fg='yellow',bg='black', anchor=W).place(x=350, y=505)
    Button(dataset1, text='Submit', width=20, font=("Open Sans", 18, 'bold'), bg='goldenrod1', fg='black',command=input_dataset1).place(x=200, y=580)

def enter_dataset2():
    global dataset2, appn, t
    appn=StringVar()
    dataset2 = Toplevel(myroot)
    dataset2.title("Data Entry")
    adjustscreen1(dataset2)
    photo = ImageTk.PhotoImage(Image.open("blacktheme.jpg")) # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(dataset2, image=photo, text="") # attaching image to the label
    label.place(x=0, y=0)
    label.image = photo
    Label(dataset2, text="Fill App Data", width='50', height="2", font=("Calibri", 22,'bold'), fg='black', bg='goldenrod1').place(x=0, y=0)
    Label(dataset2, text="App Name:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=10, y=110)
    Entry(dataset2, textvar=appn, width='45', font=("Calibri", 15)).place(x=100, y=110)
    Label(dataset2, text="Write Review:", font=("Open Sans", 11, 'bold'), fg='white',bg='black', anchor=W).place(x=10, y=160)
    t=Text(dataset2, height=3, width=60, font=("Calibri", 11))
    t.place(x=10, y=190)
    
    Button(dataset2, text='Submit', width=10, font=("Open Sans", 18, 'bold'), bg='goldenrod1', fg='black',command=input_dataset2).place(x=500, y=190)

def input_dataset1():
    if appname.get() and rating.get() and reviews.get() and size.get() and installs.get() and atype.get() and c_ver.get() and a_ver.get():
        if category.get() == "--Select Category--":
            Label(dataset1, text="*Please select Category", fg="DarkOrange2", font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
            return
        elif content_rating.get() == "--Select Content Rating--":
            Label(dataset1, text="*Please select Content Rating", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
            return
        elif genres.get() == "--Select Genre--":
            Label(dataset1, text="*Please select Genre", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
            return
        elif day.get() == "--Day--" or month.get() == "--Month--" or year.get() == "--Year--":
            Label(dataset1, text="*Please fill Date field", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
            return
        else:
            if not(rating.get().replace('.','',1).isdigit()):
                Label(dataset1, text="*App Rating entered is invalid", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                return
            else:
                if not(0<=float(rating.get())<=5):
                    Label(dataset1, text="*App Rating entered is out of bounds(should be between 0 and 5)", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                    return
                else:
                    if not(reviews.get().isdigit()):
                        Label(dataset1, text="*Number of reviews entered should be numeric", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                        return
                    else:
                        if size.get()=="Varies":
                            size_var="Varies with device"
                        else:
                            if not(size_value.get()):
                                Label(dataset1, text="*Size not entered", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                                return
                            if not(size_value.get().replace('.','',1).isdigit()):
                                Label(dataset1, text="*Size entered should be numeric", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                                return
                            else:
                                size_var=size_value.get()+"M"
                        if not(installs.get().isdigit()):
                            Label(dataset1, text="*Number of installs entered should be numeric", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                            return
                        else:
                            installs_count=installs.get()+"+"
                            if c_ver.get()=="Varies with device":
                                cur_ver=c_ver.get()
                            elif c_ver.get()=="0":
                                if not c_verog.get():
                                    Label(dataset1, text="*Current version not entered", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                                    return
                                elif not(c_verog.get().replace('.','').isdigit()):
                                    Label(dataset1, text="*Current version entered contains invalid characters", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                                    return
                                else:
                                    cur_ver=c_verog.get()
                            if a_ver.get()=="Varies with device":
                                add_ver=a_ver.get()
                            elif a_ver.get()=="0":
                                if not a_verog.get():
                                    Label(dataset1, text="*Android version not entered", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                                    return
                                elif not(a_verog.get().replace('.','').isdigit()):
                                    Label(dataset1, text="*Android version entered contains invalid characters", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                                    return
                                else:
                                    add_ver=a_verog.get()+" and up"
                            if atype.get()=="Free":
                                price_value="0"
                            else:
                                if not price.get():
                                    Label(dataset1, text="*Price not entered", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                                    return
                                elif not(price.get().replace('.','',1).isdigit()):
                                    Label(dataset1, text="*Price entered is invalid", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                                    return                           
                                else:
                                    price_value="$"+price.get()
                            import calendar
                            m=list(calendar.month_name).index(month.get())
                            if not is_date_valid(year.get(), m, day.get()):
                                Label(dataset1, text="*entered Date is invalid", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                                return
                            else:
                                date_var=month.get()+" "+day.get()+", "+year.get()
                                connection = pymysql.connect(host="localhost", user="root", passwd=None, database="playstore")
                                cursor = connection.cursor()
                                insert_query = "INSERT INTO app_details (Name,Category,Rating,Reviews,Size,Installs,Type,Price,ContentRating,Genres,LastUpdated,CurrentVer,AndroidVer) VALUES('"+ appname.get() + "', '"+ category.get() + "', '"+ rating.get() +"', '"+ reviews.get() + "', '"+ size_var + "', '"+ installs_count + "', '"+ atype.get() + "', '"+ price_value + "', '"+ content_rating.get() + "', '"+ genres.get() + "', '"+ date_var + "', '"+ cur_ver + "', '"+ add_ver + "' );" 
                                cursor.execute(insert_query) 
                                connection.commit() 
                                connection.close()
                                Label(dataset1, text="Entry Success", fg="lime green", font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
                                ok=Tk()
                                ok.title(" Confirm ")
                                ok.geometry("200x70+600+400")
                                Label(ok, text="", bg='black', width='120', height='60').place(x=0, y=0)
                                Label(ok, text="Data Entered", fg="white", font=("calibri", 17, 'bold'), width='60', anchor=CENTER, bg='black').pack()
                                Button(ok,text="OK",bg="goldenrod1",width=6,height=1,font=(" Times",11,'bold'),fg='black',command=lambda:[ok.destroy(),dataset1.destroy()]).pack()
                                ok.mainloop()
    else:
        Label(dataset1, text="Please fill all the details", fg="DarkOrange2",font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=650)
        return
                                
def input_dataset2():
        global write_rev
        write_rev=t.get('1.0','end-1c')
        if write_rev=="":
            Label(dataset2, text="*Empty review field", fg="DarkOrange2", font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=280)                          
            return
        else:
            if not appn.get():
                Label(dataset2, text="*Empty name field", fg="DarkOrange2", font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=280)                          
                return
            else:
                from textblob import TextBlob
                tr = TextBlob(write_rev)
                try:
                    tr=tr.translate(to='en')
                except Exception as e:
                    print(e.__doc__)
                sen_pol=tr.polarity
                sen_sub=tr.subjectivity
                trev=str(tr)
                if sen_pol>0:
                    sentiment="Positive"
                elif sen_pol<0:
                    sentiment="Negative"
                else:
                    sentiment="Neutral"
                connection=pymysql.connect(host="localhost",user="root",passwd=None,database="playstore")
                cursor=connection.cursor()
                insert_query= "INSERT INTO app_reviews (App,Translated_Review,Sentiment,Sentiment_Polarity,Sentiment_Subjectivity) VALUES('"+ appn.get() + "', '"+ trev + "', '"+ sentiment + "', '"+ str(sen_pol) + "', '"+ str(sen_sub) + "' );"
                cursor.execute(insert_query)
                connection.commit()
                connection.close()
                Label(dataset2, text="Entry Success", fg="lime green", font=("calibri", 11), width='60', anchor=W, bg='black').place(x=0, y=280)
                ok=Tk()
                ok.title(" Confirm ")
                ok.geometry("200x70+600+400")
                Label(ok, text="", bg='black', width='120', height='60').place(x=0, y=0)
                Label(ok, text="Data Entered", fg="white", font=("calibri", 17, 'bold'), width='60', anchor=CENTER, bg='black').pack()
                Button(ok,text="OK",bg="goldenrod1",width=6,height=1,font=(" Times",11,'bold'),fg='black',command=lambda:[ok.destroy(),dataset2.destroy()]).pack()
                ok.mainloop()
                
                            
def dataentry():
    myroot=Tk()
    Label(myroot, text="", bg='black', width='150', height='100').place(x=0, y=0)
    myroot.title("DATA ENTRY")
    myroot.geometry("600x400+200+200")
    Label(myroot, text="Enter data in Playstore App database", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=30, y=100)
    Button(myroot,text="ENTER",bg="goldenrod1",width=8,height=1,font=(" Times",13,'bold'),fg='black',command=enter_dataset1).place(x=470,y=100)
    Label(myroot, text="Enter data in App Reviews/Sentiments database", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=30, y=200)
    Button(myroot,text="ENTER",bg="goldenrod1",width=8,height=1,font=(" Times",13,'bold'),fg='black',command=enter_dataset2).place(x=470,y=200)
    Button(myroot,text="EXIT",bg="goldenrod1",width=8,height=1,font=(" Times",13,'bold'),fg='black',command=myroot.destroy).place(x=450,y=320)
    myroot.mainloop()

def forecast():
    apps=common()
    def conclusion():
        root = tk.Tk()
        T = tk.Text(root, height=30, width=100)
        T.pack()
        T.insert(tk.END,"According to the forecasting by SARIMAX Model,\n apps of SPORTS Category is most likely to be downloaded in the upcoming years")
        tk.mainloop()
    def prd():
        data=pd.concat([apps['Last Updated'],apps['Category'],apps['Installs']],axis=1)
        data['Last Updated'] =pd.to_datetime(data['Last Updated'])
        data['Year'] = pd.DatetimeIndex(data['Last Updated']).year
        data=data[data.Year > 2015]
        del data['Year']
        data.rename(index=str, columns={"Last Updated": "Date"}, inplace=True)
        aggregation_functions = {'Installs': 'sum'}
        data= data.groupby(['Category','Date']).aggregate(aggregation_functions).reset_index()
        y=data[data.Category==var.get()]
        del y['Category']
        groupby_day = y.groupby(pd.Grouper(key="Date", freq='D'))
        results = groupby_day.sum()
        idx = pd.date_range("2016-01-01 00:00:00", max(y.Date))
        y=results.reindex(idx, fill_value=0)
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=(1, 1, 1),
                                        seasonal_order=(1, 1, 1, 12),
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        
        results = mod.fit()
        pred_uc = results.get_forecast(steps=2000)
        pred_ci = pred_uc.conf_int()
        root=tk.Tk()
        figure3 = plt.Figure(figsize=(20,15), dpi=100)
        ax=figure3.add_subplot(111)
        y.plot(ax=ax, label='Observed')
        pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
        ax.fill_between(pred_ci.index,
                        pred_ci.iloc[:, 0],
                        pred_ci.iloc[:, 1], color='k', alpha=.25)
        scatter3 = FigureCanvasTkAgg(figure3, root) 
        scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        ax.legend()
        ax.set_xlabel('Date')
        ax.set_ylabel('Installs:'+var.get())
        root.mainloop()
    root = Tk()
    root.geometry("%dx%d+%d+%d" % (350, 360, 150, 150))
    root.title("View Forecast")
    tk.Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
    category=['SPORTS','ENTERTAINMENT','SOCIAL','NEWS_AND_MAGAZINES','EVENTS','TRAVEL_AND_LOCAL','GAME']
    var = tk.StringVar(root)
    var.set(category[0])
    option = tk.OptionMenu(root, var, *category)
    option.pack(side='left', padx=20, pady=20)
    button = tk.Button(root, text="FORECAST",font=("Calibri",12,'bold'), bg="goldenrod1", fg="black", command=prd)
    button.pack(side='left', padx=20, pady=20)
    tk.Button(root,text="Conclusion",bg="goldenrod1",width=10,height=1,font=(" Times",12,'bold'),fg='black',command=conclusion).place(x=100,y=300)
    root.mainloop()

def que15():
    data=common2()
    res = data.groupby(['App','Sentiment']).first()
    print(res)
    category=data['App'].unique()
    variable=category[0]
    p=data.groupby('App')
    gk=p.get_group(variable)
    print(gk)
    gg=gk.groupby('App')['Sentiment'].value_counts()
    print(gg)
    print(gg.tolist())
    a="The app has a very large number of positive reviews as compared to the number of negative reviews. It is advisable to launch this type of app as it has potential. This app has already rocked more than 500000 installs and could be shrinked to a very portable size of around 4M" 
    root = tk.Tk()
    T = tk.Text(root, height=30, width=100)
    T.pack()
    T.insert(tk.END, gg)
    T.insert(tk.END, "\n")
    T.insert(tk.END,a)
    tk.mainloop()

def que14():
    apprev=common2()
    def select():
            sf = " %s" % var.get()
            root.title(sf)
            def display_review():
                print(v.get())
                papp=apprev[apprev['App']==var.get()]
                papp=papp[papp['Sentiment']==v.get()]
                trlist=papp['Translated_Review'].tolist()
                print("\n".join(trlist))
                root1=Tk()
                T = tk.Text(root1, height=800, width=800)
                T.pack()
                T.insert(tk.END,"\n".join(trlist))
                root1.mainloop()
            Radiobutton(root, text="Positive", variable=v, value="Positive", bg='black', fg="goldenrod1",font=("Calibri",12,'bold'), command=display_review).place(x=20, y=280)
            Radiobutton(root, text="Negative", variable=v, value="Negative", bg='black', fg="goldenrod1",font=("Calibri",12,'bold'), command=display_review).place(x=120, y=280)         
            Radiobutton(root, text="Neutral", variable=v, value="Neutral", bg='black', fg="goldenrod1",font=("Calibri",12,'bold'), command=display_review).place(x=220, y=280)           
    root = Tk()
    root.geometry("%dx%d+%d+%d" % (350, 360, 150, 150))
    root.title("View Translated Reviews")
    Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
    category=apprev['App'].unique()
    var = tk.StringVar(root)
    v=tk.StringVar(root)
    var.set(category[-1])
    option = tk.OptionMenu(root, var, *category)
    option.pack(side='left', padx=20, pady=20)
    button = tk.Button(root, text="SELECT  APP",font=("Calibri",12,'bold'), bg="goldenrod1", fg="black", command=select)
    button.place(x=20,y=200)
    root.mainloop()
        
def que13():
    data=common2()
    pogo = data[['Sentiment_Polarity','Sentiment_Subjectivity']]
    correlation = pogo.corr(method='pearson')
    root= tk.Tk()
    figure3 = plt.Figure(figsize=(10,10), dpi=100)
    ax3 = figure3.add_subplot(111)
    ax3.scatter(data['Sentiment_Polarity'],data['Sentiment_Subjectivity'], color = 'blue')
    scatter3 = FigureCanvasTkAgg(figure3, root) 
    scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    ax3.legend() 
    ax3.set_xlabel('Sentiment-polarity')
    ax3.set_ylabel('sentiment-subjectivity')
    ax3.set_title('Sentiment-polarity Vs.sentiment-subjectivity')
    w2 = tk.Label(root, justify=tk.LEFT,padx = 50, text=correlation).pack(side="left")
    root1=Tk()
    T = tk.Text(root1, height=100, width=150, font=("Helvetica", 25))
    T.pack()
    T.insert(tk.END,"The correlation between sentiment polarity and subjectivity as shown by the correlation matrix is 0.26.\n This is a very small positive value. So we can say that there is a very slight relation between the two features. Therefore, Sentiment Polarity and subjectivity affect each other positively but the effect is very low.")
    root1.mainloop()
    root.mainloop()
               
def extra1():
    apps=common()
    apps['Price In Dollars'] = apps['Price']
    apps['Price In Dollars'] = apps['Price In Dollars'].astype(np.float)
    apps['Ratings'] = ''
    apps.loc[(apps['Rating']>=0.0) & (apps['Rating']<=1.0), 'Ratings'] = '0.0 - 1.0'
    apps.loc[(apps['Rating']>=1.0) & (apps['Rating']<=2.0), 'Ratings'] = '1.0 - 2.0'
    apps.loc[(apps['Rating']>=2.0) & (apps['Rating']<=3.0), 'Ratings'] = '2.0 - 3.0'
    apps.loc[(apps['Rating']>=3.0) & (apps['Rating']<=4.0), 'Ratings'] = '3.0 - 4.0'
    apps.loc[(apps['Rating']>=4.0) & (apps['Rating']<=5.0), 'Ratings'] = '4.0 - 5.0'
    f=plt.figure(figsize=(25, 8))
    sns.barplot(x='Ratings', y='Price In Dollars', data=apps, ci=None, order=['0.0 - 1.0','1.0 - 2.0','2.0 - 3.0','3.0 - 4.0','4.0 - 5.0'])
    root = Tk()
    root.wm_title("Embedding in Tk")
    root.geometry("%dx%d+%d+%d" % (900, 400, 300, 300))
    canvas = FigureCanvasTkAgg(f, root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side="top",fill='both',expand=True)
    root.mainloop()

def extra2():
    apps=common()
    f=plt.figure(figsize=(22,8))
    plt.title('Number of Apps on the basis of Android version required to run them')
    sns.countplot(x='Android Ver',data = apps.sort_values(by = 'Android Ver'),palette='hls')
    plt.xticks(rotation = 90)
    root = Tk()
    root.wm_title("Embedding in Tk")
    root.geometry("%dx%d+%d+%d" % (900, 400, 300, 300))
    canvas = FigureCanvasTkAgg(f, root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side="top",fill='both',expand=True)
    root.mainloop()

                 
def que17():
    root=Tk()
    root.title(" Analysis ")
    root.geometry("500x200+200+200")
    
    Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
    
    Label(root, text="View Correlation Matrix", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=50)
    Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=correlation).place(x=390,y=50)
    

    Label(root, text="Size vs Downloads", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=100)
    Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que17a).place(x=390,y=100)         
    Label(root, text="Conclusion", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=150)
    Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que17b).place(x=390,y=150)         
    
def que17a():
    apps=common()
    apps=apps[apps['Size'].notnull()]
    trace = [go.Scatter(x=apps["Size"], y=apps["Installs"], mode="markers")]
    layout = {"title": "Size vs Downloads",
              "xaxis": {"title": "Size in MB"},
              "yaxis": {"title": "Downloads"},
              "plot_bgcolor": "rgb(0,0,0)"} 
    plotly.offline.plot({'data': trace, 'layout': layout})
    size_list=list(apps.Size.unique())
    size_list=sorted(size_list)
    downloads=[]
    for size in size_list:
        x = apps[apps.Size == size]
        count = x.Installs.sum()
        downloads.append(count)
    
    trace0 = go.Scatter(
        x = size_list,
        y = downloads,
        mode = 'lines',
        name = 'lines'
    )
    
    data = [trace0]
    layout = dict(title = 'Size vs Downloads Trend',
                  xaxis = dict(title = 'Size(MegaBytes)'),
                  yaxis = dict(title = 'Downloads'),
                  )
    
    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, filename='svdtrend.html')

def que17b():
    root=Tk()
    T = tk.Text(root, height=15, width=60)
    T.pack()
    T.insert(tk.END,"The size of the app affects the number of installs in a positive trend.\nThe correlation b/w Size and Installs is positive.\nHowever the size cannot determine the number of installs an app can get properly as the correlation is too small")
    T.insert(tk.END,"Most of the apps with very high downloads have an optimum size between 10 and 40MB")
    root.mainloop()
    
                   
def que12():
    root=Tk()
    root.title(" Analysis ")
    root.geometry("650x200+200+200")
    
    Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
    
    Label(root, text="App Category with most Positive and Negative Sentiments", justify=LEFT, fg="white", font=("calibri",13,'bold'), width='60', anchor=W, bg='black').place(x=10, y=50)
    Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que12a).place(x=540,y=50)
    

    Label(root, text="App Category with same ratio for Positive and Negative Sentiments", justify=LEFT, fg="white", font=("calibri",13,'bold'), width='60', anchor=W, bg='black').place(x=10, y=100)
    Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que12b).place(x=540,y=100)         
  
               
    
def que12a():
    apprev=common2()
    apprev=apprev.dropna()
    app_list=apprev['App'].unique().tolist()
    pos=[]
    neg=[]
    for app in app_list:
        x = apprev[apprev.App == app]
        pos.append(x.Sentiment.str.count("Positive").sum())
        neg.append(x.Sentiment.str.count("Negative").sum())
    d={'App':app_list,'Positive':pos,'Negative':neg}
    app=pd.DataFrame(d)
    app['Ratio'] = app['Positive'] / app['Negative']
    app=app.dropna()
    array=np.asarray(app['Ratio'])
    idx = (np.abs(array - 1)).argmin()
    maxpos = pos.index(max(pos))
    maxpos1 = neg.index(max(neg))
    app_plot=[app_list[maxpos],app_list[maxpos1]]
    positive=[pos[maxpos],pos[maxpos1]]
    negative=[neg[maxpos],neg[maxpos1]]
    trace1 = go.Bar(
        x=app_plot,
        y=positive,
        name='Positive'
    )
    trace2 = go.Bar(
        x=app_plot,
        y=negative,
        name='Negative'
    )
    
    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group'
    )
    
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='grouped-bar.html')
    
def que12b():
    apprev=common2()
    apprev=apprev.dropna()
    app_list=apprev['App'].unique().tolist()
    pos=[]
    neg=[]
    for app in app_list:
        x = apprev[apprev.App == app]
        pos.append(x.Sentiment.str.count("Positive").sum())
        neg.append(x.Sentiment.str.count("Negative").sum())
    d={'App':app_list,'Positive':pos,'Negative':neg}
    app=pd.DataFrame(d)
    app['Ratio'] = app['Positive'] / app['Negative']
    app=app.dropna()
    array=np.asarray(app['Ratio'])
    idx = (np.abs(array - 1)).argmin()
    maxpos = pos.index(max(pos))
    maxpos1 = neg.index(max(neg))
    app_plot=[app_list[maxpos],app_list[maxpos1]]
    root=Tk()
    T = tk.Text(root, height=15, width=60)
    T.pack()
    T.insert(tk.END,app_plot[0])
    T.insert(tk.END," has generated the most positive sentiments")
    T.insert(tk.END,"\n")
    T.insert(tk.END,app_plot[1])
    T.insert(tk.END," has generated the most negative sentiments")
    T.insert(tk.END,"\n")
    T.insert(tk.END,app['App'].iloc[idx])
    T.insert(tk.END," has generated approximately the same ratio for positive and negative sentiments")
    root.mainloop()
    
    
    
def que11():
    apps=common()
    data=pd.concat([apps['Last Updated'],apps['Category'],apps['Installs']],axis=1)
    data['Last Updated'] =pd.to_datetime(data['Last Updated'])
    def get_quarter(d):
        return "%d_Quarter%d" % (d.year, math.ceil(d.month/3))
    quarter=[]
    for i in range(len(data)):
        quarter.append(get_quarter(data['Last Updated'].iloc[i]))
    data.drop('Last Updated', axis=1, inplace=True)
    data['Quarter']=quarter
    aggregation_functions = {'Installs': 'sum'}
    data= data.groupby(['Category','Quarter']).aggregate(aggregation_functions).reset_index()
    data2=data
    data=data.pivot(index='Quarter', columns='Category', values='Installs')
    data=data.fillna(0)
    data = [
        go.Scatter(
            x=data.index,
            y=data[name].values,
            mode='lines',
            name=name,
            line=dict(width=4)
        ) for name in data.columns
    ]
    layout = go.Layout(
        title='Downloads Trend per Category',
        xaxis=dict(title='Year and Quarter', ticklen=5, zeroline=False, gridwidth=2),
        yaxis=dict(title='Number of downloads', ticklen=5, gridwidth=2),
        showlegend=True
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='Quarter.html')
    category_list=list(data2.Category.unique())
    root=Tk()
    T = tk.Text(root, height=15, width=60)
    T.pack()
    for category in category_list:
        x=data2[data2.Category == category]
        pos=list(x.Installs)
        idx = pos.index(max(pos))
        T.insert(tk.END,category)
        T.insert(tk.END," : ")
        T.insert(tk.END,x['Quarter'].iloc[idx])
        T.insert(tk.END,"\n")
    root.mainloop()


def que10():
    root=Tk()
    root.title(" Analysis ")
    root.geometry("500x200+200+200")
    
    Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
    
    Label(root, text="Monthwise Classification of downloads", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=50)
    Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que10a).place(x=390,y=50)
    

    Label(root, text="Ratio of downloads for the App that\nqualifies as Teen versus Mature 17+", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=100)
    Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que10b).place(x=390,y=100)         
  
               
def que10a():
    apps=common()
    data=pd.concat([apps['Last Updated'],apps['Category'],apps['Installs']],axis=1)
    data['Last Updated'] =pd.to_datetime(data['Last Updated'])
    
    month=[]
    for i in range(len(data)):
        month.append((data['Last Updated'].iloc[i]).month)
    data.drop('Last Updated', axis=1, inplace=True)
    data['Month']=month
    aggregation_functions = {'Installs': 'sum'}
    data= data.groupby(['Category','Month']).aggregate(aggregation_functions).reset_index()
    data2=data
    data['Month'].replace(to_replace =[1,2,3,4,5,6,7,8,9,10,11,12],  
                                value =["01_January","02_February","03_March","04_April","05_May","06_June","07_July","08_August","09_September","10_October","11_November","12_December"],inplace=True)
    data=data.pivot(index='Month', columns='Category', values='Installs')
    data=data.fillna(0)
    data = [
        go.Scatter(
            x=data.index,
            y=data[name].values,
            mode='lines',
            name=name,
            line=dict(width=4)
        ) for name in data.columns
    ]
    layout = go.Layout(
        title='Downloads Trend per Category',
        xaxis=dict(title='Month', ticklen=5, zeroline=False, gridwidth=2),
        yaxis=dict(title='Number of downloads', ticklen=5, gridwidth=2),
        showlegend=True
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='Month.html')
    data2['Month'].replace(to_replace =["01_January","02_February","03_March","04_April","05_May","06_June","07_July","08_August","09_September","10_October","11_November","12_December"],  
                                value =["January","February","March","April","May","June","July","August","September","October","November","December"],inplace=True)
    category_list=list(data2.Category.unique())
    root=Tk()
    T = tk.Text(root, height=15, width=60)
    T.pack()
    
    for category in category_list:
        x=data2[data2.Category == category]
        pos=list(x.Installs)
        idx = pos.index(max(pos))
        T.insert(tk.END,category)
        T.insert(tk.END," : ")
        T.insert(tk.END,x['Month'].iloc[idx])
        T.insert(tk.END,"\n")
    root.mainloop()
        
def que10b():
    apps=common()
    x=apps[apps['Content Rating']=='Teen']
    d1=x.Installs.sum()
    y=apps[apps['Content Rating']=='Mature 17+']
    d2=y.Installs.sum()
    ratio=d1/d2
    
    trace0 = go.Bar(
        x=['Teen','Mature'],
        y=[d1,d2],
        marker=dict(
            color=['rgba(215,160,204,1)', 'rgba(222,45,38,0.8)']),
    )
    data = [trace0]
    layout = go.Layout(
        title="Downloads in Teen and Mature 17+",
    )
    
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='teenmature.html') 
    root=Tk()
    T = tk.Text(root, height=15, width=60)
    T.pack()
    T.insert(tk.END,"The ratio of downloads for the app that qualifies as teen versus mature17+ is ")
    T.insert(tk.END,ratio)
    root.mainloop()

def que9():
    root=Tk()
    root.title(" Analysis ")
    root.geometry("600x300+200+200")
    
    Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
    
    Label(root, text="Ratings obtained by Apps with downloads over 100k", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=50)
    Button(root,text="VIEW PLOT",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que9a).place(x=490,y=50)
    

    Label(root, text="Conclusion", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=100)
    Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que9a1).place(x=490,y=100) 

    
    Label(root, text="Ratings obtained by apps per download range", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=150)
    Button(root,text="VIEW PLOT",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que9b).place(x=490,y=150)
    

    Label(root, text="Conclusion", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=200)
    Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que9b1).place(x=490,y=200)        

             
def que9a():
    apps=common()
    apps=apps.filter(['Installs','Rating'])
    apps1=apps[apps.Installs>100000]
    data = [
        go.Box(
            y=apps1['Rating'],
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8
        )
    ]
    layout = go.Layout(
        title='Ratings obtained by apps with downloads over 100K',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )
    
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename="boxplot1.html")

def que9a1():
    root=Tk()
    T = tk.Text(root, height=15, width=60)
    T.pack()
    T.insert(tk.END,"All apps with downloads over 100K have managed to get an average rating of 4.1 and above.")
    root.mainloop()

    
def que9b():
    apps=common()
    apps=apps.filter(['Installs','Rating'])
    apps=apps.dropna()
    apps['Installs']=pd.cut(apps['Installs'], bins=[0, 10000, 50000, 100000, 500000, 5000000, 999999999999], include_lowest=True, labels=['Less than 10K','Between 10K and 50K','Between 50K and 100K','Between 150K and 500K','Between 500K and 5000K','More than 5000K'])
    a=apps.loc[apps['Installs'] == 'Between 10K and 50K']
    range_list = list(apps.Installs.unique())
    ratings = []
    for range in range_list:
        x = apps[apps.Installs == range]
        ratings.append(x.Rating.tolist())
    colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)']
    
    traces = []
    
    for xd, yd, cls in zip(range_list, ratings, colors):
            traces.append(go.Box(
                y=yd,
                name=xd,
                boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=cls,
                marker=dict(
                    size=2,
                ),
                line=dict(width=1),
            ))
    
    layout = go.Layout(
        title='Ratings obtained apps per Download Range',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )
    
    fig = go.Figure(data=traces, layout=layout)
    plotly.offline.plot(fig, filename="boxplot.html")
    
def que9b1():
    root=Tk()
    T = tk.Text(root, height=100, width=150, font=("Helvetica", 32))
    T.pack()
    T.insert(tk.END,"We can see that the median rating will be above 4 no matter how many times an app was installed. Therfore, there is no relation between the number of installs and the rating of an app.")
    root.mainloop()
    
    
    
    
    
def que7():
    
    root=Tk()
    root.title(" Analysis ")
    root.geometry("500x200+200+200")
    
    Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
    
    Label(root, text="Download trend ", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=50)
    Button(root,text="VIEW PLOT",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que7a).place(x=390,y=50)
    

    Label(root, text="Percentage increase or decrease in downloads", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=100)
    Button(root,text="VIEW PLOT",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que7b).place(x=390,y=100)         
  
  


def que7a():
    apps=common()
    apps=apps[apps['Android Ver'] != "Varies with device"]
    data=pd.concat([apps['Last Updated'],apps['Installs']],axis=1)
    data.rename(index=str, columns={"Last Updated": "Date"}, inplace=True)
    data['Date'] = pd.DatetimeIndex(data['Date'])
    aggregation_functions = {'Installs': 'sum'}
    data= data.groupby(['Date']).aggregate(aggregation_functions).reset_index()
    trace0 = go.Scatter(
        x=data.Date,
        y=data.Installs,
        name = "Downloads",
        line = dict(color = 'blue'),
        opacity = 0.8)
    data2 = [trace0]
    layout = dict(title='Downloads with Rangeslider',xaxis=dict(rangeselector=dict(buttons=list([dict(count=1,label='1m',step='month',stepmode='backward'),dict(count=6,label='6m',step='month',stepmode='backward'),dict(step='all')])),rangeslider=dict(visible = True),type='date'))
    fig = dict(data=data2, layout=layout)
    plotly.offline.plot(fig, filename = 'time-series-simple.html')
    
def que7b():
    apps=common()
    apps=apps[apps['Android Ver'] != "Varies with device"]
    data=pd.concat([apps['Last Updated'],apps['Installs']],axis=1)
    data.rename(index=str, columns={"Last Updated": "Date"}, inplace=True)
    data['Date'] = pd.DatetimeIndex(data['Date'])
    aggregation_functions = {'Installs': 'sum'}
    data= data.groupby(['Date']).aggregate(aggregation_functions).reset_index()
    data['Installs']=data['Installs'].pct_change()
    data['Installs']=data['Installs']*100
    change=data.Installs.sum()
    trace1 = go.Scatter(x=data.Date,y=data.Installs,name = "Percentage",line = dict(color = 'red'),opacity = 0.8)
    data3 = [trace1]
    layout = dict(title='Percentage increase or decrease in the downloads',xaxis=dict(rangeselector=dict(buttons=list([dict(count=1,label='1m',step='month',stepmode='backward'),dict(count=6,label='6m',step='month',stepmode='backward'),dict(step='all')])),rangeslider=dict(visible = True),type='date'))
    fig = dict(data=data3, layout=layout)
    plotly.offline.plot(fig, filename = 'time-series-pct.html')
    root=Tk()
    T = tk.Text(root, height=15, width=60)
    T.pack()
    T.insert(tk.END,"Total increase of ")
    T.insert(tk.END,change)
    T.insert(tk.END,"% for apps whose android version is not an issue and can work with varying devices")
    root.mainloop()


def que6a():
    apps=common()
    data=pd.concat([apps['Last Updated'],apps['Category'],apps['Installs']],axis=1)
    data.rename(index=str, columns={"Last Updated": "Year"}, inplace=True)
    data['Year'] = pd.DatetimeIndex(data['Year']).year
    data=data[data.Year > 2015]
    aggregation_functions = {'Installs': 'sum'}
    data= data.groupby(['Category','Year']).aggregate(aggregation_functions).reset_index()
    data.sort_values(by=['Year'],inplace=True)
    data=data.pivot(index='Year', columns='Category', values='Installs')
    data=data.fillna(1)
    category=data.columns.tolist()
    d2016=data.values[0].tolist()
    d2017=data.values[0].tolist()
    d2018=data.values[2].tolist()
    dict2016 = dict(zip(category, data.values[0].tolist()))
    maximum1 = max(dict2016, key=dict2016.get)
    a=maximum1+" Category has the most downloads in 2016"
    minimum1 = min(dict2016, key=dict2016.get)
    b=minimum1+" Category has the least downloads in 2016"
    dict2017 = dict(zip(category, data.values[1].tolist()))
    maximum2 = max(dict2017, key=dict2017.get)
    c=maximum2+" Category has the most downloads in 2017"
    minimum2 = min(dict2017, key=dict2017.get)
    d=minimum2+" Category has the least downloads in 2017"
    dict2018 = dict(zip(category, data.values[2].tolist()))
    maximum3 = max(dict2018, key=dict2018.get)
    e=maximum3+" Category has the most downloads in 2018"
    minimum3 = min(dict2018, key=dict2018.get)
    f=minimum3+" Category has the least downloads in 2018"
    data = [
        go.Scatter(
            x=data.index,
            y=data[name].values,
            mode='lines',
            name=name,
            line=dict(width=4)
        ) for name in data.columns
    ]
    layout = go.Layout(
        title='Downloads Trend per Category',
        xaxis=dict(title='Years', ticklen=5, zeroline=False, gridwidth=2),
        yaxis=dict(title='Number of downlaods', ticklen=5, gridwidth=2),
        showlegend=True
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='yearcomp.html')
    
    root=Tk()
    T = tk.Text(root, height=100, width=100, font=('Helveyica',20))
    T.pack()
    T.insert(tk.END,a)
    T.insert(tk.END,"\n")
    T.insert(tk.END,b)
    T.insert(tk.END,"\n")
    T.insert(tk.END,c)
    T.insert(tk.END,"\n")
    T.insert(tk.END,d)
    T.insert(tk.END,"\n")
    T.insert(tk.END,e)
    T.insert(tk.END,"\n")
    T.insert(tk.END,f)
    root.mainloop()

def que6b():
    
    apps=common()
    data=pd.concat([apps['Last Updated'],apps['Category'],apps['Installs']],axis=1)
    data.rename(index=str, columns={"Last Updated": "Year"}, inplace=True)
    data['Year'] = data['Year'].apply(lambda x: x.replace('2017','2018') if '2017' in str(x) else x)
    data['Year'] = pd.DatetimeIndex(data['Year']).year
    data=data[data.Year > 2015]
    aggregation_functions = {'Installs': 'sum'}
    data= data.groupby(['Category','Year']).aggregate(aggregation_functions).reset_index()
    data.sort_values(by=['Year'],inplace=True)
    data=data.pivot(index='Year', columns='Category', values='Installs')
    data=data.fillna(1)
    data=data.pct_change()
    category=data.columns.tolist()
    pct=data.values[1].tolist()
    pct = [i * 100 for i in pct]
    root=Tk()
    T = tk.Text(root, height=100, width=100, font=('Helveyica',20))
    T.pack()
    for i in range(len(category)):
        T.insert(tk.END, category[i])
        T.insert(tk.END, " : ")
        if pct[i]<0: 
            T.insert(tk.END, "-")
            T.insert(tk.END, pct[i])
            T.insert(tk.END, "%")
            T.insert(tk.END, "\n")
        else:
            T.insert(tk.END, "+")
            T.insert(tk.END, pct[i])
            T.insert(tk.END, "%")
            T.insert(tk.END, "\n")
    root.mainloop()





def que6():
    root=Tk()
    root.title(" Analysis ")
    root.geometry("500x200+200+200")
    Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
    
    Label(root, text="Download trend from 2016 to 2018", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=50)
    Button(root,text="VIEW PLOT",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que6a).place(x=390,y=50)
    

    Label(root, text="Percentage increase or decrease in downloads\n over the period of three years", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=100)
    Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que6b).place(x=390,y=100)         
   


def correlation():
        apps=common()
        corrmat = apps.corr()
        trace1 = {
                "x": corrmat.columns, 
                "y": corrmat.columns, 
                "z": corrmat.values,
                "type": "heatmap"
                }
        data = [trace1]
        layout = go.Layout(title='Features Correlation Matrix')
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig)  

def que1():
    apps=common()
    category_count=apps['Category'].tolist()
    installs_count=apps['Installs'].tolist()
    category=apps['Category'].unique()
    downloads=list()
    for i in category:
        dl=0
        for j,k in zip(category_count,installs_count):
            if j==i:
                dl=dl+k
        downloads.append(dl)
                    
    
    fig = {'data': [{'labels': category,
                  'values': downloads,
                  'type': 'pie'}],
        'layout': {'title': 'App Installations Category wise'}
         }
    
    plotly.offline.plot(fig)





def que4():
    apps=common()
    category_list = list(apps.Category.unique())
    ratings = []
    for category in category_list:
        x = apps[apps.Category == category]
        rating_rate = x.Rating.sum()/len(x)
        ratings.append(rating_rate)
    data=pd.DataFrame({'Category':category_list, 'Rating':ratings})
    new_index = (data['Rating'].sort_values(ascending=False)).index.values
    sorted_data = data.reindex(new_index)
    sns.set(style="white")
        # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(15, 9))
    sns.barplot(x=sorted_data.Category, y=sorted_data.Rating)
    plt.xticks(rotation=45)
    plt.show()
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")
    root.geometry("%dx%d+%d+%d" % (900, 400, 300, 300))
    canvas = FigureCanvasTkAgg(f, root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side="top",fill='both',expand=True)
    root.mainloop()

       
        
def que5():
    apps=common()
    data=pd.concat([apps['Last Updated'],apps['Category'],apps['Installs']],axis=1)
    data['Last Updated'] =pd.to_datetime(data['Last Updated'])
    data.rename(index=str, columns={"Last Updated": "Date"}, inplace=True)
    aggregation_functions = {'Installs': 'sum'}
    data= data.groupby(['Category','Date']).aggregate(aggregation_functions).reset_index()
    data.sort_values(by=['Date'],inplace=True)
    data=data.pivot(index='Date', columns='Category', values='Installs')
    data=data.fillna(0)
    data = [
        go.Scatter(
            x=data.index,
            y=data[name].values,
            mode='lines',
            name=name,
            line=dict(width=4)
        ) for name in data.columns
    ]
    layout = go.Layout(
        title='Downloads Trend per Category',
        xaxis=dict(title='Date', ticklen=5, zeroline=False, gridwidth=2),
        yaxis=dict(title='Number of downloads', ticklen=5, gridwidth=2),
        showlegend=True
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='Battle4TheTop.html')

def que2a():
    apps=common()
    sns.set(style="white")
    f=plt.figure(figsize = (14,12)) 
    g1 = sns.countplot(x='Installs', data=apps)
    g1.set_title("App Installs Count", fontsize=20)
    g1.set_xlabel("Number of Installs", fontsize=15)
    g1.set_ylabel("Number of Apps", fontsize=15)
    plt.xticks(rotation=45) 
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")
    root.geometry("%dx%d+%d+%d" % (900, 400, 300, 300))
    canvas = FigureCanvasTkAgg(f,root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side="top",fill='both',expand=True)
    root.mainloop()


def que2b():
    apps=common()
    sns.set(style="white")
    installs_categorical=pd.DataFrame({'InstallRange': apps['Installs']})
    installs_categorical=pd.cut(installs_categorical['InstallRange'], bins=[0, 10000, 50000, 150000, 500000, 5000000, 999999999999], include_lowest=True, labels=['Less than 10K','Between 10K and 50K','Between 50K and 150K','Between 150K and 500K','Between 500K and 5000K','More than 5000K'])
    apps=pd.concat([apps,installs_categorical],axis=1)
    f2=plt.figure(figsize = (14,12)) 
    g1 = sns.countplot(x='InstallRange', data=apps)
    g1.set_title("App Installs Count", fontsize=20)
    g1.set_xlabel("Number of Installs", fontsize=15)
    g1.set_ylabel("Number of Apps", fontsize=15)
    plt.xticks(rotation=45) 
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")
    root.geometry("%dx%d+%d+%d" % (900, 400, 300, 300))
    canvas = FigureCanvasTkAgg(f2,root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side="top",fill='both',expand=True)    
    root.mainloop()
    
def result():
    apps=common()
    installs_categorical=pd.DataFrame({'InstallRange': apps['Installs']})
    installs_categorical=pd.cut(installs_categorical['InstallRange'], bins=[0, 10000, 50000, 150000, 500000, 5000000, 999999999999], include_lowest=True, labels=['Less than 10K','Between 10K and 50K','Between 50K and 150K','Between 150K and 500K','Between 500K and 5000K','More than 5000K'])
    apps=pd.concat([apps,installs_categorical],axis=1)
    root=Tk()
    T = tk.Text(root, height=15, width=35)
    T.pack()
    a=apps['InstallRange'].value_counts()
    T.insert(tk.END,a )
    root.mainloop()  


def que2():
        
        r=Tk()
        r.title(" Analysis ")
        r.geometry("500x200+200+200")
        Label(r, text="", bg='black', width='200', height='200').place(x=0, y=0)
        Label(r, text="Downloads Count", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=10, y=50)
        Button(r,text="VIEW PLOT",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que2a).place(x=390,y=50)
                  
        Label(r, text="Downloads Count according to Range", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=10, y=100)
        Button(r,text="VIEW PLOT",bg="goldenrod1",width=10,height=1,font=(" Times",11,'bold'),fg='black',command=que2b).place(x=390,y=100)
                  
                   
        Label(r, text="Result", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=10, y=150)
        Button(r,text="VIEW ",bg="goldenrod1",width=8,height=1,font=(" Times",11,'bold'),fg='black', command=result).place(x=390,y=150)
                  
        r.mainloop()
def que16():
    apps=common()
    data=pd.concat([apps['Last Updated'],apps['Installs']],axis=1)
    data.rename(index=str, columns={"Last Updated": "Year"}, inplace=True)
    data['Year'] = pd.DatetimeIndex(data['Year']).year
    aggregation_functions = {'Installs': 'sum'}
    data= data.groupby(['Year']).aggregate(aggregation_functions).reset_index()
    #print(data)
    data1=pd.concat([apps['Last Updated'],apps['Installs']],axis=1)
    data1.rename(index=str, columns={"Last Updated": "Month"}, inplace=True)
    data1['Month'] = pd.DatetimeIndex(data1['Month']).month
    aggregation_functions = {'Installs': 'sum'}
    data1= data1.groupby(['Month']).aggregate(aggregation_functions).reset_index()
    #print(data1)
    x=data['Installs'].sum()/len(data)
    x=x/12
    print(x)
    data1['Installs']=data1['Installs']//len(data)
    array=np.asarray(data1['Installs'])
    idx = (np.abs(array - x)).argmin()
    root=Tk()
    T = tk.Text(root, height=15, width=50)
    T.pack()
    a=calendar.month_name[idx]+" and "+calendar.month_name[idx+1]+" months are the best indicator to the"
    T.insert(tk.END,a)
    T.insert(tk.END,"\nAverage downloads that an app will generate over the entire year")
    root.mainloop() 
     
def que3a():
        apps=common()
        cat_list = list(apps.Category.unique())
        dls = []
        mldl = []
        names=[]
        for category in cat_list:
            x = apps[apps.Category == category]
            dl_count = x.Installs.sum()//len(x)
            maxleast_count=x.Installs.sum()
            mldl.append(maxleast_count)
            dls.append(dl_count)
            if dl_count>=250000:
                names.append(category)
        ml=pd.DataFrame({'Category':cat_list, 'Downloads':mldl})
        new_index = (ml['Downloads'].sort_values(ascending=False)).index.values
        sorted_data = ml.reindex(new_index)
        print(sorted_data['Category'].iloc[0]," Category has the most number of downloads")
        print(sorted_data['Category'].iloc[-1]," Category has the least number of downloads")
        trace1 = go.Bar(x=sorted_data.Category,y=sorted_data.Downloads,text=sorted_data.Category,textposition='auto',marker=dict(color='rgb(158,202,225)',line=dict(color='rgb(8,48,107)',width=1.5,)),opacity=0.6)
        data = [trace1]
        layout = go.Layout(title='Total number of downloads per category in Billions',)
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='text-hover-bar.html')
        
        root = tk.Tk()
        T = tk.Text(root, height=30, width=60)
        T.pack()
        T.insert(tk.END, "\nCategory with the most number of downloads: ")
        T.insert(tk.END, sorted_data['Category'].iloc[0],"\n")
        T.insert(tk.END, "\nCategory with the least number of downloads: ")
        T.insert(tk.END, sorted_data['Category'].iloc[-1])
        tk.mainloop()
           
def que3b():
    apps=common()
    cat_list = list(apps.Category.unique())
    dls = []
    mldl = []
    names=[]
    for category in cat_list:
        x = apps[apps.Category == category]
        dl_count = x.Installs.sum()//len(x)
        maxleast_count=x.Installs.sum()
        mldl.append(maxleast_count)
        dls.append(dl_count)
        if dl_count>=250000:
            names.append(category)                          
    data=pd.DataFrame({'Category':cat_list, 'Downloads':dls})
    new_index = (data['Downloads'].sort_values(ascending=False)).index.values
    sorted_data = data.reindex(new_index)
    
    trace0 = go.Bar(x=sorted_data.Category,y=sorted_data.Downloads,text=sorted_data.Category,textposition='auto',marker=dict(color='rgb(58,200,225)',line=dict(color='rgb(8,48,107)',width=1.5,)),opacity=0.6)
    data = [trace0]
    layout = go.Layout(title='Average number of downloads per category in Millions',)

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='text-hover-barx.html')
            
    root = tk.Tk()
    T = tk.Text(root, height=30, width=60)
    T.pack()
    T.insert(tk.END, "\nCategories with an average of atleast 250K downloads: \n")
    T.insert(tk.END,', '.join(names),"\n")
    tk.mainloop()

def que3():
        root=Tk()
        root.title(" Analysis ")
        root.geometry("500x150+200+200")
        Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
        Label(root, text="App Category with most and least Downloads", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=50)
        Button(root,text="VIEW",bg="goldenrod1",width=8,height=1,font=(" Times",11,'bold'),fg='black',command=que3a).place(x=390,y=50)
        Label(root, text="Average Downloads of App Categories", justify=LEFT, fg="white", font=("calibri",14,'bold'), width='60', anchor=W, bg='black').place(x=10, y=100)        
        Button(root,text="VIEW",bg="goldenrod1",width=8,height=1,font=(" Times",11,'bold'),fg='black',command=que3b).place(x=390,y=100)
        root.mainloop()
 
def frame3():
        root=Tk()
        root.title(" Analysis ")
        root.geometry("1000x730+20+40")
        Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
        Label(root, text="Relation between the Sentiment-Polarity and\nSentiment-Subjectivity of all the apps", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=100)
        Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que13).place(x=780,y=100)
        Label(root, text="Check out the reviews categorized as positive,negative \nand neutral for any App", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=185)
        Button(root,text="GO",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que14).place(x=780,y=185)
        Label(root, text=" Is it advisable to launch an app like ’10 Best foods for you’?\nDo the users like these apps?", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=270)
        Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que15).place(x=780,y=270)
        Label(root, text="Is there any influence of the size of an App over the number of Installs?", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=355)
        Button(root,text="GO",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que17).place(x=780,y=355) 
        Label(root, text="App Ratings vs Price(in Dollars)", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=440)
        Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=extra1).place(x=780,y=440) 
        Label(root, text="Number of Apps per Android Version", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=525)
        Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=extra2).place(x=780,y=525)
        Label(root, text="Best Month Indicator to the average downloads per Year", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=600)
        Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que16).place(x=780,y=600) 
        Button(root,text="PREVIOUS",bg="goldenrod1",width=12,height=1,font=(" Times",15,'bold'),fg='black',command=lambda:[root.destroy(),frame2()]).place(x=100,y=670)
        Button(root,text="EXIT",bg="goldenrod1",width=12,height=1,font=(" Times",15,'bold'),fg='black',command=root.destroy).place(x=800,y=670)
        root.mainloop()
        
def frame2():
        root=Tk()
        root.title(" Analysis ")
        root.geometry("1000x730+20+40")
        Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
        Label(root, text="Analysis of App Downloads over the past three years", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=100)
        Button(root,text="GO",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que6).place(x=780,y=100)
        Label(root, text="Analysis of those apps whose android version is not an \nissue and can work with varying devices", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=185)
        Button(root,text="GO",bg="goldenrod1",width=10, height=1,font=(" Times",13,'bold'),fg='black',command=que7).place(x=780,y=185)
        Label(root, text="Analysis of co-relation between the number of downloads\nand the ratings received. ", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=270)
        Button(root,text="GO",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que9).place(x=780,y=270)
        Label(root, text="Analysing App downloads per month and calculating the ratio\n of downloads for the app that qualifies as teen versus mature17+", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=355)
        Button(root,text="GO",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que10).place(x=780,y=355)
        Label(root, text=" Which quarter of which year has generated the highest number\nof install for each app used in the study?", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=440)
        Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que11).place(x=780,y=440)
        Label(root, text="Categorizing the Apps according to the type of Sentiments", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=525)
        Button(root,text="GO",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que12).place(x=780,y=525)
        Button(root,text="NEXT",bg="goldenrod1",width=12,height=1,font=(" Times",15,'bold'),fg='black',command=lambda:[root.destroy(),frame3()]).place(x=800,y=670)
        Button(root,text="PREVIOUS",bg="goldenrod1",width=12,height=1,font=(" Times",15,'bold'),fg='black',command=lambda:[root.destroy(),frame1()]).place(x=100,y=670)
        root.mainloop()

def frame1():
        root=Tk()
        root.title(" Analysis ")
        root.geometry("1000x730+20+40")
        Label(root, text="", bg='black', width='200', height='200').place(x=0, y=0)
        Label(root, text="View Correlation Matrix", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=100)
        Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=correlation).place(x=780,y=100)
        Label(root, text="Percentage download in each Category on the Playstore", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=185)
        Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que1).place(x=780,y=185)
        Label(root, text="Categorization of Apps according to the number of downloads", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=270)
        Button(root,text="GO",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que2).place(x=780,y=270)
        Label(root, text="Discovering App Categories with most, least and average Downloads", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=355)
        Button(root,text="GO",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que3).place(x=780,y=355)
        Label(root, text="Analysing and Calculating average Ratings of each App Category", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=440)
        Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que4).place(x=780,y=440)
        Label(root, text="Download Trend over the period of past few years", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=100, y=525)
        Button(root,text="VIEW",bg="goldenrod1",width=10,height=1,font=(" Times",13,'bold'),fg='black',command=que5).place(x=780,y=525)       
        Button(root,text="NEXT",bg="goldenrod1",width=12,height=1,font=(" Times",15,'bold'),fg='black',command=lambda:[root.destroy(),frame2()]).place(x=800,y=670)     
        root.mainloop()
        
def mainscreen():
        global myroot
        myroot=Tk()
        myroot.title("Contents")
        myroot.geometry("800x600+20+40")
        Label(myroot, text="", bg='black', width='150', height='100').place(x=0, y=0)
        Label(myroot, text="TABLE OF CONTENTS", fg="white", font=("calibri",26,'bold'), width='24', anchor=CENTER, bg='black',relief="ridge",bd=4).place(x=150, y=70)
        Label(myroot, text="Check out analysis of data using various data Visualization tools", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=70, y=200)
        Button(myroot,text="Go",bg="goldenrod1",width=5,height=1,font=(" Times",12,'bold'),fg='black',command=frame1).place(x=710,y=200)
        Label(myroot, text="Check out Forecasting of Data in future years using \nSARIMAX Time-Series Prediction Model", justify=LEFT, fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=70, y=300)
        Button(myroot,text="Go",bg="goldenrod1",width=5,height=1,font=(" Times",12,'bold'),fg='black',command=forecast).place(x=710,y=300)
        Label(myroot, text="Add new Data to existing Databases for Analyis and Forecasting", fg="white", font=("calibri",16,'bold'), width='60', anchor=W, bg='black').place(x=70, y=400)
        Button(myroot,text="Go",bg="goldenrod1",width=5,height=1,font=(" Times",12,'bold'),fg='black',command=dataentry).place(x=710,y=400)
        Button(myroot,text="EXIT",bg="goldenrod1",width=8,height=1,font=(" Times",16,'bold'),fg='black',command=myroot.destroy).place(x=560,y=520)
        myroot.mainloop()
mainscreen()
