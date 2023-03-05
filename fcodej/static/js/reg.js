function reg() {
  if (!$('#regf').length) {
    $.ajax({
      method: 'GET',
      url: '/api/captcha',
      success: function(data) {
        let form = Mustache.render($('#regt').html(), data);
        $('#main-container').append(form);
        $('#regf').siblings().each(function () {
          $(this).slideUp('slow', function() { $(this).remove(); });
        });
        $('#regf').slideDown('slow');
      },
      dataType: 'json'
    });
  }
  let col = $(this).parents('.navbar-collapse');
  if (col.hasClass('in')) col.removeClass('in');
}
