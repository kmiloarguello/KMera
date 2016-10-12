/* TEMPLATE HOME */
var yo = require("yo-yo");

var template = yo`<nav class="header">
                        <div class="nav-wrapper">
                            <div class="container">
                                <div class="row">
                                    <div class="col s12 m6 offset-m1">
                                        <a href="/" class="brand-logo kmgram">KMera</a>
                                    </div>
                                    <div class="col s2 m6 push-m10">
                                        <a href="#" class="btn btn-large btn-flat dropdown-button" data-activates="drop-user">
                                            <i class="large material-icons">perm_identity</i>
                                        </a>
                                        <ul id="drop-user" class="dropdown-content">
                                            <li><a href="#">Log Out</a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </nav>`;

module.exports = template;
