import uuid

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def coin_to_dict(coin):
    return dict(
        id = coin.id,
        coinName = coin.coin_name,
        duties = [duty.duty_number for duty in coin.duties],
        isComplete = coin.is_complete
    )