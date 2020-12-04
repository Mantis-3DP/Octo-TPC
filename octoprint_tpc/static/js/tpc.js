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


        self.count = ko.observable();
        self.current_step = ko.observable();
        self.offsetCX = ko.observable();
        self.offsetCY = ko.observable();
        self.offsetCZ = ko.observable();
        self.offsetTX = ko.observable();
        self.offsetTY = ko.observable();
        self.offsetTZ = ko.observable();


// onDataUpdaterPluginMessage
        self.increase = function() {
            self.count(self.offsetTX());
        }

        self.increase2 = function() {
            console.log("increase called!")
            var currentValue = self.count();
            self.count(currentValue + 1);
        }

        self.start_calibration = function() {
            if (!self.started()){
                self.started(true);
                self.stage("Next");
                self.offsetTX(-1);

            }
            else{
                switch(self.current_step()) {
                    case 0:
                        self.offsetTX(1);
                        break;
                    case 1:
                        self.offsetTY(1);
                        break;
                    case 2:
                        self.offsetTZ(1);
                        break;
                    case 3:
                        self.offsetTX(2);
                        break;
                    default:
                        console.log("Problem in the switch section");
                        break;
                }
                self.current_step(self.current_step()+1);
            }

        }

        self.checkStatus = function() {
            self.offsetTX(100);
			$.ajax({
				url: API_BASEURL + "plugin/tpc",
				type: "GET",
				dataType: "json",
                data: {stopProcessing: true},
                contentType: "application/json; charset=UTF-8"
                }).done(function(data){
                    if (data.success){
                        self.offsetTY(50);
                    } else if (!data.success) {
                        self.offsetTY(40)
                    }
            });
		};

        self.stop_calibration = function() {
            self.started(false);
            self.stage("Start");
            self.current_step(0);
            self.offsetTX(self.settings.settings.plugins.tpc.tool0.x());
            self.offsetTY(self.settings.settings.plugins.tpc.tool0.y());
            self.offsetTZ(self.settings.settings.plugins.tpc.tool0.z());
        }


        self.ledOn = function() {
            $.ajax({
                url:         "/api/plugin/tpc",
                type:        "POST",
                contentType: "application/json",
                dataType:    "json",
                headers:     {"X-Api-Key": UI_API_KEY},
                data:        JSON.stringify({"command": "led", "state": self.stage()}),
                complete: function () {
                }
            });
            return true;
        }

/*

        self.multiincrease = function() {
            var currentValue = self.count();
            self.count(currentValue + 10);
        }

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
            self.offsetCX(self.settings.settings.plugins.tpc.camera.x()); // offsetX = tpc.camera aus den system defaults
            self.offsetCY(self.settings.settings.plugins.tpc.camera.y());
            self.offsetCZ(self.settings.settings.plugins.tpc.camera.z());
            self.offsetTX(self.settings.settings.plugins.tpc.tool0.x()); // offsetX = tpc.camera aus den system defaults
            self.offsetTY(self.settings.settings.plugins.tpc.tool0.y());
            self.offsetTZ(self.settings.settings.plugins.tpc.tool0.z());

        }

        self.onEventSettingsUpdated = function (payload) {
            self.offsetTX(self.settings.settings.plugins.tpc.tool0.x()); // offsetX = tpc.camera aus den system defaults
            self.offsetTY(self.settings.settings.plugins.tpc.tool0.y());
            self.offsetTZ(self.settings.settings.plugins.tpc.tool0.z());
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
        ["#tab_plugin_tpc"]
    ]);
});
