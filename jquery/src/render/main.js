/**
* Module Dependencies
**/

import $ from 'jquery'
import $tvShowsContainer from '../km-container'


var template = `<article class="djs"> 
	  <div class="left img-container"> 
		<img src=":img:" alt=":img alt:"> 
	  </div>
	  <div class="right info"> 
		<h1>:name:</h1> 
		<p>:summary:</p> 
		<i class="em em-maple_leaf"></i> 
	  </div>
	</article>`;

export default function renderShows(shows) {
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