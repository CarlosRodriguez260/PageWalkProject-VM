import sys

if len(sys.argv) != 5:
    print("Incorrect argument count!")
    print("Correct use: python ./main CR3-Register EPT-PTR EPT-TABLES.csv GVA-TO-TRANSLATE")
else:
    # Parse Arguments
    CR3 = int(sys.argv[1], 16)
    EPT_PTR = int(sys.argv[2], 16)
    TABLES = sys.argv[3]
    GVA = int(sys.argv[4], 16)

    # Turn GVA into indexes
    offset = GVA & 0xFFF
    pt     = (GVA >> 12) & 0x1FF
    pd     = (GVA >> 21) & 0x1FF
    pdpt   = (GVA >> 30) & 0x1FF
    pml4   = (GVA >> 39) & 0x1FF
    print(f"{GVA:048b}")



def read_table(address, table_name):
    print("TODO")


# GUEST_PML4_base = sys.argv[]

    # # Hex to Binary Mapper
    # hex_bin_map = {
    #     '0':'0000',
    #     '1':'0001',
    #     '2':'0010',
    #     '3':'0011',
    #     '4':'0100',
    #     '5':'0101',
    #     '6':'0110',
    #     '7':'0111',
    #     '8':'1000',
    #     '9':'1001',
    #     'A':'1010',
    #     'B':'1011',
    #     'C':'1100',
    #     'D':'1101',
    #     'E':'1110',
    #     'F':'1111',
    # }

    # # Switch GVA from hex to binary string
    # binary = ''
    # for hex in sys.argv[4][2:].upper():
    #     print(f"Hex: {hex} -> Binary: {hex_bin_map[hex]}")

    #     if len(binary) == 0 and hex=='0':
    #         continue
    #     binary += hex_bin_map[hex]
    # print(binary)

    # if len(binary)!=48:
    #     raise ValueError(f"Total bit count: {len(binary)}. Incorrect! Must be 48.")
    # print(f"Total bit count: {len(binary)}")