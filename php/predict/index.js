var $right = $('.right'),
    $main = $('#main'),
    $command = $('#command'),
    $info = $('#info'),
    $content = $('#content'),
    $canvas = $('#canvas'),
    $window = $(window),
    $symbol_input = $('#symbol_input'),
    $auto_complete = $('#auto_complete'),
    $confirm = $('#confirm'),
    $result = $('#result'),
    $predict_result = $('#predict_result'),
    $predict_price = $('#predict_price'),
    $predict_direction = $('#predict_direction'),
    $content_control = $('#content_control'),
    $process_status = $('#process_status'),
    $spark_status = $('#spark_status'),
    $training_content = $('#training_content'),
    $validation_content = $('#validation_content'),
    $test_content = $('#test_content'),
    $log_out = $('#log_out'),
    $real_time_data_template = $('#real_time_data_template'),
    $history_data_template = $('#history_data_template'),
    $predict_data_template = $('#predict_data_template'),
    $content_result_template = $('#content_result_template');

var tmp_info = {
        'real_time_data': '',
        'history_data': $history_data_template.html(),
        'predict_data': $predict_data_template.html()
    },
    command_on = 'real_time_data';

var my_chart = echarts.init(document.getElementById('canvas')),
    training_chart = false,
    validation_chart = false,
    test_chart = false;

var best_accuracy = false,
    best_diff = false,
    best_cost = false,
    best_validation_accuracy = false,
    best_relative_cost = false;

//var unique_id = Math.random().toString(36).substr(2);

function resetContent() {
    var w = $content.width();
    if(command_on == 'predict_data') {
        //$canvas.css({'width': w + 'px', 'height': '600px'});
        $canvas.css({'width': parseInt(w * 0.49) + 'px', 'height': '480px'});
        $training_content.removeClass('hide');
        $validation_content.removeClass('hide');
        $test_content.removeClass('hide');

        if(training_chart) {
            training_chart = echarts.init(document.getElementById('training_canvas'));
            validation_chart = echarts.init(document.getElementById('validation_canvas'));
            test_chart = echarts.init(document.getElementById('test_canvas'));

            getPredictResult();
        } else {
            $training_content.html('');
            $validation_content.html('');
            $test_content.html('');
        }
    } else {
        $canvas.css({'width': w + 'px', 'height': '600px'});
        $training_content.addClass('hide');
        $validation_content.addClass('hide');
        $test_content.addClass('hide');
    }
    my_chart = echarts.init(document.getElementById('canvas'));
}

function fillTemplate(template, data) {
    for(var key in data) {
        template = template.replace('%' + key + '%', data[key] + '');
    }
    return template;
}

function getRealTimeData(symbol) {
    $.getJSON('getData2.php', {symbol: symbol}, function(json) {
        if(!json) {
            return;
        }

        var template = $real_time_data_template.html(),
            html = fillTemplate(template, json);
        tmp_info['real_time_data'] = html;
        if(command_on == 'real_time_data') {
            $info.html(html);
        }
    });
}

function transformData(data, date) {
    data.reverse();
    var rtn_data = [],
        _date = date.replace(/-/g, '/'),
        data_len = data.length,
        start_time = new Date(_date + ' ' + data[data_len - 1][0]).getTime(),
        end_time = new Date(_date + ' ' + data[0][0]).getTime(),
        noon_time = new Date(_date + ' 13:00:00').getTime(),
        start_price = data[0][1],
        end_price = data[data_len - 1][1],
        lowest_price = 9999,
        highest_price = 0;

    for(var index in data) {
        var line = data[index],
            deal_time = line[0],
            deal_price = line[1],
            price_percentage = (deal_price - start_price) / start_price * 100;

        if(deal_price < lowest_price) {
            lowest_price = deal_price;
        }
        if(deal_price > highest_price) {
            highest_price = deal_price;
        }

        rtn_data.push([deal_time, price_percentage, deal_price, line[3], line[4], line[5]])
    }

    return {
        'data': rtn_data,
        'lowest_price': lowest_price,
        'highest_price': highest_price,
        'start_price': start_price,
        'end_price': end_price,
        'start_time': start_time,
        'end_time': end_time,
        'noon_time': noon_time
    }
}

function getHistoryData(symbol, date) {
    my_chart.clear();
    my_chart.showLoading();
    $.getJSON('getData.php', {date: date, symbol: symbol}, function(json) {
        my_chart.hideLoading();
        if(!json) {
            return;
        }

        var data = transformData(json, date);
        my_chart.setOption(option = {
            title: {
                text: symbol + '  \'s  data  in  ' + date,
                left: 'center',
                top: '2%'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    animation: false
                },
                formatter: function (params) {
                    return '时间: ' + params[0].name + '<br>价格: ' + data['data'][params[0].dataIndex][2] + '<br>涨跌幅: ' + params[0].value + '%<br>成交量：' + data['data'][params[0].dataIndex][3] + '<br>成交额：' + data['data'][params[0].dataIndex][4] + '<br>交易性质：' + data['data'][params[0].dataIndex][5];
                }
            },
            grid: {
                left: '2%',
                right: '2%',
                bottom: '2%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: data['data'].map(function (item) {
                    return item[0];
                }),
                axisLabel: {
                    formatter: function (value, idx) {
                        return value;
                    }
                },
                splitNumber: 8,
                splitLine: {
                    show: false
                }
            },
            yAxis: {
                axisLabel: {
                    formatter: function (val, idx) {
                        return val + '%';
                    }
                },
                splitNumber: 10,
                splitLine: {
                    show: false
                }
            },
            dataZoom: [
                {
                    show: true,
                    realtime: true,
                    start: 0,
                    end: 100
                },
                {
                    type: 'inside',
                    show: true,
                    realtime: true,
                    start: 0,
                    end: 100
                }
            ],
            series: [{
                "name": "price",
                type: 'line',
                data: data['data'].map(function (item) {
                    return item[1];
                })
            }]
        });
    });
}

function training_curve(chart, original_data) {
    var data_len = original_data.length,
        data = [];
    for(var i = 1; i < data_len; i++) {
        data.push([i, original_data[i - 1]]);
    }

    chart.setOption(option = {
        title: {
            text: 'Training Curve',
            left: 'center',
            top : '2%'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                animation: false
            },
            formatter: function (params) {
                return 'Error: ' + params[0].value + '<br>iter_times: ' + params[0].name;
            }
        },
        grid: {
            left: '2%',
            right: '3%',
            bottom: '2%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: data.map(function (item) {
                return item[0];
            }),
            axisLabel: {
                formatter: function (value, idx) {
                    return value;
                }
            },
            splitNumber: 10,
            splitLine: {
                show: false
            },
            boundaryGap : false
        },
        yAxis: {
            type : 'value',
            name : 'Error'
        },
        dataZoom: [
            {
                show: true,
                realtime: true,
                start: 0,
                end: 100
            },
            {
                type: 'inside',
                show: true,
                realtime: true,
                start: 0,
                end: 100
            }
        ],
        series: [{
            "name": "Error",
            type: 'line',
            data: data.map(function (item) {
                return item[1];
            })
        }]
    });
}

function trend_curve(chart, data_set_name, original_data) {
    var data_len = original_data['y'].length,
        data = [];
    for(var i = 1; i <= data_len; i++) {
        data.push([i, original_data['pred'][i - 1][0], original_data['y'][i - 1][0]]);
    }

    chart.setOption(option = {
        title: {
            text: data_set_name + ' set Predict Price Curve',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                animation: false
            },
            formatter: function (params) {
                return 'time: ' + params[0].name + '<br>predict: ' + params[0].value + '<br>y: ' + params[1].value;
            }
        },
        grid: {
            left: '2%',
            right: '3%',
            bottom: '2%',
            containLabel: true
        },
        legend: {
            data:['predict', 'y'],
            top: '10%',
            right: '2%'
        },
        xAxis: {
            name: 'time',
            type: 'category',
            data: data.map(function (item) {
                return item[0];
            }),
            axisLabel: {
                formatter: function (value, idx) {
                    return value;
                }
            },
            splitNumber: 8,
            splitLine: {
                show: false
            },
            boundaryGap : false
        },
        yAxis: {
            type : 'value',
            name : 'price'
        },
        dataZoom: [
            {
                show: true,
                realtime: true,
                start: 0,
                end: 100
            },
            {
                type: 'inside',
                show: true,
                realtime: true,
                start: 0,
                end: 100
            }
        ],
        series: [{
            "name": "predict",
            type: 'line',
            data: data.map(function (item) {
                return item[1];
            })
        },  {
            "name": "y",
            type: 'line',
            data: data.map(function (item) {
                return item[2];
            })
        }]
    });
}

function price_curve(chart, data_set_name, original_data) {
    var data_len = original_data['y'].length,
        data = [];
    for(var i = 1; i <= data_len; i++) {
        data.push([i, original_data['pred'][i - 1][0], original_data['y'][i - 1][0], original_data['open'][i - 1][0]]);
    }

    chart.setOption(option = {
        title: {
            text: data_set_name + ' set Predict Price Curve',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                animation: false
            },
            formatter: function (params) {
                return 'day: ' + params[0].name + '<br>predict: ' + params[0].value + '<br>y: ' + params[1].value + '<br>open: ' + params[2].value;
            }
        },
        grid: {
            left: '2%',
            right: '3%',
            bottom: '2%',
            containLabel: true
        },
        legend: {
            data:['predict', 'y', 'open'],
            top: '10%',
            right: '2%'
        },
        xAxis: {
            name: 'days',
            type: 'category',
            data: data.map(function (item) {
                return item[0];
            }),
            axisLabel: {
                formatter: function (value, idx) {
                    return value;
                }
            },
            splitNumber: 8,
            splitLine: {
                show: false
            },
            boundaryGap : false
        },
        yAxis: {
            type : 'value',
            name : 'price'
        },
        dataZoom: [
            {
                show: true,
                realtime: true,
                start: 0,
                end: 100
            },
            {
                type: 'inside',
                show: true,
                realtime: true,
                start: 0,
                end: 100
            }
        ],
        series: [{
            "name": "predict",
            type: 'line',
            data: data.map(function (item) {
                return item[1];
            })
        },  {
            "name": "y",
            type: 'line',
            data: data.map(function (item) {
                return item[2];
            })
        },  {
            "name": "open",
            type: 'line',
            data: data.map(function (item) {
                return item[3];
            })
        }]
    });
}

$window.resize(function() {
    var w = $main.width() - $command.width() - 40;
    $right.css('width', w + 'px');
    resetContent()
}).trigger('resize');

$command.on('click', '.btn', function() {
    var index = $(this).prevAll('.btn').length;
    if(index == 0 || $(this).hasClass('on')) {
        return;
    }

    $command.find('.btn').removeClass('on');
    $(this).addClass('on');

    var id = $(this).attr('id');
    tmp_info[command_on] = $info.html();
    command_on = id;
    $info.html(tmp_info[id]);

    resetContent();

    if(id == 'predict_data') {
        $result.show();
        if($info.find('#random_param_predict').hasClass('on')) {
            $content_control.show();
        } else {
            $content_control.hide();
        }
    } else {
        $result.hide();
        $predict_result.hide();
        $content_control.hide();
    }
});

$confirm.bind('click', function() {
    var symbol = $symbol_input.val();
    if(symbol) {
        if(command_on == 'real_time_data') {
            getRealTimeData(symbol);
        } else if(command_on == 'history_data') {
            var start_date = $info.find('#start_date').val(),
                end_data = $info.find('#end_date').val();
            if(!start_date) {
                return;
            }
            if($info.find('#one_day').hasClass('on')) {
                getHistoryData(symbol, start_date);
            } else {

            }
        } else {

        }
    }
});

function flushContent(json) {
    var training_record = json['training_record'],
        test_record = json['test_record'],
        original_data = json['original_data'],
        pred = parseInt(json['pred'] * 1000) / 1000,
        test_last = original_data['Test']['y'][original_data['Test']['y'].length - 1][0],
        pred_direction = (parseInt((pred - test_last) / test_last * 100 * 1000) / 1000) +'%';

    test_record['Training']['canvas_id'] = 'training_canvas';
    test_record['Validation']['canvas_id'] = 'validation_canvas';
    test_record['Test']['canvas_id'] = 'test_canvas';

    $predict_price.html(pred);
    $predict_direction.html(pred_direction);
    $predict_result.show();

    $training_content.html(fillTemplate($content_result_template.html(), test_record['Training']));
    $validation_content.html(fillTemplate($content_result_template.html(), test_record['Validation']));
    $test_content.html(fillTemplate($content_result_template.html(), test_record['Test']));

    training_chart = echarts.init(document.getElementById('training_canvas'));
    validation_chart = echarts.init(document.getElementById('validation_canvas'));
    test_chart = echarts.init(document.getElementById('test_canvas'));

    price_curve(training_chart, 'Training', original_data['Training']);
    price_curve(validation_chart, 'Validation', original_data['Validation']);
    price_curve(test_chart, 'Test', original_data['Test']);

    training_curve(my_chart, training_record);
}

function getPredictResult() {
    $.getJSON('getPredictResult.php', {}, function(json) {
        if(!json) {
            return;
        }

        flushContent(json);
    });
}

function getSparkPredictResult() {
    $.getJSON('getSparkResult.php', {}, function(json) {
        if(!json) {
            return;
        }

        best_accuracy = JSON.parse(json['best_accuracy']);
        best_diff = JSON.parse(json['best_diff']);
        best_cost = JSON.parse(json['best_cost']);
        best_validation_accuracy = JSON.parse(json['best_validation_accuracy']);
        best_relative_cost = JSON.parse(json['best_relative_cost']);

        if($content_control.find('#best_accuracy').hasClass('on')) {
            flushContent(best_accuracy);
        } else if($content_control.find('#best_diff').hasClass('on')) {
            flushContent(best_diff);
        } else if($content_control.find('#best_cost').hasClass('on')) {
            flushContent(best_cost);
        } else if($content_control.find('#best_validation_accuracy').hasClass('on')) {
            flushContent(best_validation_accuracy);
        }  else {
            flushContent(best_relative_cost);
        }
    });
}

function getPredictStatus(stopable) {
    if(typeof(timer) != 'undefined') {
        clearInterval(timer);
    }
    timer = setInterval(function() {
        $.get('getPredictStatus.php', {}, function(rtn_content) {
            if(!rtn_content) {
                return;
            }

            $process_status.html(rtn_content);
            if(rtn_content == 'done' && typeof(timer) != 'undefined' && stopable) {
                clearInterval(timer);
                getPredictResult();
                $info.find('#start_predict').removeClass('on');
            }
        });
    }, 1000);
}

function getSparkPredictStatus() {
    $spark_status.html('');
    $spark_status.show();
    if(typeof(spark_timer) != 'undefined') {
        clearInterval(spark_timer);
    }
    spark_timer = setInterval(function() {
        $.getJSON('getSparkStatus.php', {}, function(json) {
            if(!json) {
                return;
            }

            var finish = parseInt(json['finish']),
                all = parseInt(json['all']),
                text = '';

            if(finish >= all && json['last'] == 'done') {
                if(typeof(timer) != 'undefined') {
                    clearInterval(timer);
                }
                if(typeof(spark_timer) != 'undefined') {
                    clearInterval(spark_timer);
                    getSparkPredictResult();
                    $info.find('#start_predict').removeClass('on');
                }
                $spark_status.hide();
                $process_status.html('done');
            } else {
                text = 'finish ' + finish + ' | ' + all;
                $spark_status.html(text);
            }
        });
    }, 5000);
}

$info.on('click', '.select_btn', function() {
    if($(this).hasClass('on')) {
        return;
    }
    $info.find('.select_btn').removeClass('on');
    $(this).addClass('on');

    if(command_on == 'history_data') {
        if($(this).attr('id') == 'one_day') {
            $('#end_date').addClass('hide');
        } else {
            $('#end_date').removeClass('hide');
        }
    } else if(command_on == 'predict_data') {
        if($(this).attr('id') == 'random_param_predict') {
            $content_control.show();
        } else {
            $content_control.hide();
        }
    }
}).on('click', '.predict_btn', function() {
    if($(this).hasClass('on')) {
        return;
    }
    $info.find('.predict_btn').removeClass('on');
    $(this).addClass('on');
}).on('click', '#start_predict', function() {
    var symbol_input = $symbol_input.val();
    if($(this).hasClass('on') || !symbol_input) {
        return;
    }
    $info.find('#end_predict').removeClass('on');
    //$(this).addClass('on');
    $process_status.html('');

    if($info.find('#predict_tomorrow').hasClass('on') && $info.find('#fast_predict').hasClass('on')) {
        $(this).addClass('on');
        $.get('startPredict.php', {symbol: symbol_input}, function() {});
        getPredictStatus(true);
    } else if($info.find('#predict_tomorrow').hasClass('on') && $info.find('#random_param_predict').hasClass('on')) {
        $(this).addClass('on');
        $.get('startRunMultiPredict.php', {symbol: symbol_input}, function() {

        });
        getPredictStatus(false);
        getSparkPredictStatus();
    }
}).on('click', '#end_predict', function() {
    if($(this).hasClass('on')) {
        return;
    }
    $info.find('#start_predict').removeClass('on');
    $(this).addClass('on');
    $process_status.html('');

    $.get('stopPredict.php', {}, function(rtn_content) {
        $info.find('#end_predict').removeClass('on');
        if(typeof(timer) != 'undefined') {
            clearInterval(timer);
        }
        if(typeof(spark_timer) != 'undefined') {
            clearInterval(spark_timer);
        }
        if(!rtn_content) {
            return;
        }
        $process_status.html(rtn_content);
    });
});

$content_control.on('click', '.control_btn', function() {
    if($(this).hasClass('on')) {
        return;
    }
    $content_control.find('.control_btn').removeClass('on');
    $(this).addClass('on');

    if(best_accuracy) {
        var id = $(this).attr('id');
        if(id == 'best_accuracy') {
            flushContent(best_accuracy);
        } else if(id == 'best_diff') {
            flushContent(best_diff);
        } else if(id == 'best_cost') {
            flushContent(best_cost);
        } else if(id == 'best_validation_accuracy') {
            flushContent(best_validation_accuracy);
        }  else {
            flushContent(best_relative_cost);
        }
    }
});

$log_out.bind('click', function() {
    $.get('../login/logout.php', {}, function() {
        location.href = '../login';
    });
});

$auto_complete.on('click', '.symbol', function() {
    var index = $(this).prevAll('.symbol').length;
    $symbol_input.val($auto_complete.find('.symbol').eq(index).html());
    $auto_complete.hide();
});

function symbolOnInput() {
    var symbol_input = $symbol_input.val();

    $.getJSON('selectSymbol.php', {symbol: symbol_input}, function(json) {
        if(!json) {
            return;
        }

        var symbol_list = json['symbol'],
            html = '';
        for(var i in symbol_list) {
            html += '<div class="symbol">' + symbol_list[i] + '</div>';
        }
        $auto_complete.html(html);
        if($auto_complete.css('display') == 'none') {
            $auto_complete.show();
        }
    });
}

