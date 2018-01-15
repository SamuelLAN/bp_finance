var $date = $('#date_input'),
    $symbol = $('#symbol_input'),
    $canvas = document.getElementById('canvas'),
    $context = $canvas.getContext('2d');

// 返回请求的uri
function getApi(date, symbol) {
    return './getData.php?date=' + date + '&symbol=' + symbol;
}

// 画点
function point(x, y) {
    $context.beginPath();
    $context.arc(x, y, 0.7, 0, 2*Math.PI);
    $context.fill();
}

// 画坐标轴
function generateAxis(axis_size) {
    $context.fillStyle = '#333333';
    $context.lineWidth = 1;

    var w = axis_size['w'],
        h = axis_size['h'],
        ml = axis_size['ml'],
        mr = axis_size['mr'],
        mt = axis_size['mt'],
        mb = axis_size['mb'];

    $context.beginPath();
    $context.moveTo(ml, mt);
    $context.lineTo(ml, mt + h);
    $context.stroke();

    $context.beginPath();
    $context.moveTo(ml, mt + h);
    $context.lineTo(ml + w, mt + h);
    $context.stroke();

    $context.beginPath();
    $context.moveTo(ml - 10, mt + 10);
    $context.lineTo(ml, mt);
    $context.lineTo(ml + 10, mt + 10);
    $context.stroke();

    $context.beginPath();
    $context.moveTo(ml + w - 10, mt + h - 10);
    $context.lineTo(ml + w, mt + h);
    $context.lineTo(ml + w - 10, mt + h + 10);
    $context.stroke();

    $context.beginPath();
    $context.arc(ml, mt + h, 2, 0, 2*Math.PI);
    $context.fill();
}

// 画点图
function spotChart(data, axis_size) {
    var w = axis_size['w'],
        h = axis_size['h'],
        ml = axis_size['ml'],
        mr = axis_size['mr'],
        mt = axis_size['mt'],
        mb = axis_size['mb'],
        y_high = data['highest_price'],
        y_low = data['lowest_price'],
        start_price = data['start_price'],
        end_price = data['end_price'],
        start_time = data['start_time'],
        end_time = data['end_time'],
        noon_time = data['noon_time'],
        chart_data = data['data'],
        data_len = chart_data.length;

    if(start_price > end_price) {   // 高开低走的情况
        y_low = y_high - (y_high - y_low) * 1.8;
    } else {                                        // 低开高走的情况
        y_high = y_low + (y_high - y_low) * 1.8;
    }

    var per_x = w / (end_time - start_time - 5400000),
        per_y = h / (y_high - y_low);

    $context.beginPath();
    for(var index in chart_data) {
        //if(index % 20 != 0 && index < data_len - 1) {
        //    continue;
        //}

        var timestamp = chart_data[index][0],
            deal_price = chart_data[index][2],
            x = timestamp >= noon_time ? ml + (timestamp - start_time - 5400000) * per_x : ml + (timestamp - start_time) * per_x,
            y = mt + h * 0.98 - (deal_price - y_low) * per_y;

        //point(x, y);

        if(index > 0) {
            $context.lineTo(x, y);
        } else {
            $context.moveTo(x, y);
        }
    }
    $context.stroke();
}

function transformData(data, date) {
    var rtn_data = [],
        _date = date.replace(/-/g, '/'),
        data_len = data.length,
        start_time = new Date(_date + ' ' + data[data_len - 1][0]).getTime(),
        end_time = new Date(_date + ' ' + data[0][0]).getTime(),
        noon_time = new Date(_date + ' 13:00:00').getTime(),
        start_price = data[data_len - 1][1],
        end_price = data[0][1],
        lowest_price = 9999,
        highest_price = 0;

    for(var index in data) {
        var line = data[index],
            deal_time = line[0],
            deal_price = line[1],
            timestamp = new Date(_date + ' ' + deal_time).getTime(),
            price_percentage = (deal_price - start_price) / start_price * 100;

        if(deal_price < lowest_price) {
            lowest_price = deal_price;
        }
        if(deal_price > highest_price) {
            highest_price = deal_price;
        }

        rtn_data.push([timestamp, price_percentage, deal_price])
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

var axis_size = {
        w : 700,
        h : 500,
        ml : 50,
        mr : 50,
        mt : 50,
        mb : 50
    };

generateAxis(axis_size);

$('#confirm').bind('click', function(){
   var date = $date.val(),
       symbol = $symbol.val(),
       uri = getApi(date, symbol);

    $.getJSON(uri, function(json){
        if(json.length) {
            var data = transformData(json, date);
            spotChart(data, axis_size);
        }
    });
});
