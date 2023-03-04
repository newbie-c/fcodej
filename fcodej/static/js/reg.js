function reg() {
  if (!$('#regf').length) {
    $.ajax({
      method: 'GET',
      url: '/api/captcha',
      success: function(data) {
        let form = Mustache.render($('#regt').html(), data);
        $('#main-container').append(form);
        if ($('#loginf').length) $('#loginf').slideUp('slow');
        $('#main-container .top-flashed-block').slideUp('fast');
        $('.idef').slideUp('fast', function() {
          if ($('#loginf').length) {
            $('#loginf').slideUp('fast', function() {
              $('#regf').slideDown('slow');
            });
          } else {
            $('#regf').slideDown('slow');
          }
        });
      },
      dataType: 'json'
    });
  } else {
    $('#rcaptcha-reload').trigger('click');
    if ($('#loginf').length) {
      $('#loginf').slideUp('fast', function() {
        $('#regf').slideDown('slow');
      });
    } else {
      $('#regf').slideDown('slow');
    }
  }
  let col = $(this).parents('.navbar-collapse');
  if (col.hasClass('in')) col.removeClass('in');
}
