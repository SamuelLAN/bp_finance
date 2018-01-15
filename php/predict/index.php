<?php

if(!isset($_COOKIE['username'])) {
    header('Location: ../login');
    exit;
}

?>
<html>
<head lang="zh-cn">
    <meta charset="UTF-8">
    <title>Finance Predict Result</title>
    <link href="index.css" type="text/css" rel="stylesheet">
</head>
<body>
    <div id="main">
        <div id="command" class="frame">
            <input id="symbol_input" class="input" type="text" placeholder="股票代号(如sh601988)" autocomplete="off" oninput="symbolOnInput()">
            <div id="confirm" class="btn">Confirm</div>
            <div id="real_time_data" class="btn on">实时数据</div>
            <div id="history_data" class="btn">历史数据</div>
            <div id="predict_data" class="btn">预测</div>
            <div id="log_out">Logout</div>
            <div id="auto_complete"></div>
        </div>
        <div id="info" class="right frame">
        </div>
        <div id="result" class="right frame hide">
            <div id="process_status">

            </div>
            <div id="spark_status" style="display: none">

            </div>
        </div>
        <div id="predict_result" class="right frame hide">
            <div class="label_frame">
                <div class="label_name">预测价格：</div>
                <div id="predict_price" class="label_value">13.110</div>
            </div>
            <div class="label_frame">
                <div class="label_name">涨跌幅：</div>
                <div id="predict_direction" class="label_value">1</div>
            </div>
        </div>
        <div id="content_control" class="right frame hide">
            <div id="best_accuracy" class="control_btn on">accuracy</div>
            <div id="best_diff" class="control_btn">diff</div>
            <div id="best_cost" class="control_btn">cost</div>
            <div id="best_validation_accuracy" class="control_btn">validation accuracy</div>
            <div id="best_relative_cost" class="control_btn">relative cost</div>
        </div>
        <div id="content" class="right frame">
            <div id="canvas"></div>
            <div id="training_content" class="different_set_content hide">

            </div>
            <div id="validation_content" class="different_set_content hide">

            </div>
            <div id="test_content" class="different_set_content hide">

            </div>
        </div>
    </div>

    <div id="real_time_data_template" style="display: none">
        <div class="label_frame">
            <div class="label_name">Name：</div>
            <div class="label_value">%name%</div>
        </div>
        <div class="label_frame">
            <div class="label_name">price：</div>
            <div class="label_value">%price%</div>
        </div>
        <div class="label_frame">
            <div class="label_name">昨日收盘价：</div>
            <div class="label_value">%last_end%</div>
        </div>
        <div class="label_frame">
            <div class="label_name">今日开盘价：</div>
            <div class="label_value">%open%</div>
        </div>
        <div class="label_frame">
            <div class="label_name">今日最高价：</div>
            <div class="label_value">%highest%</div>
        </div>
        <div class="label_frame">
            <div class="label_name">今日最低价：</div>
            <div class="label_value">%lowest%</div>
        </div>
        <div class="label_frame">
            <div class="label_name">成交量(手)：</div>
            <div class="label_value">%volume%</div>
        </div>
        <div class="label_frame">
            <div class="label_name">成交额(元)：</div>
            <div class="label_value">%turnover%</div>
        </div>
    </div>
    <div id="history_data_template" style="display: none">
        <div class="select_days">
            <div id="one_day" class="select_btn on">单天</div>
            <div id="more_days" class="select_btn">多天</div>
        </div>
        <input id="start_date" class="input" type="text" placeholder="日期(如2016-05-10)">
        <input id="end_date" class="input hide" type="text" placeholder="结束日期(如2016-05-10)">
    </div>
    <div id="predict_data_template" style="display: none">
        <div id="predict_mode">
            <div id="fast_predict" class="select_btn on">快速预测</div>
            <div id="random_param_predict" class="select_btn">随机参数预测</div>
        </div>
        <div id="predict_type">
            <div id="predict_tomorrow" class="predict_btn on">明天收盘价</div>
            <div id="predict_one_week" class="predict_btn">一周后收盘价</div>
            <div id="predict_one_month" class="predict_btn">一个月后收盘价</div>
            <div id="predict_trend" class="predict_btn">明天走势</div>
        </div>
        <div id="predict_control">
            <div id="start_predict" class="predict_btn_red">开始预测</div>
            <div id="end_predict" class="predict_btn_red">停止预测</div>
        </div>
    </div>

    <div id="content_result_template" style="display: none">
        <div class="content_label">
            <div class="content_label_name">Cost：</div>
            <div class="content_label_value">%cost%</div>
        </div>
        <div class="content_label">
            <div class="content_label_name">Accuracy：</div>
            <div class="content_label_value">%accuracy%</div>
        </div>
        <div class="content_label">
            <div class="content_label_name">Accuracy y == 1：</div>
            <div class="content_label_value">%accuracy_y%</div>
        </div>
        <div class="content_label">
            <div class="content_label_name">Diff：</div>
            <div class="content_label_value">%diff%</div>
        </div>
        <div class="content_label">
            <div class="content_label_name">relative cost：</div>
            <div class="content_label_value">%relative_cost%</div>
        </div>
        <div id="%canvas_id%" class="content_canvas"></div>
    </div>

    <script type="text/javascript" src="jquery.min.js"></script>
    <script type="text/javascript" src="echarts.common.min.js"></script>
    <script type="text/javascript" src="index.js"></script>
</body>
</html>
