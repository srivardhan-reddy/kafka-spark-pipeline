
import boto3
from json import loads
from kafka import KafkaConsumer
from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.sql.functions import col

from pyspark.ml.feature import VectorAssembler
import pandas as pd
import pickle

import warnings

warnings.filterwarnings("ignore", category=UserWarning)

print("Connecting to consumer ...")
consumer = KafkaConsumer(
    'air-quality',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

response_list = []
print("Start of kafka session")

try:
    while True:
        messages = consumer.poll(timeout_ms=10000)
        if not messages:
            print('No messages received, stopping consumer')
            break
        for message in messages.values():
            for msg in message:
                # process message
                response_list.append(msg.value)
except KeyboardInterrupt:
    print('Stopping consumer')
finally:
    consumer.close()

try:
    print("Start of spark session")
    sc = SparkContext.getOrCreate()
    spark = SparkSession(sc)

    list_rdd = sc.parallelize(response_list)
    list_df = spark.read.json(list_rdd)
    list_df.printSchema()

    list_df.show()

    # Choosing a subset of the RDD 
    final_list = list_df.select(col('sensor.`sensor_index`'),
               col('sensor.`latitude`'),
               col('sensor.`longitude`'),
               col('sensor.`pressure`'),             
               col('sensor.`pm2.5_atm_a`'),
               col('sensor.`pm2.5_atm_b`'),
               col('sensor.`humidity_a`'),
               col('sensor.`temperature_a`'),
               col('sensor.`location_type`'),
               col('sensor.`pm1.0_atm_a`'),
               col('sensor.`pm1.0_atm_b`'),
               col('sensor.`scattering_coefficient_a`'),
               col('sensor.`scattering_coefficient_b`')
              )
    final_list.show()
    cols = final_list.columns

    for col_ in cols:
        new_col_name = col_.replace(".", "_")
        final_list = final_list.withColumnRenamed(col_, new_col_name)

    final_list.show()
    print("Writing to CSV file named sensors.csv")
    final_list.coalesce(1).write.option("header", "true").csv("sensors")
    # final_list.coalesce(1).write.option("header", "true").csv("sensors")

    rdd = final_list.rdd

    # Convert the RDD to CSV format
    csv_data = rdd.map(lambda x: ",".join([str(i) for i in x]))

    # Write the CSV data to S3
    s3 = boto3.client("s3",
                    aws_access_key_id="AKIAQK3O6QTVU3YE5ZP5",
                    aws_secret_access_key="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")
    bucket_name = "geoaici"
    file_name = "srivardhan-test.csv"
    s3.put_object(Bucket=bucket_name, Key=file_name, Body='\n'.join(csv_data.collect()))


    # Load the pre-trained models from pickle files
    print("Loading the pre-trained Regression Models")
    with open('/Users/srivardhan/Desktop/Masters/Masters Project/Kafka Implementation/kafka-pipeline-examples/producer-consumer/models/lr_model.pkl', 'rb') as f:
        lr_model = pickle.load(f)
    
    with open('/Users/srivardhan/Desktop/Masters/Masters Project/Kafka Implementation/kafka-pipeline-examples/producer-consumer/models/rf_model.pkl', 'rb') as f:
        rf_model = pickle.load(f)

    
    # Prepare the input data for prediction
    features = ['latitude', 'longitude', 'pressure', 'pm2_5_atm_a', 'pm2_5_atm_b', 
                'humidity_a', 'temperature_a', 'location_type', 'pm1_0_atm_a',
                'pm1_0_atm_b', 'scattering_coefficient_a', 'scattering_coefficient_b']

    assembler = VectorAssembler(inputCols=features, outputCol="features", handleInvalid="skip")
    data = assembler.transform(final_list)

    # Select the target variable
    data = data.select(col('scattering_coefficient_b').alias('label'), 'features')
    # Make predictions using the pre-trained models
    data_list = data.collect()

    lr_predictions = []
    rf_predictions = []

    for row in data_list:
        data_trans = row.features.toArray().reshape(1, -1)
        lr_predictions.append(lr_model.predict(data_trans)[0])
        rf_predictions.append(rf_model.predict(data_trans)[0])

    # Print the predictions
    print("Linear Regression Predictions:")
    for pred in lr_predictions:
        print(pred)

    print("Random Forest Regression Predictions:")
    for pred in rf_predictions:
        print(pred)

    # Convert the predictions to a PySpark DataFrame
    lr_pred_df = spark.createDataFrame([(float(pred),) for pred in lr_predictions], ['prediction'])
    rf_pred_df = spark.createDataFrame([(float(pred),) for pred in rf_predictions], ['prediction'])

    # Print the predictions
    print("Linear Regression Predictions:")
    lr_pred_df.show()

    print("Random Forest Regression Predictions:")
    rf_pred_df.show()

    # stop the SparkSession
    spark.stop()

except Exception as e:
   print(f"Error : {e}")
   raise
print("End of spark session")