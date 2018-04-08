

$(function () {
	$('#search').keyup(function () {

	    $.ajax({

			type:"GET",
			url:"../search/",
			data:{
				"search_text":$('#search').val(),
                'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()

	},
			success:searchSuccess,
			dataType:'html'



		});
	    // var search_results=document.querySelector('#search-results');
// 	    search_results.innerHTML='vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv';
//
    });

});

function searchSuccess(data,textStatus,jqXHR) {
    // alert('keyup');
	$('#search-results').html(data);

	};





var AlbumsListPage = {
	init: function() {
		this.$container = $('.albums-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active');
				}
			});

			return false;
		});


		$('.btn-listen_count', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {

				}
			});
			return false;
		});


	}
};

var SongsListPage = {
	init: function() {
		this.$container = $('.songs-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active');
				}
			});

			return false;
		});
			$('.btn-listen_count', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {

				}
			});
			return false;
		});
	}
};

$(document).ready(function() {
	AlbumsListPage.init();
	SongsListPage.init();
});