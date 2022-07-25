$(document).ready(function () {
  $("#submit").click(function () {
    setTimeout(() => {
        $('#create_document').find('input, textarea, button, select').prop('disabled', true);
    });
  });
});
