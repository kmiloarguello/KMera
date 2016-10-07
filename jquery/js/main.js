// JS
/*  global $ */
$(function() {
  var $tvShowsContainer = $('#app-body').find('.main-djs');
	//Evento al hacer click
	$tvShowsContainer.on('click', 'i.em-maple_leaf', function(ev){
		var $this = $(this); //boton en el que se hizo click
		$this.closest('.djs').toggleClass('liked') //Buscar elemento Padre
	})

  function renderShows(shows) {
    $tvShowsContainer.find('.loader').remove();
    shows.forEach(function (show) {
      var article = template
        .replace(':name:', show.name)
        .replace(':img:', show.image ? show.image.medium : '')
        .replace(':summary:', show.summary)
        .replace(':img alt:', show.name + " Logo")

      var $article = $(article)
      $article.hide();
      $tvShowsContainer.append($article.fadeIn(1500));
    })
  }

  /**
   * Enviar Datos
   */

  $('#app-body')
    .find('form')
    .submit(function (ev) {
      ev.preventDefault();
      var busqueda = $(this)
        .find('input[type="text"]')
        .val();

      $tvShowsContainer.find('.djs').remove()
      var $loader = $('<div class="loader">');
      $loader.appendTo($tvShowsContainer);
      $.ajax({
        url: 'http://api.tvmaze.com/search/shows',
        data: { q: busqueda },
        success: function (res, textStatus, xhr) {
          $loader.remove();
          var shows = res.map(function (el) {
            return el.show;
          })

          renderShows(shows);          
        }
      })
    })

  var template = '<article class="djs">' +
          '<div class="left img-container">' +
            '<img src=":img:" alt=":img alt:">' +
          '</div>' +
          '<div class="right info">' +
            '<h1>:name:</h1>' +
            '<p>:summary:</p>' +
			'<i class="em em-maple_leaf"></i>'+
          '</div>' +
        '</article>';
	
	//Promises
  if (!localStorage.shows) {
    $.ajax('http://api.tvmaze.com/shows')
      .then(function (shows) {
        $tvShowsContainer.find('.loader').remove();
        localStorage.shows = JSON.stringify(shows);
        renderShows(shows);
      })
  } else {
    renderShows(JSON.parse(localStorage.shows));
  }
  
})

