function showWindow() {
  let token = window.localStorage.getItem('token');
  $.ajax({
    method: 'POST',
    url: '/api/index',
    data: {
      token: token
    },
    success: function(data) {
      if (!data.cu && token) {
        window.localStorage.removeItem('token');
        window.location.reload();
      }
      data.menu = adjustMenu(data);
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
  return token;
}
