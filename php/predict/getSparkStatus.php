<?php

if(!isset($_COOKIE['username'])) {
    echo 0;
    exit;
}
$unique_id = $_COOKIE['username'];

$path = '../../tmp/' . $unique_id . '/sparkStatus.tmp';

$content = @file_get_contents($path);
$content = preg_split("/\n/", $content);

$count = count($content);
$all = (int)$content[0];
$json = array(
    'finish' => $count,
    'all' => $all,
    'last' => $content[$count - 1],
);

echo json_encode($json);
