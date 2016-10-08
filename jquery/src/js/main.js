/**
* Module Dependencies
**/

import $ from 'jquery'
import page from 'page'
import { getShows } from '../km-api-client'
import renderShows from '../render'
import $tvShowsContainer from '../km-container'

page('/', function (ctx, next) {
  if (!localStorage.shows) {
	  getShows( function () {
		$tvShowsContainer.find('.loader').remove();
        localStorage.shows = JSON.stringify(shows);
        renderShows(shows);
	  })
   }
	else {
    renderShows(JSON.parse(localStorage.shows));
  }	
})

page()