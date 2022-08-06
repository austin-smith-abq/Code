$(document).ready(function () {
  $(".phone_number").keyup(function (e) {
    var key = e.keyCode || e.charCode;
    // Bypasses backspace
    if (key != 8) {
      switch ($(this).val().length) {
        case 1:
          newStr = `(${$(this).val()}`;
          break;
        case 4:
          newStr = `${$(this).val()}) `;
          break;
        case 9:
          newStr = `${$(this).val()}-`;
          break;
        default:
          newStr = $(this).val();
          break;
      }
      $(this).val(newStr);
    }
  });
});
