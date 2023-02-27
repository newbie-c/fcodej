$(function() {
  let token = window.localStorage.getItem('token');
  let data = token ? {token: token} : {};
  console.log(window.location.hash);
  $.ajax({
    method: 'GET',
    url: '/api/index',
    data: data,
    success: function(data) {
      let dt = luxon.DateTime.now();
      data.year = dt.year;
      let html = Mustache.render($('#baset').html(), data);
      $('body').append(html);
      checkMC(800);
      $('body').on('click', '.close-top-flashed', closeTopFlashed);
      let content = Mustache.render($('#indext').html(), data);
      $('#main-container').append(content);
      if ($('.today-field').length) renderTF('.today-field', dt);
    },
    dataType: 'json'
  });
  $('body').on('click', '#lcaptcha-reload', function() {
    $(this).blur();
    $.ajax({
      method: 'GET',
      url: '/api/captcha',
      success: function(data) {
        $('#lcaptcha-field').attr({"style": 'background:url(' + data.url +')'});
        $('#lsuffix').val(data.captcha);
        $('#lcaptcha').focus();
      },
      dataType: 'json'
    });
  });
  $('body').on('click', '#login', function() {
    if (!$('#loginf').length) {
      $.ajax({
        method: 'GET',
        url: '/api/captcha',
        success: function(data) {
          let form = Mustache.render($('#logint').html(), data);
          $('#main-container').append(form);
          $('#main-container .alert').slideUp('fast');
        },
        dataType: 'json'
      });
    }
    let col = $(this).parents('.navbar-collapse');
    if (col.hasClass('in')) col.removeClass('in');
  });
});
