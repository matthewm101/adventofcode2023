digit_strings = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
numerical_digit_sum = 0
digit_sum = 0

with open("input.txt") as f:
    for line in f:
        first_numerical_digit = None
        last_numerical_digit = None
        first_digit = None
        last_digit = None
        for i in range(0,len(line)):
            if line[i].isdigit():
                last_digit = int(line[i])
                last_numerical_digit = int(line[i])
            for j in range(0,10):
                dstr = digit_strings[j]
                if line[i:i+len(dstr)] == dstr:
                    last_digit = j
            if first_digit is None:
                first_digit = last_digit
            if first_numerical_digit is None:
                first_numerical_digit = last_numerical_digit
        numerical_digit_sum += first_numerical_digit * 10 + last_numerical_digit
        digit_sum += first_digit * 10 + last_digit

print(f"The sum made by combining numerical digits only is {numerical_digit_sum}.")
print(f"The sum made by combining written or numerical digits is {digit_sum}.")
    