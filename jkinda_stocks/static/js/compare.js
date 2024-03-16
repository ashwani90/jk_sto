const chartFunctionBase = function(chart_container, companyValue=false,aChart=false, range=false){
    // If range is false fetch 1 year data
    // If range is 1 then fetch for week
    // If range is 4 then fetch for month
    // If range is 50 then fetch for year
    // If range is 500 then fetch for 5 year

    if (!range) {
      range = 50;
    }

    let colors = [
        "rgba(0,0,0,1)", "rgba(120,0,32,1)", "rgba(40,80,70,1)", "rgba(10,80,220,1)"
    ];

    let data_url = "http://0.0.0.0:8000/show_data?code=500570&is_single=0&range="+range;
      if (companyValue) {
          data_url = "http://0.0.0.0:8000/show_data?code="+companyValue+"&is_single=0&range="+range;
      }
      let datasetData = [];
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
          let chartArrayData = convertChartData(result.data);
          
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
          
          
          
      }});
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

function sourceFunction(request, response) {
    let term = request.term;
        let data_url = window.main_url+"get_companies/"+term;
        
        $.get({url: data_url, success: (result) => {
            
            if (result.success) {
                let data = result.companies;
                res = [];
                for (let i=0;i<data.length;i++) {
                    res.push(data[i].id+" - "+data[i].name);
                }
                response(res);
            } 
        }})
  }

  function changeFunction() {
    // $("#company_name_show").html(event.target.value);
    var IDs = [];
    $("#companies").find("input").each(function(){ IDs.push(this.id); });
    let companies = [];
    for (let i=0; i<IDs.length;i++) {
        try {
            val = $("#"+IDs[i]).val().split(" ")[0];
        } catch {
            console.log("All companies adding is recommended");
        }
        if (val.length>0) {
            companies.push(val);
        }
    }
    companies = companies.join(",");
    
    
    myChart = chartDataFunction("chart-area",companies,false, 'line', 0);
  }

  function addData(chart, label, newData) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(newData);
    });
    chart.update();
  }

  

  function addListeners() {
    $( "#company_select_1" ).autocomplete({
        source: sourceFunction,
        change: changeFunction
      });
      $("#company_select_1_close").click(() => {
        changeFunction();
        $("#company_select_1").remove();
        $("#company_select_1_close").remove();
      })
      $("#company_select_2_close").click(() => {
        changeFunction();
        $("#company_select_2").remove();
        $("#company_select_2_close").remove();
      })
      $("#company_select_3_close").click(() => {
        changeFunction();
        $("#company_select_3").remove();
        $("#company_select_3_close").remove();
      })
      $("#company_select_4_close").click(() => {
        changeFunction();
        $("#company_select_4").remove();
        $("#company_select_4_close").remove();
      })
      $( "#company_select_2" ).autocomplete({
        source: sourceFunction,
        change: changeFunction
      });
    
      $( "#company_select_3" ).autocomplete({
        source: sourceFunction,
        change: changeFunction
      });
    
      $( "#company_select_4" ).autocomplete({
        source: sourceFunction,
        change: changeFunction
      });
  }

$( "#add_company" ).click(() => {
    let ids = [
        "company_select_1","company_select_2","company_select_3","company_select_4"
    ];
    
    
    var IDs = [];
    $("#companies").find("input").each(function(){ IDs.push(this.id); });
    let difference = ids.filter(x => !IDs.includes(x));
    $("#companies").append('<input type="text" class="form-control shadow-sm ml-2 company-select-in_compare_view" id="'+difference[0]+'" placeholder="Company"><i id="'+difference[0]+'_close" class="custom-close-icons fa fa-times fa-sm text-black-50"></input>');
    if ($(".company-select-in_compare_view").length == 4) {
        $("#add_company").prop("disabled",true);
    } 
    addListeners();
  });

  function changeFinancialFunction(event) {
    // $("#company_name_show").html(event.target.value);
    let symbol = event.target.value.split(" ")[0];
    let id_num = 2;
    if ($(this).attr('id') == "company_select_fin_1") {
      id_num = 1;
    }
    
    let data_url = window.main_url+"get_short_financials/"+symbol;
    let ids = [
      "company_name", "total_revenue", "profit", "face_value", "equity_share",
        "e_per_share", "debt_equity", "symbol", "sector"
    ];
    $.get({url: data_url, success: (result) => {
        
      if (result.success) {
          let data = result.companies;
          for (let i=0;i<ids.length;i++) {
            $("#financials_"+id_num+"_"+ids[i]).html(data[ids[i]]??"0");
          }
      } 
  }})
  }

  $( "#company_select_fin_1" ).autocomplete({
    source: sourceFunction,
    change: changeFinancialFunction
  });

  $( "#company_select_fin_2" ).autocomplete({
    source: sourceFunction,
    change: changeFinancialFunction
  });

  $(document).ready(function () {
    companies = "TATAMOTORS";
    myChart = chartDataFunction("chart-area",companies,false, 'line', 0);
  });

  $(document).ready(function () {
    
    window.chartData = {};
    
    let data_url = window.main_url+"api/get_dashboards/";
    $.get({url: data_url, success: (result) => {
          
      if (result.success) {
          let data = result.dashboards;
          console.log(data);
          res = [];
          for (let i=0;i<data.length;i++) {
            let val = '<button class="dropdown-item dashboard-chart-select-compare">'+data[i].id+" - "+data[i].name+'</button>';
            $("#select_dash_options_compare").append(val);
            let val2 = '<button class="dropdown-item dashboard-chart-select-fin">'+data[i].id+" - "+data[i].name+'</button>';
            $("#select_dash_options_fin").append(val2);
          }
      } else {
        console.log("Error");
        // toastr["success"]("Unable to fetch dashboards");
      }
      
  }})

  $("#select_dash_options_compare").click((event) => {
    let dashval = event.target.innerHTML;
    var IDs = [];
    $("#companies").find("input").each(function(){ IDs.push(this.id); });
    let companies = [];
    for (let i=0; i<IDs.length;i++) {
        try {
            val = $("#"+IDs[i]).val().split(" ")[0];
        } catch {
            console.log("All companies adding is recommended");
        }
        if (val.length>0) {
            companies.push(val);
        }
    }
    company = companies.join(",");
    // When chart is created add info to this var
    let chartData = window.chartData;
    chartData.type = 1;
    console.log(chartData);
    if (!dashval || !company || !chartData) {
      return;
    }
    let dashboard_id = dashval.split(" ")[0];
    company = company.split(" ")[0];
    let data = {
      company: company,
      chartData: JSON.stringify(chartData),
      dashboard_id: dashboard_id
    };
    let data_url = window.main_url+"api/add_chart_to_dashboard/";
    $.post({url: data_url,data: data, success: (result) => {
      if (result.success) {
        toastr["success"]("Added chart to dashboard");
      } else {
        toastr["success"]("Unable to add chart to dashboard");
      }
    }})
    // else send this data back to the server
    // and server will create an entry into the db
  
  });

  $("#select_dash_options_fin").click((event) => {
    let dashval = event.target.innerHTML;
    let company = $("#company_select_fin_1").val();
    // When chart is created add info to this var
    let chartData = window.chartData;
    chartData.type = 2;
    if (!dashval || !company || !chartData) {
      return;
    }
    let dashboard_id = dashval.split(" ")[0];
    company = company.split(" ")[0];
    let data = {
      company: company,
      chartData: JSON.stringify(chartData),
      dashboard_id: dashboard_id
    };
    let data_url = window.main_url+"api/add_chart_to_dashboard/";
    $.post({url: data_url,data: data, success: (result) => {
      if (result.success) {
        toastr["success"]("Added chart to dashboard");
      } else {
        toastr["success"]("Unable to add chart to dashboard");
      }
    }})
    // else send this data back to the server
    // and server will create an entry into the db
  
  });
});