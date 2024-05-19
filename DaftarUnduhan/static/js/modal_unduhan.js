// Ketika form penghapusan di-submit
$('form').on('submit', function(event) {
    event.preventDefault(); // Mencegah submit form secara default
    var form = $(this);
    $.ajax({
        url: form.attr('action'),
        type: form.attr('method'),
        data: form.serialize(),
        success: function(data) {
            // Jika berhasil, sembunyikan modal dan muat ulang halaman
            $('#myModal').modal('hide');
            location.reload();
        },
        error: function(error) {
            // Jika terjadi kesalahan, tampilkan modal dengan pesan kesalahan
            $('.remove-button').text(error.responseJSON.error);
            $('#myModal').modal('show');
        }
    });
});
