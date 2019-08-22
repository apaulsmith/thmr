function getEntitySelectorValue() {
  var entity = document.getElementById("entitySelect").value
  return entity
}

function gridLoadData(create_grid) {
  // specify the columns
  var columnDefs = {
    "Holiday": [
      { headerName: "Name", field: "name" },
      { headerName: "Address", field: "address" },
    ],
    "User": [
      { headerName: "Name", field: "name" },
      { headerName: "Email", field: "email" },
      { headerName: "Type", field: "type" },      
    ]
  };

  // let the grid know which columns to use
  var gridOptions = {
    defaultColDef: {
      sortable: true,
      editable: false,
      onCellValueChanged: function (params) {
        console.log(params)
      },
    },
    columnDefs: columnDefs[getEntitySelectorValue()]
  };

  if(create_grid) {
    // lookup the container we want the Grid to use
    var eGridDiv = document.querySelector('#myGrid');

    // create the grid passing in the div to use together with the columns & data we want to use
    new agGrid.Grid(eGridDiv, gridOptions);
  }

  url = 'http://127.0.0.1:5000/thmr/data/' + getEntitySelectorValue() + '?flat'
  fetch(url).then(function (response) {
    return response.json();
  }).then(function (data) {
    gridOptions.api.setRowData(data);
  })
}
