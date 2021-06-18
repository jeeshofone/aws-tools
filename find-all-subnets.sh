#!/bin/bash

touch all-subnets.csv
echo "region","CIDR","VPCID" > all-subnets.csv
mkdir regions

IFS=$'\n' regionlist=$(aws ec2 describe-regions --query Regions[*].[RegionName] --output text)

for region in $regionlist
do
     echo -e "\nListing all subnets in region:'$region'"
     aws ec2 describe-subnets --region $region --query "Subnets[*]" --output json > regions/$region-subnets.json
     jq -r '.[] | [.AvailabilityZone, .CidrBlock, .VpcId] | @csv' regions/$region-subnets.json  > regions/$region-subnets.csv
     cat regions/$region-subnets.csv >> all-subnets.csv

done

bin/python overlapper.py