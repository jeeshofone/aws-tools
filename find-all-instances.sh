#!/bin/bash
IFS=$'\n' regionlist=$(aws ec2 describe-regions --query Regions[*].[RegionName] --output text)

for region in $regionlist
do
     echo $region
     aws ec2 describe-instances --region $region
    
done
