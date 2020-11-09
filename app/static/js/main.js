// custom javascript

$(document).ready(function() {
    $('#modalEdit').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target-link');
      const modal = $(this);
      modal.find('.modal-body .form').attr('action', target_link);
    });
    $('#modalDelete').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target-link');
      const modal = $(this);
      modal.find('.form').attr('action', target_link);
    });
    $('#modalEditindex').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target-link');
      const modal = $(this);
      modal.find('.modal-body .form').attr('action', target_link);
    });

} );