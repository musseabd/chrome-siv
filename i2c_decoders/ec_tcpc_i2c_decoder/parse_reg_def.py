import csv

reg_defs = []

capture_csv = 'tcpci_reg_def.csv'
with open(capture_csv, mode ='r')as file:
    csv_dict_reader = csv.DictReader(file)

    for row in csv_dict_reader:
        reg_defs.append(row)

print("reg_map = {\n")

for reg_def in reg_defs:
    # print(reg_def)

    '''
    reg_map = {
        "0x10" : {
        NAME : "ALERT",
        SIZE : 2
    },
    '''
    print(f'\t"0x{reg_def["offset"]}" : {{')
    print(f'\t\tREG_MAP_NAME : "{reg_def["short_name"]}",')
    print(f"\t\tREG_MAP_SIZE : {int(reg_def['size_num'])}")
    print("\t},")
    print()

