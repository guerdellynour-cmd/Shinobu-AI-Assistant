function escapeHtml(str) {
    return $('<div>').text(str == null ? '' : str).html();
}

function appendChatMessage(text, from) {
    if (!text) return;
    var $log = $('#chat-log');
    if (!$log.length) return;
    var $bubble = $('<div class="chat-bubble ' + from + '"><span>' + escapeHtml(text) + '</span></div>');
    $log.append($bubble);
    $log.scrollTop($log[0].scrollHeight);
}

function openChatPanel() {
    var el = document.getElementById('offcanvasScrolling');
    if (!el || typeof bootstrap === 'undefined') return;
    bootstrap.Offcanvas.getOrCreateInstance(el).show();
}

function openSettingsPanel() {
    var el = document.getElementById('offcanvasSettings');
    if (!el || typeof bootstrap === 'undefined') return;
    bootstrap.Offcanvas.getOrCreateInstance(el).show();
}

function loadSettingsData() {
    if (typeof eel === 'undefined' || !eel.get_settings) return;

    eel.get_settings()(function (settings) {
        settings = settings || {};
        $('#setting-name').val(settings.assistant_name || 'Shinobu');
        var rate = settings.rate || 190;
        $('#setting-rate').val(rate);
        $('#rate-value').text(rate);
        populateVoices(settings.voice_index);
    });
    loadShortcuts();
}

function populateVoices(selectedIndex) {
    if (typeof eel === 'undefined' || !eel.get_available_voices) return;

    eel.get_available_voices()(function (voices) {
        var $select = $('#setting-voice').empty();
        voices = voices || [];

        if (!voices.length) {
            $select.append('<option value="">No voices found on this machine</option>');
            return;
        }

        voices.forEach(function (v) {
            $select.append('<option value="' + v.index + '">' + escapeHtml(v.name) + '</option>');
        });
        $select.val(String(selectedIndex));
    });
}

function loadShortcuts() {
    if (typeof eel === 'undefined' || !eel.get_shortcuts) return;

    eel.get_shortcuts()(function (data) {
        data = data || { apps: [], web: [] };
        renderShortcutList('#app-shortcut-list', data.apps, 'app');
        renderShortcutList('#web-shortcut-list', data.web, 'web');
    });
}

function renderShortcutList(selector, items, kind) {
    var $list = $(selector).empty();
    items = items || [];

    if (!items.length) {
        $list.append('<li class="empty">Nothing added yet.</li>');
        return;
    }

    items.forEach(function (item) {
        var detail = kind === 'app' ? item.path : item.url;
        var $li = $(
            '<li>' +
                '<div><strong>' + escapeHtml(item.name) + '</strong>' +
                '<span>' + escapeHtml(detail) + '</span></div>' +
                '<button type="button" class="remove-shortcut-btn" title="Remove">&#10005;</button>' +
            '</li>'
        );

        $li.find('.remove-shortcut-btn').on('click', function () {
            if (kind === 'app') {
                eel.delete_app_shortcut(item.id)(loadShortcuts);
            } else {
                eel.delete_web_shortcut(item.id)(loadShortcuts);
            }
        });

        $list.append($li);
    });
}

$(document).ready(function() {
	$('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });


    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: 1,
        speed: 0.30,
        autostart: true,
        curveDefinition: [
            { color: [181, 122, 241], supportLine: true }, // #b57af1
            { color: [157, 106, 207] },                     // #9d6acf
            { color:  [189, 45, 241] },                      // #bd2df1
            { color: [102, 24, 165] },                       // #6618a5
    ]
});

      $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    $("#MicBtn").click(function() {
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.playClickSound();
        eel.allCommands()();
    });

    /* ---------- New: typed messages via #chatbox ---------- */
    $("#chatbox").on('keydown', function (e) {
        if (e.key !== 'Enter') return;
        e.preventDefault();

        var text = $(this).val().trim();
        if (!text) return;

        appendChatMessage(text, 'user');
        $(this).val('');
        openChatPanel();

        if (typeof eel !== 'undefined' && eel.sendTextCommand) {
            eel.sendTextCommand(text);
        }
    });

    /* ---------- New: SettingsBtn opens the settings panel ---------- */
    $("#SettingsBtn").click(function () {
        loadSettingsData();
        openSettingsPanel();
    });

    /* ---------- New: settings panel controls ---------- */
    $('#setting-rate').on('input', function () {
        $('#rate-value').text($(this).val());
    });

    $('#save-settings-btn').on('click', function () {
        var data = {
            assistant_name: $('#setting-name').val().trim() || 'Shinobu',
            voice_index: $('#setting-voice').val(),
            rate: $('#setting-rate').val(),
        };

        eel.save_settings(data)(function () {
            var $status = $('#settings-status').text('Saved.').stop(true, true).show();
            setTimeout(function () { $status.fadeOut(); }, 1500);
        });
    });

    $('#add-app-shortcut-btn').on('click', function () {
        var name = $('#app-name').val().trim();
        var path = $('#app-path').val().trim();
        if (!name || !path) return;

        eel.add_app_shortcut(name, path)(function () {
            $('#app-name').val('');
            $('#app-path').val('');
            loadShortcuts();
        });
    });

    $('#add-web-shortcut-btn').on('click', function () {
        var name = $('#web-name').val().trim();
        var url = $('#web-url').val().trim();
        if (!name || !url) return;

        eel.add_web_shortcut(name, url)(function () {
            $('#web-name').val('');
            $('#web-url').val('');
            loadShortcuts();
        });
    });
});