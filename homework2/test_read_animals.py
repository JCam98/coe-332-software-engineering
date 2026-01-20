''' Property of Justin Campbell                                                                                                                                                                                                                           
    Purpose of Use: COE 332: Software Engineering and Design                                                                                                                                                                                                                  
    Script File Name: test_read_animals.py                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                              
        Homework #2: The Island of Dr. Moreau                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                              
Description: This script constitutes the third part of three scripts                                                                                                                                                                                                          
used for homework assignment #2. This program uses the "unittest" framework                                                                                                                                                                                                   
to perform simple unit tests using "assertEqual()", and "assertRaises()" on the                                                                                                                                                                                               
functions "check_arm_num()", and "check_tail_num()". These two functions were                                                                                                                                                                                                 
defined in the script "read_animals.py" as part of the new breeding feature                                                                                                                                                                                                   
of the program. '''

# Import "unittest" framework:                                                                                                                                                                                                                                                

import unittest

# Import the functions defined for unit testing in "read_animals.py":                                                                                                                                                                                                         

from read_animals import check_arm_num, check_tail_num

# Create class and subclass for testing our application:                                                                                                                                                                                                                      

class TestReadAnimals(unittest.TestCase):

    # Define "test_check_arm_num()" method for testing "check_arm_num()" function:                                                                                                                                                                                            

    def test_check_arm_num(self):

        '''Use "assertEqual()" method to check that certain calls to the                                                                                                                                                                                                      
        function return expected results'''

        self.assertEqual(check_arm_num(4), 'COUNT PASSES')
        self.assertEqual(check_arm_num(5), 'COUNT FAILS')

        '''Use the "assertRaises()" method to make sure that                                                                                                                                                                                                                  
        errors are properly generated when an incompatible data type is used: '''

        self.assertRaises(AssertionError, check_arm_num, 1.5)
        self.assertRaises(AssertionError, check_arm_num, '2')
        self.assertRaises(AssertionError, check_arm_num, [1,2])
        self.assertRaises(AssertionError, check_arm_num, {'arms': 4})

    # Define "test_check_tail_num()" method for testing "check_tail_num()" function:                                                                                                                                                                                          

    def test_check_tail_num(self):

        '''Use "assertEqual()" method to check that certain calls to the                                                                                                                                                                                                      
        function return expected results: '''

        self.assertEqual(check_tail_num(4,6,10),'COUNT PASSES')
        self.assertEqual(check_tail_num(4,6,11),'COUNT FAILS')

        '''Use the "assertRaises()" method to make sure that                                                                                                                                                                                                                  
        errors are properly generated when an incompatible data type is used: '''

        self.assertRaises(AssertionError, check_tail_num, 1.5,2.5,4.0)
        self.assertRaises(AssertionError, check_tail_num, 'True','False','True')
        self.assertRaises(AssertionError, check_tail_num, [1,2],[2,3],[4,5])
        self.assertRaises(AssertionError, check_tail_num, {'arms': 4} \
                          , {'legs': 6}, {'tails': 10})

  # Wrap the "unittest.main()" function at the bottom so the script can be called:                                                                                                                                                                                            

if __name__ == '__main__':
    unittest.main()
