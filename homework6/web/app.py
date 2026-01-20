''' Property of Justin Campbell                                                                                                                                                                                         \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    \
                                                                                                                                                                                                                                            
    Purpose of Use: COE 332: Software Engineering and Design                                                                                                                                                                               \
                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                           \                                                                                                                                                                                                                              
    Script File Name: app.py                                                                                                                                                                                                               \
                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                           \
                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                           \                                                                                                                                                                                                                                        \
                                                                                                                                                                                                                                           \
                                                                                                                                                                                                                                            
        Midterm Project: The Island of Dr. Moreau                                                                                                                                                                                          \
                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                           \
                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                           \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   \
                                                                                                                                                                                                                                            
Description: This python script contains the flask application for the midterm                                                                                                                                                              
project that contains routes that will:                                                                                                                                                                                                     
                                                                                                                                                                                                                                            
    1) query a range of  dates                                                                                                                                                                                                              
    2) selects a particular creature by its unique identifier                                                                                                                                                                               
    3) edits a particular creature by passing the UUID, and updated stats                                                                                                                                                                   
    4) deletes a selection of animals by a date range(s)                                                                                                                                                                                    
    5) returns the average number of legs per animal                                                                                                                                                                                        
    6) returns a total count of animals   '''

# Import modules:                                                                                                                                                                                                                           
from __future__ import print_function #Enables compatibility of python2 print statements to python3 syntax                                                                                                                                  
import petname, random, datetime, uuid, redis, flask, json, os, sys

# Create a client connection for the redis server:                                                                                                                                                                                          

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()
rd=redis.StrictRedis(host=redis_ip, port=6379, db=0)

''' Initialize list "head_choices" with the five animal head choices: '''

head_choices = ["snake", "bull", "lion", "raven", "bunny"]
animals_list_output = [] # Initialize list to store animals to write to json file                                                                                                                                                           

for i in range(0,20):

    ''' Invoke "random()" method to randomly generate one of the head choices: '''

    head_type = head_choices[random.randint(0,4)]

    ''' Invoke "name()" method to randomly generate two animal strings for                                                                                                                                                                  
    the two body components: '''

    body_comp_1 = petname.name()
    body_comp_2 = petname.name()

    ''' Employ "while loop" to ensure that the two components of the body                                                                                                                                                                   
    are not identical '''

    while (body_comp_1 == body_comp_2):
        body_comp_2 = petname.name()


    ''' Generate a random even number of arms between 2 and 10 inclusive: '''
    
    arms_number = random.randint(2,10)

    ''' Employ "while loop" to ensure that the number of arms meets the                                                                                                                                                                     
    aforementioned criteria: '''

    while ((arms_number % 2) > 0):
        arms_number = random.randint(2,10)

    ''' Generate a random number of legs that is both a multiple of three and                                                                                                                                                               
    between the numbers 3, and 12 inclusive: '''

    legs_number = random.randint(3,12)

    ''' Employ "while loop" to ensure that the number of legs meets the                                                                                                                                                                     
    aforementioned criteria: '''

    while ((legs_number % 3) != 0):
        legs_number = random.randint(3,12)


    ''' Append a non-random number of tails that is equal to the sum of the                                                                                                                                                                 
    number of arms and legs: '''

    tails_num = arms_number + legs_number

    # Invoke "uuid4()" method to assign random unique identifier to animal                                                                                                                                                                  

    UUID = str(uuid.uuid4())

    # Invoke "now()" method from "datetime" module to assign random timestamp                                                                                                                                                               

    timestamp = str(datetime.datetime.now())

    animal_label = 'animal' + str(i+1) # String label to serve as key in database                                                                                                                                                           

    ''' Store data structure in redis database: '''
    
    animals_list_output.append(rd.hmset(animal_label, {'head': head_type, \
                        'body': body_comp_1 + "-" + body_comp_2, \
                            'arms': arms_number, 'legs': legs_number, \
                                'tails': tails_num, 'UUID': UUID, 'timestamp':timestamp}))



''' Insert the list of dictionaries data structure "animals_list_output" into a                                                                                                                                                             
    dictionary to create an exportable JSON object and write to json file:                                                                                                                                                                  
                                                                                                                                                                                                                                            
    Note: This data is written out to a json file to allow for the user to                                                                                                                                                                  
    pull information that they would like to query from the database when                                                                                                                                                                   
    curling to the routes in the flask application.'''

animal_struct = {'animals': animals_list_output}

with open('animals.json', 'w') as out:

      json.dump(animal_struct, out, indent=2)


app = flask.Flask(__name__) # Use "Flask()" method to create web app                                                                                                                                                                        

animal_num = rd.dbsize() # Store the number of animals in redis database                                                                                                                                                                   \
                                                                                                                                                                                                                                            

''' Define route "/animals/query_dates" that queries a range of dates. Note: This                                                                                                                                                           
route is defined such that there are three pairs of query parameters, namely,                                                                                                                                                               
minutes, seconds, and microseconds In order for this route to return a range of                                                                                                                                                             
dates, each of these query parameters (6 in total) must be read in                                                                                                                                                                          
through the command line". In particular:                                                                                                                                                                                                   
                                                                                                                                                                                                                                            
    "initial_min" - string containing the initial minute of date range                                                                                                                                                                      
    "final_min" - string containing the final minute of date range                                                                                                                                                                          
    "initial_sec" - string containing the initial second of date range                                                                                                                                                                      
    "final_sec" - string containing the final second of date range                                                                                                                                                                          
    "initial_microsecond" - string containing the initial microsecond of date range                                                                                                                                                         
    "final_microsecond" - string containing the final microsecond of date range '''

@app.route('/animals/query_dates', methods=['GET'])
def query_dates():

     ''' Get the "initial_min" query parameter from the command line and assign                                                                                                                                                            \
                                                                                                                                                                                                                                            
     to string "initial_min_str '''

     initial_min_str = flask.request.args.get('initial_min')
     initial_min = int(initial_min_str)

     ''' Get the "final_min" query parameter from the command line and assign                                                                                                                                                              \
                                                                                                                                                                                                                                            
     to string "final_min_str '''

     final_min_str = flask.request.args.get('final_min')
     final_min = int(final_min_str)

     ''' Get the "initial_sec" query parameter from the command line and assign                                                                                                                                                            \
                                                                                                                                                                                                                                            
     to string "initial_sec_str '''

     initial_sec_str = flask.request.args.get('initial_sec')
     initial_sec = int(initial_sec_str)

     ''' Get the "final_sec" query parameter from the command line and assign
     
     to string "final_sec_str '''

     final_sec_str = flask.request.args.get('final_sec')
     final_sec = int(final_sec_str)

     ''' Get the "initial_microsecond" query parameter from the command line and assign                                                                                                                                                    \
                                                                                                                                                                                                                                            
     to string "initial_micro_str '''

     initial_micro_str = flask.request.args.get('initial_microsecond')
     initial_microsecond = int(initial_micro_str)

     ''' Get the "final_microsecond" query parameter from the command line and assign                                                                                                                                                      \
                                                                                                                                                                                                                                            
     to string "final_micro_str '''

     final_micro_str = flask.request.args.get('final_microsecond')
     final_microsecond = int(final_micro_str)

     query_date_struct = {'StartMinute': initial_min, 'StartSecond': initial_sec,
                          'StartMicrosecond': initial_microsecond,
                          'FinalMinute': final_min, 'FinalSecond': final_sec,
                          'FinalMicrosecond': final_microsecond}

     return query_date_struct

''' Define route "/animals/creature/UUID " to return a particular creature by                                                                                                                                                              \
                                                                                                                                                                                                                                            
its unique identifier. '''

@app.route('/animals/creature/UUID', methods=['GET'])
def get_creature_UUID():

     ''' Get the "UUID" query parameter from the command line and assign                                                                                                                                                                   \
\                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                           \
                                                                                                                                                                                                                                            
     to string "UUID" '''

     UUID = flask.request.args.get('UUID')

     print("The value of UUID read in is ", file=sys.stderr)
     print(UUID, file=sys.stderr)
     print("\n", file=sys.stderr)

     animal_num = rd.dbsize() # Store the number of animals in redis database                                                                                                                                                               

     ''' Define a "for loop" to iterate through each of the animals in the                                                                                                                                                                 \
\                                                                                                                                                                                                                                           
     redis database. Return the animal with UUID equal                                                                                                                                                                                     \
\                                                                                                                                                                                                                                           
     to "UUID" value read in through the route '''                                                                                                                                                                                         \
 ''\

     for i in range(0,animal_num):

         animal_label = 'animal' + str(i+1) # Define animal label                                                                                                                                                                          \
                                                                                                                                                                                                                                            
         left_cond = rd.hget(animal_label,'UUID').decode('utf-8')#decode UUID
         
         print("The value of UUID decoded from database is ", file=sys.stderr)
         print(left_cond, file=sys.stderr)
         print("\n", file=sys.stderr)

         animal_list_binary = [] # Initialize list to store animal with UUID query parameter                                                                                                                                                

         right_cond = UUID

         # If UUID read in through route equals that in database store animal                                                                                                                                                              \
                                                                                                                                                                                                                                            
         if (left_cond == right_cond):

            print('inside this if statement', file=sys.stderr)
            print('The value of "animal_label" is ', file=sys.stderr)
            print(animal_label, file=sys.stderr)
            animal_list_binary=rd.hmget(animal_label,'head','body','arms','legs','tails','UUID','timestamp')
            break


     print("The value of the list of animal parameters in binary is ", file=sys.stderr)
     print(animal_list_binary, file=sys.stderr)
     print("\n", file=sys.stderr)

     animal_list_string = [] # Initialize empty list to store hash values as strings                                                                                                                                                        

     # Define list to store hash names                                                                                                                                                                                                      

     animal_list_hashes = ['head','body','arms','legs','tails','UUID','timestamp']

     # Use a for loop to decode hash values to strings and assign to "animal_list_string"                                                                                                                                                  \
                                                                                                                                                                                                                                            

     for i in range(0,len(animal_list_binary)):
          animal_list_string.append(animal_list_hashes[i] + ":" + animal_list_binary[i].decode('utf-8'))

     print("The value of the list storing the animal parameters in strings is ", file=sys.stderr)
     print(animal_list_string, file=sys.stderr)
     print("\n", file=sys.stderr)


     animal_output = {'animal': animal_list_string}

     print("The value of the dictionary storing the animal parameters in strings is ", file=sys.stderr)
     print(animal_output, file=sys.stderr)

     return animal_output


''' Define route "/animals/creature/UUID/stats" to update the statistics (leg                                                                                                                                                               
number) of an animal with the unique identifier read in through the query                                                                                                                                                                   
parameter, "UUID", and return the animal to the console: '''

@app.route('/animals/creature/UUID/stats', methods=['GET'])
def get_updated_creature():

     ''' Get the "UUID" query parameter from the command line and assign to
     string "UUID": '''

     UUID = flask.request.args.get('UUID')

     ''' Get the "tailnum" query parameter from the command line and assign                                                                                                                                                                \
                                                                                                                                                                                                                                            
     to string "tail_num '''

     tail_num = flask.request.args.get('tailnum')

     animal_num = rd.dbsize() # Store the number of animals in redis database                                                                                                                                                              \
                                                                                                                                                                                                                                            

     ''' Define a "for loop" to iterate through each of the animals in the                                                                                                                                                                 \
                                                                                                                                                                                                                                            
     redis database. Append the animal with the UUID equal                                                                                                                                                                                 \
                                                                                                                                                                                                                                            
     to "UUID" value read in through the route, to a new list, "animal_list",                                                                                                                                                               
     and update the tail number (statistic) of this animal using the query parameter'''

     for i in range(0,animal_num):

         animal_label = 'animal' + str(i+1) # Define animal label                                                                                                                                                                           
         left_cond = rd.hget(animal_label,'UUID').decode('utf-8')#decode UUID                                                                                                                                                              
         right_cond = UUID

         animal_list_binary = [] # Initialize list to store animal with UUID query parameter                                                                                                                                                

         if (left_cond == right_cond):
             rd.hset(animal_label,'tails', tail_num) # Update the tail number                                                                                                                                                               
             animal_list_binary = rd.hmget(animal_label,'head','body','arms','legs','tails','UUID','timestamp')
             break

     animal_list_string = [] # Initialize empty list to store hash values as strings                                                                                                                                                        

     # Define list to store hash names                                                                                                                                                                                                      

     animal_list_hashes = ['head','body','arms','legs','tails','UUID','timestamp']

     # Use a for loop to decode hash values to strings and assign to "animal_list_string"                                                                                                                                                  \
                                                                                                                                                                                                                                            

     for i in range(0,len(animal_list_binary)):
          animal_list_string.append(animal_list_hashes[i] + ":" + animal_list_binary[i].decode('utf-8'))

     animal_output = {'animal': animal_list_string}

     return animal_output


''' Define route "/animals/delete" to delete a selection of animals by a date                                                                                                                                                               
range read in through the route. Note: This route is defined such that                                                                                                                                                                      
there are three pairs of query parameters, namely, minutes, seconds, and microseconds                                                                                                                                                       
In order for this route to return an updated list of animals, each of these                                                                                                                                                                 
query parameters (6 in total) must be read in through the command line". In particular:                                                                                                                                                     
                                                                                                                                                                                                                                            
    "initial_min" - string containing the initial minute of date range                                                                                                                                                                      
    "final_min" - string containing the final minute of date range
    "initial_sec" - string containing the initial second of date range                                                                                                                                                                      
    "final_sec" - string containing the final second of date range                                                                                                                                                                          
    "initial_microsecond" - string containing the initial microsecond of date range                                                                                                                                                         
    "final_microsecond" - string containing the final microsecond of date range                                                                                                                                                             
                                                                                                                                                                                                                                            
Then, the updated list of animals will be returned to the console:'''

@app.route('/animals/delete', methods=['GET'])
def get_updated_animal_list():


     ''' Get the "initial_min" query parameter from the command line and assign                                                                                                                                                            \
                                                                                                                                                                                                                                            
     to string "initial_min_str '''

     initial_min_str = flask.request.args.get('initial_min')
     initial_min = int(initial_min_str)

     ''' Get the "final_min" query parameter from the command line and assign                                                                                                                                                              \
                                                                                                                                                                                                                                            
     to string "final_min_str '''

     final_min_str = flask.request.args.get('final_min')
     final_min = int(final_min_str)

     ''' Get the "initial_sec" query parameter from the command line and assign                                                                                                                                                            \
                                                                                                                                                                                                                                            
     to string "initial_sec_str '''

     initial_sec_str = flask.request.args.get('initial_sec')
     initial_sec = int(initial_sec_str)

     ''' Get the "final_sec" query parameter from the command line and assign                                                                                                                                                              \
                                                                                                                                                                                                                                            
     to string "final_sec_str '''

     final_sec_str = flask.request.args.get('final_sec')
     final_sec = int(final_sec_str)

     ''' Get the "initial_microsecond" query parameter from the command line and assign                                                                                                                                                    \
                                                                                                                                                                                                                                            
     to string "initial_micro_str '''

     initial_micro_str = flask.request.args.get('initial_microsecond')
     initial_microsecond = int(initial_micro_str)

     ''' Get the "final_microsecond" query parameter from the command line and assign                                                                                                                                                      \
                                                                                                                                                                                                                                            
     to string "final_micro_str '''

     final_micro_str = flask.request.args.get('final_microsecond')
     final_microsecond = int(final_micro_str)

     ''' Initialize empty list to assign animals whose time stamps of creation                                                                                                                                                              
     fall outside of the specified query range for minute parameter '''

     animal_list_min_binary = []

     animal_num = rd.dbsize() # Store the number of animals in redis database                                                                                                                                                              \
                                                                                                                                                                                                                                            

     ''' Define a "for loop" to iterate through each of the animals in the                                                                                                                                                                 \
                                                                                                                                                                                                                                            
     redis database. Append the animal with a minute paramter                                                                                                                                                                               
     that lies on the bounds, or outside of the initial and final bounds, to the list                                                                                                                                                       
     "animal_list_min_binary"  '''

     for i in range(0,animal_num):

         animal_label = 'animal' + str(i+1) # Define animal label
         
         # Get the first character of minute from the timestamp:                                                                                                                                                                            

         timestamp_min_1 = (rd.hget(animal_label,'timestamp').decode('utf-8'))[14]

         # Get the second character of minute from the timestamp:                                                                                                                                                                           

         timestamp_min_2 = (rd.hget(animal_label,'timestamp').decode('utf-8'))[15]

         # Concatenate the two characters into a single string:                                                                                                                                                                             

         timestamp_min_str = timestamp_min_1 + timestamp_min_2

         # Convert the timestamp from a string to integer type:                                                                                                                                                                             

         timestamp_min = int(timestamp_min_str)

         # Append animal to list if minute of creation lies outside of range:                                                                                                                                                               

         if (timestamp_min <= initial_min or timestamp_min >= final_min):

             animal_list_min_binary.append(rd.hmget(animal_label,'head','body','arms','legs','tails','UUID','timestamp'))


     animal_list_min = [] # Initialize list to store binary-decoded animals                                                                                                                                                                 

     # Use a for loop to decode hash values to strings and assign to "animal_list_min"                                                                                                                                                      

     for i in range(0,len(animal_list_min_binary)):

         ''' Decode each of the hash values for the animal of the current                                                                                                                                                                   
         iteration: '''

         head_hash_val = animal_list_min_binary[i][0].decode('utf-8')
         body_hash_val = animal_list_min_binary[i][1].decode('utf-8')
         arms_hash_val = animal_list_min_binary[i][2].decode('utf-8')
         legs_hash_val = animal_list_min_binary[i][3].decode('utf-8')
         tails_hash_val = animal_list_min_binary[i][4].decode('utf-8')
         UUID_hash_val = animal_list_min_binary[i][5].decode('utf-8')
         timestamp_hash_val = animal_list_min_binary[i][6].decode('utf-8')

         ''' Add each of the decoded hash values to a new list: '''

         animal_hash_values = [head_hash_val, body_hash_val, arms_hash_val, \
                              legs_hash_val, tails_hash_val, UUID_hash_val,
                              timestamp_hash_val]

         ''' Append the list "animal_hash_values" to the list "animal_list_min" '''

         animal_list_min.append(animal_hash_values)


     ''' Initialize empty list to assign animals whose time stamps of creation                                                                                                                                                              
     both fall in between the specified query ranges for minute and second                                                                                                                                                                  
     of creation '''

     animal_list_min_sec = []

     ''' Define a "for loop" to iterate through each of the animals in list                                                                                                                                                                 
     "animal_list_min". Append the animal with a second paramter                                                                                                                                                                            
     that lies either on one of the bounds, or outside the initial and final                                                                                                                                                                
     bounds for the second parameters, to the list, "animal_list_min_sec"  '''                                                                                                                                                             \


     for i in range(0,len(animal_list_min)):
         
         # Get the first character of second from the timestamp:                                                                                                                                                                            

         timestamp_sec_1 = animal_list_min[i][6][17]

         # Get the second character of minute from the timestamp:                                                                                                                                                                           

         timestamp_sec_2 = animal_list_min[i][6][18]

         # Concatenate the two characters into a single string:                                                                                                                                                                             

         timestamp_sec_str = timestamp_sec_1 + timestamp_sec_2

         # Convert the timestamp from a string to integer type:                                                                                                                                                                             

         timestamp_sec = int(timestamp_sec_str)

         ''' Append animal to list if second of creation lies outside of range                                                                                                                                                              
         or on one of the bounds '''

         if (timestamp_sec <= initial_sec or timestamp_sec >= final_sec):

             animal_list_min_sec.append(animal_list_min[i])


     ''' Initialize empty list to assign animals whose time stamps of creation                                                                                                                                                              
     fall outside of, or on one of the bounds of the microsecond parameter time range: '''

     animal_list_min_sec_mic = []

     ''' Define a "for loop" to iterate through each of the animals in list                                                                                                                                                                 
     "animal_list_min_sec". Append the animal with a microsecond parameter                                                                                                                                                                  
     that lies outside of, or on one of the bounds of the microsecond parameter                                                                                                                                                             
     time range, to the list, "animal_list_min_sec_mic"  '''                                                                                                                                                                               \


     for i in range(0,len(animal_list_min_sec)):

         # Get the six characters of microsecond from the timestamp:                                                                                                                                                                        

         timestamp_micsec_1 = animal_list_min_sec[i][6][20]
         timestamp_micsec_2 = animal_list_min_sec[i][6][21]
         timestamp_micsec_3 = animal_list_min_sec[i][6][22]
         timestamp_micsec_4 = animal_list_min_sec[i][6][23]
         timestamp_micsec_5 = animal_list_min_sec[i][6][24]
         timestamp_micsec_6 = animal_list_min_sec[i][6][25]

         # Concatenate the characters into a single string:                                                                                                                                                                                 

         timestamp_micsec_str = timestamp_micsec_1 + timestamp_micsec_2 + timestamp_micsec_3 \
             + timestamp_micsec_4 + timestamp_micsec_5 + timestamp_micsec_6

         # Convert the timestamp from a string to integer type:                                                                                                                                                                             

         timestamp_micsec = int(timestamp_micsec_str)

         ''' Append animal to list if microsecond of creation lies outside of                                                                                                                                                               
         the range or on one of the bounds '''

         if (timestamp_micsec < initial_microsecond or timestamp_micsec > final_microsecond):

             animal_list_min_sec_mic.append(animal_list_min_sec[i])

     rd.flushall() # Clear all elements from the redis database                                                                                                                                                                             

     ''' Store new data structure in redis database: '''

     for i in range(0,len(animal_list_min_sec_mic)):

        animal_label = 'animal' + str(i+1) # Define animal label                                             

        rd.hmset(animal_label, {'head': animal_list_min_sec_mic[i][0], \
                        'body': animal_list_min_sec_mic[i][1], \
                            'arms': animal_list_min_sec_mic[i][2], \
                            'legs': animal_list_min_sec_mic[i][3], \
                                'tails': animal_list_min_sec_mic[i][4], \
                                    'UUID': animal_list_min_sec_mic[i][5], \
                                        'timestamp': animal_list_min_sec_mic[i][6]})

     status = "Route Terminated Successfully"

     return status


''' Define route "/animals/average_leg_num" to return the average number of                                                                                                                                                                 
legs per animal: '''

@app.route('/animals/average_leg_num', methods=['GET'])
def get_avg_leg_num():

     ''' Initialize lists to store the leg number for each animal: '''

     leg_num_list_str = []
     leg_num_list = []
     animal_num = rd.dbsize() # Store the number of animals in redis database                                                                                                                                                               
     animal_labels_binary = rd.keys() # Store the animal labels in redis database                                                                                                                                                           
     animal_labels = []

     for i in range(0,len(animal_labels_binary)):
         animal_labels.append(animal_labels_binary[i].decode('utf-8'))

     ''' Use a for loop to assign the leg number for each animal to the list'''

     for i in range(0,animal_num):

         leg_num = rd.hget(animal_labels[i],'legs').decode('utf-8') # Return leg number                                                                                                                                                     
         leg_num_list_str.append(leg_num) # Append leg number to list                                                                                                                                                                       
         leg_num_list.append(int(leg_num_list_str[i]))


     ''' Evaluate the average leg number '''

     avg_leg_num = sum(leg_num_list) / len(leg_num_list)

     ''' Convert float type to string to return to console: '''

     avg_leg_num = str(avg_leg_num)

     return avg_leg_num

''' Define route "/animals/total_count" to return the total number of animals: '''

@app.route('/animals/total_count', methods=['GET'])
def get_total_animal_count():

     animal_num = rd.dbsize() # Store the number of animals in redis database                                                                                                                                                               

     animal_num = str(animal_num)

     return animal_num


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
