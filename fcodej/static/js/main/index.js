$(function() {
  let token = window.localStorage.getItem('token');
  let tee = token ? {token: token} : {};
  $.ajax({
    method: 'GET',
    url: '/api/index',
    data: tee,
    success: function(data) {
      if (!data.cu && token) {
        window.localStorage.removeItem('token');
        window.location.reload();
      }
      data.menu = adjustMenu(data);
      console.log(data);
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
  if (!token) {
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
    $('body').on('click', '#login-submit', function() {
      $(this).blur();
      let tee = {
        login: $('#logininput').val(),
        passwd: $('#password').val(),
        rme: $('#remember_me').is(':checked') ? 1 : 0,
        cache: $('#lsuffix').val(),
        captcha: $('#lcaptcha').val(),
        token: token
      };
      if (tee.login && tee.passwd && tee.captcha && tee.cache) {
        $.ajax({
          method: 'POST',
          url: '/api/login',
          data: tee,
          success: function(data) {
            if (data.token) {
              window.localStorage.setItem('token', data.token);
            }
            $('.navbar-brand')[0].click();
          },
          dataType: 'json'
        });
      }
    });
    $('body').on('click', '#login-reg', function() {
      $(this).blur();
      $('#reg').trigger('click');
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
  }
});
