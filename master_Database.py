
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
        cur.execute('INSERT INTO purchaser VALUES (%s, %s, %s)', (email, None, name)) 
	conn.commit()
    else:
        print('Must sign in or sign up to use application')
        return
    
    command2=1
    while (command2==1 or command2==2 or command2==3 or command2==4 or command2==5 or command2==6):
        command2=int(input('Options: \nEnter 1 to add user infromation. \nEnter 2 to edit user information. \nEnter 3 to enroll in an airline milage program. \nEnter 4 to search for flight connections. \nEnter 5 to book a flight. \nEnter 6 to modify bookings. \nEnter any other number to quit. \n'))
       
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
                if (add_exist[0]==0):
                	cur.execute('INSERT INTO address VALUES (%s,%s,%s,%s,%s)',(streetnum,streetname,Zip,city,state))
			conn.commit()
                	cur.execute('INSERT INTO credit_cards VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cardnum,email,civ,expiration,Type,bank,streetnum,streetname,Zip))
			conn.commit()
                	cur.execute('INSERT INTO billing_address VALUES (%s,%s,%s,%s)',(cardnum,streetnum,streetname,Zip))
			conn.commit()
                	print('payment method added \n')
                
            elif command3==2:
                streetnum=input('Enter the address street number: ')
                streetname=input('Enter the address street name: ')
                Zip=input('Enter the address zip code: ')
                city=input('Enter the address city: ')
                state=input('Enter the address state: ')
                cur.execute('INSERT INTO address VALUES (%s,%s,%s,%s,%s)',(streetnum,streetname,Zip,city,state))
		conn.commit()
                #check to see if this is a living address
                print('added address')
                
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
                    #check that the new address is in address, if not add it.
                    cur.execute('UPDATE billing_address SET streetnum=%s AND streetname=%s AND zip=%s WHERE cardnum=%s AND email=%s',(streetnum,streetname,Zip,cardnum, email))
		    conn.commit()
                    print('billing address is updated.')
                elif command4==2:
                    old_streetnum=input('Enter the old billing address street number: ')
                    old_streetname=input('Enter the old billing address street name: ')
                    old_Zip=input('Enter the old billing address zip code: ')
                    streetnum=input('Enter the new billing address street number: ')
                    streetname=input('Enter the new billing address street name: ')
                    Zip=input('Enter the new billing address zip code: ')
                    city=input('Enter the new billing address city: ')
                    state=input('Enter the new billing address state: ')
                    cur.execute('UPDATE address SET streetnum=%s, streetname=%s, zip=%s, city=%s, state=%s WHERE streetname=%s AND streetnum=%s AND zip=%s',(streetnum, streetname, Zip, city, state, old_streetname, old_streetnum, old_Zip))
		    conn.commit()
                    print('address is updated.')
            
            elif command3==2:
                command4=int(input('Enter 1 to delete payment information. \nEnter 2 to delete your addresses'))
                if command4==1:
                    cardnum=input('Enter the credit card number you wish to delete: ')
                    cur.execute('DELETE FROM credit_cards WHERE cardnum=%s AND email=%s', (cardnum, email))
                    print('Credit Card deleted.')
                elif command4==2:
                    streetnum=input('Enter the address street number you wish to delete: ')
                    streetname=input('Enter the address street name you wish to delete: ')
                    Zip=input('Enter the address zip code you wish to delete: ')
                    cur.execute('DELETE FROM address WHERE streetnum=%s AND streetname=%s AND zip=%s AND (%s,%s,%s) NOT IN (SELECT streetnum,streetname,zip FROM billing_address WHERE streetnum=%s AND streetname=%s AND zip=%s)',(streetnum, streetname, Zip, streetnum, streetname, Zip, streetnum, streetname, Zip))
		    conn.commit()
                    print('address deleted')
        
        elif command2==3:
            cur.execute('SELECT aId, name FROM airline')
            rows = cur.fetchall()
            print('aID   Airline')
            for row in rows:
                print "   ", row
            airline=input('Enter the airline aID that has the milage program you wish to enroll in. ')
            #need a way to check what ailrines have a milage program
	    #before we can put them in the mileage program we need to check their current bookings and make that their mileage_count. This is necessary because when they cancel a booking, we reduce their mileage_count so the user could theoretically book a flight -> enter mileage program -> cancel booking in order to recieve negative miles which we want to avoid
	    cur.execute('SELECT date,departureTime FROM bookings WHERE email LIKE %s',(email,))#get foreign keys to schedule table
	    scheds = cur.fetchall()
	    if (scheds != []):#possibly no bookings
	    	newdist = 0
	    	for sched in scheds:#possibly multiple bookings by 1 person
	        	cur.execute('SELECT distance FROM schedule WHERE date = %s AND departureTime = %s',(sched[0],sched[1]))#uses foreign keys to schedule to get distance
	    		distance = cur.fetchone()
	    		newdist += distance[0]#updates distance for every booking they have
	    	cur.execute('INSERT INTO mileage_program VALUES (%s,%s,%s)',(airline, email, newdist))
	    	conn.commit()
	    else:
            	cur.execute('INSERT INTO mileage_program VALUES (%s,%s,%s)',(airline, email, 0))
	    	conn.commit()
            print('enrolled in mileage program')
            #maybe add a way to withdraw from mileage program.
        
        elif command2==4:
            cur.execute('SELECT IATA, name FROM airport')
            rows = cur.fetchall()
            for row in rows:
                print "   ", row
            from_airport=input('Enter the IATA of the starting airport. \n')
            to_airport=input('Enter the IATA of the destination airport. \n')
            cur.execute('SELECT * FROM schedule WHERE iata_from=%s AND iata_to=%s',(from_airport,to_airport))
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
	    	return;#user wants to go back
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
	    	cur.execute('INSERT INTO bookings VALUES (%s,%s,%s,%s,%s,%s,%s)',(email,str(cardrows[desired_card-1][0]),tickrows[desired_ticket-1][0],tickrows[desired_ticket-1][1],tickrows[desired_ticket-1][2],tickrows[desired_ticket-1][3],name))
	    	conn.commit()
#from now on we will check if customer is in mileage program and if so add the miles to his bonus
	    	cur.execute('SELECT email,mileCount FROM mileage_program WHERE email LIKE %s',(email,))
		mileageinfo = cur.fetchone()
		if (mileageinfo != None):
			#updates mileage info if customer has info in there already (is registered)
			new_miles = mileageinfo[1] + rows[desired_sched-1][5]
			cur.execute('UPDATE mileage_program SET mileCount = %s WHERE email = %s',(new_miles,email))
			conn.commit()
	    else:
	    	return#cancel transaction
        elif command2==5:
            from_airport=input('Where are you departing from (IATA)? \n')
            to_airport=input('Where are you flying to (IATA)?\n')
            date=input('Enter the desired departure date (MM-DD-YYYY).\n')
#            print('find tickets given info')
        
        elif command2==6:
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
	    cur.execute('DELETE FROM bookings WHERE email LIKE %s AND cardNum = %s AND class LIKE %s AND date = %s AND departureTime = %s AND flightNum = %s AND nameOfPassenger LIKE %s',(bookrows[book_delete-1][0],bookrows[book_delete-1][1],bookrows[book_delete-1][2],bookrows[book_delete-1][3],bookrows[book_delete-1][4],bookrows[book_delete-1][5],bookrows[book_delete-1][6]))
	    conn.commit()
#from now on we will check if the user is in a mileage program and reduce his miles due to cancelled booking
	    cur.execute('SELECT email,mileCount FROM mileage_program WHERE email LIKE %s',(email,))
	    mileageinfo = cur.fetchone()
	    if (mileageinfo != None):
	    	cur.execute('SELECT distance FROM schedule WHERE Date = %s AND departureTime = %s',(bookrows[book_delete-1][3],bookrows[book_delete-1][4]))
	    	bookmile = cur.fetchone()
	    	newmiles = mileageinfo[1] - bookmile[0]
	    	cur.execute('UPDATE mileage_program SET mileCount = %s WHERE email LIKE %s',(newmiles,email))
		conn.commit()
#            print('modify bookings')


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




