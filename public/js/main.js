//Enlazar el codigo lo que se hara es que cuando este listo va a ejecutar una funcion la cual sera todo el prox code
$(document).ready(function(){
	$('ul.tabs li a:first').addClass('active');
	$('.secciones article').hide(); /* Ocultamos a todos */
	$('.secciones article:first').show();

	$('ul.tabs li a').click(function(){          /* Cuando le undamos click a un enlace se va a ejecutar una funcion */
		$('ul.tabs li a').removeClass('active');
		$(this).addClass('active');
		$('.secciones article').hide();          /* Cuando hagamos clik todas las secciones se ocultan */
		var activeTab = $(this).attr('href');  /* Cuando le undamos click va a traer el atributo del href que sea */
		/*TheTab(activeTab);*/
		console.log(activeTab);
		$(activeTab).show();					 /* Se muestra el tab seleccionado */
		return false;

	});  
});