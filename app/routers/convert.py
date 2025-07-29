from fastapi import APIRouter, Depends
from app.types.enums import Convert, IndonesianNumber, IndonesianNumberBase
from app.types.models import ConvertModel  
from app.types.responses import ConvertResponse

router = APIRouter(
    prefix="/converter",
    tags=["converter"],
)

@router.get('', response_model=ConvertResponse)
async def read_converter(params: ConvertModel = Depends()): 
    number = params.idr
    
    if (params.suffix):
        number = (number * getattr(IndonesianNumberBase, params.suffix).value)

    writting = get_writting(number)

    return {
        "currency": 'IDR',
        "amount": f"{number:,}", 
        "writting": f"{writting} rupiah",
        "convert": {
            "eur": round((number / Convert.eu), 2),
            "usd": round((number / Convert.usd), 2)
        }
    }

def get_writting(number: int) -> str:
    if number < 20:
        return IndonesianNumber(number).name

    devide = [1000000, 1000, 100, 10, 1]

    numberLeft = number

    results = {
        1000000: 0,
        1000: 0,
        100: 0,
        10: 0,
        1: 0
    }

    for index, num in enumerate(devide):
        if numberLeft <= 0: break

        sum = (numberLeft - num)

        if sum < 0: continue

        while (numberLeft >= num):
            numberLeft -= num
            results[num] += 1

    string = ''

    for index, amount in results.items(): 
        if amount == 0: continue

        if amount < 20: 
            if index == 1000000 or index == 1000 or index == 100:
                string += f"{IndonesianNumber(amount).name} {IndonesianNumberBase(index).name} "
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
        return f"{IndonesianNumber(amount).name}"

    listOfDigits = [int(i) for i in str(amount)]
    length = len(listOfDigits)

    string = ''

    for index, digit in enumerate(listOfDigits):
        if (digit == 0): continue

        if (length == 3 and index == 1):
            print('hello')
        else:
            string += f"{IndonesianNumber(digit).name} "

        if index == 0 and length == 2: 
            string += f"{IndonesianNumberBase(10).name} "
        if length == 3: 
            if index == 0:
                string += f"{IndonesianNumberBase(100).name} "
            if index == 1:
                sum = ((listOfDigits[1] * 10) + listOfDigits[2])

                if (sum < 19): 
                    string += f"{IndonesianNumber(sum).name} "
                    break

                string += f"{IndonesianNumber(digit).name} {IndonesianNumberBase(10).name} "

    return string