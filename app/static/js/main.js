// custom javascript

$(document).ready(function() {
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