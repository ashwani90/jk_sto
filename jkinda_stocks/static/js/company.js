
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
  myChart = chartFunction("selectedCompanyChart",code,false, 500);
})

$( "#range_year" ).click(() => {
  let code = "TATAMOTORS";
  if (window.code) {
    code = window.code;
  }
  window.chartData.range = 50;
  myChart = chartFunction("selectedCompanyChart",code,false, 50);
})

$( "#range_month" ).click(() => {
  let code = "TATAMOTORS";
  if (window.code) {
    code = window.code;
  }
  window.chartData.range = 4;
  myChart = chartFunction("selectedCompanyChart",code,false, 4);
})

$( "#range_week" ).click(() => {
  let code = "TATAMOTORS";
  if (window.code) {
    code = window.code;
  }
  window.chartData.range = 1;
  myChart = chartFunction("selectedCompanyChart",code,false, 1);
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
          
            myChart = chartFunction("selectedCompanyChart",code,false);
            
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
    myChart = chartFunction("selectedCompanyChart",false,false);
  });

  $(document).ready(() => {
    getFinancials("SANOFI");
    
  });

 
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

function changeFunctionDashboard(event, ui) {
    console.log("hello");
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