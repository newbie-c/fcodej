function login() {
  if (!$('#loginf').length) {
    $.ajax({
      method: 'GET',
      url: '/api/captcha',
      success: function(data) {
        let form = Mustache.render($('#logint').html(), data);
        $('#main-container').append(form);
        $('#main-container .top-flashed-block').slideUp('fast');
        $('.idef').slideUp('fast', function() {
          if ($('#regf').length) {
            $('#regf').slideUp('fast', function() {
              $('#loginf').slideDown('slow');
            });
          } else {
            $('#loginf').slideDown('slow');
          }
        });
      },
      dataType: 'json'
    });
  } else {
    $('#lcaptcha-reload').trigger('click');
    if ($('#regf').length) {
      $('#regf').slideUp('fast', function() {
        $('#loginf').slideDown('slow');
      });
    } else {
      $('#loginf').slideDown('slow');
    }
  }
  let col = $(this).parents('.navbar-collapse');
  if (col.hasClass('in')) col.removeClass('in');
}
