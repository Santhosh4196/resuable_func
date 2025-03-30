'''def uniquenessPct(spark,df,cols):
    columns=""
    for i in cols:#(count(distinct id)/count(id))*100
        columns+='(count(distinct '+i+')/count('+i+'))*100 as '+i+','
    columns=columns[:-1]#removal of last ,
    df.createOrReplaceTempView("dfview")
    sql="select "+columns+" from dfview"
    print(sql)
    df_dist_cnt=spark.sql(sql)
    df_dist_cnt_lst=list(df_dist_cnt.rdd.flatMap(lambda x:x).collect())#convert the row object to list
    print(df_dist_cnt_lst)
    uniquenesspct=sum(df_dist_cnt_lst)/len(df_dist_cnt_lst)
    #print(f"overall uniqueness percent is {completionpct}")
    return uniquenesspct,df_dist_cnt_lst

def completenessPct(spark,df,cols):
    pct=[]
    for i in cols:
        actualcnt=df.select(i).count()
        notnullcnt=df.select(i).na.drop().count()
        #print(notnullcnt)
        completenesspctvalue=(notnullcnt/actualcnt)*100
        #print(completenesspctvalue)
        pct.append(completenesspctvalue)
        print(pct)
        completenesspct=sum(pct)/len(pct)
    #print(f"completeness percent is {completenesspct}")
    return completenesspct

def validateSchema(df1,df2):
    if (sorted(df1.columns) == sorted(df2.columns)):
        return "valid"
    else:
        return "invalid"


from pyspark.sql.types import *
from pyspark.sql import *
spark = SparkSession.builder\
       .appName("Very Important SQL End to End App") \
       .config("spark.jars","/home/hduser/install/mysql-connector-java.jar")\
       .enableHiveSupport()\
       .getOrCreate()
custstructtype1 = StructType([StructField("id", IntegerType(), False),
                                  StructField("custfname", StringType(), False),
                                  StructField("custlname", StringType(), True),
                                  StructField("custage", ShortType(), True),
                                  StructField("custprofession", StringType(), True)])
custdf_clean=spark.read.csv("file:///home/hduser/hive/data/custsmodified",mode='dropmalformed',schema=custstructtype1)

uniquepct,uniquepctcols=uniquenessPct(spark,custdf_clean,["id","custprofession"])
print(f"Unique percentage is {uniquepct}")
completepct=completenessPct(spark,custdf_clean,["id","custprofession"])
print(f"Completeness percent is {completepct}")
print(f"Schema is {validateSchema(custdf_clean,custdf_clean)}")

#store the expected count in a table as per the source system/files/table
#read the metadata table and take the expected count, threshold pct (+-10%)
#count of source data for today
#compare with the metadata count + threshold pct +-10%
#if deviates - source data deviates howmuch % or howmuch count
#store that info in an audit table
#visualize using some visualization tool'''