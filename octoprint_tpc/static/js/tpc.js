

$(function() {
    function tpcViewModel(parameters) {
        var self = this;

        self.settings = parameters[0];

        // this will hold the URL currently displayed by the iframe
        self.currentUrl = ko.observable();

        // this will hold the URL entered in the text field
        self.newUrl = ko.observable();

        self.count = ko.observable();

        // cali
        self.running = ko.observable();
        self.gcode_arr = ko.observableArray();


        self.increase = function() {
            console.log("increase called!")
            var currentValue = self.count();
            self.count(currentValue + 1);
            self.gcode_arr.push('G91');
            self.gcode_arr.push('Z10');
            self.gcode_arr.push('G90');

            OctoPrint.control.sendGcode(self.gcode_arr());
        }
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

        self.ledOn = function() {
            $.ajax({
                url:         "/api/plugin/tpc",
                type:        "POST",
                contentType: "application/json",
                dataType:    "json",
                headers:     {"X-Api-Key": UI_API_KEY},
                data:        JSON.stringify({"command": "led", "state": self.count()}),
                complete: function () {
                }
            });
            return true;
        }
        // this function should issue a function in cv.py to take a picture -> save position of orifice
        self.nozzle_position = function() {
            $.ajax({
                url:         "/api/plugin/tpc",
                type:        "POST",
                contentType: "application/json",
                dataType:    "json",
                headers:     {"X-Api-Key": UI_API_KEY},
                data:        JSON.stringify({"command": "nozzle_position", "wert": [3, 4]}),
                complete: function (data) {
                    self.wertanpassung(data)
                }
            });
            return true;
        }

        self.wertanpassung = function(data) {
            if (data == 7){
                self.gcode_arr.push(data)
            } else {
                self.gcode_arr.push(data);
            }
            OctoPrint.control.sendGcode(self.gcode_arr());
            self.gcode_arr([]);
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


            // cali
            self.running(false);


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
