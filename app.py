from flask import Flask,render_template,request
from num2words import num2words
from datetime import datetime , timedelta
# from flask_mysqldb import MySQL



app= Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'myflask'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# cnx = MySQL(app)

@app.route("/")
def index():
    return render_template('details.html')

@app.route('/register', methods=['GET','POST'])
def register():

    def roundTraditional(val,digits):
            return round(val+10**(-len(str(val))-1), digits)

    if request.method=='POST':
        data=request.form
        parcel=request.form['parcel']


        def is_float(value):
            try:
                float(value)
                return True
            except:
                return False
        
        # print(data)
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

        header=mainlist[:11]
        goods=mainlist[11:]

        finallist=[]
        passlist=[]
        for i in range(len(goods)):
            if goods[i][1]!='':
                finallist.append(goods[i][1])
        # print(finallist)

        i = 3
        j=0
        while (i <= len(finallist)):
            passlist.append(finallist[j:i])
            i+=3
            j+=3
        # print(passlist)
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
        igst=(total*5)/100
        final=total+igst 
        final_0_decimal=roundTraditional(final,0)
        roun=final_0_decimal-final 
        roff=roundTraditional(roun,2)
        finaltotal=final+roun


        #purchase due date
        date= datetime.strptime(header[1][1], "%Y-%m-%d")
        purchase_due_date =(date + timedelta(days=header[4][1])).strftime("%d-%m-%Y")
        print(purchase_due_date)

        
        #Sell due date
        date1= datetime.strptime(header[1][1], "%Y-%m-%d")
        sell_due_date =(date1 + timedelta(days=header[9][1])).strftime("%d-%m-%Y")
        print(sell_due_date)


        date= datetime.strptime(header[1][1], "%Y-%m-%d")
        date1 =date.strftime("%d-%m-%Y")



        # sql="INSERT INTO USERS (name,email,username,password) VALUES (%s,%s,%s,%s)"
        # value=(header[3][1],header[5][1],header[6][1],header[7][1])
        # cur=cnx.connection.cursor()
        # cur.execute(sql, value)
        # cnx.connection.commit()
        # cur.close()
        

        textfinal=num2words(finaltotal).upper()+' ONLY'
        pdfname = header[0][1].split("/")[0]+ " " + header[5][1]

        

        return render_template('taxinvoice.html',header=header,goods=goods,total=total,igst=igst,final=final,roff=roff,finaltotal=finaltotal,textfinal=textfinal ,date1=date1,parcel=parcel,pdfname=pdfname,list2=list2,qty=qty)


if __name__=="__main__":
    app.run(debug=True)