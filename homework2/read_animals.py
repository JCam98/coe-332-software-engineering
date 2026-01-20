#!/usr/bin/env python3                                                                                                                                                                                                                                                        

''' Property of Justin Campbell                                                                                                                                                                                                                          
    Purpose of Use: COE 332: Software Engineering and Design                                                                                                                                                                                                                  
    Script File Name: read_animals.py                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                              
        Homework #2: The Island of Dr. Moreau                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                              
Description: This script constitutes the second of three scripts                                                                                                                                                                                                              
used for homework assignment #2. This program uses the I/O method "open()"                                                                                                                                                                                                    
to read in the contents of the JSON file "animals.JSON" to a JSON object.                                                                                                                                                                                                     
The "random" module is then used to randomly choose one of the animal descriptions                                                                                                                                                                                            
to output to the console. The "random" module is used a second time to randomly                                                                                                                                                                                               
choose two of the animals in the generated list to breed, and the characteristics                                                                                                                                                                                             
of the parents, and offspring, are output to the console. This constitutes the                                                                                                                                                                                                
new feature that is incorporated within this script. Lastly, this script                                                                                                                                                                                                      
defines two functions that are called in "test_read_animals.py" for simple unit                                                                                                                                                                                               
testing applications for the new features incorporated in this script. '''


# Import modules:                                                                                                                                                                                                                                                             

import json, random, sys

''' Define functions encompassing unit testing for new feature (breeding of                                                                                                                                                                                                   
two unique, and randomly-chosen animals): '''

''' The function "check_arm_num()" checks whether there are an even number of                                                                                                                                                                                                 
arms in the offspring animal: '''

def check_arm_num(arms_number):

    assert isinstance(arms_number,int) # Input to this function should be an int                                                                                                                                                                                              

    if ((arms_number % 2) == 0):
        return('COUNT PASSES')
    else:
        return ('COUNT FAILS')

''' The function "check_tail_num()" check whether the number of tails in the                                                                                                                                                                                                  
offspring animal is equal to the sum of the number of arms and legs: '''

def check_tail_num(arms_number, legs_number, tails_number):

    # Inputs to this function should be integers:                                                                                                                                                                                                                             

    assert isinstance(arms_number,int)
    assert isinstance(legs_number,int)
    assert isinstance(tails_number,int)

    if (tails_number == (arms_number + legs_number)):
        return ('COUNT PASSES')
    else:
        return ('COUNT FAILS')

def main():

    ''' Open the json file in read-only mode and assign contents                                                                                                                                                                                                              
    of file to datastructure "animals": '''

    with open(sys.argv[1],'r') as f:
            animals= json.load(f)

    ''' Print the details of one of the animals at random to the console: '''

    print("Depicted below are the physical characteristics of one randomly generated animal:\n")

    print(animals['animals'][random.randint(0,19)])
    print("\n")

    ''' New Feature: Randomly choose two different animal species to breed: '''
    
    parent_1 = animals['animals'][random.randint(0,19)]

    diff_species_cond = False # Initialize boolean condition to false                                                                                                                                                                                                         

    ''' Continue randomly choosing a second animal while the species are non-unique: '''

    while(diff_species_cond == False):
        parent_2 = animals['animals'][random.randint(0,19)]

        if (parent_1 != parent_2):
            diff_species_cond = True

    ''' Breed the two unique animals by mixing their elements to create new animal: '''

    offspring = [] # Initialize a list to store dictionary elements for new animal                                                                                                                                                                                            

    ''' Take the body and head type of the offspring to be a combination of that                                                                                                                                                                                              
    of the respective parents, and of equal contribution: '''

    head_type = parent_1['head'] + "-" + parent_2['head']
    body_type = parent_1['body'] + "-" + parent_2['body']

    ''' Take the number of arms and legs of the offspring to be equal to the average of                                                                                                                                                                                       
    that of the two parents: '''

    arms_number = (1/2) * (parent_1['arms'] + parent_2['arms'])
    legs_number = (1/2) * (parent_1['legs'] + parent_2['legs'])

    ''' If the number of arms is an odd number, round down to the nearest                                                                                                                                                                                                     
    even number: '''

    if (arms_number % 2 != 0):
        arms_number = arms_number - 1

    ''' Take the number of tails of the offspring to be equal to the sum of the                                                                                                                                                                                               
    number of arms and legs of the offspring: '''
    
    tails_number = arms_number + legs_number

    ''' Assemble dictionary of physical characteristics of offspring and append                                                                                                                                                                                               
    to list "offspring": '''

    offspring.append({'head': head_type, \
                            'body': body_type, \
                                'arms': arms_number, 'legs': legs_number, \
                                    'tails': tails_number})



    ''' Print characteristics of both parents and offspring to the console:'''

    print("Below are the characteristics for parent 1, parent 2, and the offspring respectively:\n")
    print("Parent 1:\n ")
    print(parent_1)
    print("\n")
    print("Parent 2:\n ")
    print(parent_2)
    print( "\n")
    print("Offspring:\n ")
    print(offspring)
    print( "\n")

if (__name__ == '__main__'):
    main()
