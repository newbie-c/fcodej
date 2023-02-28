$(function() {
  let token = window.localStorage.getItem('token');
  let data = token ? {token: token} : {};
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
  $('body').on('click', '#rcaptcha-reload', function() {
    $(this).blur();
    $.ajax({
      method: 'GET',
      url: '/api/captcha',
      success: function(data) {
        $('#rcaptcha-field')
          .attr({"style": 'background:url(' + data.url +')'});
        $('#rsuffix').val(data.captcha);
        $('#rcaptcha').focus();
      },
      dataType: 'json'
    });
  });
  $('body').on('click', '#lcaptcha-reload', function() {
    $(this).blur();
    $.ajax({
      method: 'GET',
      url: '/api/captcha',
      success: function(data) {
        $('#lcaptcha-field')
          .attr({"style": 'background:url(' + data.url +')'});
        $('#lsuffix').val(data.captcha);
        $('#lcaptcha').focus();
      },
      dataType: 'json'
    });
  });
  $('body').on('click', '#reg', function() {
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
  });
});
