import ipaddress
import pandas

# import csv with list of all CIDR ranges and VPC-ID's
##################
# Sample Schema below
# region,CIDR,VPCID
# "eu-north-1b","172.31.32.0/20","vpc-12345678"
##################

dfsource = pandas.read_csv('all-subnets.csv')
dfoverlap = pandas.DataFrame(columns =['OVERLAPS'])
dfoverlap['OVERLAPS'].astype('object')

for CIDR, VPCID, index in zip(dfsource['CIDR'], dfsource['VPCID'], dfsource.index):
    blockaOverlap = []
    blocka = ipaddress.ip_network(CIDR)
    blockaVPCID = VPCID
    for CIDR, VPCID, index in zip(dfsource['CIDR'], dfsource['VPCID'], dfsource.index):
        print('comparing', blockaVPCID, 'with', VPCID, blocka, ipaddress.ip_network(CIDR))
        if VPCID == blockaVPCID:
            print('same vpc - do not check')
            continue
        elif blocka.overlaps(ipaddress.ip_network(CIDR)):
            print(blocka, 'matches', ipaddress.ip_network(CIDR))
            blockaOverlap.append(VPCID)
        else:
            print(blocka, 'does not match', ipaddress.ip_network(CIDR))
        dfoverlap.at[index, 'OVERLAPS'] = blockaOverlap


result = pandas.concat([dfsource, dfoverlap], axis=1)

print(result)
result.to_csv(r'result.csv')