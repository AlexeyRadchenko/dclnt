/**
 * Created by alexey on 26.02.17.     .panel-heading span.clickable
 */
$(function() {
    //перейти к последней вкладки, если она существует:
  var lastPanelElectric = localStorage.getItem('lastPanelElectric');
  if (lastPanelElectric=='close') {
	  var panelElectric = $('#panelelectric')
	  panelElectric.parents('.panel').find('.panel-body').hide();
	  panelElectric.addClass('panel-collapsed');
	  panelElectric.find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
  }
  var lastPanelWater = localStorage.getItem('lastPanelWater');
  if (lastPanelWater=='close') {
	  var panelWater = $('#panelwater')
	  panelWater.parents('.panel').find('.panel-body').hide();
	  panelWater.addClass('panel-collapsed');
	  panelWater.find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
  }
  var lastPanelGas = localStorage.getItem('lastPanelGas');
  if (lastPanelGas == 'close') {
  	  var panelGas = $('#panelgas')
	  panelGas.parents('.panel').find('.panel-body').hide();
  	  panelWater.addClass('panel-collapsed');
  	  panelWater.find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
  }
});


$(document).on('click', '#panelelectric', function(e){
    var $this = $(this);
	if(!$this.hasClass('panel-collapsed')) {
		$this.parents('.panel').find('.panel-body').slideUp();
		$this.addClass('panel-collapsed');
		$this.find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
		localStorage.setItem('lastPanelElectric', 'close');
	} else {
		$this.parents('.panel').find('.panel-body').slideDown();
		$this.removeClass('panel-collapsed');
		$this.find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
		localStorage.setItem('lastPanelElectric', 'open');
	}
})

$(document).on('click', '#panelwater', function(e){
    var $this = $(this);
	if(!$this.hasClass('panel-collapsed')) {
		$this.parents('.panel').find('.panel-body').slideUp();
		$this.addClass('panel-collapsed');
		$this.find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
		localStorage.setItem('lastPanelWater', 'close');
	} else {
		$this.parents('.panel').find('.panel-body').slideDown();
		$this.removeClass('panel-collapsed');
		$this.find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
		localStorage.setItem('lastPanelWater', 'open');
	}
})

$(document).on('click', '#panelgas', function(e){
    var $this = $(this);
	if(!$this.hasClass('panel-collapsed')) {
		$this.parents('.panel').find('.panel-body').slideUp();
		$this.addClass('panel-collapsed');
		$this.find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
		localStorage.setItem('lastPanelGas', 'close');
	} else {
		$this.parents('.panel').find('.panel-body').slideDown();
		$this.removeClass('panel-collapsed');
		$this.find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
		localStorage.setItem('lastPanelGas', 'open');
	}
})
