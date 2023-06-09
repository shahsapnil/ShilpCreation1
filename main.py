from flask import Flask,render_template,request,redirect,url_for
from num2words import num2words
from datetime import datetime , timedelta ,date,time
from deta import Deta
# from flask_mysqldb import MySQL



deta = Deta('d06ll08k_6APby2dWjWjPYHD37hy28PoMNgdaTzpA') 
user = deta.Base('user')
sell = deta.Base('selldata')
bank = deta.Base('bankentry')
app= Flask(__name__)



# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'myflask'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# cnx = MySQL(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/createbill")
def createbill():
    if request.method=="GET":
        today = date.today()
        res = user.fetch()
        all_items = res.items
        list1=[]
        for i in all_items:
            list1.append(i["key"])


        return render_template('details.html',list1=list1,date=today)
    return render_template('details.html')

@app.route('/register', methods=['GET','POST'])
def register():

    def roundTraditional(val,digits):
            return round(val+10**(-len(str(val))-1), digits)

    if request.method=='POST':
        data=request.form
        parcel=request.form['parcel'].upper()


        # logic for duplicate bill

        # res=sell.fetch({'key':data['inumber'],'bill type':data['btype']})
        # all_items = res.items
        # list1=[]
        # for i in all_items:
        #     list1.append(i["data"])

        # if len(list1) ==0:
            
        def is_float(value):
            try:
                float(value)
                return True
            except:
                return False
            
        print(data)
        # convert dict in to itratable list
        mainlist=[]
        for i,j in data.items():
            list1=[]
            list1.append(i)
            if j.isdigit() or is_float(j):
                k=float(j)
                list1.append(k)
            else:
                list1.append(j.upper())
            mainlist.append(list1)

        header=mainlist[1:5]
        goods=mainlist[5:]
        # print(header)

        finallist=[]
        passlist=[]
        for i in range(len(goods)):
            if goods[i][1]!='':
                finallist.append(goods[i][1])
        print(finallist)

        i = 3
        j=0
        while (i <= len(finallist)-2):
            passlist.append(finallist[j:i])
            i+=3
            j+=3
        print(passlist)
        list2=[]
        for i in passlist:
            net_mtr=i[1]-((100-header[-1][1])*i[1])/100
            total=net_mtr*i[2]
            i.append(net_mtr)
            i.append(total)
            list2.append(i)
        print(list2)

        qty=0
        total=0
        for i in list2:
            qty+=i[3]
            total+=i[4]


        # total=net_mtr*goods[2][1]
        dtotal=total-float(data['discount'])
        igst=(dtotal*5)/100
        final=dtotal+igst 
        final_0_decimal=roundTraditional(final,0)
        roun=final_0_decimal-final 
        roff=roundTraditional(roun,2)
        finaltotal=final+roun


            # #purchase due date
            # date= datetime.strptime(header[1][1], "%Y-%m-%d")
            # purchase_due_date =(date + timedelta(days=header[4][1])).strftime("%d-%m-%Y")
            # # print(purchase_due_date)

            
            # #Sell due date
            # date1= datetime.strptime(header[1][1], "%Y-%m-%d")
            # sell_due_date =(date1 + timedelta(days=header[9][1])).strftime("%d-%m-%Y")
            # # print(sell_due_date)


        date= datetime.strptime(header[1][1], "%Y-%m-%d")
        date1 =date.strftime("%d-%m-%Y")


        a=header[2][1]
        result=user.fetch([{"key":a}])
        all_items = result.items

        list3=[]
        for i in all_items:
            list3.append(i['key'])
            list3.append(i["baddr"].upper())
            list3.append(i["saddr"].upper())
            list3.append(i["gstno"])



            # # sql="INSERT INTO USERS (name,email,username,password) VALUES (%s,%s,%s,%s)"
            # # value=(header[3][1],header[5][1],header[6][1],header[7][1])
            # # cur=cnx.connection.cursor()
            # # cur.execute(sql, value)
            # # cnx.connection.commit()
            # # cur.close()
            
        
        textfinal=num2words(finaltotal).upper()+' ONLY'
        pdfname = header[0][1].split("/")[0]+ " " + header[2][1]


        if data['vtype'] == "CREDIT NOTE" or data['vtype'] == "PURCHASE":
            sell.put({"key":header[0][1],"data":mainlist,"bill amt":" ","bill party":header[2][1],"date":date1,"vtype":data['vtype'],"credit":finaltotal})
        else:
            sell.put({"key":header[0][1],"data":mainlist,"bill amt":finaltotal,"bill party":header[2][1],"date":date1,"vtype":data['vtype'],"credit":" "})

            

        return render_template('taxinvoice.html',header=header,goods=goods,total=total,igst=igst,final=final,roff=roff,finaltotal=finaltotal,textfinal=textfinal ,date1=date1,parcel=parcel,pdfname=pdfname,list2=list2,qty=qty,list3=list3,vtype=data['vtype'],dis=data['discount'])
        # return passlist

        # else:
            # return "Bill Number Already Exsist"


@app.route("/addcustomer", methods=['GET','POST'])
def addcustomer():
    if request.method=="POST":
        cust=request.form

        list1=[]
        for i in cust.values():
            list1.append(i)
        # print(list1)

        user.put({"key": list1[0], "baddr": list1[1],"saddr":list1[2],"gstno":list1[3]})

        return "Customer added successfully"
    return render_template('addcustomer.html')


@app.route('/changecustomer', methods=['GET','POST'])
def changecustomer():
    if request.method=="POST":
        cust=request.form

        result=user.fetch([{"key":cust['sparty']}])
        all_items = result.items

        list3=[]
        for i in all_items:
            list3.append(i['key'])
            list3.append(i["baddr"].upper())
            list3.append(i["saddr"].upper())
            list3.append(i["gstno"])
        


        return render_template('changedeletecustomer.html',list3=list3)
    else:
        res = user.fetch()
        all_items = res.items
        list1=[]
        for i in all_items:
            list1.append(i["key"])
        return render_template('changecustomer.html',list1=list1)
    
@app.route('/deletecustomer',methods=['GET','POST'])
def deletecustomer():
    if request.method=='POST':
        cust=request.form

        res = user.delete(cust['sparty'])

        return cust['sparty']+' deleted successfully'



@app.route('/printbill', methods=['GET','POST'])
def printbill():

    def roundTraditional(val,digits):
            return round(val+10**(-len(str(val))-1), digits)

    if request.method=='POST':
        data=request.form

        res=sell.fetch({'key':data['bno']})
        all_items = res.items
        list1=[]
        for i in all_items:
            list1.append(i["data"])
    
        if len(list1) !=0:

            header=list1[0][1:5]
            goods=list1[0][5:]



            finallist=[]
            passlist=[]
            for i in range(len(goods)):
                if goods[i][1]!='':
                    finallist.append(goods[i][1])


            i = 3
            j=0
            while (i <= len(finallist)-2):
                passlist.append(finallist[j:i])
                i+=3
                j+=3
            list2=[]
            for i in passlist:
                net_mtr=i[1]-((100-header[-1][1])*i[1])/100
                total=net_mtr*i[2]
                i.append(net_mtr)
                i.append(total)
                list2.append(i)


            qty=0
            total=0
            for i in list2:
                qty+=i[3]
                total+=i[4]

            # total=net_mtr*goods[2][1]
            a=float(str(list1[0][-2][1]))
            dtotal=total-a
            igst=(dtotal*5)/100
            final=dtotal+igst 
            final_0_decimal=roundTraditional(final,0)
            roun=final_0_decimal-final 
            roff=roundTraditional(roun,2)
            finaltotal=final+roun


                # #purchase due date
                # date= datetime.strptime(header[1][1], "%Y-%m-%d")
                # purchase_due_date =(date + timedelta(days=header[4][1])).strftime("%d-%m-%Y")
                # # print(purchase_due_date)

                
                # #Sell due date
                # date1= datetime.strptime(header[1][1], "%Y-%m-%d")
                # sell_due_date =(date1 + timedelta(days=header[9][1])).strftime("%d-%m-%Y")
                # # print(sell_due_date)


            date= datetime.strptime(header[1][1], "%Y-%m-%d")
            date1 =date.strftime("%d-%m-%Y")


            a=header[2][1]

            result=user.fetch([{"key":a}])
            all_items = result.items


            list3=[]
            for i in all_items:
                list3.append(i['key'])
                list3.append(i["baddr"].upper())
                list3.append(i["saddr"].upper())
                list3.append(i["gstno"])
            print(list3)



                # # sql="INSERT INTO USERS (name,email,username,password) VALUES (%s,%s,%s,%s)"
                # # value=(header[3][1],header[5][1],header[6][1],header[7][1])
                # # cur=cnx.connection.cursor()
                # # cur.execute(sql, value)
                # # cnx.connection.commit()
                # # cur.close()
                

            textfinal=num2words(finaltotal).upper()+' ONLY'
            pdfname = header[0][1].split("/")[0]+ " " + header[2][1]

            # sell.put({"key":header[0][1],"data":mainlist,"bill type":goods[-2][1],"bill amt":finaltotal,"bill party":header[2][1]})

                

            return render_template('taxinvoice.html',header=header,goods=goods,total=total,igst=igst,final=final,roff=roff,finaltotal=finaltotal,textfinal=textfinal ,date1=date1,parcel=list1[0][-1][1],pdfname=pdfname,list2=list2,qty=qty,list3=list3,vtype=list1[0][0][1],dis=str(list1[0][-3][1]))

            # else:
            #     return "Bill Number Already Exsist"

        else:
            return "Bill no not exsist"
    else:
        return render_template('printbill.html')


# for test purpose endpoint

@app.route('/getuser', methods=["GET","POST"])
def userss():  
      
    res = sell.fetch()
    all_items = res.items
    print(res)
    print(type(res))


    for i in all_items:
        print(i)

    # fetch until last is 'None'
    return all_items



@app.route('/changebill', methods=["GET","POST"])
def changebill():
    if request.method=='POST':
        data=request.form
        
        res=sell.fetch({'key':data['bno']})
        all_items = res.items
        list1=[]
        for i in all_items:
            list1.append(i["data"])

        if len(list1) !=0:

            res = user.fetch()
            all_items = res.items
            list2=[]
            for i in all_items:
                list2.append(i["key"])


            return render_template('changebill.html',list1=list1,list2=list2)
        else:
            return "Bill number not exsist"
    return render_template('printbill.html')



@app.route('/ledger', methods=["GET","POST"])
def ledger():
    if request.method=='POST':
        data=request.form
        a=data['sparty']
        result=sell.fetch([{"bill party":a}])
        bankres=bank.fetch([{"partyname":a}])

        all_items = result.items

        list1=[]
        debit=0
        credit=0
        for i in all_items:
            list3=[]
            list3.append(i['date'])
            list3.append(i['vtype'])
            list3.append(i['key'])
            list3.append(i['bill amt'])
            list3.append(i['credit'])

                        
            if str(i['bill amt'])!=" ":
                debit=debit + int(str(i['bill amt']))
            if str(i['credit'])!=" ":
                credit=credit + int(str(i['credit']))
            list1.append(list3)

        all_items = bankres.items
        for i in all_items:
            list3=[]
            list3.append(i['entrydate'])
            list3.append(i['perticular'])
            list3.append(i['key'])
            list3.append(i['debit'])
            list3.append(i['credit'])
            if str(i['debit'])!=" ":
                debit=debit + int(str(i['debit']))
            if str(i['credit'])!=" ":
                credit=credit + int(str(i['credit']))
            list1.append(list3)
        sorted_list = sorted(list1, key=lambda t: datetime.strptime(t[0], '%d-%m-%Y'))
        return render_template('ledgerprint.html',list1=sorted_list,credit=credit,debit=debit)
    else:
        res = user.fetch()
        all_items = res.items
        list1=[]
        for i in all_items:
            list1.append(i["key"])
        return render_template('ledger.html',list1=list1)
    

@app.route('/bankentry', methods=['GET','POST'])
def bankentry():
    if request.method=='POST':
        data=request.form

        date= datetime.strptime(data['entrydate'], "%Y-%m-%d")
        date1 =date.strftime("%d-%m-%Y")
        
        if data['vtype']=='Credit':
            bank.put({"key": data['vno'],"vouchertype":data['vtype'], "partyname":data['pname'],"bankname":data['bank'],"entrydate":date1,"credit":data['amt'],"debit":" ","perticular":data['Miscellaneous']})
        if data['vtype']=='Debit':
            bank.put({"key": data['vno'],"vouchertype":data['vtype'], "partyname":data['pname'],"bankname":data['bank'],"entrydate":date1,"credit":" ","debit":data['amt'],"perticular":data['Miscellaneous']})
        
        return redirect(url_for('bankentry'))
    
    bankres = bank.fetch()
    bankres1=bankres.items
    list2=[]
    for i in bankres1:
        list2.append(int(i["key"]))
    vno=int(str(max(list2)))+1

    res = user.fetch()
    all_items = res.items
    list1=[]
    for i in all_items:
        list1.append(i["key"])
    return render_template('bank.html',list1=list1,vno=vno)

@app.route('/changebank', methods=['GET','POST'])
def changebank():
    bankres = bank.fetch()
    bankres1=bankres.items
    # return bankres1
    list1=[]
    for i in bankres1:
        list2=[]
        list2.append(i['key'])
        list2.append(i['entrydate'])
        list2.append(i['bankname'])
        list2.append(i['partyname'])
        list2.append(i['debit'])
        list2.append(i['credit'])
        list1.append(list2)
    # return list1
    return render_template('changebank.html',list1=list1)


@app.route('/editbank/<string:id>/', methods=['GET','POST'])
def editbank(id):
    bankres=bank.fetch({"key":id})

    list1=[]
    for i in bankres.items:
        list1.append(i['vouchertype'])
        list1.append(i['key'])
        list1.append(datetime.strptime(i['entrydate'], '%d-%m-%Y').date())
        list1.append(i['bankname'])
        list1.append(i['partyname'])
        list1.append(i['perticular'])
        if i['vouchertype'] == "Credit":
            list1.append(i['credit'])
        else:
            list1.append(i['debit'])

    res = user.fetch()
    all_items = res.items
    list2=[]
    for i in all_items:
        list2.append(i["key"])
    return render_template('editbank.html',list2=list2,list1=list1)

# if __name__=="__main__":
#     app.run(debug=True)