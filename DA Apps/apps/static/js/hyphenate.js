$(document).ready(function () {
  $("#case_number").keyup(function (e) {
    // Allows user to disable auto-formatting
    if ($("#disable_auto_format").is(":checked") === false) {
      var key = e.keyCode || e.charCode;
      // Bypasses backspace
      if (key != 8) {
        $(this).val($(this).val().toUpperCase());
        switch ($(this).val().charAt(0)) {
          case "T":
            metro_case_num($(this));
            break;
          case "D":
            district_case_num($(this));
            break;
          default:
            da_case_num($(this));
        }
      }
    }
  });
});

function da_case_num(case_number) {
  switch (case_number.val().length) {
    case 4:
    case 10:
      newStr = `${case_number.val()}-`;
      case_number.val(newStr);
      break;
    default:
      break;
  }
}

function district_case_num(case_number) {
  switch (case_number.val().length) {
    case 1:
    case 5:
    case 8:
    case 13:
      newStr = `${case_number.val()}-`;
      case_number.val(newStr);
      break;
    default:
      break;
  }
}

function metro_case_num(case_number) {
  switch (case_number.val().length) {
    case 1:
    case 3:
    case 6:
    case 11:
      newStr = `${case_number.val()}-`;
      case_number.val(newStr);
      break;
  }
}
