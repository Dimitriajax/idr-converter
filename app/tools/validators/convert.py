from fastapi import HTTPException, status

def validate_idr_range(number: int):
    if number <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number too small. Minimum allowed is above 1 IDR."
        )

    if number >= 1_000_000_000_000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number too big. Maximum allowed is below 1 triliun IDR."
        )