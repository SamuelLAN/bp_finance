var $date = $('#date_input'),
    $symbol = $('#symbol_input'),
    $canvas = document.getElementById('canvas');

// 返回请求的uri
function getApi(date, symbol) {
    return './getData.php?date=' + date + '&symbol=' + symbol;
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

        rtn_data.push([deal_time, price_percentage, deal_price])
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

var myChart = echarts.init($canvas);

$('#confirm').bind('click', function(){
    var date = $date.val(),
        symbol = $symbol.val(),
        uri = getApi(date, symbol);

    myChart.showLoading();
    $.getJSON(uri, function(json){
        if(json.length) {
            var data = transformData(json, date);

            myChart.hideLoading();
            myChart.setOption(option = {
                title: {
                    text: symbol + '  \'s  data  in  ' + date,
                    left: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        animation: false
                    },
                    formatter: function (params) {
                        return 'time: ' + params[0].name + '<br />price (%): ' + params[0].value;
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
        } else {
            myChart.hideLoading();
        }
    });
});
