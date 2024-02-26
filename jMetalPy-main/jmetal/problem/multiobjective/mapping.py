# 映射机位号到0-59
def mapping(number):
    if number <= 26:
        return number - 1
    if number <= 321:
        return number - 279
    if number <= 332:
        return number - 283
    if number <= 519:
        return number - 460
