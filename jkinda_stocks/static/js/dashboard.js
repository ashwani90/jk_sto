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

 
function createFinancials(id,content) {
  let html = `
  <table class="table">
                                            <tr>
                                                <td><b>Company Name:</b> <span>${content.company_name}</span></td>
                                                <td><b>Symbol:</b> <span>${content.symbol}</span></td>
                                            </tr>
                                            <tr>
                                                <td><b>Total Revenue:</b> <span>${content.total_revenue}</span> Lacs</td>
                                                <td><b>Profit:</b> <span>${content.profit}</span> Lacs</td>
                                            </tr>
                                            <tr>
                                                <td><b>Paid Up Equity Share:</b> <span>${content.equity_share}</span> Lacs</td>
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