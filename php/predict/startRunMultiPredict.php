<?php

if(!isset($_COOKIE['username']) || !isset($_GET['symbol'])) {
    echo 0;
    exit;
}
$unique_id = $_COOKIE['username'];
$symbol = $_GET['symbol'];
$symbol = preg_replace('/[^szh0-9]/', '', $symbol);

if(preg_match('/Windows/', php_uname('s'), $matches)) {
    $exec = 'cd ../../&python runMulti.py ' . $unique_id . ' ' . $symbol;
} else {
    $exec = 'cd ../../;python runMulti.py ' . $unique_id . ' ' . $symbol;
}
exec($exec, $out_put);

foreach($out_put as $value)
{
    echo $value . "<br>";
}
