
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
        login=cur.fetchone()
       	if (login[0]<1):
        	print('Could not find your account')
        	return
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
                add_exist=cur.fetchall()
                #if (add_exist==0):
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
            cur.execute('INSERT INTO mileage_program VALUES (%s,%s,%s)',(airline, email, None))
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
            for row in rows:
                print "   ", row
        
        elif command2==5:
            from_airport=input('Where are you departing from? \n')
            to_airport=input('Where are you flying to? \n')
            date=input('Enter the desired departure date.')
#            print('find tickets given info')
        
        elif command2==6:
            pass
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




