from scipy import optimize

from pyspark import SparkConf, SparkContext

from scipy import optimize


conf = SparkConf().setMaster('local[2]').setAppName('Finance_Predict(%s)' % str('test'))
sc = SparkContext(conf = conf)

a = sc.parallelize(range(100))

print a.count()
print a.collect()
