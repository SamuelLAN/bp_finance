<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2016/3/8
 * Time: 19:27
 */

?>

<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>Finance Chart</title>
    <link href="chart.css" type="text/css" rel="stylesheet">
</head>
<body>
<div id="canvas"></div>
<div id="command">
    <input id="date_input" class="input" placeholder="日期(如2016-03-07)" value="">
    <input id="symbol_input" class="input" placeholder="股票代号(如sh601988)" value="">
    <div id="confirm">Confirm</div>
</div>
<script type="text/javascript" src="jquery.min.js"></script>
<script type="text/javascript" src="echarts.common.min.js"></script>
<script type="text/javascript" src="index.js"></script>
</body>
</html>