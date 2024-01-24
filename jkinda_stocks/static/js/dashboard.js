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