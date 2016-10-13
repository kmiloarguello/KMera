if (!window.Intl) {
    window.Intl = require('intl'); 
    require("intl/locale-data/jsonp/en-US.js");
    require("intl/locale-data/jsonp/es-CO.js");
    require("intl/locale-data/jsonp/fr.js");
}

var IntlRelativeFormat = window.IntlRelativeFormat  = require('intl-relativeformat');
var IntlMessageFormat = require("intl-messageformat");

require('intl-relativeformat/dist/locale-data/en.js');
require('intl-relativeformat/dist/locale-data/es.js');
require('intl-relativeformat/dist/locale-data/fr.js');

var rf = new IntlRelativeFormat('en-US');

var es = require("./es");
var en = require("./en-US");
var fr = require("./fr");

var MESSAGES = {};

MESSAGES.es = es;
MESSAGES['en-US'] = en;
MESSAGES.fr = fr;

var local = localStorage.local || 'en-US';

module.exports = {
    message: function (text, opts= {}) {
        opts = opts || {};
        var msg = new IntlMessageFormat(MESSAGES[local][text], local, null);
        return msg.format(opts);
    },
    date: new IntlRelativeFormat(local)
}

