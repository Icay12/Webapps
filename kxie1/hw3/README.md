Please put hw3 files in this directory.

Python Version:  **2.7.10**

1. The website will show error message on the bottom of the calculator. 

	There are two error messages currently:

	* You must press the buttons! (when requests are not sent by the buttons)
	* Can't divided by 0! (when the divisor is 0)
		

2. If two (or more) operation buttons are clicked without a digit in between, the calculator will remember the last operation input.
   
		press:  7 7 + - * / 1 1 = 
		result: 7

3. If "=" is pressed, users can continue pressing operation buttons to calculate based on the previous result, or they can also press digit buttons to input new numbers.

		press:  7 7 / 1 1 = + 3 =
		result: 10 (calculate based on the result 7, 7 + 3 = 10)
		
		press: 7 7 / 1 1 = 3
		result: 3 (when press new digit after "=" , the result 7 is erased)