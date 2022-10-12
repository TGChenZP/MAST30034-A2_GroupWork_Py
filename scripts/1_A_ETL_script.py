from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, FloatType
import collections
import re
import pandas as pd

# Running spark
print("RUNNING PYSPARK\n\n")
spark = (
    SparkSession.builder.appName("preprocessing of taxi data")
    .config("spark.sql.repl.eagerEval.enabled", True) 
    .config("spark.sql.parquet.cacheMetadata", "true")
    .config("spark.sql.session.timeZone", "Etc/UTC")
    .config("spark.driver.memory", "15g")
    .getOrCreate()
)
print("\n\nSUCCESSFUL RUN PYSPARK\n")

# five tries for entering correct file name
tries = 6
while(tries):
    try:
        #transactions_20210828_20220227_snapshot
        #transactions_20210228_20210827_snapshot
        file_to_read = str(input("ENTER TRANSACTION FILE NAME TO ETL: "))
        transaction_sdf = spark.read.parquet("../data/tables/" + file_to_read)
    except:
        print("FILENAME ERROR, FILE NOT READ")
        print("TRYA AGAIN")
        tries -= 1
        print(str(tries) + " MORE TRIES")
        if not tries:
            print("FAILED, RERUN SCRIPT")
            break
    else:
        print("FILE READ OK\n\n")
        break

print("READING IN NECCESARY FILE, CONSUMER, MERCHANT, CONSUMER_DETAIL DATAS\n\n")
try:
    merchant_sdf = spark.read.parquet("../data/tables/tbl_merchants.parquet")
    merchant_sdf = merchant_sdf.withColumnRenamed("name", "merchant_name")
    consumer_detail_sdf = spark.read.parquet("../data/tables/consumer_user_details.parquet")
    consumer_sdf = spark.read.option("header",True) \
                            .option("inferSchema",True) \
                            .options(delimiter='|') \
                            .csv("../data/tables/tbl_consumer.csv")
    consumer_sdf = consumer_sdf.withColumnRenamed("name", "consumer_name")
except:
    print("READIN FAIL, ENSURE DATA IN data/tables PATH\n\n")
    exit()
else:
    print("READIN OKAY\n\n")

print("PROCESSING MERCHANT DATA, FOR CLEAN FORMAT\n\n")

split_col = F.split(merchant_sdf['tags'], '\]|\)', 3)
merchant_sdf = merchant_sdf.withColumn('prod_desc', split_col.getItem(0))
merchant_sdf = merchant_sdf.withColumn('revenue_level', split_col.getItem(1))
merchant_sdf = merchant_sdf.withColumn('take_rate', split_col.getItem(2))

@F.udf(returnType=StringType())
def clean_str(str):
    """ cleans string after extractions from TAGS columns

    Args:
        str (str): 

    Returns:
        str: lowercase, with no leading or trailing parenthesis 
    """
    str = str.lstrip(' ,([')
    str = str.rstrip(')]')
    str = str.lower()
    return str

# cleaning merchant and take rate and revenune level.
merchant_sdf = merchant_sdf.withColumn('prod_desc', clean_str(F.col('prod_desc')))
# removing extra spaces
merchant_sdf = merchant_sdf.withColumn("prod_desc", F.regexp_replace("prod_desc", r' +', ' '))

merchant_sdf = merchant_sdf.withColumn('take_rate', clean_str(F.col('take_rate')))
merchant_sdf = merchant_sdf.withColumn('revenue_level', clean_str(F.col('revenue_level')))
# extracting take rate and changing it to double.

merchant_sdf = merchant_sdf.withColumn('take_rate', F.regexp_extract('take_rate', '\\d*\\.\\d', 0))
merchant_sdf = merchant_sdf.withColumn('take_rate', F.col('take_rate').cast('double'))
merchant_sdf = merchant_sdf.drop("tags")


print("FINISH MERCHANT PROCESS\n\n")

print("JOINING REQUIRE DATA\n\n")

join_sdf = transaction_sdf.join(merchant_sdf, 
                                transaction_sdf.merchant_abn == merchant_sdf.merchant_abn,
                                "left"
                               ) \
                            .drop(merchant_sdf.merchant_abn)
consumer_sdf = consumer_sdf.join(consumer_detail_sdf, 
                                 consumer_sdf.consumer_id == consumer_detail_sdf.consumer_id,
                                 "left"
                                ) \
                            .drop(consumer_detail_sdf.consumer_id)
join_sdf = join_sdf.join(consumer_sdf, 
                         join_sdf.user_id == consumer_sdf.user_id, 
                         "left"
                        ) \
                    .drop(consumer_sdf.user_id)
print("DATA JOIN OK\n\n")

join_sdf.show()

COLUMNS = []
for col in join_sdf.columns:
    if "datetime" not in col:
        COLUMNS.append(col)

print("CHECK NULL VALs \n\n")

join_missing = join_sdf.select([F.count(F.when(F.col(c).contains('None') | \
                                                       F.col(c).contains('NULL') | \
                                                      (F.col(c) == '' ) | \
                                                       F.col(c).isNull() | \
                                                       F.isnan(c), c 
                                                      )).alias(c)
                                                       for c in COLUMNS])
join_missing.show()

flag = str(input("SAVE FILES? ENTER YES OR NO: "))

# code to save file
if flag == "YES":
    print("FILE WILL BE SAVE IN data/tables/curated")
    nametosave = file_to_read + "_all_details"
    join_sdf.write.mode('overwrite').parquet('../data/curated/' + file_to_read + "_all_details")
    missing_count_save_name = nametosave + "_missing_counts"
    print("MISSING VALUE COUNTS WILL BE SAVE AS " + missing_count_save_name)
    join_missing.write.mode('overwrite').parquet('../data/curated/' + missing_count_save_name)