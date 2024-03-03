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
    $("#dashboard_select").autocomplete({
        appendTo: "#dashboard_select",
        source: function (request,response) {
            sourceFunctionDashboard(request, response); 
        },
        change: function (event, ui) {
            changeFunctionDashboard(event, ui);
        }
        });
  });
