<?php

if(preg_match('/Windows/', php_uname('s'), $matches)) {
    $exec = 'cd ../../&spark-submit test_spark.py';
} else {
    $exec = 'cd ../../;spark-submit test_spark.py';
}

exec($exec, $out_put);

foreach($out_put as $value)
{
    echo $value . "<br>";
}

echo 'done';
