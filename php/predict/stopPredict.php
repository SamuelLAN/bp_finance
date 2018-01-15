<?php

if(!isset($_COOKIE['username'])) {
    echo 0;
    exit;
}
$unique_id = $_COOKIE['username'];

if(preg_match('/Windows/', php_uname('s'), $matches)) {
    $exec = 'cd ../../&python clear.py ' . $unique_id;
} else {
    $exec = 'cd ../../;python clear.py ' . $unique_id;
}
exec($exec, $out_put);

foreach($out_put as $value)
{
    $value = preg_replace('/ /', '&nbsp;', $value);
    echo $value . ';&nbsp;&nbsp;&nbsp;';
}
