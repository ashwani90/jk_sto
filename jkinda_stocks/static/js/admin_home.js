function addData(chart, label, newData) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(newData);
    });
    chart.update();
}

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}

const chartFunction = function(chart_container, companyValue=false,aChart=false){
    let data_url = "http://0.0.0.0:8000/show_data?code=500570";
    if (companyValue) {
        data_url = "http://0.0.0.0:8000/show_data?code="+companyValue;
    }
    $.ajax({url: data_url, success: function(result){
        xValues = [];
        yValues = [];
        if (aChart) {
            aChart.destroy();
        }
        if (result.data.length == 0) {
            aChart = new Chart(chart_container, {});
            return;
        }
        for (let i=0;i<result.data.length;i++) {
            xValues.push(result.data[i].date);
            yValues.push(result.data[i].close);
            
        }
        xValues = xValues.reverse();
        yValues = yValues.reverse();
        if (aChart) {
            removeData(aChart);
            addData(aChart, xValues, yValues);
        } else {
            aChart = new Chart(chart_container, {
                type: "line",
                data: {
                  labels: xValues,
                  datasets: [{
                    backgroundColor:"transparent",
                    borderColor: "rgba(0,0,0,1)",
                    data: yValues
                  }]
                },
                options:{
                    maintainAspectRatio: false,
                    layout: {
                      padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                      }
                    },
                    scales: {
                      xAxes: [{
                        time: {
                          unit: 'date'
                        },
                        gridLines: {
                          display: false,
                          drawBorder: false
                        },
                        ticks: {
                          maxTicksLimit: 7
                        }
                      }],
                      yAxes: [{
                        ticks: {
                          maxTicksLimit: 5,
                          padding: 10,
                          // Include a dollar sign in the ticks
                          callback: function(value, index, values) {
                            return number_format(value);
                          }
                        },
                        gridLines: {
                          color: "rgb(234, 236, 244)",
                          zeroLineColor: "rgb(234, 236, 244)",
                          drawBorder: false,
                          borderDash: [2],
                          zeroLineBorderDash: [2]
                        }
                      }],
                    },
                    legend: {
                      display: false
                    },
                    tooltips: {
                      backgroundColor: "rgb(255,255,255)",
                      bodyFontColor: "#858796",
                      titleMarginBottom: 10,
                      titleFontColor: '#6e707e',
                      titleFontSize: 14,
                      borderColor: '#dddfeb',
                      borderWidth: 1,
                      xPadding: 15,
                      yPadding: 15,
                      displayColors: false,
                      intersect: false,
                      mode: 'index',
                      caretPadding: 10,
                      callbacks: {
                        label: function(tooltipItem, chart) {
                          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                          return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
                        }
                      }
                    }
                  }
              });
        }
        
        
        
    }});
    return aChart;
  };

  const companyGet = function(company_select,company_name=false){
    let company_url = "http://0.0.0.0:8000/company_dropdown";
    if (company_name) {
        company_url = "http://0.0.0.0:8000/company_dropdown?name="+company_name;
    } 
    $.ajax({url: company_url, success: function(result){
        xValues = [];
        for (let i=0;i<result.data.length;i++) {
            xValues.push({name: result.data[i].name, code: result.data[i].code})
        }
        xValues = xValues.reverse();
        let htmlString = ''
        for (let i in xValues) {
            htmlString += `<option value="${xValues[i].code}">${xValues[i].name}</option>`
        }
        $('#'+company_select).html(htmlString);
        
    }});
  };

$(document).ready(() => {
    myChart = false;
    myChart2 = false;
    myChart = chartFunction("myAdminCompanyChart",false,myChart);
    myChart2 = chartFunction("myAdminCompanyChart2",false,myChart2);
}
);
$(document).ready(() => {
    companyGet("company_select");
    companyGet("company_select2");
}
    
);
$("#company_search").keyup(() => {
    let searchValue = $('#company_search').val();
    companyGet("company_select",searchValue);
 });

 $("#company_search2").keyup(() => {
    let searchValue = $('#company_search2').val();
    companyGet("company_select2",searchValue);
 });
$("#company_select").change(() => {
    if (myChart) {
        myChart.destroy();
    }
    $("#myAdminCompanyChartContainer").html()
    $("#myAdminCompanyChartContainer").html('<canvas id="myAdminCompanyChart"></canvas>')
    let companyValue = $('#company_select option:selected').val();
    let companyName = $('#company_select option:selected').text();
    $("#company_name").html(companyName)
    myChart = chartFunction("myAdminCompanyChart",companyValue,myChart);
}
)
$("#company_select2").change(() => {
    if (myChart2) {
        myChart2.destroy();
    }
    $("#myAdminCompanyChart2Container").html()
    $("#myAdminCompanyChart2Container").html('<canvas id="myAdminCompanyChart2"></canvas>')
    let companyValue = $('#company_select2 option:selected').val();
    let companyName = $('#company_select2 option:selected').text();
    $("#company_name2").html(companyName)
    myChart2 = chartFunction("myAdminCompanyChart2",companyValue,myChart2);
}
)


$(".chart-form-id").change(function() {
  console.log("Hello");
  chart = false;
  let chartType = $('#chart_type').val();
  let chartCompany = $('#chart_company').val();
  let chartRange = $('#chart_range').val();
   if (chartType && chartCompany && chartRange) {
    $("#custom_chart_container").html()
    $("#custom_chart_container").html('<canvas id="custom_chart"></canvas>')
    chart = chartFunction("custom_chart",chartCompany,chart);
   }
});

$(document).ready(() => {
  companyGet("chart_company");
});

$("#company_search3").keyup(() => {
  let searchValue = $('#company_search3').val();
  companyGet("chart_company",searchValue);
});

toastr.options = {
  "closeButton": false,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-right",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}