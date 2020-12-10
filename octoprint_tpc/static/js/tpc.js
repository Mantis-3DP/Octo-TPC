$(function() {
    function tpcViewModel(parameters) {
        var self = this;

        self.settings = parameters[0];

        // this will hold the URL currently displayed by the iframe
        self.currentUrl = ko.observable();

        // this will hold the URL entered in the text field
        self.newUrl = ko.observable();

        // stages of calibration
        self.started = ko.observable();
        self.stage = ko.observable();

        self.currentTool = ko.observable()
        self.count = ko.observable();
        self.feed_rate = ko.observable();
        self.current_step = ko.observable();

        // TODO: change to array
        self.offsetCX = ko.observable();
        self.offsetCY = ko.observable();
        self.offsetCZ = ko.observable();
        self.offsetTX = ko.observable();
        self.offsetTY = ko.observable();
        self.offsetTZ = ko.observable();
        self.posTX = ko.observable();
        self.posTY = ko.observable();
        // noch umbenennen
        self.gcode_cmds = ko.observableArray();

        self.posX = ko.computed(function(){return Number(self.offsetCX()) + Number(self.offsetTX())});
        self.posY = ko.computed(function(){return Number(self.offsetCY()) + Number(self.offsetTY())});

        self.pxPos = ko.observableArray();
        self.pxPos = ko.observableArray();

        self.moveDis = ko.observableArray();
        self.webcamUrl = ko.observable();
        self.klipperOffsetString = ko.observable();


// onDataUpdaterPluginMessage

        self.start_calibration = function() {
            //self.gcode_cmds.push("G28");
            if (self.current_step() === 0){
                self.nozzle_position(self.webcamUrl());
            }
            if (self.current_step() < 7 && self.current_step() >=0) {
                self.stage(self.current_step());
                self.sendToPy(self.current_step());
            }
            else if (self.current_step() === 7) {
                self.getPosition();
                self.stage(self.current_step());
            }
            self.increaseStep();
        }
            /*            OctoPrint.control.sendGcode(self.gcode_cmds());
                        self.gcode_cmds([]);*/




        self.getPosition = function() {
			$.ajax({
				url: API_BASEURL + "plugin/tpc",
				type: "GET",
				dataType: "json",
                data: {getPosition: true},
                contentType: "application/json; charset=UTF-8"
                }).done(function(data){
                    if (data.success){
                        // self.tempPos([data.x, data.y])
                        self.offsetTX(data.x);
                        self.offsetTY(data.y);
                        self.klipperOffset(self.offsetTX(), self.offsetTY(), self.offsetTZ());
                    } else if (!data.success) {
                        self.offsetTZ(40);
                    }

            });
		};

        self.saveOffset = function() {
            self.settings.settings.plugins.tpc.tool0.x(self.offsetTX());
            self.settings.settings.plugins.tpc.tool0.y(self.offsetTY());
            self.settings.saveData();
            self.sendToPy(10)


        }

        self.stop_calibration = function() {
            self.started(false);
            self.stage("Start");
            self.current_step(0);
            self.offsetTX(self.settings.settings.plugins.tpc.tool0.x());
            self.offsetTY(self.settings.settings.plugins.tpc.tool0.y());
            self.offsetTZ(self.settings.settings.plugins.tpc.tool0.z());
        }

//      self.sendToPy(self.current_step());
        self.sendToPy = function(step) {
            $.ajax({
                url:         "/api/plugin/tpc",
                type:        "POST",
                contentType: "application/json",
                dataType:    "json",
                headers:     {"X-Api-Key": UI_API_KEY},
                data:        JSON.stringify({"command": "sendToPy", "step": step}),
                complete: function (data) {
                }
            });
            return true;
        }


        self.ledOn = function(wert) {
            $.ajax({
                url:         "/api/plugin/tpc",
                type:        "POST",
                contentType: "application/json",
                dataType:    "json",
                headers:     {"X-Api-Key": UI_API_KEY},
                data:        JSON.stringify({"command": "led", "wert": wert}),
                complete: function () {
                }
            });
            return true;
        }

              // this function should issue a function in cv.py to take a picture -> save position of orifice
        self.nozzle_position = function(test) {
            $.ajax({
                url:         "/api/plugin/tpc",
                type:        "POST",
                contentType: "application/json",
                dataType:    "json",
                headers:     {"X-Api-Key": UI_API_KEY},
                data:        JSON.stringify({"command": "nozzle_position", "wert": test}),
                complete: function (data) {
                    self.wertanpassung(data)
                }
            });
            return true;
        }

        self.increaseStep = function() {
            var currentValue = self.current_step();
            self.current_step(currentValue + 1);
        }

        self.klipperOffset = function(x, y, z) {
            self.klipperOffsetString(`SET_GCODE_OFFSET X=${x} Y=${y} Z=${z}`)
        }

/*



        self.decrease = function() {
            var currentValue = self.count();
            if (currentValue > 0) {
                self.count(currentValue - 1);
            }
        }

        self._getLocation = function() {
             $.ajax({
                    url: PLUGIN_BASEURL + "tpc/camera_image",
                    type:        "GET",
                    contentType: "application/json",
                    dataType:    "json",
                    // headers:     {"X-Api-Key": UI_API_KEY},
                    // data:        JSON.stringify({"command": "led", "state": self.count()}),
                    success: function (response) {
                        if(response.hasOwnProperty("error")) {
                            alert(response.error);
                        }
                    }
             });
        }




        // cali
        self.start_cali = function()  {
            if (!self.running()) {
                self.running(true)
                self.gcode_arr.push("now running");
            } else if (self.running()){
                self.running(false)
                self.gcode_arr.push('stopped');
            }
            OctoPrint.control.sendGcode(self.gcode_arr());
            self.gcode_arr([]);
        }

        self.aftersuccess = function(sum) {
            self.count = sum;
            self.gcode_arr.push(self.count);
            OctoPrint.control.sendGcode(self.gcode_arr());
        }
*/

        // this will be called when the user clicks the "Go" button and set the iframe's URL to
        // the entered URL
        self.goToUrl = function() {
            self.currentUrl(self.newUrl());
        };

        // This will get called before the HelloWorldViewModel gets bound to the DOM, but after its
        // dependencies have already been initialized. It is especially guaranteed that this method
        // gets called _after_ the settings have been retrieved from the OctoPrint backend and thus
        // the SettingsViewModel been properly populated.
        self.onBeforeBinding = function() {
            self.newUrl(self.settings.settings.plugins.tpc.url());
            self.goToUrl();
            self.count(0);
            self.stage("Start")
            self.started(false)
            self.current_step(0)
            self.feed_rate(self.settings.settings.plugins.tpc.feed_rate());
            self.offsetCX(self.settings.settings.plugins.tpc.camera.x()); // offsetX = tpc.camera aus den system defaults
            self.offsetCY(self.settings.settings.plugins.tpc.camera.y());
            self.offsetCZ(self.settings.settings.plugins.tpc.camera.z());
            self.offsetTX(self.settings.settings.plugins.tpc.tool0.x()); // offsetX = tpc.camera aus den system defaults
            self.offsetTY(self.settings.settings.plugins.tpc.tool0.y());
            self.offsetTZ(self.settings.settings.plugins.tpc.tool0.z());
            self.posTX(0);
            self.posTY(0);
            self.currentTool(0);
            self.moveDis([2, 2]);
            self.gcode_cmds([]);
            self.webcamUrl(self.settings.webcam_snapshotUrl());
            self.klipperOffset(self.offsetTX(), self.offsetTY(), self.offsetTZ());

        }

        self.onEventSettingsUpdated = function (payload) {
            self.offsetTX(self.settings.settings.plugins.tpc.tool0.x()); // offsetX = tpc.camera aus den system defaults
            self.offsetTY(self.settings.settings.plugins.tpc.tool0.y());
            self.offsetTZ(self.settings.settings.plugins.tpc.tool0.z());
            self.feed_rate(self.settings.settings.plugins.tpc.feed_rate());
            self.klipperOffset(self.offsetTX(), self.offsetTY(), self.offsetTZ());
            //self.currentTool(self.settings.settings.plugins.tpc.currentTool());
        }
        self.onEventToolChange = function (payload) {
            self.currentTool(payload["new"])
            //self.currentTool(self.settings.settings.plugins.tpc.currentTool());
        }


    }





    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    OCTOPRINT_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        tpcViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        ["settingsViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        ["#tab_plugin_tpc", "#wizard_plugin_corewizard_webcam", "#settings_plugin_tpc"]
    ]);
});
