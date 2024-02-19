$( "#company_select" ).autocomplete({
    source: function (request,response) {
        let term = request.term;
        let data_url = window.main_url+"get_companies/"+term;
        console.log(data_url);
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
        $("#company_name_show").html(event.target.value);
        code = event.target.value.split(" ")[0];
        if (code) {
            myChart = chartFunction("selectedCompanyChart",code,false);
        }
        
    }
  });

  $(document).ready(() => {
    myChart = chartFunction("selectedCompanyChart",false,false);
  });