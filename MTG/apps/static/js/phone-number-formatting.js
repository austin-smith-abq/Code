//create a function that formats a phone number as its entered
function formatPhoneNumber(phoneNumberString) {
    var cleaned = ('' + phoneNumberString).replace(/\D/g, '')
    var match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
    if (match) {
        return '(' + match[1] + ') ' + match[2] + '-' + match[3]
    }
    return phoneNumberString;
}

$(document).ready(function() {
  //assign formatphone function to the input field on keyup event
$('#phone').keyup(function(event) {
  // skip for arrow keys
  if(event.which >= 37 && event.which <= 40) return;

  // format number
  $(this).val(function(index, value) {
      return formatPhoneNumber(value);
  });
});
});

//function that sums up all points values and returns the total and average
function sumPoints() {
  var total = 0;
  var average = 0;
  var count = 0;
  $('.points').each(function() {
    total += parseInt($(this).val());
    count++;
  });
  average = total / count;
  $('#total').val(total);
  $('#average').val(average);
}

//take two lists and return the common elements
function commonElements(list1, list2) {
  var common = [];
  for (var i = 0; i < list1.length; i++) {
    for (var j = 0; j < list2.length; j++) {
      if (list1[i] == list2[j]) {
        common.push(list1[i]);
      }
    }
  }
  return common;
}
