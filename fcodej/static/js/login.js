function login() {
  if (!$('#loginf').length) {
    $.ajax({
      method: 'GET',
      url: '/api/captcha',
      success: function(data) {
        let form = Mustache.render($('#logint').html(), data);
        $('#main-container').append(form);
        slidePage('#loginf');
      },
      dataType: 'json'
    });
  }
  let col = $(this).parents('.navbar-collapse');
  if (col.hasClass('in')) col.removeClass('in');
}
