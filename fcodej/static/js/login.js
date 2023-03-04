function login() {
  if (!$('#loginf').length) {
    $.ajax({
      method: 'GET',
      url: '/api/captcha',
      success: function(data) {
        let form = Mustache.render($('#logint').html(), data);
        $('#main-container').append(form);
        $('#main-container .alert').slideUp('fast');
        $('#regf').slideUp('slow');
      },
      dataType: 'json'
    });
  } else {
    $('#lcaptcha-reload').trigger('click');
    $('#loginf').slideDown('slow');
    if ($('#regf').length) $('#regf').slideUp('slow');
  }
  let col = $(this).parents('.navbar-collapse');
  if (col.hasClass('in')) col.removeClass('in');
}
