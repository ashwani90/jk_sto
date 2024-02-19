function get_portfolio_stocks(portfolio_id) {
    data = {
        "portfolio_id": portfolio_id,
    }
    let data_url = "portfolio_stocks/";
    $.get({url: data_url,data: data, success: (result) => {
        if (result.success) {
            let table_html = "";
            for (let i=0;i<result.stocks.length;i++) {
                table_html += "<tr>";
                table_html += `<td>${result.stocks[i].company}</td>`;
                table_html += `<td>${result.stocks[i].invested}</td>`;
                table_html += `<td>${result.stocks[i].current}</td>`;
                table_html += `<td>${result.stocks[i].shares}</td>`;
                table_html += `<td>${result.stocks[i].bought_at}</td>`;
                table_html += `<td>${result.stocks[i].date_bought}</td>`;
                table_html += `<td>${result.stocks[i].date_released}</td>`;
                table_html += "</tr>";
            }
            $("#portfolio_stocks_table").html(table_html)
        } 
    }})
}

$("#save_chart").click(() => {
  data = {
    "portfolio_id": chart_name,
  }
  let data_url = "portfolio_stocks";
  $.post({url: data_url,data: data, success: (result) => {
    if (result.success) {
      window.location.reload();
    } 
  }})
 });

 $( document ).ready(function() {
    if (window.portfolio_id) {
        get_portfolio_stocks(window.portfolio_id);
    }
});
$('.datepicker').datepicker();

$( "#company_add_stock" ).autocomplete({
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
    }
  });

$( document ).ready(function() {
    new DataTable('#stock-table', {
        initComplete: function () {
            this.api()
                .columns()
                .every(function () {
                    let column = this;
                    let title = column.footer().textContent;
     
                    // Create input element
                    let input = document.createElement('input');
                    input.placeholder = title;
                    column.footer().replaceChildren(input);
     
                    // Event listener for user input
                    input.addEventListener('keyup', () => {
                        if (column.search() !== this.value) {
                            column.search(input.value).draw();
                        }
                    });
                });
        }
    });
});

$("#add-stock").click(function(e) {
    e.preventDefault();
    if (!window.portfolio_id) {
        toastr["error"]("Portfolio selection is not valid");
        return;
    }
    let company = $("#company_add_stock").val();
    let company_id = company.split("-")[0];
    let invested = $("#invested_add_stock").val();
    let shares = $("#shares_add_stock").val();
    let date_bought = $("#date_bought_add_stock").val();
    let portfolio_id = window.portfolio_id;

    data = {
        "portfolio_id": portfolio_id, // get selected portfolio keep a global variable
        "company_id": company_id,
        "invested": invested,
        "shares": shares,
        "date_bought": date_bought
      }
      let data_url = "add_stock/";
      $.post({url: data_url,data: data, success: (result) => {
        if (result.success) {
            portfolio_id = result.portfolio_id;
            $("#company_add_stock").val("")
            $("#invested_add_stock").val("");
            $("#shares_add_stock").val("");
            $("#date_bought_add_stock").val("");
            toastr["success"]("Added stock to Portfolio");
            get_portfolio_stocks(portfolio_id);
            // show toaster kind of message
          // reload data
        } 
      }})
})

$(".portfolio_list_item").click(function(e) {
    
    $(".list-group-item").removeClass( "portfolio-item-active" );
    // const abc = document.querySelector(".portfolio_list_item");
    let portfolio_id = $(this).data().id;
    $(this).addClass("portfolio-item-active");
    window.portfolio_id = portfolio_id;
    get_portfolio_stocks(portfolio_id)
    // load stocks
    // load graph - this will be done later on I guess
})