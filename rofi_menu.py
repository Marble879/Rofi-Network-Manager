from rofi import Rofi

rofi = Rofi()

def quickOptionsTest():
    options = ['Red', 'Green', 'Blue', 'White', 'Silver', 'Black', 'Other']
    index, key = rofi.select('What colour car do you drive?', options)
    return index, key

if __name__ == '__main__':
    index, key = quickOptionsTest()
    print("index: " + str(index) + "\n" + "key: " + str(key))
