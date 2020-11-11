// custom javascript

$(document).ready(function() {    
    var filter = document.getElementById('filter');

    filter.addEventListener('change', function() {
      var option = this.options[this.selectedIndex];
      var targets = option.dataset.targets.split(/(\s+)/);
      for (var target of document.getElementsByClassName('target')) {
        if (targets.indexOf(target.id) >= 0)
          target.classList.remove('hidden');
        else
          target.classList.add('hidden');
      }
    });

    var filter_edit = document.getElementById('filter_edit');

    filter_edit.addEventListener('change', function() {
      var option = this.options[this.selectedIndex];
      var targets = option.dataset.targets.split(/(\s+)/);
      for (var target of document.getElementsByClassName('target')) {
        if (targets.indexOf(target.id) >= 0)
          target.classList.remove('hidden');
        else
          target.classList.add('hidden');
      }
    });

    $('#modalEdit').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target-link');

      const modal = $(this);
      modal.find('.form').attr('action', target_link);
      modal.find('#edit_CustomerName').val(button.data('customername'));
      modal.find('#edit_JobName').val(button.data('jobname'));
      modal.find('#edit_MapscoLocation').val(button.data('mapscolocation'));
      modal.find('#edit_Source').val(button.data('source'));
      modal.find('#edit_JobNumber').val(button.data('jobnumber'));
      modal.find('#edit_JobNumberString').val(button.data('jobnumber'));
      modal.find('#edit_JobNumberSelect').val(button.data('jobnumber'));
      modal.find('#edit_MaterialName').val(button.data('materialname'));
      modal.find('#edit_LoadTotal').val(button.data('loadtotal'));
    });
    $('#modalDelete').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target-link');
      const modal = $(this);
      modal.find('.form').attr('action', target_link);
    });
    $('#modalAssign').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target-link');
      const modal = $(this);
      modal.find('.form').attr('action', target_link);
    });


} );