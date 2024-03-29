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