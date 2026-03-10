def averager():
    total = 0.0
    count = 0
    average = None

    while True:
        # Yield the current average and wait for the next number
        term = yield average

        total += term
        count += 1
        average = total / count


# Usage
calc = averager()
next(calc)  # Start it (yields None)

print(calc.send(10))  # Returns 10.0
print(calc.send(20))  # Returns 15.0
print(calc.send(30))  # Returns 20.0