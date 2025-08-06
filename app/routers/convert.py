from fastapi import APIRouter, Depends, HTTPException, status
from app.types.enums import Convert, IndonesianNumber, IndonesianNumberBase
from app.types.models import ConvertModel, ReverseConvertModel
from app.types.responses import ConvertResponse, ReverseConvertResponse
from app.tools.validators import validate_idr_range

router = APIRouter(
    prefix="/converter",
    tags=["converter"],
)

@router.get('', response_model=ConvertResponse)
async def read_converter(params: ConvertModel = Depends()) -> dict: 
    number = params.idr
    
    if (params.suffix):
        number = (number * getattr(IndonesianNumberBase, params.suffix).value)

    validate_idr_range(number)

    writting = get_writting(number)

    return {
        "currency": 'IDR',
        "amount": number, 
        "writting": f"{writting} rupiah",
        "convert": {
            "eur": round((number / Convert.eu), 2),
            "usd": round((number / Convert.usd), 2)
        }
    }

@router.get('/reverse', response_model=ReverseConvertResponse)
async def read_reverse_converter(params: ReverseConvertModel = Depends()) -> dict:
    splited = params.idr.split()

    grouped = {}

    for index, word in enumerate(splited):
        if word in ('miliar', 'juta', 'ratus', 'puluh'):
            grouped[index - 1] = f"{grouped[index - 1]} {word}"            
        else:
            grouped[index] = word

    grouped_list = list(grouped.values())
    grouped_numbers = []

    for index, word in enumerate(grouped_list):
        splited = word.split()

        if "se" in splited[0]:
            parts = splited[0].split("se")
            splited[0] = 1
            splited.append(parts[1])
            number = 1
        else:
            try:
                number = getattr(IndonesianNumber, splited[0]).value
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid"
                )
            
        if len(splited) > 1 and splited[1]:
            try:
                base = getattr(IndonesianNumberBase, splited[1]).value
                number = number * base
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid"
                )

        grouped_numbers.append(number)

    total = sum(grouped_numbers)

    return {
        "amount": total,
         "convert": {
            "eur": round((total / Convert.eu), 2),
            "usd": round((total / Convert.usd), 2)
        }
    }

def get_writting(number: int) -> str:
    if number < 20:
        return IndonesianNumber(number).name

    devide = [1000000000, 1000000, 1000, 100, 10, 1]

    number_left = number

    results = {
        1000000000: 0,
        1000000: 0,
        1000: 0,
        100: 0,
        10: 0,
        1: 0
    }

    for index, num in enumerate(devide):
        if number_left <= 0: break

        sum = (number_left - num)

        if sum < 0: continue

        while (number_left >= num):
            number_left -= num
            results[num] += 1

    string = ''

    for index, amount in results.items(): 
        if amount == 0: continue

        if amount < 20:
            if index not in (1, 10):
                if index in (1000000, 1000, 100) and amount == 1:
                    string += f"{IndonesianNumberBase(1).name}{IndonesianNumberBase(index).name} "
                    continue
                else:
                    string += f"{IndonesianNumber(amount).name.replace("_", " ")} {IndonesianNumberBase(index).name} "
                    continue

            if index == 10:
                sum = ((amount * 10) + results[1])
                string += f"{get_writting_of_base(sum)}"
                break

            if amount == 1:
                sum = (amount + (results[10] * 10))

                string += f"{get_writting_of_base(sum)}"
                break
            else:
                if index == 1:
                    string += f"{IndonesianNumber(amount).name}"
                else:
                    string += f"{IndonesianNumber(amount).name} {IndonesianNumberBase(index).name} "
        else:
            string += f"{get_writting_of_base(amount)}{IndonesianNumberBase(index).name} "

    return string.rstrip()

def get_writting_of_base(amount) -> str:
    if amount < 19:
        return f"{IndonesianNumber(amount).name.replace("_", " ")}"

    list_of_digits = [int(i) for i in str(amount)]
    length = len(list_of_digits)

    string = ''

    for index, digit in enumerate(list_of_digits):
        if (digit == 0): continue

        if (length == 3 and index == 1):
            print()
        else:
            if digit == 1 and length > 2:
                string += f"{IndonesianNumberBase(1).name}"
            else:
                string += f"{IndonesianNumber(digit).name} "

        if index == 0 and length == 2: 
            string += f"{IndonesianNumberBase(10).name} "
        if length == 3: 
            if index == 0:
                string += f"{IndonesianNumberBase(100).name} "
            if index == 1:
                sum = ((list_of_digits[1] * 10) + list_of_digits[2])

                if (sum < 19): 
                    string += f"{IndonesianNumber(sum).name.replace("_", " ")} "
                    break

                string += f"{IndonesianNumber(digit).name} {IndonesianNumberBase(10).name} "

    return string