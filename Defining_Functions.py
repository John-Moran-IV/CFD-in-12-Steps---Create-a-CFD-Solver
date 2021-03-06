def simpleadd(a, b):  # Creating a function called simpleadd with 2 parameters.
    return a+b  # The function returns the sum of arguments a and b.


X = simpleadd(3, 4)  # Call the function and add 3 with 4.
print(X)  # Display the sum.


def fibonacci(n):  # Creating a function called fibonacci with 1 parameter.
    a, b = 0, 1  # Set initial values of a and b to 0 and 1 respectively.
    for i in range(n):  # Start looping, for n times
        a, b = b, a + b  # Old b becomes new a, old a + old b becomes new b.
    return a  # Returns the value of a in the sequence upon loop completion.


Y = fibonacci(7)  # Call the fibonacci function with an argument of 7, store as Y.
print(Y)  # Print the value of Y when the function is finished.

for n in range(10):  # Calls the fibonacci function 10 times, with arg's 0-9.
    print(fibonacci(n))  # Prints each function call result.
