def snafu_to_decimal(snafu_input: str) -> int:
    value_dict = {"2":2, "1":1, "0":0,"-":-1, "=":-2 }
    input_len = len(snafu_input)
    output =0
    for idx in range(input_len):
        addition = (5**(input_len-idx-1))*value_dict[snafu_input[idx]]
        output += addition
    return output
def get_closest_snafu(decimal_input: int) -> str:
    value_dict = {9:"2-", 8:"2=", 7:"12", 6:"11", 5:"10", 4:"1-", 3:"1=", 2:"2", 1:"1", 0:"0"}
    if decimal_input <10:
        return value_dict[decimal_input]
    digit_position = len(str(decimal_input))-1    
    decimal_num = 5**digit_position
    while decimal_num<decimal_input: 
        snafu_num =1
        if decimal_num*2 <= decimal_input:
            snafu_num = 2
        digit_position += 1
        decimal_num = 5**digit_position
    output = snafu_num*5**(digit_position-1)
    snafu_output =[str(snafu_num)]
    for i in range(digit_position-1):
        idx = digit_position-2 -i
        last_num =0
        for num in [0,1,2]:
            if output +  num*5**idx>decimal_input:
                output += last_num*5**idx
                snafu_output.append(str(last_num))
                break
            elif num==2:
                output += 2*5**idx
                snafu_output.append(str(num))
            else:
                last_num = num



    # remaining = decimal_input- snafu_num*(5**(digit_position-1))
    # print("remaining ", remaining)
    # print("snafu_num ", snafu_num)
    # output = str(snafu_num)
    # output += get_closest_snafu(remaining)
    # print("closet decimal ", output )
    # print(snafu_output)
    # print(snafu_to_decimal("".join(snafu_output)))
    return "".join(snafu_output)

def descartes_mix(a,b):
    return [i+j for i in a for j in b]

def decimal_to_snafu(decimal_input: int) -> str:
    
    # num_digits = len(str(decimal_input))-1
    init_number = get_closest_snafu(decimal_input)
    difference = decimal_input- snafu_to_decimal(init_number)
    result = add_n(init_number,difference,10)

    return result

def format(digit):
    if digit == -1: return "-"
    elif digit ==-2: return "="
    else: return str(digit)       
def add_n(input,n, power):
    n_power = n//(5**power)
    print("n_power ", n_power)
    remaining = n%(5**power)
    for _ in range(n_power):
        input = add_5powern(input, power)
    # print("power 5 in decimal ",snafu_to_decimal(input) )
    # print("decimal from power 5, " , 5**power)
    # print("done getting power 5 with remaining ", remaining)
    for _ in range(remaining):
        input = add_one(input)
    return input

def add_5powern(input,n):
    input = list(input)
    n_digit = input[-n-1]

    if n_digit =="-":
        n_digit=0
    elif n_digit =="=":
        n_digit=-1
    else:
        n_digit= 1 + int(n_digit)
    if n_digit <3 and n_digit > -3:
        if n_digit== -1:
            n_digit = "-"
        elif n_digit=="-2":
            n_digit= "="
        input[-n-1] = str(n_digit)
        return "".join(input)
    elif n_digit==3:
        n_digit ="="
        input[-n-1] = n_digit
        new_input = "".join(input[:-n-1])
        return add_one(new_input)+"".join(input[-n-1:])

def add_one(input):
    last_digit = input[-1]

    if last_digit =="-":
        last_digit=0
    elif last_digit =="=":
        last_digit=-1
    else:
        last_digit= 1 + int(last_digit)
    if last_digit <3 and last_digit > -3:
        if last_digit== -1:
            last_digit = "-"
        elif last_digit=="-2":
            last_digit= "="
        return input[:-1] + str(last_digit)
    elif last_digit==3:
        last_digit ="="

    if len(input)>1:
        new_input = input[:-1]
    else:
        new_input = "0"
    return add_one(new_input)+str(last_digit)


if __name__=="__main__":
    assert snafu_to_decimal("11=02=02===1=222-12")==4282300054607
    assert decimal_to_snafu(4282300054607) =="11=02=02===1=222-12"

    with open("day25/input.txt","r") as file:
        lines = file.readlines()
    new_lines = [line.strip() for line in lines]
    count = sum([snafu_to_decimal(line) for line in new_lines])
    print(count)
    print(decimal_to_snafu(count))
