<?php

echo 'start<br>';

exec('python test.py', $out_put);

var_dump($out_put);

echo '<br>done ' . time();
