
function getShortFinancials(symbol) {
  let data_url = window.main_url+"get_short_financials/"+symbol;
    let ids = [
      "company_name", "total_revenue", "profit", "face_value", "equity_share",
        "e_per_share", "debt_equity", "symbol", "sector"
    ];
    $.get({url: data_url, success: (result) => {
        
      if (result.success) {
          let data = result.companies;
          for (let i=0;i<ids.length;i++) {
            $("#financials__"+ids[i]).html(data[ids[i]]??"0");
          }
      } 
  }})
}

function getOperatorsForData() {
  if (event.target.value) {
    if (window.operator_data) {
      let operator_data = window.operator_data;
      let operator_actions = "";
      for (let i=0;i<operator_data.length;i++) {
        if (operator_data[i].value == event.target.value) {
          operator_actions = operator_data[i].operators;
        }
      }
      operator_actions = operator_actions.split(",");
      let operator_obj = {
        "lte": "<=",
        "gte": ">=",
        "lt": "<",
        "gt": ">",
        "e": "=",
        "ne": "!=",
      };
      operator_drop = [];
      for (let j=0;j<operator_actions.length;j++) {
        let opKey = operator_actions[j];
        operator_drop.push([opKey, operator_obj[opKey]]);
      }
      let htmlO = "";
      for (let i=0;i<operator_drop.length;i++) {
        htmlO += `<option value="${operator_drop[i][0]}">${operator_drop[i][1]}</option>`
      }
      return htmlO;
    }
  }
}

function getAllOperators() {
  let data_url = window.main_url+"/api/get_operators";
  $.get({url: data_url, success: (result) => {
        
    if (result.success) {
        let data = result.operators;
        for (let i=0;i<data.length;i++) {
          window.operator_data = data;
        }
    } 
}})
}

function getFinancials(symbol) {
  let data_url = window.main_url+"get_financials/"+symbol;
  let id_elements = [
    "revenue", "other_income", "total_revenue", "material_consumed", "material_consumed2",
    "change_inventories", "employee_benefit", "finance_costs", "depre_amor_expenses", "other_expenses",
    "profit", "exceptional_items", "profit_before_tax", "current_tax", "defferred_tax", 
    "associate_share", "total_tax_expense", "profit_period", "consolidated_profit", "comprehensive_income",
    "total_compr_income", "profit_attributes", "total_profit_non_controlling", "comprehensive_income_parent",
    "total_compr_non_contr_interests", "paid_up_equity_share", "face_value", "basic_eps", "diluted_eps",
    "interest_service_coverage"
  ];
  $.get({url: data_url, success: (result) => {
        
    if (result.success) {
        let data = result.financials;
        for (let i=0;i<id_elements.length;i++) {
         
          $("#financials_"+id_elements[i]).html(data[id_elements[i]]??"0");
        }
    } 
}})
}

$( "#range_5_year" ).click(() => {
  let code = "TATAMOTORS";
  if (window.code) {
    code = window.code;
  }
  window.chartData.range = 500;
  chartDataFunction("chart-area",code,500);
  
})

$( "#range_year" ).click(() => {
  let code = "TATAMOTORS";
  if (window.code) {
    code = window.code;
  }
  window.chartData.range = 50;
  chartDataFunction("chart-area",code,50);
  
})

$( "#range_month" ).click(() => {
  let code = "TATAMOTORS";
  if (window.code) {
    code = window.code;
  }
  window.chartData.range = 4;
  chartDataFunction("chart-area",code,4);
  
})

$( "#range_week" ).click(() => {
  let code = "TATAMOTORS";
  if (window.code) {
    code = window.code;
  }
  window.chartData.range = 1;
  chartDataFunction("chart-area",code,4);
  
})

$("#change-chart").click(function () {
  if ($(this).hasClass('active')) {
    $(this).removeClass('active');
    window.type = 'line';
    chartDataFunction('chart-area', window.code, false, 'line')
  } else {
    $(this).addClass('active');
    window.type = 'candle';
    chartDataFunction('chart-area', window.code, false, 'candle')
  }
})

$( "#company_select" ).autocomplete({
    source: function (request,response) {
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
    },
    change: function( event, ui ) {
        // $("#company_name_show").html(event.target.value);
        code = event.target.value.split(" ")[0];
        if (code) {
          window.code = code;
        }
        
        if (code) {
          getShortFinancials(code);
          getFinancials(code);
            myChart = chartDataFunction("chart-area",code,false);
            
        }
        
    },
    _renderItem: function( select, item ) {
        return $( "<option>" )
          .attr( "data-value", item.value )
          .append( item.label )
          .appendTo("#appendToElement");
      },
    _renderMenu: function( ul, items ) {
        var that = this;
        $.each( items, function( index, item ) {
          that._renderItemData( ul, item );
        });
        $( ul ).find( "li" ).odd().addClass( "odd" );
      }
  });

  $(document).ready(() => {
    myChart = chartDataFunction("chart-area");
  });

  $(document).ready(() => {
    getFinancials("SANOFI");
    getAllOperators();
  });

  $("#add_operator").click(function () {
    let htmlInput = `<div class="d-flex align-items-center  form-close-container"><span>&</span>`;
    
    htmlInput += `<select class="key-selector form-select form-control shadow-sm m-1 wi-15" aria-label="Default select example">
    <option selected>Op</option>`;
    for (let i=0;i<window.operator_data.length;i++) {
      htmlInput += `<option value="${window.operator_data[i].value}">${window.operator_data[i].name}</option>`;
    }
    htmlInput += `</select>
    <select class="op-selector form-control shadow-sm m-1 wi-10">
                                        <option selected>Op</option>
                                    </select>
                                    <input type="text" class="value-selector form-control shadow-sm m-1 wi-15" placeholder="val" />
                                    <i class="close-icon-form fa fa-times-circle form-control-close text-danger" aria-hidden="true"></i>
                                    </div>
    `;
    $("#operator-container").append(htmlInput);
    $(".close-icon-form").click(function () {
      console.log("Getting called");
      $(this).parent().remove();
    });

    $(".key-selector").change(function (event) {
      let abc = getOperatorsForData();
      $(this).next().html(abc);
  })
    
  })

  $(".close-icon-form").click(function () {
    console.log("Getting called");
    $(this).parent().remove();
  });

  $(".key-selector").change(function (event) {
      let abc = getOperatorsForData();
      $(this).next().html(abc);
  })

 
  function sourceFunctionDashboard(request,response) {

    let term = request.term;
    let data_url = window.main_url+"api/get_dashboards/"+term;
    
    $.get({url: data_url, success: (result) => {
        
        if (result.success) {
            let data = result.dashboards;
            res = [];
            for (let i=0;i<data.length;i++) {
                res.push(data[i].id+" - "+data[i].name);
            }
            console.log(res);
            console.log("Why is it not working");
            response(res);
            
        } else {
          let res = ["No Data Found"];
          response(res);
        }
    }})
}


$(document).ready(() => {
  window.chartData = {};
  let data_url = window.main_url+"api/get_dashboards/";
  $.get({url: data_url, success: (result) => {
        
    if (result.success) {
        let data = result.dashboards;
        console.log(data);
        res = [];
        for (let i=0;i<data.length;i++) {
          let val = '<button class="dropdown-item dashboard-chart-select">'+data[i].id+" - "+data[i].name+'</button>';
          $("#select_dash_options").append(val);
        }
    } else {
      console.log("Error");
      // toastr["success"]("Unable to fetch dashboards");
    }
}})

$("#select_dash_options").click((event) => {
  let val = event.target.innerHTML;
  let company = $("#company_select").val();
  // When chart is created add info to this var
  let chartData = window.chartData;
  chartData.type = 1;
  console.log(chartData);
  if (!val || !company || !chartData) {
    return;
  }
  let dashboard_id = val.split(" ")[0];
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

$("#search-btn-stock").click((event) => {
  // get all the values and send to the server
  let data = '';
  for (let i=0;i<$("#operator-container").find('div').length; i++) {
    let key = $("#operator-container").find('div .key-selector')[i].value;
    let value = $("#operator-container").find('div .op-selector')[i].value;
    let operator = $("#operator-container").find('div .value-selector')[i].value;
    data += key+","+value+","+operator+":";
  }
  // redirect the user to company list page with these params
  window.location.href = "/company-list/"+data
})