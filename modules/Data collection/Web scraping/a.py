data = [["tomhanks", 73], ["toby.hadoke", 55], ["tchalamet", 52], ["zendaya", 45], ["tonyleung_official", 45], ["yoorajung", 20], ["vancityreynolds", 17], ["thesupertoken", 11]]
import json

def process_data(data):
    less_than_10 = 0
    greater_than_30 = 0

    between_10_and_20_list = []
    between_20_and_30_list = []

    for name, value in data:
        if value < 10:
            less_than_10 += 1
        elif 10 <= value <= 20:
            
            between_10_and_20_list.append(f"{name}: {value}")
        elif 20 < value <= 30:
           
            between_20_and_30_list.append(f"{name}: {value}")
        else:
            greater_than_30 += 1

    print("Number of elements less than 10:", less_than_10)
    print("Number of elements between 10 and 20:", len(between_10_and_20_list))
    print("Number of elements between 20 and 30:", len(between_20_and_30_list))
    print("Number of elements greater than 30:", greater_than_30)

    with open("between_10_and_20.txt", "w") as file_10_20:
        file_10_20.write("\n".join(between_10_and_20_list))

    with open("between_20_and_30.txt", "w") as file_20_30:
        file_20_30.write("\n".join(between_20_and_30_list))

    print("Data written to files: between_10_and_20.txt, between_20_and_30.txt")


# Process the data
process_data(data)

#%%
