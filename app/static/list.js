var open_modal = function(id) {
    var jcreate_and_edit_modal = jQuery('#create_or_edit_modal'),
        username_filed = jcreate_and_edit_modal.find('input[name="username"]'),
        password_field = jcreate_and_edit_modal.find('input[name="password"]');

    password_field.parents('.form-group').removeClass('has-error');
    password_field.val("");
    jcreate_and_edit_modal.find('input[name="full_rights"]').removeAttr('checked');
    username_filed.parents('.form-group').removeClass('has-error');

    if (id) {
        var jel = jQuery('#user_' + id);

        jcreate_and_edit_modal.find('input[name="id"]').val(id);
        username_filed.val(jel.find('td:nth-child(2) > a').text());

        if (jel.find('td:nth-child(3)').text().trim() == "Full") {
            jcreate_and_edit_modal.find('input[name="full_rights"]').attr('checked', 'checked');
        }
    } else {
        jcreate_and_edit_modal.find('input[name="id"]').val('');
        username_filed.val('');
    }

    jcreate_and_edit_modal.show();
};

var remove_line = function(id) {
    jQuery.ajax({url: '/api/user/' + id, method: 'DELETE'}).done(function(data) {
        if (data.reload) {
            window.location = "/";
        } else {
            jQuery('#user_' + id).remove();
        }
    });
};

var escape = function(str) {
    var tagsToReplace = {'&': '&amp;', '<': '&lt;', '>': '&gt;'};

    return str.replace(/[&<>]/g, function(tag) {
        return tagsToReplace[tag] || tag;
    });
};

jQuery(document).ready(function() {
    var jcreate_and_edit_modal = jQuery('#create_or_edit_modal');

    jcreate_and_edit_modal.on('shown.bs.modal', function() {
        jcreate_and_edit_modal.focus();
    }).find('.close').on('click', function() {
        jcreate_and_edit_modal.hide()
    });

    jQuery('#create_button').on('click', function() {open_modal();});

    jQuery('.modal-footer > button').on('click', function() {
        var username_filed = jQuery('input[name="username"]'),
            password_field = jQuery('input[name="password"]');

        var username = username_filed.val().trim(),
            password = password_field.val().trim(),
            full_rights = jQuery('input[name="full_rights"]').is(':checked');

        var url = "/api/user",
            id = jQuery('input[name="id"]').val(),
            method = "POST";

        if (id) {
            method = "PUT";
            url += "/" + id;
        }

        var has_errors = false;

        if (username) {
            username_filed.parents('.form-group').removeClass('has-error');
        } else {
            has_errors = true;
            username_filed.parents('.form-group').addClass('has-error');
        }

        if (password || id) {
            password_field.parents('.form-group').removeClass('has-error');
        } else {
            has_errors = true;
            password_field.parents('.form-group').addClass('has-error');
        }

        if (!has_errors) {
            jQuery.ajax({
                url: url, method: method, data: {
                    username: username, password: password, full_rights: full_rights
                }
            }).done(function (data) {
                if (data.reload) {
                    window.location = "/";
                } else {
                    if (id) {
                        var jel = jQuery('#user_' + id);

                        jel.find('td:nth-child(2) > a').html(escape(data.user.username));
                        if (data.user.full_rights) {
                            jel.find('td:nth-child(3) > a').html("Full");
                        } else {
                            jel.find('td:nth-child(3) > a').html("Read only");
                        }
                    } else {
                        jQuery('tbody').append('<tr id="user_' + data.user.id + '">' +
                            jQuery('.template_row').html().replace(new RegExp('{user_id}', 'g'), data.user.id)
                                .replace('{username}', escape(data.user.username))
                                .replace('{full_rights}', data.user.full_rights ? "Full" : "Read only") + '</tr>');
                    }

                    jcreate_and_edit_modal.hide();
                }
            });
        }
    });
});