

// as per https://aws.amazon.com/de/blogs/big-data/implement-serverless-log-analytics-using-amazon-kinesis-analytics/

// Lambda function to handle the aggregate results
public void recordHandler(KinesisEvent event) throws IOException {

  // Configure CloudWatch
  AWSCredentialsProvider provider = new EnvironmentVariableCredentialsProvider();
  cloudWatchClient = new AmazonCloudWatchClient(provider);

  // Initialize put request
  PutMetricDataRequest putMetricDataRequest = new PutMetricDataRequest();
  putMetricDataRequest.setNamespace(“namespace”);

  // Process event from stream
  for (KinesisEventRecord rec : event.getRecords()) {

      YourObject yourObject = YourObject.fromJsonAsBytes(rec.getKinesis().getData().array());

      MetricDatum metricDatum = new MetricDatum();
      metricDatum.setMetricName(yourObject.getApplicationName());metricDatum.setTimestamp(yourObject.getMetricTime());
      metricDatum.setUnit(StandardUnit.Count);
      metricDatum.setValue(yourObject.getValue());
      putMetricDataRequest.getMetricData().add(metricDatum);
  }

  // send to CloudWatch
  cloudWatchClient.putMetricData(putMetricDataReqeust);
}
