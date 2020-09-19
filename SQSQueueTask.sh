



###################################################################
#     Test example to use SQS for queuing a large batch of tasks
#     Here, the task is to separate individual samples
#               from a very big VCF files
###################################################################
cd /home/mzabidi/temp/

#First, start an SQS queue at the Console
#Then, populate the SQS queue with sample names
#use the URL from the console
URL=https://sqs.ap-southeast-1.amazonaws.com/453984338776/BigGermlineSplit
for sample in $(awk 'NR>1' /people/mzabidi/tumor_project/data/germline_variants/pairs.txt | cut -f4 | sort | uniq | sed 's/_MN//'); do
  echo $sample
  aws sqs send-message \
  --queue-url $URL \
  --message-body $sample
done


#do in screens
screen -R split_by_SQS
SQS=$(mktemp)
URL=https://sqs.ap-southeast-1.amazonaws.com/453984338776/BigGermlineSplit
#poll queue to begin
aws sqs receive-message --queue-url $URL > $SQS

#keep splitting until the queue exhausts
while [ -s $SQS ]; do
  #parse message
  sample=$(cat $SQS | awk '$1=="\"Body\":"{print $2}' | sed 's/\"//g' | sed 's/,//')
  rhandle=$(cat $SQS | awk '$1=="\"ReceiptHandle\":"{print substr($2,2,length($2)-3)}')

  echo $sample $rhandle

  #split samples
  time /usr/lib/jvm/java-8-oracle/bin/java -jar /opt/software/GenomeAnalysisTK-3.8-0/GenomeAnalysisTK.jar \
  -T SelectVariants \
  -R /home/ubuntu/shared/ref/hg19/with_decoy_genome/hs37d5.fa \
  -V MyBrCa.recal_snps.recal_indels.vcf.gz \
  -sn $sample -o ${sample}.vcf.gz \
  2>log/${sample}.log

  #delete message
  aws sqs delete-message --queue-url $URL --receipt-handle $rhandle

  #poll next message
  aws sqs receive-message --queue-url $URL > $SQS

done



#check logs see if all has succeeded
ls log/*log | while read l; do
  echo $log $(grep "Done. ---" $l)
done
#all 559 are OK!







#######DONE
