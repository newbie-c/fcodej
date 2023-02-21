$(function() {
  let dt = luxon.DateTime.now();
  let cur = {
    year: dt.year
  };
  let html = Mustache.render($('#baset').html(), cur);
  $('body').append(html);
  checkMC(800);
  $('body').on('click', '.close-top-flashed', closeTopFlashed);
  let content = Mustache.render($('#indext').html(), cur);
  $('#main-container').append(content);
  if ($('.today-field').length) renderTF('.today-field', dt);
});
