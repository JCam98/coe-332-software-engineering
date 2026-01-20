#!/usr/bin/env python3                                                                                                                                                                                                                                                 

''' Property of Justin Campbell                                                                                                                                                                                                                              
    Purpose of Use: COE 332: Software Engineering and Design                                                                                                                                                                                                                  
    Script File Name: generate_animals.py                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                              
        Homework #2: The Island of Dr. Moreau                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                              
Description: This script constitutes the first part of three scripts (the others                                                                                                                                                                                              
being "read_animals.py", and "test_read_animals.py") used for homework                                                                                                                                                                                                        
assignment #2. In this program, the "petname", and "random" modules are used                                                                                                                                                                                                  
to randomly generate a 20 element list of animals and their associated                                                                                                                                                                                                        
attributes (head type, body type, arm number,leg number, and tail number)                                                                                                                                                                                                     
and assigns them each to a dictionary. In turn, these dictionaries are then                                                                                                                                                                                                   
appended to a list. The list of dictionaries is then assigned to a one-element                                                                                                                                                                                                
dictionary to create an exportable JSON object. This JSON object is then                                                                                                                                                                                                      
exported to a JSON file whose filename is read in through the terminal                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                              
'''

# Import modules:                                                                                                                                                                                                                                                             

import json, petname, random, sys

def main():

    ''' Initialize list "head_choices" with the five animal head choices: '''

    head_choices = ["snake", "bull", "lion", "raven", "bunny"]
    animal_list = [] # Initialize data structure to contain dictionaries of animals                                                                                                                                                                                           

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

        animal_list.append({'head': head_type, \
                            'body': body_comp_1 + "-" + body_comp_2, \
                                'arms': arms_number, 'legs': legs_number, \
                                    'tails': tails_num})

    ''' Insert the list of dictionaries data structure "animal_list" into a                        
    dictionary to create an exportable JSON object: '''

    animal_struct = {'animals': animal_list}

    ''' Use the JSON library to dump the data structure into a json file whose file name is read i\
n from the terminal": '''

    with open(sys.argv[1], 'w') as out:

      json.dump(animal_struct, out, indent=2)

if (__name__ == '__main__'):
    main()



