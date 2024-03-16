$(".add_chart_btn").click(() => {
    var clicked = $(this);
});

$(".add_chart_btn").click(function(){
    clicked = $(this).attr("data-dashboard-id");
    $("#dashboard_id").val(clicked)
    // Do what you need to do to the newly defined click here
 });
 
 $("#save_chart").click(() => {
    let chartType = $('#chart_type').val();
  let chartCompany = $('#chart_company').val();
  let chartRange = $('#chart_range').val();
  let dashboard_id = $('#dashboard_id').val();
  let chart_name = $('#chart_name').val();
  let chart_title = $('#chart_title').val();
  data = {
    "chart_name": chart_name,
    "chart_title": chart_title,
    "chart_type": chartType,
    "chart_company": chartCompany,
    "chart_range": chartRange,
    "dashboard_id": dashboard_id
  }
  let data_url = "create_chart";
  $.post({url: data_url,data: data, success: (result) => {
    if (result.success) {
      window.location.reload();
    } 
  }})
 });

 const chartFunctionDashboard = function(chart_container, data=false,aChart=false){    
        xValues = [];
        yValues = [];
        datasetData= [];
        let colors = [
          "rgba(0,0,0,1)", "rgba(120,0,32,1)", "rgba(40,80,70,1)", "rgba(10,80,220,1)"
      ];
  
        if (aChart) {
            aChart.destroy();
        }
        if (data.length == 0) {
            aChart = new Chart(chart_container, {});
            return;
        }
        let chartArrayData = convertChartData(data);
        
        xValues = chartArrayData[0].reverse();
        yValues = yValues.reverse();
        i=0;
        for (let iter in chartArrayData[1]) {
          datasetData.push({
              backgroundColor:"transparent",
              borderColor: colors[i],
              data: chartArrayData[1][iter].reverse()
            });
            i++;
        }
        
        if (aChart) {
            removeData(aChart);
            addData(aChart, xValues, yValues);
        } else {
            aChart = new Chart(chart_container, {
                type: "line",
                data: {
                  labels: xValues,
                  datasets: datasetData
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
                          return datasetLabel + ': ' + number_format(tooltipItem.yLabel);
                        }
                      }
                    }
                  }
              });
        }
    return aChart;
  };

  function convertChartData(object) {
    let outputObject = {};
    for (let i in object) {

    for (let j=0; j<object[i].length;j++) {
        let objA = object[i][j];
        if (outputObject[objA["date"]] === undefined) {
        outputObject[objA["date"]] = Array();
        }
        // console.log(outputObject[objA["date"]]);
        outputObject[objA["date"]].push({"code": i, "close": objA.close});
    }
    }

    
    let companies = Object.keys(object);
    let yValues = {};
    for (let i=0;i<companies.length;i++) {
    yValues[companies[i]] = Array();
    }

    let xValues = Object.keys(outputObject);


    for (let i=0;i<xValues.length; i++) {
        let valueObj = outputObject[xValues[i]];
        let valueToInsert = 0;
        for (k=0;k<valueObj.length;k++) {
        valueToInsert = valueObj[k].close;
        yValues[valueObj[k].code].push(valueToInsert);
        }
        for (let j=0; j<companies.length; j++) {
        if (j==0 && (yValues[companies[j]].length != i+1)) {
            yValues[companies[j]].push(0);
        } else if (yValues[companies[j]].length != i+1) {
            yValues[companies[j].toString()].push(yValues[companies[j]][yValues[companies[j]].length-1]);
        }
        }
        }

    return [xValues,yValues,companies];
}

function createFinancials(id,content) {
  let html = `
  <table class="table">
                                            <tr>
                                                <td><b>Company Name:</b> <span>${content.company_name}</span></td>
                                                <td><b>Symbol:</b> <span>${content.symbol}</span></td>
                                            </tr>
                                            <tr>
                                                <td><b>Total Revenue:</b> <span>${content.total_revenue}</span></td>
                                                <td><b>Profit:</b> <span>${content.profit}</span></td>
                                            </tr>
                                            <tr>
                                                <td><b>Equity Share:</b> <span>${content.equity_share}</span></td>
                                                <td><b>Equity Per Share:</b> <span>${content.e_per_share}</span></td>
                                            </tr>
                                            <tr>
                                                <td><b>Debt Equity Ratio:</b> <span>${content.debt_equity}</span></td>
                                                <td><b>Face Value:</b> <span>${content.face_value}</span></td>
                                            </tr>
                                            <tr>
                                                <td><b>Sector:</b> <span>${content.sector}</span></td>
                                                
                                            </tr>
                                        </table>`;
                                        $("#"+id).html(html);
}

 function getDataForChart(id) {
  let data_url = "get_chart_data?ids="+id;
  $.get({url: data_url, success: (result) => {
        
    if (result.success) {
        let data = result.data;
        if (data.length>0) {
          for (let i=0;i<data.length;i++) {
            curr = data[i];
            let id = curr.id;
            if (curr.content[1] && curr.content[1].code != undefined) {
              
              let preData = {}
              preData[curr.content[1].code] = curr.content[0];
              createChartJK(preData, "selectedCompanyChart_container_"+id, true);
            } 
            if (curr.type == '1') {
              createChartJK(curr.content, "selectedCompanyChart_container_"+id, true);
            }
            if (curr.type == '2') {
              createFinancials("selectedCompanyChart_"+id, curr.content);
            }
          }
        }
        
        
    } 
}})
 }

 $(document).ready(() => {
  let IDs = [];
  $(".row").find(".charts_for_dash").each(function(){ IDs.push(this.id); });
  let ids = []
  for (let j=0;j<IDs.length;j++) {
    let id = IDs[j].split("_")[1];
    ids.push(id);
  }
  getDataForChart(ids.join(","));
});
 
$(".delete_chart_component").click(function(event) {
  console.log(event.target);
  let chart_id = event.target.dataset.id;
  let data_url = "delete_chart?chart_id="+chart_id;
  $.get({url: data_url, success: (result) => {
        
    if (result.success) {
      toastr["success"]("Deleted Chart");
      window.location.reload();
    } else {
      toastr["success"]("Unable to delete Chart");
    }
}})
});