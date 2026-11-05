
a = None

try:
    a = 10/0
    print(f"The value of a inside try is: {a}")
except ZeroDivisionError as e:
    print(f"A zero division error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print(f"The value of a is: {a}")

print("Done")