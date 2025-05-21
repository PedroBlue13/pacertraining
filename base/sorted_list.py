
try:
    inputnumb = input("enter numbers with space: \n'Ex: 2 3 4'\n")

    number = [int(blue) for blue in inputnumb.split()]
    print (f"List of numbers {number}")

    if len(number) >=10:
        print(f"Wow many numbers in list: {number}")

    sorted_even = sorted([num for num in number if num %2 ==0])
    print(f"Ordebated even numbers: {sorted_even}")
except Exception as e:
    print("An error ocurred:", e)
