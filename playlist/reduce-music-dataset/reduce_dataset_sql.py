import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import IntegerType,BooleanType,DateType
from pyspark.sql import Row
from py4j.java_gateway import java_import # to rename the output file


music_schema = types.StructType([
    types.StructField('uuid', types.IntegerType()),
    types.StructField('artist_name', types.StringType()),
    types.StructField('track_name', types.StringType()),
    types.StructField('release_date', types.IntegerType()),
    types.StructField('genre', types.StringType()),
    types.StructField('lyrics', types.StringType()),
    types.StructField('topic', types.StringType()),
])


def main(music_file, output):
    # main logic starts here

    # Read air quality data file
    music = spark.read.csv(music_file, header=True, schema=music_schema)

    # ref: https://spark.apache.org/docs/2.2.0/sql-programming-guide.html
    # "Register the DataFrame as a SQL temporary view"
    music.createOrReplaceTempView("music")

    # Only select 100 rows from df
    music_reduced = spark.sql("SELECT * from music LIMIT 100 ")

    # drop rows with empty lat/long to avoid issues during data ingestion into Postgres
    music_reduced = music_reduced.na.drop("any")

    # write as a single csv file with header information
    music_reduced.coalesce(1).write.option("header",True).csv(output, mode='overwrite')

    # ref: https://stackoverflow.com/questions/40792434/spark-dataframe-save-in-single-file-on-hdfs-location?rq=1
    # rename the output filename from output/part-00000-* to output.csv (eg: CO_1980_2008_cleaned.csv)
    java_import(spark._jvm, 'org.apache.hadoop.fs.Path')
    fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(spark._jsc.hadoopConfiguration())
    file = fs.globStatus(sc._jvm.Path(output + '/part*'))[0].getPath().getName()
    fs.rename(sc._jvm.Path(output + '/' + file), sc._jvm.Path(output + '.csv'))
    fs.delete(sc._jvm.Path(output), True)

if __name__ == '__main__':
    music_file = sys.argv[1] # example: "tcc_ceds_music_with_id_less_cols.csv"
    output = sys.argv[2] # example: "music_100"

    spark = SparkSession.builder.appName('Reduce CSV to 100 rows - SQL').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main(music_file, output)
