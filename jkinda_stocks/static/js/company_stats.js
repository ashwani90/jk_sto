$(document).ready(function () {
    function toggleBulkButton() {
        let selected = $("input[name='rowCheckbox']:checked").length > 0;
        $("#bulkActionBtn").prop("disabled", !selected);
    }

    // Load table data on dropdown change
    $("#dataSelector").change(function () {
        let selectedValue = $(this).val();
        if (selectedValue) {
            $.ajax({
                url: "/get-data/",
                type: "GET",
                data: { option: selectedValue },
                success: function (response) {
                    let tableBody = $("#dataTableBody");
                    tableBody.empty();

                    response.data.forEach(function (item) {
                        let row = `<tr>
                            <td><input type="checkbox" name="rowCheckbox" value="${item.id}"></td>
                            <td>${item.id}</td>
                            <td>${item.name}</td>
                            <td>${item.value}</td>
                        </tr>`;
                        tableBody.append(row);
                    });

                    toggleBulkButton(); // Ensure button is updated
                },
                error: function () {
                    alert("Error fetching data.");
                }
            });
        }
    });

    // Enable bulk button when at least one row is selected
    $(document).on("change", "input[name='rowCheckbox']", toggleBulkButton);

    // "Select All" functionality
    $("#selectAll").change(function () {
        $("input[name='rowCheckbox']").prop("checked", $(this).prop("checked"));
        toggleBulkButton();
    });

    // Bulk action button click
    $("#bulkActionBtn").click(function () {
        let selectedIds = $("input[name='rowCheckbox']:checked").map(function () {
            return $(this).val();
        }).get();

        if (selectedIds.length > 0) {
            $.ajax({
                url: "/bulk-action/",
                type: "POST",
                headers: { "X-CSRFToken": "{{ csrf_token }}" },
                data: { ids: JSON.stringify(selectedIds) },
                success: function (response) {
                    alert(response.message);
                    $("#selectAll").prop("checked", false);
                    $("input[name='rowCheckbox']").prop("checked", false);
                    toggleBulkButton();
                },
                error: function () {
                    alert("Error processing bulk action.");
                }
            });
        }
    });
});