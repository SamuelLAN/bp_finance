<?php

if(!isset($_COOKIE['username'])) {
    echo 0;
    exit;
}
$unique_id = $_COOKIE['username'];

$path = '../../tmp/' . $unique_id . '/status.tmp';

$content = @file_get_contents($path);
echo preg_replace('/ /', '&nbsp;', $content);
