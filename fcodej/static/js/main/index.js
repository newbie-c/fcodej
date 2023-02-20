$(function() {
  let cur = {
    year: luxon.DateTime.now().year
  };
  let template = $('#baset').html();
  let html = Mustache.render(template, cur);
  $('body').append(html);
  console.log($('#main-container'));
});
