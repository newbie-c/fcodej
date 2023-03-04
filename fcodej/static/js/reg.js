function reg() {
  if (!$('#regf').length) {
    $.ajax({
      method: 'GET',
      url: '/api/captcha',
      success: function(data) {
        let form = Mustache.render($('#regt').html(), data);
        $('#main-container').append(form);
        $('#main-container .alert').slideUp('fast');
        $('#loginf').slideUp('slow');
      },
      dataType: 'json'
    });
  } else {
    $('#rcaptcha-reload').trigger('click');
    $('#regf').slideDown('slow');
    if ($('#loginf').length) $('#loginf').slideUp('slow');
  }
  let col = $(this).parents('.navbar-collapse');
  if (col.hasClass('in')) col.removeClass('in');
}
