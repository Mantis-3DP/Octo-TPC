Put your plugin's Jinja2 templates here.
{# here lege ich eine Variable newUrl an. diese muss noch eine Funktion in tpc_2.js erhalten #}

<div class="row-fluid text-center">
    <div class="col-xs-12" style="background-color:yellow;">
        <label for="go">Start Calibration</label>
        <label for="confirm">confirm calculated offset</label>
    </div>
</div>


<button class="btn btn-primary" id="go" data-bind="click: decrease">Go</button>
<button class="btn btn-primary" id="go" data-bind="click: decrease">Go</button>

<div class="panel panel-primary" style="padding-top: 20px;">
        <div class="panel-heading">Panel Heading</div>
        <div class="panel-body">Panel Content</div>
</div>
<button id="confirm" class="btn btn-primary" data-bind="click: increase">confirm</button>

<div class="container-fluid">
     <div class="row">
          <div class="col-sm-4">.col-sm-4</div>
          <div class="col-sm-8">.col-sm-8</div>
    </div>
</div>
<br>
<div class="input-append">
    <input type="text" class="input-xxlarge" data-bind="value: newUrl">
    <button class="btn btn-primary" data-bind="click: goToUrl">{{ _('Go') }}</button>
</div>


<iframe data-bind="attr: {src: currentUrl}" style="width: 100%; height: 100px; border: 1px solid #808080"></iframe>

<br>

<button data-bind="click: decrease">-</button>
<span data-bind="text: count">0</span>
<button data-bind="click: increase">+</button>
<button data-bind="click: multiincrease">++</button>
<br>
<div class="row-fluid text-center" style="padding-top: 20px;">
    <button class="btn btn-primary" data-bind="click: _getLocation">Cali</button>
    <button class="btn btn-primary" data-bind="click: nozzle_position('Hello World!')">Totol kills: ({{ _('tool') }})</button>
</div>



<div class="row-fluid">
	<div class="input-append span6">
		<label for="offset_z">Z Leveling Height</label>
		<input class="input-mini text-right" type="number" id="offset_z" step=".1" min="0" data-bind="value: offset_z,disable: started()"/>
		<div class="add-on">
			<span class="input-group-text" id="basic-addon2">mm</span>
		</div>
	</div>
	<div class="input-append span6">
		<label for="speed_xy">X/Y Speed</label>
		<input class="input-mini text-right" type="number" id="speed_xy" data-bind="value: speed_xy,disable: started()"/>
		<div class="add-on">
			<span class="input-group-text" id="basic-addon2">mm/s</span>
		</div>
	</div>
</div>
<div class="row-fluid">
	<div class="input-append span6">
		<label for="offset_z_travel">Z Travel Height</label>
		<input class="input-mini text-right" type="number" id="offset_z_travel" step="1" min="0" data-bind="value: offset_z_travel,disable: started()"/>
		<div class="add-on">
			<span class="input-group-text" id="basic-addon2">mm</span>
		</div>
	</div>
	<div class="input-append span6">
		<label for="speed_z_probe">Z Speed</label>
		<input class="input-mini text-right" type="number" id="speed_z_probe" data-bind="value: speed_z_probe,disable: started()"/>
		<div class="add-on">
			<span class="input-group-text" id="basic-addon2">mm/s</span>
		</div>
	</div>
</div>
<div class="row-fluid" data-bind="visible: !settingsViewModel.settings.plugins.tpc.use_custom_points()"  style="display: none;">
	<div class="input-append span6">
		<label for="offset_xy">X/Y Offset</label>
		<input class="input-mini text-right" type="number" id="offset_xy" step="1" min="0" data-bind="value: offset_xy"/>
		<div class="add-on">
			<span class="input-group-text" id="basic-addon2">mm</span>
		</div>
	</div>
</div>
<div class="row-fluid" data-bind="visible: settingsViewModel.settings.plugins.bedlevelingwizard.use_custom_points" style="display: none;">
	<div class="row-fluid">Using custom points, configure points in settings.</div>
</div>
<div class="row-fluid text-center" style="padding-top: 20px;">
	<button class="btn btn-primary" data-bind="click:function(){start_level();}, text:stage, enable: controlViewModel.isOperational() && !controlViewModel.isPrinting() && !controlViewModel.isPaused() && loginStateViewModel.isUser()">Start</button>
	<button class="btn btn-danger" data-bind="enable: started(), click:function(){stop_level();}">Stop</button>
</div>
