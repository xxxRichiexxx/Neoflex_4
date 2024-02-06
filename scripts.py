from pyspark.sql import SparkSession


def get_my_disciplines(spark):
    """Возвращает датафрейм моих дисциплин"""
    data = [
        (1,"volleyball", "summer"),
        (2,"football", "summer"),
        (3,"basketball", "summer"),
        (4,"handball", "summer"),
        (5,"Cycling Road", "summer"),
        (6,"volleyball", "winter"),
        (7,"football", "winter"),
        (8,"basketball", "winter"),
        (9,"handball", "winter"),
        (10,"Cycling Road", "winter"),
    ]
    columns = ['Row_id', 'Discipline', 'Season']
    disciplines = spark.createDataFrame(data=data, schema=columns)
    disciplines.write.format('csv') \
            .option("header", True)\
            .option('sep', '\t')\
            .mode("overwrite")\
            .save("/data/disciplines")
    return disciplines

def get_disciplines_with_cnt(spark):
    """Возвращает датафрейм дисциплин c количеством атлетов"""
    athletes = spark.read.csv(
    	path = "/data/Athletes.csv",
    	sep=";",
    	inferSchema=True,
    	header=True,
    )
    result = athletes.groupby('Discipline').count()
    result.write.format('parquet') \
           .option("header", True)\
           .mode("overwrite")\
           .save("/data/disciplines_with_cnt")
    return result

def get_my_disciplines_with_cnt(spark, df1, df2):
    """Количество участников, только по тем дисциплинам, что есть в
       моем сгенерированном DataFrame"""
    result = df1.join(df2, ['Discipline'], how='left') \
                .select('Discipline', 'count')
    result.write.format('parquet') \
                 .option("header", True)\
                 .mode("overwrite")\
                 .save("/data/result")
    return result


if __name__ == '__main__':
    spark = SparkSession.builder \
                        .master("local") \
                        .appName("task2.1") \
                        .getOrCreate()
    
    df1 = get_my_disciplines(spark)
    df1.show()
    df2 = get_disciplines_with_cnt(spark)
    df2.show()
    
    result = get_my_disciplines_with_cnt(spark, df1, df2)
    result.show()
