
# coding: utf-8

# In[1]:


#get_ipython().system('pip install -r ./requirements.txt')


# In[2]:


#get_ipython().system('pip install psycopg2')
#get_ipython().system('pip install pprint')


# In[15]:


#!/usr/bin/python
import psycopg2
import sys

def main():

    try:
        conn = psycopg2.connect("dbname='flightdb' user='user1' host='localhost' password='secret'")
    except:
        print('unable to connect')
        
    cur=conn.cursor()
    
    command1=1
    print('Welcome to flight app!')
    command1=int(input('Enter 1 to sign in or Enter 2 to sign up. \n'))
    if command1==1:
        email=input('Enter email: ')
        cur.execute('SELECT COUNT(email) FROM purchaser WHERE email LIKE (%s)', (email,))#yes the comma after email is required or we get an error, this is the world we live in
        login=cur.fetchone()#only ever gonna get 1 row
       	if (login[0]<1):#login[0] selects first element of row (it's the only element)
        	print('Could not find your account')
        	return
	cur.execute('SELECT name FROM purchaser WHERE email LIKE (%s)', (email,))
	namearray=cur.fetchone()
	name = namearray[0]# makes name the purchaser's name same as when an account is made, we do this because we'll need name later for flight booking
    elif command1==2:
        email=input('Enter email: ')
        name=input('Enter your name: ')
        try:
            cur.execute('INSERT INTO purchaser VALUES (%s, %s, %s)', (email, None, name)) 
            conn.commit()
        except:
            print('Could not sign you up. Possibly entered an incorrect data type.')
            return
    else:
        print('Must sign in or sign up to use application')
        return
    
    command2=1
    while (command2==1 or command2==2 or command2==3 or command2==4 or command2==5 or command2==6):
        command2=int(input('Options: \nEnter 1 to add user infromation. \nEnter 2 to edit user information. \nEnter 3 to enroll in an airline milage program. \nEnter 4 to search for flight connections. \nEnter 5 to modify bookings. \nEnter any other number to quit. \n'))
       
        if command2==1:
            command3=int(input('Enter 1 to add payment information. \nEnter 2 to add an address. \n'))
            
            if command3==1:
                cardnum=input('Enter the credit card number: ')
                civ=input('Enter the security code: ')
                expiration=input('Enter the expiration date: ')
                Type=input('Enter the type of credit card (Visa, Mastercard, Discover...): ')
                bank=input('Enter the bank it is associated with: ')
                streetnum=input('Enter the billing address street number: ')
                streetname=input('Enter the billing address street name: ')
                Zip=input('Enter the billing address zip code: ')
                city=input('Enter the billing address city: ')
                state=input('Enter the billing address state: ')
                cur.execute('SELECT COUNT(*) FROM address WHERE streetnum=%s AND streetname=%s AND zip=%s', (streetnum, streetname, Zip))
                add_exist=cur.fetchone()
                try:
                    if (add_exist[0]==0):
                        cur.execute('INSERT INTO address VALUES (%s,%s,%s,%s,%s)',(streetnum,streetname,Zip,city,state))
                        conn.commit()
                    cur.execute('INSERT INTO credit_cards VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cardnum,email,civ,expiration,Type,bank,streetnum,streetname,Zip))
                    conn.commit()
                    cur.execute('INSERT INTO billing_address VALUES (%s,%s,%s,%s)',(cardnum,streetnum,streetname,Zip))
                    conn.commit()
                    print('payment method added \n')
                except:
                    print('payment method could not be added. Possibly wrong data type entered. \n')
                
            elif command3==2:
                streetnum=input('Enter the address street number: ')
                streetname=input('Enter the address street name: ')
                Zip=input('Enter the address zip code: ')
                city=input('Enter the address city: ')
                state=input('Enter the address state: ')
                living=input('Enter 1 if this is your living address, otherwise enter any other number\n')
                try:
                    cur.execute('INSERT INTO address VALUES (%s,%s,%s,%s,%s)',(streetnum,streetname,Zip,city,state))
                    conn.commit()
                    if (living==1):
                        try:
                            #only can have 1 livng address, so try to delete any existing first.
                            cur.execute('DELETE FROM living_address WHERE email=%s',(email))
			    conn.commit()
                            cur.execute('INSERT INTO living_address VALUES (%s,%s,%s,%s)',(email,streetnum,streetname,Zip))
			    conn.commit()
			except:
				print('Could not add living address, possibly a wrong data type entered')
                    print('added address')
                except:
                    print('Could not add address. Possibly a wrong data type entered\n')
                    
        elif command2==2:
            command3=int(input('Enter 1 to modify existing information. \nEnter 2 to delete existing information. \n'))
            
            if command3==1:
                command4=int(input('Enter 1 to modify billing address. \nEnter 2 to modify your addresses'))
                
                if command4==1:
                    cardnum=input('Enter the credit card number: ')
                    streetnum=input('Enter the new billing address street number: ')
                    streetname=input('Enter the new billing address street name: ')
                    Zip=input('Enter the new billing address zip code: ')
                    city=input('Enter the new billing address city: ')
                    state=input('Enter the new billing address state: ')
                    try:
                        cur.execute('UPDATE billing_address SET streetnum=%s, streetname=%s, zip=%s WHERE cardnum=%s AND email=%s',(streetnum,streetname,Zip,cardnum, email))
                        print('billing address is updated.\n')
                    except:
                        print('This billing address does not exist, or a wrong data type was entered.\n')
                    conn.commit()
                elif command4==2:
                    old_streetnum=input('Enter the old billing address street number: ')
                    old_streetname=input('Enter the old billing address street name: ')
                    old_Zip=input('Enter the old billing address zip code: ')
                    streetnum=input('Enter the new billing address street number: ')
                    streetname=input('Enter the new billing address street name: ')
                    Zip=input('Enter the new billing address zip code: ')
                    city=input('Enter the new billing address city: ')
                    state=input('Enter the new billing address state: ')
                    try:
                        cur.execute('UPDATE address SET streetnum=%s, streetname=%s, zip=%s, city=%s, state=%s WHERE streetname=%s AND streetnum=%s AND zip=%s',(streetnum, streetname, Zip, city, state, old_streetname, old_streetnum, old_Zip))
                        print('address is updated.\n')
                    except:
                        print('could not update address. Possibly wrong data types entered\n')
		    conn.commit()
            
            elif command3==2:
                command4=int(input('Enter 1 to delete payment information. \nEnter 2 to delete your addresses'))
                if command4==1:
                    cardnum=input('Enter the credit card number you wish to delete: ')
                    try:
                        cur.execute('DELETE FROM credit_cards WHERE cardnum=%s AND email=%s', (cardnum, email))
                        print('Credit Card deleted.\n')
                    except:
                        print('Could not find billing address to delete.\n')
                        
                elif command4==2:
                    streetnum=input('Enter the address street number you wish to delete: ')
                    streetname=input('Enter the address street name you wish to delete: ')
                    Zip=input('Enter the address zip code you wish to delete: ')
                    try:
                        cur.execute('DELETE FROM address WHERE streetnum=%s AND streetname=%s AND zip=%s AND (%s,%s,%s) NOT IN (SELECT streetnum,streetname,zip FROM billing_address WHERE streetnum=%s AND streetname=%s AND zip=%s)',(streetnum, streetname, Zip, streetnum, streetname, Zip, streetnum, streetname, Zip))
                        print('address deleted')
                    except:
                        print('Could not delete address. Either the address does not exist, the data type entered is wrong, or the address entered is a billing address')
		    conn.commit()
        
        elif command2==3:
            cur.execute('SELECT aId, name FROM airline WHERE has_mileage=1')
            rows = cur.fetchall()
            print('aID   Airline')
            for row in rows:
                print "   ", row
            airline=input('Enter the airline aID that has the milage program you wish to enroll in. ')
            cur.execute('SELECT date,departureTime FROM bookings WHERE email LIKE %s',(email,))#get foreign keys to schedule table
            scheds = cur.fetchall()
            if (scheds != []):#possibly no bookings
                newdist = 0
                for sched in scheds:#possibly multiple bookings by 1 person
                	cur.execute('SELECT distance FROM schedule WHERE date = %s AND departureTime = %s',(sched[0],sched[1]))#uses foreign keys to schedule to get distance
                	distance = cur.fetchone()
                	newdist += distance[0]#updates distance for every booking they have
                try:
                    cur.execute('INSERT INTO mileage_program VALUES (%s,%s,%s)',(airline, email, newdist))
                    conn.commit()
                    print('enrolled in mileage program')
                except:
                    print('could not enroll in mileage program')
            else:
                try:
                    cur.execute('INSERT INTO mileage_program VALUES (%s,%s,%s)',(airline, email, 0))
                    conn.commit()
                    print('enrolled in mileage program')
                except:
                    print('could not enroll in mileage program')
                #maybe add a way to withdraw from mileage program.
        
        elif command2==4:
            cur.execute('SELECT IATA, name FROM airport')
            rows = cur.fetchall()
            for row in rows:
                print "   ", row
            from_airport=input('Enter the IATA of the starting airport. \n')
            to_airport=input('Enter the IATA of the destination airport. \n')
            cur.execute('SELECT * FROM schedule s, ticket t WHERE s.date=t.date AND s.departuretime=t.departuretime AND iata_from=%s AND iata_to=%s ORDER BY departuretime, price',(from_airport,to_airport))
            rows = cur.fetchall()
            if rows == []:
                print("Sorry, no matching flights found.")
                return#this should take us back to the main option select but doesn't right now, there are other returns that don't work too
            tempi = 0
            rownames = ["date: ","departure time: ","start iata: ","destination iata: ","estimated arrival time: ","distance: "]
            for row in rows:
                for units in row:
                	print "   ", rownames[tempi], units
                        tempi+=1
                tempi = 0
                print " "
            #results from flight schedule search is a bit more readable now
            inputstr = "Enter the number representing your desired schedule for booking [1-"+str(len(rows))+"]. Enter 0 to go back."
            desired_sched=input(inputstr)
            if (desired_sched == 0) or (desired_sched > len(rows)):
                return#user wants to go back
            cur.execute('SELECT * FROM ticket WHERE date = %s AND departureTime = %s', (rows[desired_sched-1][0], rows[desired_sched-1][1]))
            tickrows = cur.fetchall()
            if tickrows == []:
                print("Sorry, no available tickets")
                return#return to main menu
            print("Available Tickets:")
            tickrownames = ["class: ","departure date: ","departure time: ","flight number :", "price: ","milage price: "]
            for tickrow in tickrows:
                for tickunits in tickrow:
                    print "   ", tickrownames[tempi], tickunits
                    tempi +=1
                tempi = 0
                print " "
            inputstr = "Enter the number representing the ticket you would like to purchase [1-"+str(len(tickrows))+"]. Enter 0 to go back."
            desired_ticket = input(inputstr)
            if (desired_ticket == 0) or (desired_ticket > len(tickrows)):
                return#user wants to go back
            cur.execute('SELECT cardNum,type,bank FROM credit_cards WHERE email = %s',(email,))
            cardrows = cur.fetchall()
            if cardrows == []:
                print("You have no valid credit cards on file. Please add a valid credit card in PAYMENT INFORMATION to pay.")
                return#no credit cards available -> main menu
            print("Available payment methods: ")
	    #from here on, we need to print out payment methods same as with previous prints then let the user select one, print out all info, and confirm puchase (update bookings)
            cardrownames = ["card #: ","type: ","bank: "]
            for cardrow in cardrows:
                for cardunits in cardrow:
                    print "   ", cardrownames[tempi], cardunits
                    tempi +=1
                tempi = 0
                print " "
            inputstr = "Enter the number representing the payment method you would like to use [1-"+str(len(cardrows))+"]. Enter 0 to go back."
            desired_card = input(inputstr)
            if (desired_card == 0) or (desired_card > len(cardrows)):
                return #user wants to go back
            print("Transaction Summary:")
            print("email: "+email)
            print("card number: "+str(cardrows[desired_card-1][0]))
            print("class: "+tickrows[desired_ticket-1][0])
            print("departure date: "+str(tickrows[desired_ticket-1][1]))
            print("departure time: "+str(tickrows[desired_ticket-1][2]))
            print("flight number: "+str(tickrows[desired_ticket-1][3]))
            print("your name: "+name)
            print(" ")
            confirm_trans = input("Enter 1 to confirm transaction and book flight. Enter 0 to cancel.")
            if (confirm_trans == 1):
                try:
                    cur.execute('INSERT INTO bookings VALUES (%s,%s,%s,%s,%s,%s,%s)',(email,str(cardrows[desired_card-1][0]),tickrows[desired_ticket-1][0],tickrows[desired_ticket-1][1],tickrows[desired_ticket-1][2],tickrows[desired_ticket-1][3],name))
                    conn.commit()
                except:
                    print('Sorry, could not complete the transaction.\n')
#from now on we will check if customer is in mileage program and if so add the miles to his bonus
                cur.execute('SELECT email,mileCount FROM mileage_program WHERE email LIKE %s',(email,))
            mileageinfo = cur.fetchone()
            if (mileageinfo != None):
			#updates mileage info if customer has info in there already (is registered)
                new_miles = mileageinfo[1] + rows[desired_sched-1][5]
                try:
                    cur.execute('UPDATE mileage_program SET mileCount = %s WHERE email = %s',(new_miles,email))
                    conn.commit()
                except:
                    print('could not update mile count for the milage program.\n')
            else:
                return#cancel transaction
        
        elif command2==5:
            cur.execute('SELECT * FROM bookings WHERE email LIKE (%s)', (email,))
            bookrows = cur.fetchall()
            if bookrows == []:
                print("You have no booked flights, please use [4] - book flights to book a flight")
                return
            tempi = 0
            bookrownames = ["email: ","card number: ","class: ","date: ","departure time: ","fight number: ","name: "]
            print("Your booked flights:")
            for bookrow in bookrows:
                for bookunit in bookrow:
                    print "   " ,bookrownames[tempi],bookunit
                    tempi += 1
                tempi = 0
            inputstr = "Please enter the number corresponding to the booking you wish to cancel [1-"+str(len(bookrows))+"]. Enter 0 to go back"
            book_delete = input(inputstr)
            if (book_delete == 0) or (book_delete > len(bookrows)):
                return#user wants to go back
            try:
                cur.execute('DELETE FROM bookings WHERE email LIKE %s AND cardNum = %s AND class LIKE %s AND date = %s AND departureTime = %s AND flightNum = %s AND nameOfPassenger LIKE %s',(bookrows[book_delete-1][0],bookrows[book_delete-1][1],bookrows[book_delete-1][2],bookrows[book_delete-1][3],bookrows[book_delete-1][4],bookrows[book_delete-1][5],bookrows[book_delete-1][6]))
                conn.commit()
            except:
                print('Could not delete the booking(s).\n')
#from now on we will check if the user is in a mileage program and reduce his miles due to cancelled booking
            cur.execute('SELECT email,mileCount FROM mileage_program WHERE email LIKE %s',(email,))
            mileageinfo = cur.fetchone()
            if (mileageinfo != None):
                cur.execute('SELECT distance FROM schedule WHERE Date = %s AND departureTime = %s',(bookrows[book_delete-1][3],bookrows[book_delete-1][4]))
                bookmile = cur.fetchone()
                newmiles = mileageinfo[1] - bookmile[0]
                try:
                    cur.execute('UPDATE mileage_program SET mileCount = %s WHERE email LIKE %s',(newmiles,email))
                    conn.commit()
                except:
                    print('could not subtract miles from mileage program.\n')
        else:
            print('Thank you for using our app.')


# In[16]:


main()


# In[15]:


# Create a curson
cur = conn.cursor()

# Execute a statements and fetch results
try:
    cur.execute("SELECT name FROM student")
except:
    print "I can't SELECT from student"

# now let's fetch all the rows and print them
rows = cur.fetchall()
print "\nResults: \n"
for row in rows:
    print "   ", row


# now a query with more result columns
try:
    cur.execute("SELECT id, name, tot_cred FROM student ORDER BY name ASC")
except:
    print "I can't SELECT from student"

rows = cur.fetchall()
print "\nResults: \n"
for row in rows:
    print "   ", row
    print " or to access a particular column (2nd one):", row[1]

# close the connection
cur.close()

# close the connection
conn.close()


# In[15]:


#!/usr/bin/python
import psycopg2
import sys

try:
    conn = psycopg2.connect("dbname='flight_info' user='parkerjoncus' host='localhost' password='secret'")
except:
    print('unable to connect')
        


# In[ ]:




