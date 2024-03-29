function getTime(ts) {
    var myDate = ts.split("-");
    var newDate = new Date( myDate[0], myDate[1] - 1, myDate[2]);
    return newDate.getTime();
}

function generateChart(id,all_dates) {
  var options = {
    series: all_dates,
    chart: {
    type: 'area',
    stacked: false,
    height: 350,
    zoom: {
      type: 'x',
      enabled: true,
      autoScaleYaxis: true
    },
    toolbar: {
      autoSelected: 'zoom'
    }
  },
  dataLabels: {
    enabled: false
  },
  markers: {
    size: 0,
  },
  title: {
    text: 'Stock Price',
    align: 'left'
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      inverseColors: false,
      opacityFrom: 0.5,
      opacityTo: 0,
      stops: [0, 90, 100]
    },
  },
  yaxis: {
    labels: {
      formatter: function (val) {
        return val;
      },
    },
    title: {
      text: 'Price'
    },
  },
  xaxis: {
    type: 'datetime',
  },
  tooltip: {
    shared: false,
    y: {
      formatter: function (val) {
        return val
      }
    }
  }
  };
  document.querySelector("#"+id).innerHTML = "";
  var chart = new ApexCharts(document.querySelector("#"+id), options);
  chart.render();
}

function createChartJK(dataAll, id, isMultiple=false, type=false) {
  if (type == "portfolio") {
    var all_dates = [];
    var dates = [];
    var dates2 = [];
    for (var i=0;i<dataAll.length;i++) {
      var ts2 = dataAll[i].date;
      ts2 = getTime(ts2);
      var innerArr = [ts2, dataAll[i].returns];
      var innerArr2 = [ts2, dataAll[i].invested];
      dates.push(innerArr);
      dates2.push(innerArr2);
    }
    all_dates.push({
      name: key,
      data: dates
    });
    all_dates.push({
      name: key,
      data: dates2
    });
    generateChart(id, all_dates);
    return;
  }
  var dataSeries;
  if (dataAll.data == undefined) {
    dataSeries = dataAll;
  } else {
    dataSeries = dataAll.data;
  }
  if (isMultiple) {
    var all_dates = [];
    for (var key in dataSeries) {
      var value = dataSeries[key];
      var dates = [];
      for (var i = value.length-1; i>=0; i--) {
        
        ts2 = value[i].date;
        ts2 = getTime(ts2);
        var innerArr = [ts2, value[i].close];
        dates.push(innerArr);
      }
      all_dates.push({
        name: key,
        data: dates
      });
    }
  } else {
    var companyDetails = dataAll.companyDetails;
    var dataSeries = dataAll.data;
    var ts2 = 1484418600000;
    var dates = [];
    var spikes = [5, -5, 3, -3, 8, -8];
    var all_dates = [];
    for (var i = dataSeries.length-1; i>=0; i--) {
      ts2 = dataSeries[i].date;
      ts2 = getTime(ts2);
      var innerArr = [ts2, dataSeries[i].close];
      dates.push(innerArr)
    }
    all_dates.push({
      name: companyDetails ? companyDetails.name : "Company Chart",
      data: dates
    });
  }
  generateChart(id, all_dates);
}

function createCandleSticksChart(dataSeries, id) {
  var companyDetails = dataSeries.companyDetails;
  var dataSeries = dataSeries.data;
  var ts2 = 1484418600000;
  var dates = [];
  var spikes = [5, -5, 3, -3, 8, -8];
  var lineData = [];
  var candleData = [];
  for (var i = dataSeries.length-1; i>=0; i--) {
    ts2 = dataSeries[i].date;
    ts2 = getTime(ts2);
    var lineOb = {
        x: new Date(ts2),
        y: dataSeries[i].close
    }
    var innerArr = {
        x: new Date(ts2),
        y: [dataSeries[i].open, dataSeries[i].high, dataSeries[i].low, dataSeries[i].close]
    }
    lineData.push(lineOb);
    candleData.push(innerArr);
  }
    var options = {
        series: [{
        name: 'line',
        type: 'line',
        data: lineData
      }, {
        name: 'candle',
        type: 'candlestick',
        data: candleData
      }],
        chart: {
        height: 350,
        type: 'line',
      },
      title: {
        text: 'CandleStick Chart',
        align: 'left'
      },
      stroke: {
        width: [3, 1]
      },
      tooltip: {
        shared: true,
        custom: [function({seriesIndex, dataPointIndex, w}) {
          return w.globals.series[seriesIndex][dataPointIndex]
        }, function({ seriesIndex, dataPointIndex, w }) {
          var o = w.globals.seriesCandleO[seriesIndex][dataPointIndex]
          var h = w.globals.seriesCandleH[seriesIndex][dataPointIndex]
          var l = w.globals.seriesCandleL[seriesIndex][dataPointIndex]
          var c = w.globals.seriesCandleC[seriesIndex][dataPointIndex]
          return (
            '<div class="apexcharts-tooltip-candlestick">' +
            '<div>Open: <span class="value">' +
            o +
            '</span></div>' +
            '<div>High: <span class="value">' +
            h +
            '</span></div>' +
            '<div>Low: <span class="value">' +
            l +
            '</span></div>' +
            '<div>Close: <span class="value">' +
            c +
            '</span></div>' +
            '</div>'
          )
        }]
      },
      xaxis: {
        type: 'datetime'
      }
      };
      document.querySelector("#"+id).innerHTML = "";
      var chart = new ApexCharts(document.querySelector("#"+id), options);
      chart.render();
}

function chartDataFunction(id, companyValue=false, range=false, type=false, isSingle=true) {
    if (!range) {
        range = 50;
      }
      if (window.type) {
        type = window.type;
      }
      let data_url = "http://0.0.0.0:8000/show_data?code=500570&range="+range;
        if (companyValue) {
            data_url = "http://0.0.0.0:8000/show_data?code="+companyValue+"&range="+range;
        }
        if (!isSingle) {
          data_url = "http://0.0.0.0:8000/show_data?code="+companyValue+"&is_single=0&range="+range;
        }
        $.ajax({url: data_url, success: function(result){
          if (!isSingle) {
            createChartJK(result, id, true);
          } else if (!type || type == 'line') {
            createChartJK(result, id);
          } else {
            createCandleSticksChart(result, id);
          }
        }});
}

