// JS
/*  global $ */
$(function () {
	
    /**
     * Submit form
     **/
     
     $('#app-body')
        .find('form')
        .submit(function onsubmit(ev){
            ev.preventDefault(); // Para que no se recargue la pantalla
            var busqueda = $(this)
                .find('input[type="text"]') // Devuelve el JQ Object
                .val(); // LLamado del metodo val
            alert('Se busco: ' + busqueda)
                
     })
     
	 var template =  '<article class="djs" alt=":img alt:">' +
                    '<div class="left img-container">' +
                        '<img src=":img:"></img>' +
					'</div>' +
                   ' <div class="right info"> ' +
                        '<h1>:name:</h1>'+
                        '<p>:summary:</p>' +
                    '</div>' +
                '</article>';
	 
    /** 
    * REQUEST AJAX
    **/
	
    $.ajax({
        url: 'http://api.tvmaze.com/shows',
        success: function (djs, textStatus, xhr){
			
			var $djsContainer = $('#app-body').find('div.main-djs');
			$djsContainer.find('.loader').remove();
			
            djs.forEach(function (dj){
				var article = template
					.replace(':name:', dj.name)
					.replace(':img:', dj.image.medium)
					.replace(':summary:', dj.summary)
					.replace(':img alt:', dj.name + " Logo")

					$djsContainer.append($(article))
			})
        }
    });
});
