<?php

if(!isset($_COOKIE['username'])) {
    echo 0;
    exit;
}
$unique_id = $_COOKIE['username'];

if(preg_match('/Windows/', php_uname('s'), $matches)) {
    $exec = 'cd ../../predict&spark-submit spark.py ' . $unique_id;
} else {
    $exec = 'cd ../../predict;spark-submit spark.py ' . $unique_id;
}
exec($exec, $out_put);

foreach($out_put as $value)
{
    echo $value . "<br>";
}

echo 'done';
