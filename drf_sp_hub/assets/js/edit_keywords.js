const dataContainer = $('input#id_data');
const delButton = '<button class="btn btn-sm btn-outline-danger delete mx-2 my-1">Delete</button>';

const handleFormSubmit = event => {
  //event.preventDefault();
  const data = {};
  $('form #autoDataDiv').children('label').each(function() {
    console.log($(this));
    data[$(this).text()] = $(this).nextUntil('label', 'input').val();
  });
  dataContainer.val(JSON.stringify(data, null, " "));
}

const refreshDeleteButtons = () => {
  $('form #autoDataDiv').children('button.delete').click(function(e) {
    event.preventDefault();
    $(this).prev('label').remove();
    $(this).next('input').remove();
    $(this).remove();
  });
}

const addLineBtnHandler = (e) => {
  e.preventDefault();
  myModal = $('#addAlignmentModal');
  newLabel = myModal.find('input#newLabel').val();
  newValue = myModal.find('input#newValue').val();
  labelElm = '<label>' + newLabel + '</label>';
  inputElm = '<input type="text" value="' + newValue + '" class="form-control">';
  $('div#autoDataDiv').append(labelElm, delButton, inputElm);
  $('#addAlignmentModal').modal('hide');
  refreshDeleteButtons();
}

$(document).ready(function () {
  // parse data from hidden form element
  data = JSON.parse(dataContainer.val());

  // create new form group
  $('input#id_name').after('<div id="autoDataDiv"></div>');
  autoDataDiv = $('div#autoDataDiv');
  // add elements to form group
  for(var k in data) {
    labelElm = '<label>' + k + '</label>';
    inputElm = '<input type="text" value="' + data[k] + '" class="form-control">';
    autoDataDiv.append(labelElm, delButton, inputElm);
  }
  refreshDeleteButtons();
  $('button#addLineSaveBtn').click(addLineBtnHandler);
  $('form').submit(handleFormSubmit);
});
