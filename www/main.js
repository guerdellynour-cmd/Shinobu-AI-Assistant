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
});
