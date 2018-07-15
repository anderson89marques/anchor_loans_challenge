$(document).ready(function() {
    $('#modalApprove').on('show.bs.modal', function (event) {
        var div = $(event.relatedTarget) // div that triggered the modal
        var recipient = button.data('whatever') // Extract info from data-* attributes
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this)
        console.log(recipient);
        modal.find('.modal-body img').attr('src', recipient)
      }); 
});