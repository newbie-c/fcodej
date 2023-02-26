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
});
