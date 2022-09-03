
$(function () {
    $(".autocomplete").autocomplete({
      source: function (request, response) {
        $.getJSON(
          '/autocomplete',
          {
            q: request.term,
          },
          function (data) {
            response(data.matching_results);
          }
        );
      },
    });
  });