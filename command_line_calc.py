sign = input("What do you want to calculcate ( + - * / )? ")

if sign != "+" and sign != "-" and sign != "*" and sign != "/":
    print("Invalid operation. Please enter one of +, -, *, or /.")
else:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if sign == "+":
        result = num1 + num2
    elif sign == "-":
        result = num1 - num2
    elif sign == "*":
        result = num1 * num2
    else:
        result = num1 / num2

print(result)
