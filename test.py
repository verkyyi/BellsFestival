import re
def get_contact(contract_part):
    dic = {}
    address_matches = re.search(r'(?<=\()(A)(?=\))([\s\S]*?)T:', contract_part)
    if address_matches:
        address = address_matches.group(2).strip().replace('\n', ', ').replace('   ', ' ')
        dic['Address'] = address
    phone_matches = re.search(r'T: (\(\d{3}\)\d{3}-?\d{4})', contract_part)
    if phone_matches:
        phone = phone_matches.group(1)
        dic['Telephone:'] = phone
    return dic

if __name__ == '__main__':
    read_file = open("data.txt", "r")
    contract_part = read_file.read()
    get_contact(contract_part)
    print(get_contact(contract_part))
    read_file.close()